#!/usr/bin/env python
import utils.power as power
import atexit
import time

from utils.utils import cmd

import utils.settings as settings
import utils.procedures as procedures
from utils.parser import HostScriptParserClass

parser = HostScriptParserClass()

#OPENING PSU
session = power.power()

#setting up PSU
session.power_set()

#registering off handler
nb_process_list = []
handlers_args_dic = {"parser":parser}
atexit.register(procedures.off_procedure, nb_process_list, **handlers_args_dic)

print("Starting the digital supplies...")
#TURNING ON DIGITAL SUPPLIES
session.channel_active(settings.chdic['board_plus'])
session.channel_active(settings.chdic['board_minus'])
session.channel_active(settings.chdic['vddio'])
session.channel_active(settings.chdic['vdd'])

print("Starting the FPGA program...")
zedb_p = procedures.spawn_zedb_p(parser)
nb_process_list += [("ZEDBP",zedb_p)]

print("Starting the chip program...")
openocd_p = procedures.spawn_openocd_p()
nb_process_list += [("OPENOCD",openocd_p)]

gdb_session_p = procedures.spawn_gdb_p(parser)
nb_process_list += [("GDB",gdb_session_p)]

print("Waiting for FPGA core to be sync...")
while(cmd("ssh {} 'test -f {}'".format(parser.args.zedb_name, settings.VDDE_FLAG_FILE))):
    time.sleep(1)

session.channel_active(settings.chdic['vdde'])
session.channel_active(settings.chdic['ana_vh'])


print("Release FPGA core. Sending acknoledge signal...")
cmd("ssh zedb-diana 'rm -rf {}'".format(settings.VDDE_FLAG_FILE))

#TODO good to have a synch here
_ = input("Press ENTER to shot down the supplies.")
