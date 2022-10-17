import os
import sys
from lib.Bcolors import Bcolors as Bc
import struct

class WritePort:
	writePortCount = 0
	
	def __init__(self, devfile, width, dummy=False):
	
		if width%8 != 0:
			Bc.printError("width: " + str(width) + " is no multiple of 8 bits (1 byte)")
		else:
			self.devfile = devfile
			self.width = width
			self.portId = 0
			self.totalBytesForTransmission = 0
			self.totalBytesTransmitted = 0
			WritePort.writePortCount += 1
			self.dummy = dummy
			self.dummyId = 0
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.closePort
		
	def openPort(self):
		self.portId = open(self.devfile, 'wb',0)
		if self.portId == 0:
			Bc.printError("Could not open " + devfile + " for write")
			return False
		else:
			#Bc.printInfo("Succesfully opened write port to " + self.devfile)
			
			if self.dummy:
				self.dummyId = open("./writeLog_" + str(WritePort.writePortCount), 'w')
				Bc.printInfo("Opened dummy port with id " + str(self.dummyId))
			
			return True
			
	def closePort(self):
		self.portId.close()
		if self.dummy:
			os.close(self.dummyId)
	
	def __sendData(self, data):
		#print("Sending " + str(data))
		sizeReq = len(data)
		sizeSend = self.portId.write(data)
		#self.portId.write("")
		#self.totalBytesForTransmission += sizeReq
		#self.totalBytesTransmitted += sizeSend
		#if(sizeReq != sizeSend):
		#	print(Bcolors.WARNING + "WARNING: Not all data transmitted" + Bcolors.ENDC)
		#	return False
		#else:
		#	if self.dummy:
		#		self.dummyId.write(data)
		#		print("Send data is:")
		#		print(str(struct.unpack('i',data)[0]))
		#	
		return True
			
	def sendString(self,data):
		print("send", data)
		return self.__sendData(data)
	
	def sendByte(self,num):
		data = struct.pack("B",num)
		return self.__sendData(data)
					
	def sendInt(self,num):
		data = struct.pack("I",num)
		return self.__sendData(data)
	
	def sendIntArray(self, array):
		data = struct.pack("%si" % len(array),*array)
		return self.__sendData(data)
			
	def sendFloat(self,num):
		data = struct.pack("f",num)
		return self.__sendData(data)
			
	def sendFloatArray(self, array):
		data = struct.pack("%sf" % len(array),*array)
		return self.__sendData(data)
	
	def sendDouble(self,num):
		data = struct.pack("d",num)
		return self.__sendData(data)
			
	def sendDoubleArray(self, array):
		data = struct.pack("%sd" % len(array),*array)
		return self.__sendData(data)
			
	def getBytesLost(self):
		return self.totalBytesForTransmission - self.totalBytesTransmitted
