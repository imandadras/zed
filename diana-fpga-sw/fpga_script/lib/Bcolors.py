

class Bcolors:
	HEADER = '\033[95m'
	OKBLUE = '\033[94m'
	OKGREEN = '\033[92m'
	WARNING = '\033[93m'
	FAIL = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'
	
	@staticmethod
	def printInfo(string):
		print(Bcolors.OKBLUE + "INFO: " + string + Bcolors.ENDC)
		
	@staticmethod
	def printPassed(string):
		print(Bcolors.OKGREEN + "PASSED: " + string + Bcolors.ENDC)
		
	@staticmethod
	def printWarning(string):
		print(Bcolors.WARNING + "WARNING: " + string + Bcolors.ENDC)
		
	@staticmethod
	def printError(string):
		print(Bcolors.FAIL + "ERROR: " + string + Bcolors.ENDC)
