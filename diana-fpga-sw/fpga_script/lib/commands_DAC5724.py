#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.FPGA_ISA as instructions
import time

def DAC_acknowledge(ack_value, readPort, verbose=False):
	verbose = True
	available_tries = 512
	command_acknowledged = False
	while (not command_acknowledged) and (available_tries>0):
		available_tries = available_tries - 1
		data = readPort.readInt()
		if not data is None:
			if data==ack_value:
				command_acknowledged = True
			elif verbose:
				print("Encountered an unexpected value while waiting for acknowledgement.")
				print("Value was " + str(data) + ", but expected " + str(ack_value) + ".")
		time.sleep(0.01)
	if not command_acknowledged:
		print("ERROR: command was not acknowledged")
	return command_acknowledged

def DAC_reset(readPort, writePort, acknowledge=True, verbose=False):
	# Basic settings for the DAC
	channel = 4
	register = 1
	data = 3
	dac_setup_part1 = (instructions.dac_config << 29) | (channel << 19) | (register << 16) | data
	channel = 0
	register = 2
	data = 15
	dac_setup_part2 = (instructions.dac_config << 29) | (channel << 19) | (register << 16) | data
	channel = 1
	register = 3
	data = 4
	dac_setup_part3 = (instructions.dac_config << 29) | (channel << 19) | (register << 16) | data
	# Set the basic settings for the DAC
	writePort.sendInt(dac_setup_part1)
	if acknowledge:
		ack = DAC_acknowledge(instructions.dac_config, readPort, verbose)
		if (not ack) and verbose:
			print("DAC setup part 1 was not acknowledged.")
	writePort.sendInt(dac_setup_part2)
	if acknowledge:
		ack = DAC_acknowledge(instructions.dac_config, readPort, verbose)
		if (not ack) and verbose:
			print("DAC setup part 1 was not acknowledged.")
	writePort.sendInt(dac_setup_part3)
	if acknowledge:
		ack = DAC_acknowledge(instructions.dac_config, readPort, verbose)
		if (not ack) and verbose:
			print("DAC setup part 1 was not acknowledged.")

def DAC_set_voltage(channel, voltage, readPort, writePort, acknowledge=True, verbose=False):
	if voltage >= 0:
		voltage_DAC = int( (voltage * 10) / 1.252 )
	else:
		voltage_DAC = (1<<16) - int( (-voltage * 10) / 1.252 )
	register = 0
	instruction = (instructions.dac_config << 29) | (channel << 19) | (register << 16) | voltage_DAC
	writePort.sendInt(instruction)
	if acknowledge:
		ack = DAC_acknowledge(instructions.dac_config, readPort, verbose)
		if (not ack) and verbose:
			print("DAC instruction was not acknowledged.")

