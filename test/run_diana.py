from lib.Bcolors import Bcolors as Bcol
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.commands_chip as chip
from utils.parser import FPGAScriptParserClass

import time
import os

base_clk = 5 #MHz

parser = FPGAScriptParserClass()

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

Bcol.printInfo("Setting FLL freq to {} MHz...".format(parser.args.fll_clk))
time.sleep(0.5)
chip.set_fll(   chipReadPort, 
		chipWritePort, 
		int(parser.args.fll_clk * 1e6 /32768))

Bcol.printInfo("Starting the chip...")
time.sleep(0.5)
chip.run_chip(chipReadPort, chipWritePort, 0, 0, 0, 1, 0)

Bcol.printInfo("Triggering the boot procedure...")
time.sleep(0.5)
chip.trigger_boot(chipReadPort, chipWritePort)

if (not parser.args.digital_only):
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

if parser.rx_link:
	Bcol.printInfo("Channel open for transmission...")
	tx = True
	size = 128
	arr = size*[0]
	cc = 0
	with open("log.txt","w") as logout:
		while(tx):              #TODO improve this blob
			i_cnt = 0
			read_instr = True
			trans_index = 0
			logout.write("Transmission number {}\n".format(cc))
			while(read_instr):
				data = chipReadPort.readInt()
				if not data is None:
					i_cnt += 1
					logout.write("instruction: {}, {}\n".format(i_cnt, data))
					if i_cnt == 1:
						pass #used to express direction of connectivity
					if i_cnt == 2:
						trans = data>>1
						read_instr = False
				time.sleep(0.002)
			i_cnt = 0
			print (i_cnt)
			logout.write(str(trans)+"\n")
			while(trans_index != trans):
				data = chipReadPort.readInt()
				if not data is None:
				#print(trans_index, data)
					arr[trans_index%size]=data
				if (trans_index==size-1):
					with open(parser.args.dump_path +"char_data{}.dat".format(cc),"w") as outp:
						for i in range(len(arr)):
							outp.write(hex(arr[i])+"\n")
					cc+=1
				trans_index += 1
		if(cc==parser.args.rx_packet_num):
			tx=False
end_flag_file="CHAR_DONE"
Bcol.printInfo("Sending DONE rqst signal...")
if (os.path.exists(end_flag_file)):
	Bcol.printError("End flag file exists already. Error in the sync process. Exiting...")
	exit()
open(end_flag_file,"w")
while (os.path.exists(end_flag_file)):
	time.sleep(1)
chipWritePort.closePort()
chipReadPort.closePort()
