#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.supplyChannels as supplies
import lib.measurementChannels as measurements
import lib.commands_DAC5724 as DAC
import lib.commands_ADS8331 as ADC
import lib.commands_chip as chip
import time
import numpy as np
import pickle
#import program_setup as program

def preload_memory():
	return

def save_data_to_file(filename, data, format='b'):
	with open(filename, 'w') as f:
		for item in data:
			formatted_data = ""
			if format is 'b':
				formatted_data = str( bin(item) )[2:].zfill(26)
			elif format is 'h':
				formatted_data = str( hex(item) )[2:].zfill(7)
			else:
				formatted_data = str( item )
			f.write("%s\n" % formatted_data)
	return

def try_chip_at_settings(program_file, data_in_file, data_out_file, f, V, ports, interactive=False):
	chipReadPort    = ports[0]
	chipWritePort   = ports[1]
	supplyReadPort  = ports[2]
	supplyWritePort = ports[3]

	print(supplyWritePort)

	vdd_default  =  800 #VDDE
	vddio_default  =  800 #VDD_MEM
	vddsram_default =  1800 #VDDIO
	vddscl_default  = 800 #VDD
	freq_default  =   20

	reset = 1

	# Set the basic settings for the DAC and ADC
	#DAC.DAC_reset(supplyReadPort, supplyWritePort)
	#ADC.ADC_reset(supplyReadPort, supplyWritePort)
	#input("Hit enter to set VDD")
	#DAC.DAC_set_voltage(supplies.VDD, vdd_default, supplyReadPort, supplyWritePort)
	#input("Hit enter to set VDDIO")
	#DAC.DAC_set_voltage(supplies.VDDIO, vddio_default, supplyReadPort, supplyWritePort)
	#input("Hit enter to set VDDSRAM")
	#DAC.DAC_set_voltage(supplies.VDDSRAM, vddsram_default,  supplyReadPort, supplyWritePort)
	#input("Hit enter to set VDDSCL")
	#DAC.DAC_set_voltage(supplies.VDDSCL, vddscl_default,  supplyReadPort, supplyWritePort)
	chip.set_clock(chipReadPort, chipWritePort, freq_default)
	print("clock set done")

	# Load the program to the chip
#	if interactive:
#		input("Hit enter to load the program to the chip...")
#	n_cycles = chip.load_data_to_FPGA(chipReadPort, chipWritePort, program_file)
#	chip.set_clock(chipReadPort, chipWritePort, freq_default)
#	time.sleep(0.1)
#	chip.run_chip(chipReadPort, chipWritePort, reset, 1, 1, n_cycles, 1)

	# Load the data to the chip
#	if interactive:
#		input("Hit enter to load the input data to the chip...")
#	n_cycles = chip.load_data_to_FPGA(chipReadPort, chipWritePort, data_in_file)
#	chip.set_clock(chipReadPort, chipWritePort, freq_default)
#	time.sleep(10)
#	chip.run_chip(chipReadPort, chipWritePort, 1, 1, 1, n_cycles, 1)

	# Run the chip
	if interactive:
		input("Hit enter to set the desired settings (voltages and frequency)...")
	# Set the desired supply voltages
	#DAC.DAC_set_voltage(supplies.VDDIO, V[1], supplyReadPort, supplyWritePort)
	#time.sleep(1)
	#DAC.DAC_set_voltage(supplies.VDD, V[0], supplyReadPort, supplyWritePort)
	#time.sleep(1)
	#DAC.DAC_set_voltage(supplies.VDDSRAM, V[2], supplyReadPort,  supplyWritePort)
	#time.sleep(1)
	#DAC.DAC_set_voltage(supplies.VDDSCL, V[3], supplyReadPort, supplyWritePort)
	#time.sleep(1)
	# Set the desired clock frequency
	chip.set_clock(chipReadPort, chipWritePort, f)
	fll_freq = int(input("Enter fll freq: "))
	fll_freq = int(fll_freq * 1e6 /32768)
	chip.set_fll(chipReadPort, chipWritePort, fll_freq)
	# Actually run the chip
	if interactive:
		input("Hit enter to start the chip...")
	chip.run_chip(chipReadPort, chipWritePort, 0, 0, 0, 1, 0)
	oc = []

	trans = 0	
	trans_index = 0
	i_cnt = 0
	y_hat_data = []
	while (1):
		i_cnt = 0
		read_instr = True
		trans_index = 0
		e2r = False
		input_idx = 0
		output_data_vals = []
		while(read_instr):
			data = chipReadPort.readInt()
			if not data is None:
				if i_cnt == 0:
					print()
				print("instruction: ",i_cnt, data)
				i_cnt += 1
				if i_cnt == 1:
					input_idx = data>>1
					e2r = data&1
				if i_cnt == 2:
					trans = data>>1
					read_instr = False
			time.sleep(0.002)	
		i_cnt = 0
		while(trans_index != trans):
			if e2r:
				input_data = np.uint32(np.int32(input_data_list[trans_index]))
				#print("INPUT DATA", trans_index, input_data)
				chipWritePort.sendInt(input_data)
				chip_wb = False
				while not chip_wb:
					data_x = chipReadPort.readInt()
					if not data is None:
						if data_x == input_data:
							chip_wb = True
				#print(input_data_list[input_idx*768 + trans_index])
				#print(trans_index, input_data)
				trans_index += 1
				#time.sleep(0.002)	
			else:
				data = chipReadPort.readInt()
				if not data is None:
					print(trans_index, data)
					#y_hat_data.append(data)
					#print("output data", hex((data & 0xff000000)>>24), " ",hex((data & 0x00ff0000)>>16)," ", hex((data & 0x0000ff00)>>8), " ",hex((data & 0x000000ff))) 	
					#output_data_vals.append(np.int8((data & 0xff000000)>>24))					
					#output_data_vals.append(np.int8((data & 0x00ff0000)>>16))					
					#output_data_vals.append(np.int8((data & 0x0000ff00)>>8))					
					#output_data_vals.append(np.int8((data & 0x000000ff)>>0))				
					#output_data_vals.append(data)
					trans_index += 1		
					#time.sleep(0.002)	
					#if trans_index == trans and not e2r and not read_instr:
					#if input_idx == 0:
					#	print(trans_index, "Test dataset: expected ", oc[trans_index-1], "received ", hex(data))
					#if input_idx == 1:
					#	print("Test dataset: expected ", hex(int(output_data_list_c1[0][trans_index-1])), "received ", hex(data))
					#if input_idx == 2:
					#	print("Test dataset: expected ", hex(int(output_data_list_c2[0][trans_index-1])), "received ", hex(data))
					#if input_idx == 3:
					#	print("Test dataset: expected ", hex(int(output_data_list_c3[0][trans_index-1])), "received ", hex(data))

	time.sleep(50000)
	# And stop it again
	#chipWritePort   = WritePort("/dev/xillybus_write_chip",32)
	#chipReadPort    = ReadPort("/dev/xillybus_read_chip",32)


	chip.run_chip(chipReadPort, chipWritePort, 1, 0, 0, 1, 1)
	
	# Set the basic settings for the DAC and ADC
	if interactive:
		input("Hit enter to read the results...")
	DAC.DAC_set_voltage(supplies.VDD, vdd_default, supplyReadPort,  supplyWritePort)
	DAC.DAC_set_voltage(supplies.VDDIO, vddio_default, supplyReadPort,  supplyWritePort)
	DAC.DAC_set_voltage(supplies.VDDSRAM, vddsram_default, supplyReadPort,  supplyWritePort)
	DAC.DAC_set_voltage(supplies.VDDSCL, vddscl_default, supplyReadPort,  supplyWritePort)
	chip.set_clock(chipReadPort, chipWritePort, freq_default)
	time.sleep(0.1)

	# Figure out what is in the memory right now
	test_data = chip.load_data_from_FPGA(chipReadPort, chipWritePort, n_cycles, interactive)
	if interactive:
		save_data_to_file("/root/Documents/measurements/FPGA_mem_content_hex.txt",test_data,'h')

	# Read the results
	chip.run_chip(chipReadPort, chipWritePort, 0, 1, 1, n_cycles, 1)
	output_data = chip.load_data_from_FPGA(chipReadPort, chipWritePort, n_cycles, interactive)

	# Write the results to a file
	if interactive:
		save_data_to_file("/root/Documents/measurements/chip_outputs_bin.txt",output_data,'b')
		save_data_to_file("/root/Documents/measurements/chip_outputs_dec.txt",output_data,'d')
		save_data_to_file("/root/Documents/measurements/chip_outputs_hex.txt",output_data,'h')

	# Compare the results to the expected results
	different = False
	n = 0
	for correct_output in open(data_out_file, "r"):
		mask = correct_output.replace("0","1").replace("x","0")
		mask = int(mask,2)
		masked_correct_number = int(correct_output.replace("x","0"),2)
		masked_output_data = output_data[n] & mask
		if not masked_correct_number is masked_output_data:
			different = True
			if interactive:
				print("Output "+str(n)+" was "+str(masked_output_data)+" instead of "+str(masked_correct_number))
		n = n + 1
	# Return whether the chip was operating correctly
	return not different

def critical_supply_voltage(program_file, data_in_file, data_out_file, ports, interactive=False):
	frequency =  400 # MHz
	vdd        =  800 # mV
	vddio      = 1800 # mV
	vddsram    =  800 # mV
	vddscl     =  800 # mV
	vdd_margin =  50 # mV
	vdd_decr   =  10 # mV
	freq_results = []
	vddsram_results = []
	vddscl_results = []
	while frequency >= 5:
		# If we start at a new frequency, we increase the supply voltage by a little bit
		vddsram = vddsram + vdd_margin
		vddscl = vddscl + vdd_margin
		# If we start at a new frequency, we want to keep track whether we have atually had a success
		at_least_one_success = False
		# Loop over the common supply voltage
		success = True
		while success:
			vddsram = vddsram - vdd_decr
			vddscl = vddscl - vdd_decr
			print("Trying to drop VDDSRAM to " + str(vddsram) + "/" + str(vddscl) + "...")
			# Run the chip
			success = try_chip_at_settings(program_file, data_in_file, data_out_file, frequency, [vdd,vddio,vddsram,vddscl], ports, interative)
			if success:
				at_least_one_success = True
		vddsram = vddsram + vdd_decr
		vddscl = vddscl + vdd_decr
		# Loop over VDD only
		success = True
		while success:
			vdd = vdd - vdd_decr
			print("Trying to drop VDD to " + str(vdd) + "...")
			# Run the chip
			success = try_chip_at_settings(program_file, data_in_file, data_out_file, frequency, [vdd,vddio,vddsram,vddscl], ports, interactive)
			if success:
				at_least_one_success = True
		vdd = vdd + vdd_decr
		# Loop over VDDIO only
		success = True
		while success:
			vddio = vddio - vdd_decr
			print("Trying to drop VDDIO to " + str(vddio) + "...")
			# Run the chip
			success = try_chip_at_settings(program_file, data_in_file, data_out_file, frequency, [vdd,vddio,vddsram,vddscl], ports, interactive)
			if success:
				at_least_one_success = True
		vddio = vddio + vdd_decr
		# Add the new point to the list
		if at_least_one_success:
			freq_results.append(frequency)
			vdd_results.append(vdd)
			vddio_results.append(vddio)
		# Let's move to the next frequency
		frequency = frequency * 9 / 10
	# Return the results
	return [vdd_results, vddio_results, freq_results]

def power_consumption():
	return

def minimum_energy_point():
	return

def run_all(interactive=False):
	supplyWritePort = WritePort("/dev/xillybus_write_supplies",32)
	supplyReadPort  = ReadPort("/dev/xillybus_read_supplies",32)

	chipWritePort   = WritePort("/dev/xillybus_write_chip",32)
	chipReadPort    = ReadPort("/dev/xillybus_read_chip",32)

	if not supplyWritePort.openPort():
		print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
		quit()
	if not supplyReadPort.openPort():
		print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
	if not chipWritePort.openPort():
		print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)
		quit()
	if not chipReadPort.openPort():
		print(Bcolors.FAIL + "Could not open write port, quitting" + Bcolors.ENDC)

	ports = [chipReadPort, chipWritePort, supplyReadPort, supplyWritePort]

	# Test 1: just try to run the chip
	if interactive:
		input("Hit enter to start the chip for a first test.")
	#data_in_file = "/root/Documents/images/chip_data_in.txt"
	#data_out_file = "/root/Documents/images/chip_data_out.txt"
	#program_file = "/root/Documents/program/critpath_24b_1hop.txt"

	data_in_file = "/root/Documents/images/test.txt"
	data_out_file = data_in_file
	program_file = data_in_file
	
	soc_freq = 5 #MHz

	success = try_chip_at_settings(program_file, data_in_file, data_out_file, soc_freq, [800,800,1800,800], ports, interactive)
	if success:
		print("Test has completed successfully.")
	else:
		print("Test has completed. No success :(")

	# Test 2: critical supply voltage
	#if interactive:
	#	input("Hit enter to start the critical supply voltage measurements.")
	#[Vddc, Vddm,f] = critical_supply_voltage("", "", "", ports, interactive)

	# Close ports
	supplyWritePort.closePort()
	supplyReadPort.closePort()
	chipWritePort.closePort()
	chipReadPort.closePort()

	return

if __name__ == '__main__':
    run_all(True)
