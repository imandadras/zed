#!/usr/bin/env python
import  pyvisa
import  time
import  yaml
from    utils.utils import cmd, cd, check_return_zero, current_utctime_string
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass
from    utils.SCP_RTB2004 import SCP_RTB2004
import  pickle

def change_ut(ima_file, ut, instr=0):
    with open(settings.DIANA_SDK_PATH+"measurement_inputs/aim/{}".format(ima_file), "r") as f:
        list_doc = yaml.safe_load(f)
        list_doc[instr]["INSTR1"]["UNIT_TIME"] = ut
    with open(settings.DIANA_SDK_PATH+"measurement_inputs/aim/{}".format(ima_file), "w") as f:
        yaml.dump(list_doc, f)

parser = HostScriptParserClass()

#OPENING PSU
RM = pyvisa.ResourceManager()
PSU_N6705B = RM.open_resource(settings.PSU_N6705B_addr,read_termination='\n')
PSU_E36312A = RM.open_resource(settings.PSU_E36312A_addr,read_termination='\n')
SCOPE_RTB2004 = SCP_RTB2004("SCP_RS", settings.SCP_RTB2004_addr)

#setting up PSU
procedures.set_psu(PSU_N6705B,PSU_E36312A)

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="power_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("mkdir ../data/{}".format(RESULT_PARENT_DIR))
check_return_zero(p)
print("Starting the loop experiments...")

MAX_TRIALS=2
DEADLOCK=False
ACT_SIZE=63*63*64
WEIGHT_POLARITY = 1
PARAM_INDEX = 0

#Not general line
pareto_cfg = pickle.load(open("../data/characterization_pareto.pickle","rb"))
pareto_cfg.sort_index(inplace=True)

for act in pareto_cfg.act.unique():
    for index, cfg in pareto_cfg[pareto_cfg.act == act].iterrows():
        if index < PARAM_INDEX:
            continue
        with open("param_done.txt", "a") as f:
            f.write(f'{int(index)}\n') 
        DONE=False
        #add here possible parameter sweep
        PSU_E36312A.write('SOUR:VOLT {}, (@1)'.format(str(cfg.bias)))
        print("Generating header data files for the experiment...")
        with cd(settings.DIANA_SDK_PATH + "tests"):
            change_ut("peak_.yaml",int(cfg.tunit), instr=1)
            print(cfg)
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
                                                                        activation_value=int(cfg.act),
                                                                        weight_polarity=WEIGHT_POLARITY
                                                                        ), verbose=False, timeout=10*60)
            check_return_zero(p)
        print("Compiling C code...")
        procedures.c_compile(parser)
        print("Running the experiment on chip...")
        dump_path = "../data/" + RESULT_PARENT_DIR + "POWER_char_data_BIASxP{}_ACTVx{}_WPOLx{}_UTx{}/".format(   str(cfg.bias).split(".")[-1],
                                                                                        int(cfg.act),
                                                                                        WEIGHT_POLARITY if WEIGHT_POLARITY>0 else "M"+str(abs(WEIGHT_POLARITY)),
                                                                                        int(cfg.tunit))
        p = cmd("mkdir {}".format(dump_path))
        check_return_zero(p)

        trials=0
        stuck=False
        while(not DONE):
            if trials:
                DEADLOCK=True
            trials=0
            while((procedures.run_diana_experiment(parser, PSU_N6705B, PSU_E36312A, SCOPE_RTB2004, power_path=dump_path, sync_out=False,**{"dump_path":"."})) and (trials<MAX_TRIALS)):
                print("Experiment with path {} failed! Trying again {}...".format(dump_path,trials))
                p = cmd("rm -rf {}/*".format(dump_path))
                check_return_zero(p)
                trials+=1
            if(trials==MAX_TRIALS):
                procedures.reset(PSU_N6705B, PSU_E36312A, parser)
            else:
                DEADLOCK=False
                DONE=True
            if DEADLOCK:
                print("Deadlock in execution of experiment {}. Please recover from here...".format(dump_path))
                with open("checkpoint.txt","w") as logp:
                    logp.write(dump_path)
                exit()