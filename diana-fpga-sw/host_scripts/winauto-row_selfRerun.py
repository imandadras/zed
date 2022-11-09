from os import mkdir
from os.path import exists
from tkinter import N
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
import os

#set the variables here
weight_form= "CLM"
csbias_steps = [x/100 for x in list(range(71, 59, -1))]
activation = 61  #-63,63
weight_polarity = [1] #-1, 1
N_tests = 1

sess = []
atexit.register(procedures.off_procedure, session=sess)
print ("Making the parent directory for experiment results")
first_time = True

make_directory = subprocess.Popen(shlex.split("ssh zedb-diana mkdir results"), stdout = subprocess.PIPE, stderr = subprocess.STDOUT, shell= True)
#if not make_directory.wait == 0:

 #   print ('the result directory did not make. See the line below:')
for l in make_directory.stdout:
    print (l)
    

for test_N in range(0, N_tests):
    for cs_b in csbias_steps:
        if first_time == False:
            activation = -62
        first_time = False
        while activation < 64:
            for weight_p in weight_polarity:
                for row in range(1):
                    results_path = "C:/results/{}/model/{}/{}-{}/".format(weight_form, cs_b,activation,weight_p) 
                    session = power.power (ana_csbias=cs_b,measurementFolder=results_path+'/power')
                    sess=[session]
                    session.power_set()
                    if test_N==12:
                        test_N=11.52
                    print("Generating header data files for the experiment...")
                    with cd ("C:/zedboard/diana-sdk/tests/"):
                        header = cmd("""python MS_gen_data1.py  -p ana_boot_ex\
                                -imp utc_ima.yaml\
                                -ima\
                                -a ROW\
                                -as {activation_size}\
                                -v {activation_value}\
                                -w {weight_form}\
                                --weight_pol {weight_polarity}\
                                --weight_str_val 1\
                                --weight_step 2\
                                -crp char_cra.yaml\
                                -cra\
                                --weight_start_row {row}\
                                --weight_batch_row {range}\
                                --weight_start_col 0\
                                --weight_batch_col 512\
                                --actv_start_row {a_row}\
                                --actv_range_row {a_range}\
                                --actv_batch_num 1\
                                --actv_batch_size 2048""".format( weight_form = weight_form,   
                                 activation_size=4*4*128,
                                 activation_value=activation,
                                 weight_polarity=weight_p,
                                 row=0, #1152-(128*test_N), #int(1152-(100*test_N)),
                                 range=6,
                                 a_row=0, #1152-(128*test_N),
                                 a_range=6
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
                    dump_path = "/root/results/"
                    #p = cmd ("ssh zedb-diana mkdir {}".format(dump_path))
                #_ = input ("run fpga program")
                procedures.spawn_zedb_p(dump_path=dump_path)
                time.sleep(5)
                print("Starting the chip program...")
                openocd_check = procedures.spawn_openocd_p()
                if openocd_check == False:
                    print ("openocd check is false")
                    procedures.off_procedure(session=[]) 
                    break
                #a = input ("run gdb")
                time.sleep(2)
                #non_blocking_cmd ("riscv64-unknown-elf-gdb.exe Z:/home/imandadras/diana-riscv-src/ana_boot_ex/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/diana-fpga-sw/host_scripts/templates/gdb-run-soc.sh")
                Path(results_path).mkdir(parents=True, exist_ok=True)
                with cd (results_path):
                    non_blocking_cmd ("riscv64-unknown-elf-gdb.exe C:/zedboard/diana-riscv-src/ana_boot_ex/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/diana-fpga-sw/host_scripts/templates/gdb-run-soc1.sh")
                time.sleep (2)
                print("Waiting for FPGA core to be sync...")
                time.sleep(1)
                
                TURNVDDON_C = 0
                TURNVDDON_check = True 
                while cmd("wsl ssh zedb-diana 'test -f ~/diana-fpga-sw/TURNVDDEON'", verbose=True, shell=True):
                    
                    print ("flag is not there")
                    TURNVDDON_C += 1
                    if TURNVDDON_C == 4 :
                        TURNVDDON_check = False
                        break
                    time.sleep(1)
                if TURNVDDON_check == False:
                    procedures.off_procedure(session=[]) 
                    break
                print ("flag is there")
                print ("starting analog supplies")
                session.channel_active(settings.chdic['vh'])
                session.channel_active(settings.chdic['vdde'])
                session.channel_active(settings.chdic['csbias'])
                session.initiate()
                time.sleep(1)
                print("Release FPGA core. Sending acknoledge signal...")
                cmd("wsl ssh zedb-diana 'rm -f ~/diana-fpga-sw/TURNVDDEON'" , shell=True)
                DONE_C=0
                DONE_check = True
                with cd (results_path):
                    while not exists("Done.txt"):
                        print ("waiting for the chip program to be completed")
                        DONE_C += 1
                        if DONE_C == 15:
                            DONE_check = False 
                            break       
                        time.sleep(1)
                if DONE_check == False:
                    procedures.off_procedure(session=[]) 
                    break     
                print ("flag is there")
                cmd ("wsl ssh zedb-diana ' touch /root/diana-fpga-sw/SHUT'")
                time.sleep(2)
                session.terminate()
                print ("running offprocedure")
                activation +=1
                procedures.off_procedure(session=[]) 
atexit.unregister(procedures.off_procedure)
