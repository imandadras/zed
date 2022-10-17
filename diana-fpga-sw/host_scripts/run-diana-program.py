#!/usr/bin/env python
import pyvisa
import atexit
import time

from    utils.utils import cmd, cd, check_return_zero, current_utctime_string
import  utils.settings as settings
import  host_scripts.utils.procedures as procedures
from    utils.parser import HostScriptParserClass

C_CODE="/users/micas/gsarda/diana/pulp-rt-examples/ana_cell2_bkp"
zedb_name="zedb-diana"

parser = HostScriptParserClass()

#OPENING PSU
RM = pyvisa.ResourceManager()
PSU_N6705B = RM.open_resource(settings.PSU_N6705B_addr)
PSU_E36312A = RM.open_resource(settings.PSU_E36312A_addr)

#setting up PSU
procedures.set_psu(PSU_N6705B,PSU_E36312A)

#---------experiments----------------------------------//
print("Making parent directory for experiment results...")
RESULT_PARENT_DIR="/root/char_data_" + current_utctime_string(settings.TIME_FORMAT) + "/"
p = cmd("ssh {} 'mkdir {}'".format(zedb_name,RESULT_PARENT_DIR))
check_return_zero(p)

print("Starting the experiment...")
procedures.run_diana_experiment(parser,PSU_N6705B,PSU_E36312A,**{"dump_path":RESULT_PARENT_DIR})