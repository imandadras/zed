from lib.Bcolors import Bcolors as Bcol
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip

import time
import os

base_clk = 5 #MHz


chipWritePort   = WritePort("/dev/xillybus_write_chip",32)
chipReadPort    = ReadPort("/dev/xillybus_read_chip",32)
if not chipWritePort.openPort():
    Bcol.printError("Could not open write port, quitting")
    quit()
if not chipReadPort.openPort():
    Bcol.printError("Could not open read port, quitting")
    quit()

Bcol.printInfo("Starting booting procedure ...")
time.sleep(0.5)

Bcol.printInfo("Setting base clock freq to {} MHz...".format(base_clk))
time.sleep(0.5)
chip.set_clock(chipReadPort, chipWritePort, base_clk)

Bcol.printInfo("Setting FLL freq to 260 MHz...")
time.sleep(0.5)
chip.set_fll(   chipReadPort, 
                chipWritePort, 
                int(260 * 1e6 /32768))

Bcol.printInfo("Starting the chip...")
time.sleep(0.5)
chip.run_chip(chipReadPort, chipWritePort, 0, 0, 0, 1, 0)

Bcol.printInfo("Triggering the boot procedure...")
time.sleep(0.5)
chip.trigger_boot(chipReadPort, chipWritePort)


#wait for VDDE_ON request
Bcol.printInfo("Waiting for VDDE ON request...")
lock = True
while(lock):
    data = chipReadPort.readInt()
    if(data==0x12345678):
        lock=False
lock = True
while(lock):
    data = chipReadPort.readInt()
    if(data==0x11111111):
        lock=False
Bcol.printInfo("Turning VDDE ON...")
time.sleep(0.5)
flag_file="TURNVDDEON"
Bcol.printInfo("Sending VDDE ON rqst signal...")
if (os.path.exists(flag_file)):
    Bcol.printError("Flag file exists already. Error in the sync process. Exiting...")
    exit()
open(flag_file,"w")

Bcol.printInfo("Waiting for host to acknoledge...")
while (os.path.exists(flag_file)):
    time.sleep(1)
Bcol.printPassed("Host ack VDDE is ON!")
chip.vddeon_ack(chipReadPort, chipWritePort, acknowledge=False)

end_flag_file="CHAR_DONE"
while (os.path.exists(end_flag_file)==0):
    time.sleep(1)
       

chipWritePort.closePort()
chipReadPort.closePort()