import sys
sys.path.append("C:/zedboard/Resnet20/preprocess/")
import utils.power as power
import  utils.settings as settings
from utils.utils import is_alive, non_blocking_cmd, cmd, cd, check_return_zero , pushd
import time
import utils.procedures as procedures
import atexit
from os.path import exists
import preprocess.Inputs as inputs
from preprocess.data_class import InstructionMemory


#settings
#Select which preprocess is needed.
weights = True
activation = True
IMh = True

cs_b = 0.7
results_path = "./results/secondLayer/{}".format(cs_b)

if weights :
    weight = [inputs.weights("./preprocess/test.txt",bottom=True)[1]]
    weight = inputs.mirror_Y(weight)
    weight = inputs.flip_weights(weight)
    weight = inputs.map_weights(weight)
    weight = inputs.flatten_list(weight)

if activation :
    activ = inputs.activations("./preprocess/test.txt")[1]
    inputs.gen_hdata_file("C:/zedboard/Resnet20/C_program/data/input_memory_ania.h", activ, 32, 8, "input_ania",endian="big")

if IMh:
    ima = InstructionMemory(yaml_file="C:/zedboard/Resnet20/preprocess/instructionmemory.yaml", yaml_template="C:/zedboard/diana-sdk/diana_rf_metadata/ima_template.yaml")
    ima.print_hfile("C:/zedboard/Resnet20/C_program/data/instruction_memory_ania.h","im_ania")

if any ([weights, activation, IMh]):
    print ("compiling c code ...")
    procedures.c_compile()



CHECK = [False, False, False]
atexit.register(procedures.off_procedure, CHECK=CHECK)
session = power.power (ana_csbias=cs_b,measurementFolder=results_path+'/power')
print ("starting power")
CHECK[0]=session
session.power_set()
session.channel_active(settings.chdic['plus'])
session.channel_active(settings.chdic['minus'])
session.channel_active(settings.chdic['vddio'])
session.channel_active(settings.chdic['vdd'])
session.channel_active(settings.chdic['vddmem'])

print("Starting the FPGA program...")
zedb_p = non_blocking_cmd("ssh zedb-diana 'source zedb-run-soc.sh'")
if is_alive(zedb_p):
    pass
else:
    print("The zedboard process crashed. Exiting...")
    P = cmd ("ssh zedb-diana killall python3")
    raise IOError

time.sleep(5)
print("Starting the chip program...")
openocd_check = procedures.spawn_openocd_p()
if openocd_check == False:
    print ("openocd check is false")
    procedures.off_procedure(CHECK=CHECK)
    exit()

with cd (results_path):
    non_blocking_cmd ("riscv64-unknown-elf-gdb.exe C:/zedboard/Resnet20/C_program/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/Resnet20/preprocess/gdb-run-soc1.sh")
time.sleep (2)
print("Waiting for FPGA core to be sync...")
time.sleep(1)
#print ("Please run GDB")
#Fat = input ("press enter to continue")

TURNVDDON_C = 0
TURNVDDON_check = True
while cmd("wsl ssh zedb-diana 'test -f /root/diana-fpga-sw/TURNVDDEON'", verbose=True, shell=True):
    print ("flag is not there")
    TURNVDDON_C += 1
    if TURNVDDON_C == 5 :
        TURNVDDON_check = False
        exit()
    time.sleep(1)
if TURNVDDON_check == False:
    procedures.off_procedure(CHECK=CHECK)
    exit()
print ("flag is there")
print ("starting analog supplies")
session.channel_active(settings.chdic['vh'])
session.channel_active(settings.chdic['vdde'])
session.channel_active(settings.chdic['csbias'])
session.initiate()
CHECK[1] = True
time.sleep(1)

print("Release FPGA core. Sending acknoledge signal...")
cmd("wsl ssh zedb-diana 'rm -f ~/diana-fpga-sw/TURNVDDEON'" , shell=True)
CHECK[1] = False
DONE_C=0
DONE_check = True
with cd (results_path):
    while not exists("Done.txt"):
        print ("waiting for the chip program to be completed")
        DONE_C += 1
        if DONE_C == 150:
            DONE_check = False 
            exit()       
        time.sleep(1)
if DONE_check == False:
    procedures.off_procedure(CHECK=CHECK) 
time.sleep(5)
#iman = input ("Press enter to close the program")
cmd ("wsl ssh zedb-diana ' touch /root/diana-fpga-sw/CHAR_DONE'")
CHECK[2] = True
session.terminate()
CHECK[0] = False
time.sleep(2)
print ("running offprocedure")
procedures.off_procedure(CHECK=CHECK) 
atexit.unregister(procedures.off_procedure)
