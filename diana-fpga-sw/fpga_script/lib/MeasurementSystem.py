#!/usr/bin/env python
from lib.WritePort import WritePort
from lib.ReadPort import ReadPort
import lib.FPGA_ISA as instructions
import time
class MeasurementSystem(object):
	def __init__(self):

		self.chipWritePort = WritePort("/dev/xillybus_write_chip",32)
		self.chipReadPort = ReadPort("/dev/xillybus_read_chip",32)

	def initialize(self):
		print("WritePort Open Success:",str(self.chipWritePort.openPort()))
		print("ReadPort Open Success:",str(self.chipReadPort.openPort()))
		
	def acknowledge(self,ack_value):
		available_tries = 1000
		command_acknowledged = False
		while (not command_acknowledged) and (available_tries>0):
			available_tries = available_tries - 1
			data = self.chipReadPort.readInt()
			if not data is None:
				if data==ack_value:
					command_acknowledged = True
			time.sleep(0.01)
		return command_acknowledged
		
	def setupScanChain(self,scanChainDataIn=[]):
		ack = self.sendDataToFPGA(scanChainDataIn)
		print("ScanChain Data Send Success:",str(ack))
		instruction=(instructions.chip_activate_scan_chain << 29)
		self.chipWritePort.sendInt(instruction)
		ack = self.acknowledge(instructions.chip_activate_scan_chain)
		print("Activate ScanChainSuccess:",str(ack))
		dataOut, success = self.loadDataFromFPGA(len(scanChainDataIn))
		return dataOut, success

	def setupFLL(self,fllCfgData,fllCfgAddr):
		instruction=(instructions.chip_setfll << 29)
		self.chipWritePort.sendInt(instruction)
		self.chipWritePort.sendInt(fllCfgAddr)
		lsb = fllCfgData&((1<<16)-1)
		msb = fllCfgData>>16
		self.chipWritePort.sendInt(lsb)
		self.chipWritePort.sendInt(msb)
		return self.acknowledge(instructions.chip_setfll)

	def sendDataToFPGA(self,dataIn=[]):
		instruction=(instructions.chip_send_data << 29) + len(dataIn)
		self.chipWritePort.sendInt(instruction)
		for item in dataIn:
			self.chipWritePort.sendInt(item)
		return self.acknowledge(instructions.chip_send_data)


	def loadDataFromFPGA(self, n_elements=1):
		i = 0
		s = 0
		while i < 512:
			i = i + 1
			data = self.chipReadPort.readInt()
			if not data is None:
				s = s + 1
		instruction=(instructions.chip_read_data << 29) + n_elements+1
		self.chipWritePort.sendInt(instruction)	
		n = 0
		output_values = []
		while n < n_elements+1:
			data = self.chipReadPort.readInt()
			if not data is None:
				if n > 0:
					output_values.append(data)
				n = n + 1
		return output_values, self.acknowledge(instructions.chip_read_data)
