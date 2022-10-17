#!/usr/bin/env python
import utils.power as power
import time

from    utils.utils import cmd, cd, check_return_zero, current_utctime_string
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass
import atexit

parser = HostScriptParserClass()
#cmd ("pushd //wsl$/Ubuntu/home/imandadras/" , shell=True)
#cmd ("pushd c:/" , shell=True)

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="/root/char_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("ssh {} 'mkdir {}'".format(parser.args.zedb_name,RESULT_PARENT_DIR))
check_return_zero(p)
print("Starting the loop experiments...")
print("The script will produce {} iterations".format(len(parser.csbias_steps)*len(parser.actv_uni_steps)*len(parser.weight_pol_steps)))

I_LOOP=1

MAX_TRIALS=20
DEADLOCK=False
for csbias_V in parser.csbias_steps:
    for actv_v in parser.actv_uni_steps:
        for weight_p in parser.weight_pol_steps:
            DONE=False
            #add here possible parameter sweep
            #PSU_E36312A.write('SOUR:VOLT {}, (@1)'.format(str(csbias_V)))
            session = power.power(ana_csbias=csbias_V)
            session.power_set()
            print("Generating header data files for the experiment...")
            with cd(settings.DIANA_SDK_PATH + "tests"):
                p = cmd("""python {sdk_script_name}     -p ana_boot_ex\
                                                        -imp utc_ima.yaml\
                                                        -ima\
                                                        -a UNI\
                                                        -as {activation_size}\
                                                        -v {activation_value}\
                                                        -w STR\
                                                        --weight_pol {weight_polarity}\
                                                        --weight_str_val 1
                                                        --weight_step 2
                                                        -crp char_cra.yaml\
                                                        -cra""".format(    sdk_script_name=parser.args.sdk_script_name,
                                                                            activation_size=4*4*128,
                                                                            activation_value=actv_v,
                                                                            weight_polarity=weight_p
                                                                            ), verbose=True, timeout=10*60)
                check_return_zero(p)
            print("Compiling C code...")
            procedures.c_compile(parser,I_LOOP)
            print("Running the experiment on chip...")
            dump_path = RESULT_PARENT_DIR + "char_data_BIASxP{}_ACTVx{}_WPOLx{}/".format(   str(csbias_V).split(".")[-1],
                                                                                            actv_v,
                                                                                            weight_p if weight_p>0 else "M"+str(abs(weight_p)))
            p = cmd("ssh {} 'mkdir {}'".format(parser.args.zedb_name,dump_path))
            check_return_zero(p)

            trials = 0
            stuck = False
            while(not DONE):
                if trials:
                    DEADLOCK = True
                trials = 0
                while( (procedures.run_diana_experiment(parser, session = session,**{"dump_path":dump_path,"i_loop":I_LOOP})) and (trials<MAX_TRIALS)):
                    print("Experiment with path {} failed! Trying again {}...".format(dump_path,trials))
                    p = cmd("ssh {} 'rm -rf {}/*'".format(parser.args.zedb_name,dump_path))
                    check_return_zero(p)
                    trials+=1
                if(trials==MAX_TRIALS):
                    procedures.reset(session, parser)
                else:
                    DEADLOCK=False
                    DONE=True
                if DEADLOCK:
                    print("Deadlock in execution of experiment {}. Please recover from here...".format(dump_path))
                    with open("checkpoint.txt","w") as logp:
                        logp.write(dump_path)
                    exit()
