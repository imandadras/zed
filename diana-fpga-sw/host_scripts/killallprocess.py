import utils.power as power
import time
from utils.procedures import off_procedure
from    utils.parser import HostScriptParserClass

session = power.power()

off_procedure (CHECK=[session,True])