#!/usr/bin/env python
import pyvisa
import time

from    utils.utils import cmd, cd, check_return_zero, current_utctime_string
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass
from    utils.SCP_RTB2004 import SCP_RTB2004

parser = HostScriptParserClass()

#OPENING PSU
RM = pyvisa.ResourceManager()
PSU_N6705B = RM.open_resource(settings.PSU_N6705B_addr,read_termination='\n')
PSU_E36312A = RM.open_resource(settings.PSU_E36312A_addr,read_termination='\n')
SCOPE_RTB2004 = SCP_RTB2004("SCP_RS", settings.SCP_RTB2004_addr)

#setting up PSU
procedures.set_psu(PSU_N6705B,PSU_E36312A)

handlers_args_dic = {"parser":parser}
procedures.off_procedure(process_list=[], PSU_N6705B=PSU_N6705B, PSU_E36312A=PSU_E36312A, **handlers_args_dic)

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="power_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("mkdir ../data/{}".format(RESULT_PARENT_DIR))
check_return_zero(p)
print("Starting the loop experiments...")

MAX_TRIALS=1
DEADLOCK=False
ACT_SIZE=63*63*64
WEIGHT_TILES=1

for im in parser.ima_list:
    for actv_dev in parser.actv_dev_steps: #activ_sparsity
        for weight_sparsity in parser.weight_sparsity_steps:
            DONE=False
            PSU_E36312A.write('SOUR:VOLT {}, (@1)'.format(str(parser.args.cs_bias[0])))
            print("Generating header data files for the experiment...")
            with cd(settings.DIANA_SDK_PATH + "tests"):
                p = cmd("""python3 {sdk_script_name}    -p ana_power_meas\
                                                        -imp {ima}\
                                                        -ima\
                                                        -a NOR\
                                                        -as {activation_size}\
                                                        --actv_loc 0\
                                                        --actv_scale {actv_dev}\
                                                        --actv_clip 1\
                                                        --actv_range 7\
                                                        -w RPD\
                                                        --weight_tiles {weight_tiles}
                                                        --weight_nd {weight_nd}\
                                                        --weight_pd {weight_pd}\
                                                        -crp peak_.yaml\
                                                        -cra""".format(     sdk_script_name=parser.args.sdk_script_name,
                                                                            ima=im,
                                                                            activation_size=ACT_SIZE,
                                                                            actv_dev=actv_dev,
                                                                            weight_tiles=WEIGHT_TILES,
                                                                            weight_nd=(100 - weight_sparsity)//2,
                                                                            weight_pd=(100 - weight_sparsity)//2
                                                                            ), verbose=False, timeout=10*60)
                check_return_zero(p)
            print("Compiling C code...")
            procedures.c_compile(parser)
            dump_path = "../data/" + RESULT_PARENT_DIR + "power_data_WLOADx{}_ACTVxSIGMAx{}_WEIGHTxSPARSITYx{}/".format(     im.split(".")[0],
                                                                                                                str(actv_dev).split(".")[-1],
                                                                                                                weight_sparsity)
            p = cmd("mkdir {}".format(dump_path))
            check_return_zero(p)

            trials = 0
            stuck = False
            while(not DONE):
                if trials:
                    DEADLOCK = True
                trials = 0
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
