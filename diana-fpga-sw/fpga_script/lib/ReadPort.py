import os
import io
import struct
from lib.Bcolors import Bcolors as Bc

class ReadPort:
	readPortCount = 0
	
	def __init__(self, devfile, width):
	
		if width%8 != 0:
			Bc.printError(" width: " + str(width) + " is no multiple of 8 bits (1 byte)")
		else:
			self.devfile = devfile
			self.width = width
			self.nbBytes = width/8
			self.portId = 0
			ReadPort.readPortCount += 1
	
	def __exit__(self, exc_type, exc_value, traceback):
		self.closePort
		
	def openPort(self):
		self.portId = os.open(self.devfile, os.O_RDONLY | os.O_NONBLOCK)
		if self.portId == 0:
			Bc.printError("Could not open " + self.devfile + " for read")
			return False
		else:
			return True
			
	def closePort(self):
		os.close(self.portId)
		self.portId = 0
		#self.portId.close()
		
		
	def readString(self, size):
		try:
			data = os.read(self.portId,size)
			return data
		except:
			return ""
	def readByte(self):
		try:
			data = os.read(self.portId,1)
			return struct.unpack("B",data)[0]
		except:
			return None
			
	def readInt(self):
	
		try:
			data = os.read(self.portId,4)
			return struct.unpack("I",data)[0]
		except:
			return None
			
			
	def readIntArray(self,length):
		data = os.read(self.portId,4*length)
		return struct.unpack("%si" % length, data)
		
	def readFloat(self):
		data = os.read(self.portId,4)
		return struct.unpack("f",data)[0]
		
	def readFloatArray(self,length):
		data = os.read(self.portId,4*length)
		return struct.unpack("%sf" % length, data)
		
	def readDouble(self):
		data = os.read(self.portId,8)
		return struct.unpack("d",data)[0]
		
	def readDoubleArray(self,length):
		data = os.read(self.portId,8*length)
		return struct.unpack("%sd" % length, data)
		
