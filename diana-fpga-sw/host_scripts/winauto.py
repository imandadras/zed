from os import mkdir
from os.path import exists
import utils.power as power
from    utils.utils import cd, check_return_zero, current_utctime_string, cmd, non_blocking_cmd
import subprocess
import shlex
import  utils.settings as settings
import  utils.procedures as procedures
from    utils.parser import HostScriptParserClass
import atexit
import time 
from pathlib import Path


#set the variables here
csbias_steps = [0.6]
activations = [4]
weight_polarity = [1]
N_tests = 4

sess = []
atexit.register(procedures.off_procedure, session=sess)
print ("Making the parent directory for experiment results")


weight_form= "ONE"
make_directory = subprocess.Popen(shlex.split("ssh zedb-diana mkdir results"), stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell= True)
#if not make_directory.wait == 0:

 #   print ('the result directory did not make. See the line below:')
for l in make_directory.stdout:
    print (l)
    
    #exit()



"""""
cs_default = [0.6]
cs = True
while (cs):
    csbias_steps = input ("Please insert the values for csbiase steps, seperate float numbers with space for each experiment. pass empty "\
        "value for using default {}:  ".format(cs_default))
    csbias_steps = csbias_steps or cs_default
    if not isinstance (csbias_steps, list):
        csbias_steps = csbias_steps.split()
        try:
            csbias_steps = [float(csbias) for csbias in csbias_steps]
            cs = False
        except ValueError:
            print ("please inset floats only")

activations_default = [1]
activ = True
while (activ):
    activations = input ("please insert one value for activation or three values (start stop step_size) seperated by spaces for activation"\
        " values. Please press enter to use the default value ({}):  ".format(activations_default))
    activations = activations or activations_default
    if not isinstance (activations, list):
        activations = activations.split()
        try:
            activations = [int(activation) for activation in activations]
            if not any([len(activations) == 1 , len(activations)==3]):
                print ("invalid intigers for activation, please insert three floats seperated by spaces")
            elif (len(activations)==3):
                activ = False
                activations = list (range(activations[0],activations[1]+1,activations[2])) 
            else:
                activ = False
        except ValueError:
            print ("invalid value for activation, please insert three floats seperated by spaces")

weight_polarity = [1]

wq = input ("Please insert 'y' to have weight polority otherwise only positive weights")
if wq == 'y':
    weight_polarity = [1 , -1]
print (weight_polarity)
print (csbias_steps, activations, weight_polarity)
"""

print ("The script will produce {} iterations".format(len(csbias_steps)*len(activations)*len(weight_polarity)))
for test_N in range(N_tests):
    for cs_b in csbias_steps:
        for activation in activations:
            for weight_p in weight_polarity:
                results_path = "C:/results/{}/{}-{}-{}".format(weight_form, cs_b,activation,weight_p) 
                session = power.power (ana_csbias=cs_b,measurementFolder=results_path+'/power')
                sess.append(session)
                session.power_set()
                print("Generating header data files for the experiment...")
                with cd ("C:/zedboard/diana-sdk/tests/"):
                    header = cmd("""python MS_gen_data1.py  -p ana_boot_ex\
                            -imp utc_ima.yaml\
                            -ima\
                            -a UNI\
                            -as {activation_size}\
                            -v {activation_value}\
                            -w {weight_form}\
                            --weight_pol {weight_polarity}\
                            --weight_str_val 1\
                            --weight_step 2\
                            -crp char_cra.yaml\
                            -cra""".format( weight_form = weight_form,   
                             activation_size=4*4*128,
                             activation_value=activation,
                             weight_polarity=weight_p
                             ))
                    time.sleep (10)
                    #if not header.wait == 0:

                     #   print ('Error, See the line below:')
                    for l in make_directory.stdout:
                        print (l)
                        #exit()
                print ("compiling c code ...")
                procedures.c_compile()
                print ("running the experiment on chip ...")

                #power MB on
                session.channel_active(settings.chdic['plus'])
                session.channel_active(settings.chdic['minus'])

                session.channel_active(settings.chdic['vddio'])
                session.channel_active(settings.chdic['vdd'])
                session.channel_active(settings.chdic['vddmem'])

                print("Starting the FPGA program...")
                dump_path = "/root/results/{}_{}_{}/".format(cs_b,activation,weight_p)
                p = cmd ("ssh zedb-diana mkdir {}".format(dump_path))



                #_ = input ("run fpga program")
                procedures.spawn_zedb_p(dump_path=dump_path)
                time.sleep(5)

                print("Starting the chip program...")
                procedures.spawn_openocd_p()

                #a = input ("run gdb")
                time.sleep(2)

                #non_blocking_cmd ("riscv64-unknown-elf-gdb.exe Z:/home/imandadras/diana-riscv-src/ana_boot_ex/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/diana-fpga-sw/host_scripts/templates/gdb-run-soc.sh")
                Path(results_path).mkdir(parents=True, exist_ok=True)
                with cd (results_path):
                    non_blocking_cmd ("riscv64-unknown-elf-gdb.exe C:/zedboard/diana-riscv-src/ana_boot_ex/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/diana-fpga-sw/host_scripts/templates/gdb-run-soc1.sh")

                time.sleep (2)

                print("Waiting for FPGA core to be sync...")
                time.sleep(1)
                while cmd("wsl ssh zedb-diana 'test -f ~/diana-fpga-sw/TURNVDDEON'", verbose=True, shell=True):
                    print ("flag is not there")
                    time.sleep(1)
                print ("flag is there")

                print ("starting analog supplies")
                session.channel_active(settings.chdic['vh'])
                session.channel_active(settings.chdic['vdde'])
                session.channel_active(settings.chdic['csbias'])
                session.initiate()
                time.sleep(1)

                print("Release FPGA core. Sending acknoledge signal...")
                cmd("wsl ssh zedb-diana 'rm -f ~/diana-fpga-sw/TURNVDDEON'" , shell=True)

                with cd (results_path):
                    while not exists("Done.txt"):
                        print ("waiting for the chip program to be completed")        
                        time.sleep(1)
                print ("flag is there")
                cmd ("wsl ssh zedb-diana ' touch /root/diana-fpga-sw/SHUT'")
                time.sleep(2)
                session.terminate()
                print ("running offprocedure")
                procedures.off_procedure(session=[]) 
atexit.unregister(procedures.off_procedure)


