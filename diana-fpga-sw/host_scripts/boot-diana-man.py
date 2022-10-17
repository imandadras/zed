#!/usr/bin/env python
import utils.power as power
import atexit
import time
from utils.settings import chdic
from utils.utils import cmd


ZED_TARGET = 'zedb-diana'
flag_file = "~/diana-fpga-sw/TURNVDDEON"

#OPENING PSU
session = power.power()
session.power_set()

def off_sequence():
    session. force_terminate()

atexit.register(off_sequence)

#SETTING PSU
session.channel_active(chdic["plus"])
session.channel_active(chdic["minus"])

_ = input("Press ENTER to start the digital supplies.")
#SETTING VDDIO
session.channel_active(chdic["vddio"])      #voltage to 1.8V

#SETTING VDD
session.channel_active(chdic["vdd"])      #voltage to 1.8V

session.channel_active(chdic["vddmem"])



_ = input("Please start up the FPGA program.")
_ = input("Please start up the chip program.")


print("Waiting for FPGA core to be sync...")
while(cmd("wsl ssh zedb-diana 'test -f {}'".format(flag_file))):
    time.sleep(1)

#turn on vdde
session.channel_active(chdic["vdde"])      #voltage to 1.8V
session.channel_active(chdic["csbias"])

print("Release FPGA core. Sending acknoledge signal...")
cmd("wsl ssh zedb-diana 'rm -rf {}'".format(flag_file))

_ = input("Press ENTER to shot down the supplies.")
