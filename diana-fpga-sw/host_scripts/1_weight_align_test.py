#!/usr/bin/env python
import pyvisa
import time

from    utils.utils import cmd, cd, check_return_zero, current_utctime_string
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass

parser = HostScriptParserClass()

#OPENING PSU
RM = pyvisa.ResourceManager()
PSU_N6705B = RM.open_resource(settings.PSU_N6705B_addr)
PSU_E36312A = RM.open_resource(settings.PSU_E36312A_addr)

#setting up PSU
procedures.set_psu(PSU_N6705B,PSU_E36312A)

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="/root/weight_align_test_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("ssh {} 'mkdir {}'".format(parser.args.zedb_name,RESULT_PARENT_DIR))
check_return_zero(p)
print("Starting the loop experiments...")
print("Generating header data files for the experiment...")
with cd(settings.DIANA_SDK_PATH + "tests"):
    p = cmd("""python3 {sdk_script_name}    -p ana_boot_ex\
                                            -imp 1_wat_ima.yaml\
                                            -ima\
                                            -a ROW\
                                            -as {activation_size}\
                                            -v {activation_value}\
                                            --actv_start_row 0\
                                            --actv_range_row 1\
                                            --actv_batch_size 1152\
                                            --actv_batch_num 4\
                                            -w CLM\
                                            --weight_pol {weight_polarity}\
                                            --weight_start_row 0
                                            --weight_batch_row 64
                                            --weight_start_col 0
                                            --weight_batch_col 1
                                            -crp char_cra.yaml\
                                            -cra""".format(    sdk_script_name=parser.args.sdk_script_name,
                                                                activation_size=4*4*128,
                                                                activation_value=parser.actv_uni_steps[0],
                                                                weight_polarity=parser.weight_pol_steps[0],
                                                                 
                                                                ), verbose=True, timeout=10*60)
    check_return_zero(p)
print("Compiling C code...")
procedures.c_compile(parser)
dump_path = RESULT_PARENT_DIR + "wat/"
p = cmd("ssh {} 'mkdir {}'".format(parser.args.zedb_name,dump_path))
check_return_zero(p)
while(procedures.run_diana_experiment(parser,PSU_N6705B,PSU_E36312A,**{"dump_path":dump_path})):
    print("Experiment with path {} failed! Trying again...".format(dump_path))
    p = cmd("ssh {} 'rm -rf {}/*'".format(parser.args.zedb_name,dump_path))
    check_return_zero(p)