#!/usr/bin/env python
from itertools import islice, product
import pyvisa
import yaml
from    utils.utils import cmd, cd, check_return_zero, current_utctime_string
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass
from    utils.SCP_RTB2004 import SCP_RTB2004

def change_ut(ima_file, ut, instr=0):
    with open(settings.DIANA_SDK_PATH+"measurement_inputs/aim/{}".format(ima_file), "r") as f:
        list_doc = yaml.safe_load(f)
        list_doc[instr]["INSTR1"]["UNIT_TIME"] = ut
    with open(settings.DIANA_SDK_PATH+"measurement_inputs/aim/{}".format(ima_file), "w") as f:
        yaml.dump(list_doc, f)

parser = HostScriptParserClass()

#OPENING PSU
RM = pyvisa.ResourceManager()
PSU_N6705B = RM.open_resource(settings.PSU_N6705B_addr)
PSU_E36312A = RM.open_resource(settings.PSU_E36312A_addr)
SCOPE_RTB2004 = SCP_RTB2004("SCP_RS", settings.SCP_RTB2004_addr)

#setting up PSU
procedures.set_psu(PSU_N6705B,PSU_E36312A,reset=True)

handlers_args_dic = {"parser":parser}
procedures.off_procedure(process_list=[], PSU_N6705B=PSU_N6705B, PSU_E36312A=PSU_E36312A, **handlers_args_dic)

#---------experiments----------------------------------//
if parser.args.checkpoint_file:
    with open(parser.args.checkpoint_file, "r") as f:
        checkpoint_d = yaml.safe_load(f)
    dump_path = checkpoint_d["dump_path"]
    experiment_i = checkpoint_d["I"]
else:
    _ = input("No checkpoint_file! Press ENTER to continue or CTRL+C to drop.")
    print("Making parent directory for experiment results...")
    RESULT_PARENT_DIR="power_char_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
    p = cmd("mkdir ../data/{}".format(RESULT_PARENT_DIR))
    check_return_zero(p)
    dump_path = "../data/" + RESULT_PARENT_DIR
    print("Starting the loop experiments...")
    experiment_i = parser.args.starting_iteration

MAX_TRIALS=2
DEADLOCK=False
ACT_SIZE=63*63*64
ut_list = list(range(0,10))

i=experiment_i
for ut, actv_v, csbias_V, weight_p in islice( product( ut_list, parser.actv_uni_steps, parser.csbias_steps, parser.weight_pol_steps), experiment_i, None):
    DONE=False
    params={"I"         : i,
            "UT"        : ut,
            "CBV"       : float(csbias_V),
            "ACTVV"     : actv_v,
            "WEIGHTP"   : weight_p}

    #add here possible parameter sweep
    PSU_E36312A.write('SOUR:VOLT {}, (@1)'.format(str(csbias_V)))
    print("Generating header data files for the experiment...")
    with cd(settings.DIANA_SDK_PATH + "tests"):
        change_ut("peak_.yaml", ut, instr=1)
        p = cmd("""python3 {sdk_script_name}    -p ana_power_meas\
                                                -imp peak_.yaml\
                                                -ima\
                                                -a UNI\
                                                -as {activation_size}\
                                                -v {activation_value}\
                                                -w STR\
                                                --weight_pol {weight_polarity}\
                                                --weight_str_val 1
                                                --weight_step 2
                                                -crp peak_.yaml\
                                                -cra""".format(    sdk_script_name=parser.args.sdk_script_name,
                                                                    activation_size=ACT_SIZE,
                                                                    activation_value=actv_v,
                                                                    weight_polarity=weight_p
                                                                    ), verbose=False, timeout=10*60)
        check_return_zero(p)
    print("Compiling C code...")
    procedures.c_compile(parser)
    print("Running the experiment on chip...")
    trials = 0
    stuck = False
    while(not DONE):
        if trials:
            DEADLOCK = True
        trials = 0
        while( (procedures.run_diana_experiment(parser, PSU_N6705B, PSU_E36312A, SCOPE_RTB2004, power_path=dump_path, sync_out=False, dump_path=".", params=params)) and (trials<MAX_TRIALS)):
            print("Experiment with path {} failed! Trying again {}...".format(dump_path,trials))
            p = cmd("rm -rf {}/*".format(dump_path))
            check_return_zero(p)
            trials+=1
        if(trials==MAX_TRIALS):
            procedures.reset(PSU_N6705B, PSU_E36312A, parser, hard=True)
        else:
            DEADLOCK=False
            DONE=True
        if DEADLOCK:
            print("Deadlock in execution of experiment {}. Please recover from here...".format(dump_path))
            checkpoint_d = {"dump_path" : dump_path,
                            "I"         : i}
            with open("checkpoint.yaml","w") as logp:
                yaml.dump(checkpoint_d, logp)
            exit()
    i+=1 #increment experiment iterator
