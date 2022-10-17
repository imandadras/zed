#!/usr/bin/env python
from lib.Bcolors import Bcolors
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
from lib.ReadPort import ReadPort
import lib.FPGA_ISA as instructions
import lib.measurementChannels as measurementChannels
import lib.calibration_VDD as coeff_VDD
import lib.calibration_VDDIO as coeff_VDDIO
import lib.calibration_VDDSCL as coeff_VDDSCL
import lib.calibration_VDDSRAM as coeff_VDDSRAM
import time

def ADC_acknowledge(ack_value, readPort, verbose=False):
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

def ADC_reset(readPort, writePort, acknowledge=True, verbose=False):
	# Basic settings for the ADC
	sw_reset = 0
	adc_setup_part1 = (instructions.adc_config << 29) | sw_reset
	start_config = 1021 + 1024
	adc_setup_part2 = (instructions.adc_config << 29) | start_config
	# Set the basic settings for the ADC
	writePort.sendInt(adc_setup_part1)
	if acknowledge:
		ack = ADC_acknowledge(instructions.adc_command,readPort,verbose)
		if (not ack) and verbose:
			print("ADC reset part 1 was not acknowledged")
	else:
		time.sleep(0.1)
	writePort.sendInt(adc_setup_part2)
	if acknowledge:
		ack = ADC_acknowledge(instructions.adc_command,readPort,verbose)
		if (not ack) and verbose:
			print("ADC reset part 2 was not acknowledged")


def ADC_flush(readPort, verbose=False):
	i=0
	s=0
	while i<512:
		i = i + 1
		data = readPort.readInt()
		if not data is None:
			s = s + 1
	if verbose and (not s == 0):
		print("Flushing the FIFO has purged " + str(s) + " values.")
	return

def ADC_measure(readPort, writePort, channel, frequency, n_values=0, averaged=True, acknowledge=True, verbose=False):
	# Reset the ADC
	ADC_reset(readPort, writePort, acknowledge, verbose)
	# Check the inputs for correctness
	if n_values>=2**13:
		n_values = 2**13 - 1
		if verbose:
			print("Cannot sample the requested amount of values. Sampling " + str(n_values) + " instead.")
	# Signal the ADC which channel is to be sampled
	instruction = (instructions.adc_command << 29) | (channel << 12)
	writePort.sendInt(instruction)
	if acknowledge:
		ack = ADC_acknowledge(instructions.adc_command, readPort, verbose)
		if (not ack) and verbose:
			print("ADC channel selection was not acknowledged")
	# Before starting to sample, draw all values from the FIFO
	ADC_flush(readPort, verbose)
	# Calculate the number of cycles between 2 samples
	period = int((25*10**6 / frequency -1))  # FPGA fabric runs at 25 MHz
	if period<100:
		period=99
		if verbose:
			print("Warning: cannot reach such fast measurements. Resetting to approximately 250 kHz.")
	if period>(1<<16):
		period=65535
		if verbose:
			print("Warning: cannot reach such slow measurements. Resetting to approximately 382 Hz.")
	# Start the ADC
	instruction = (instructions.adc_sample_n << 29) | (n_values << 16) | period
	writePort.sendInt(instruction)
	# Read the samples from the FIFO
	n = 0
	measurements = []
	while n < n_values:
		data = readPort.readInt()
		if not data is None:
			header = data >> 16
			value  = data - (header << 16)
			measurements.append(value)
			n = n + 1
			#if verbose:
			#	print("Measured " + str(n) + " values.")
	if acknowledge:
		ADC_acknowledge(instructions.adc_sample, readPort, verbose)
		if (not ack) and verbose:
			print("ADC sample state was not acknowledged")
	# Return the output values
	if averaged:
		return sum(measurements) / len(measurements) / 135
		#return mean(measurements)
	else:
		return measurements / 135

def ADC_apply_calibration(raw_data, channel, voltage):
	if channel is measurementChannels.VDD:
		alpha = coeff_VDD.alpha
		beta  = coeff_VDD.beta
		I_LDO = coeff_VDD.I_LDO
		G_load= coeff_VDD.G_load
	elif channel is measurementChannels.VDDIO:
		alpha = coeff_VDDIO.alpha
		beta  = coeff_VDDIO.beta
		I_LDO = coeff_VDDIO.I_LDO
		G_load= coeff_VDDIO.G_load
	elif channel is measurementChannels.VDDSCL:
		alpha = coeff_VDDSCL.alpha
		beta  = coeff_VDDSCL.beta
		I_LDO = coeff_VDDSCL.I_LDO
		G_load= coeff_VDDSCL.G_load
	elif channel is measurementChannels.VDDSRAM:
		alpha = coeff_VDDSRAM.alpha
		beta  = coeff_VDDSRAM.beta
		I_LDO = coeff_VDDSRAM.I_LDO
		G_load= coeff_VDDSRAM.G_load
	else:
		print("ERROR: invalid measurement channel")
	# Process all data with the correct compensation coefficients
	calibrated_data = []
	for raw_value in raw_data:
		calibrated_value = 1 / beta * ( int(raw_value) - (I_LDO + G_load*voltage) - alpha)
		calibrated_data.append(calibrated_value)
	return calibrated_data

