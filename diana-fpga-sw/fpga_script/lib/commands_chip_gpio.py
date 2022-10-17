#!/usr/bin/env python
from lib.Bcolors import Bcolors
import lib.FPGA_ISA as instructions
from lib.WritePort import WritePort
from lib.commands_clock import Clock
import time

def chip_acknowledge(ack_value, readPort, verbose=False):
	verbose=True
	#available_tries = 512
	#available_tries = 1000
	available_tries = 5
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

def load_data_to_FPGA(readPort, writePort, filename, n_elements=0, acknowledge=True, verbose=True):
	# Check the inputs
	if n_elements is 0:
		n_elements = sum(1 for line in open(filename))
	if n_elements >= 65536:
		n_elements = 65535
		if verbose:
			print("The input range is too long. We will only process the 65536 first inputs.")
	# Open the input file
	input_file=open(filename,"r")
	# Announce the data transfer to the FPGA FSM
	instruction=(instructions.chip_send_data << 29) | n_elements
	writePort.sendInt(instruction)
	# Send the data
	for i in range(0, n_elements):
		data = input_file.readline()[:-1]
		data = data.replace("x","0")
		writePort.sendInt(int(data,2))
	# Close the input file
	input_file.close()
	if acknowledge:
		ack = chip_acknowledge(instructions.chip_send_data, readPort, verbose)
		if (not ack) and verbose:
			print("Chip data send was not acknowledged.")
	return n_elements

def load_data_from_FPGA(readPort, writePort, n_elements, acknowledge=True, verbose=False):
	# Check the inputs
	if n_elements >= 65535:
		n_elements = 65534
		if verbose:
			print("The input range is too long. We will only process the 65534 first outputs.")
	i = 0
	s = 0
	while i<512:
		i = i + 1
		data = readPort.readInt()
		if not data is None:
			s = s + 1
	if s is not 0:
		if verbose:
			print("Flushed the FIFO of " + str(s) + " data elements.")
	# Announce the data transfer to the FPGA FSM
	#instruction=(instructions.chip_read_data << 29) | (n_elements+1)
	instruction=(instructions.chip_read_data << 29) | n_elements
	writePort.sendInt(instruction)
	# Read the output values from the FIFO
	n = 0
	# The first cycle is not valid, since address generation for the input and output memories is the same
	while n < 1:
		data = readPort.readInt()
		if not data is None:
			n = n + 1
	# The next cycles are valid outputs
	n = 0
	output_values = []
	while n < n_elements:
		data = readPort.readInt()
		if not data is None:
			header = data >> 26
			value  = data - (header << 26)
			output_values.append(value)
			n = n + 1
	if acknowledge:
		ack = chip_acknowledge(instructions.chip_read_data, readPort, verbose)
		if (not ack) and verbose:
			print("Chip data read was not acknowledged.")
	# Return the output values
	return output_values

def set_clock(readPort, writePort, frequency, acknowledge=True, verbose=False):
	clock = Clock()
	freq  = clock.setFrequency(frequency, writePort)
	#Setting the clock requires 24 instructions, so we need to acknowledge all 26 of them.
	if acknowledge:
		for i in range(0,24):
			ack = chip_acknowledge(instructions.chip_setclk, readPort, verbose)
			if (not ack) and verbose:
				print("Clock frequency set was not acknowledged.")
	return freq

def run_chip(readPort, writePort, reset, prog, mem_en, cycles_per_loop, loop_iterations=0, acknowledge=True, verbose=False):
	# Check the inputs
	if (reset>1) or (reset<0):
		reset = 0
		if verbose:
			print("Invalid request for reset value. The chip will not be reset.")
	if (prog>1) or (prog<0):
		prog = 0
		if verbose:
			print("Invalid request for prog value. The chip will treat the data as data (not instructions).")
	if (mem_en>1) or (mem_en<0):
		mem_en = 0
		if verbose:
			print("Invalid request for mem_en value. The chip will not store the data in the interface memory.")
	if cycles_per_loop >= 2**16:
		cycles_per_loop = 2**16 - 1
		if verbose:
			print("Cannot handle this large amount of cycles. Truncating to " + str(2**16 - 1) + ".")
	if loop_iterations >= 2**10:
		loop_iterations = 2**10 - 1
		if verbose:
			print("Cannot handle this large amount of loop iterations. Truncating to " + str(2**10 - 1) + ".")
	# Start the chip
	instruction=(instructions.gpio_test << 29) | (prog << 28) | (mem_en << 27) | (reset << 26) | (loop_iterations << 16) | cycles_per_loop
	writePort.sendInt(instruction)
	if acknowledge and not (loop_iterations == 0):
		ack = chip_acknowledge(instructions.chip_start, readPort, verbose)
		if (not ack) and verbose:
			print("Chip start was not acknowledged.")
	return



