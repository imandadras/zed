#!/usr/bin/env python
import  pyvisa
import  time
import  yaml
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

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="MEM_char_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("mkdir ../data/{}".format(RESULT_PARENT_DIR))
check_return_zero(p)

with cd(settings.DIANA_SDK_PATH + "tests"):
    p = cmd("""python3 {sdk_script_name}    -p memcopy_loops\
                                            -a NOR\
                                            -as {activation_size}\
                                            --actv_loc 0\
                                            --actv_scale {actv_dev}\
                                            --actv_clip 1\
                                            --actv_range 7""".format(   sdk_script_name=parser.args.sdk_script_name,
                                                                        activation_size=128*1024,
                                                                        actv_dev=1/6), verbose=True, timeout=10*60)
check_return_zero(p)
print("Compiling C code...")
procedures.c_compile(parser, gen_data_h=False)
print("Running the experiment on chip...")
dump_path = "../data/" + RESULT_PARENT_DIR
while( (procedures.run_diana_experiment(parser, PSU_N6705B, PSU_E36312A, SCOPE_RTB2004, memchar_path=dump_path, sync_out=False, dump_path="."))):
    print("Experiment with path {} failed! Trying again...".format(dump_path))
    p = cmd("rm -rf {}/*".format(dump_path))