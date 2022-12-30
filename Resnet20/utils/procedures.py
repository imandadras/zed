from tabnanny import verbose
import time
import signal
import yaml
from utils.utils import gen_file_from_template
#import atexit
import utils.power as power
from utils.utils import is_alive, non_blocking_cmd, cmd, cd, check_return_zero , pushd
import utils.settings as settings
import subprocess
import shlex

nonblocking_process_tags = ["ZEDBP", "OPENOCD", "GDB"]

def c_compile(i_loop=1, gen_data_h=True):
    if gen_data_h:
        data_h_template_dict={}
        data_h_template_dict["I_CYCLES"] = i_loop
        gen_file_from_template("C:/zedboard/diana-fpga-sw/host_scripts/templates/data.h", "C:/zedboard/diana-riscv-src/ana_boot_ex/data/data.h", data_h_template_dict)

    #script_template_dict={}
    #script_template_dict["C_CODE_PATH"] = "/mnt/c/zedbord/diana-riscv-src/ana_boot_ex/"
    #SCRIPT_PATH = "C:/zedboard/diana-riscv-src/compile.sh"
    #gen_file_from_template("C:/zedboard/diana-fpga-sw/host_scripts/templates/compile.sh",SCRIPT_PATH, script_template_dict)
    with cd ("C:/zedboard/Resnet20/"):

        p = cmd ("wsl source compile.sh", verbose=True, shell=True)
        check_return_zero(p)
        #p = cmd("del compile.sh", shell=True)

def ssh_sync_wall(ssh_client, flag_file, session, process=None, timeout=30):
    tries=0
    while(cmd("wsl ssh {} 'test -f {}'".format(ssh_client, flag_file))):
        if process:
            if is_alive(process):
                pass
            else:
                print("Let's try last time...")
                p = cmd("ssh {} 'test -f {}'".format(ssh_client, flag_file))
                if p==0:
                    return
                else:
                    print("The zedboard process crashed. Exiting...")
                    off_procedure(session)
                    exit()
        time.sleep(1)
        tries += 1
        if tries == timeout:
            raise TimeoutError

#zedb_p handlers
def spawn_zedb_p(dump_path, i_loop=1, **kwargs): #kwargs only to avoid python complaining
    with open("C:/zedboard/diana-fpga-sw/host_scripts/templates/zedb-run-soc.sh","r") as inp, open("temp","w", newline= '\n') as outp:
        for l in inp:
            if ("SCRIPT_NAME=" in l):
                outp.write("SCRIPT_NAME=run-diana-soc.py\n")
            elif("SCRIPT_ARGS=" in l):
                outp.write("SCRIPT_ARGS='-p {} --rx_packet_num {}'\n".format(dump_path, i_loop)) #TODO exted here for more support rx_packet_num
            else:
                outp.write(l)
    cmd("scp temp zedb-diana:~/zedb-run-soc.sh")
    zedb_p = non_blocking_cmd("ssh zedb-diana 'source zedb-run-soc.sh'")
    time.sleep(3)
    if is_alive(zedb_p):
        pass
    else:
        print("The zedboard process crashed. Exiting...")
        P = cmd ("ssh zedb-diana killall python3")
        raise IOError
    return zedb_p

def kill_zedb_python(parser):
    ZEDB_TARGET = "zedb-diana"
    KILL_ZEDB_P = settings.KILL_ZEDB_P(ZEDB_TARGET)

    PPROCESS = True
    while(PPROCESS):
        pid_p = non_blocking_cmd(KILL_ZEDB_P)
        pid = pid_p.stdout.readline()
        if pid:
            cmd("ssh {} 'kill -2 {}'".format(ZEDB_TARGET, pid))
        else:
            PPROCESS = False

#openocd_p handlers
def spawn_openocd_p(verbose = False):
    attempts = 0
    max_attempts = 5
    openocd_p = non_blocking_cmd(settings.openocd_df2)
    time.sleep(3) 
    while(not(is_alive(openocd_p)) and attempts < max_attempts):
        if verbose:
            for l in openocd_p.stdout:
                print(l)
        attempts += 1 
        openocd_p = non_blocking_cmd(settings.openocd_df2)
        time.sleep(3)
    if(attempts == max_attempts):
        print("Can't establish a stable JTAG connection. Exiting...")
        return False
    print("Stable JTAG connections established after {} attempts...".format(attempts+1))
    return True

#gdb_session_p
def spawn_gdb_p(parser):
    C_CODE_PATH = "~/diana-riscv-src/{}".format(parser.args.riscv_c_program)
    GDB_COMMAND = settings.GDB_COMMAND(parser.args.gdb_script)
    cmd("wsl cp ~/diana-fpga-sw/host_scripts/templates/gdb-run-soc.sh {}/{}".format(C_CODE_PATH,parser.args.gdb_script), verbose=True)
    with cd(parser.C_CODE_PATH):
        gdb_session_p = non_blocking_cmd(GDB_COMMAND)
    return gdb_session_p

#off_procedure
def off_procedure(CHECK ,  ctrlc=False, **kwargs):
    print("Executing off procedure...")
    print("Please DO NOT press ctrl+C before explicitly required!")
    cmd ("ssh zedb-diana killall python3")
    #cmd ("ssh zedb-diana rm char* -rf")
    print ("process is killed")
    if CHECK[2]:
        cmd("wsl ssh zedb-diana 'rm -f ~/diana-fpga-sw/CHAR_DONE'")
    if CHECK[1]:
        cmd("wsl ssh zedb-diana 'rm -f /root/diana-fpga-sw/TURNVDDEON'")
    if CHECK[0]:
        CHECK[0].force_terminate()
    cmd ("openocd -c shutdown")
    #SIGINT to all the
    cmd ("taskkill /IM ssh.exe /f")
    #cmd ("taskkill /IM powershell.exe /f")
    cmd ("taskkill /IM riscv64-unknown-elf-gdb.exe /f")
    cmd ("taskkill /IM openocd.exe /f")    


    #cmd("stty sane") #cleaning the mess from shell=True stdout
    if ctrlc:
        print("If you want to kill the process press ctrl+C")
        time.sleep(5)


def run_memchar(memchar_path, SCP_RTB2004, PSU_N6705B):
    time.sleep(0.5)
    print("Running memchar measurement for {}".format(memchar_path))
    #data_dic = SCP_RTB2004.get_logic_waveform(channels=[6,7], period=5e-6)
    #print(data_dic["d7"])
    #print(data_dic["dh7"])
    power = get_power(PSU_N6705B, [1,2,3,4], 7, 20e-6, [0,3])
    print("Power: ",power)
    yaml_dict = { "VDDIOW"    : power[1],
                "VDDCW"     : power[2],
                "VDDEW"     : power[3],
                "VDDMEMW"   : power[4]}

    yaml_p = memchar_path + "tops.yaml"
    with open(yaml_p, 'w') as fout:
        _ = yaml.dump(yaml_dict, fout)
    return 0

def run_diana_experiment(parser, session , SCP_RTB2004=None, power_path='', memchar_path='', sync_out=True, **kwargs):
    #registering off handler
    session.channel_active(settings.chdic['plus'])
    session.channel_active(settings.chdic['minus'])
    nb_process_list = []
    handlers_args_dic = {"parser":parser}
    try:
        print("Starting the digital supplies...")
        #TURNING ON DIGITAL SUPPLIES
        session.channel_active(settings.chdic['vddio'])
        session.channel_active(settings.chdic['vdd'])
        session.channel_active(settings.chdic['vddmem'])
        #PSU_N6705B.write('OUTP:STAT ON, (@1)')
        #PSU_N6705B.write('OUTP:STAT ON, (@2)')
        #PSU_N6705B.write('OUTP:STAT ON, (@4)')
        print("Starting the FPGA program...")
        zedb_p = spawn_zedb_p(parser, **kwargs)
        nb_process_list += [("ZEDBP",zedb_p)]

        time.sleep(5)
        print("Starting the chip program...")
        # _ = input ("start openocd")
        openocd_p = spawn_openocd_p(verbose=True)
        nb_process_list += [("OPENOCD",openocd_p)]
        #non_blocking_cmd ("openocd -f  C:/zedboard/diana-rtl/fpga/pulpissimo-zedboard/openocd-zedboard-hs2.cfg")
        time.sleep (2)

        #a = input ("please run gdb")
        non_blocking_cmd ("riscv64-unknown-elf-gdb.exe Z:/home/imandadras/diana-riscv-src/ana_boot_ex/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/diana-fpga-sw/host_scripts/templates/gdb-run-soc.sh")
        #gdb_session_p = spawn_gdb_p(parser)
        #nb_process_list += [("GDB",gdb_session_p)]

        time.sleep (2)

        print("Waiting for FPGA core to be sync...")
        time.sleep(1)
        cmd ("wsl ssh zedb-diana ls ~/diana-fpga-sw")
        while cmd("wsl ssh zedb-diana 'test -f ~/diana-fpga-sw/TURNVDDEON'", verbose=True ):
            print ("flag is not there")
            time.sleep(1)
        print ("flag is there")
        #ssh_sync_wall(parser.args.zedb_name, settings.VDDE_FLAG_FILE, session=session, process=zedb_p, timeout=20)
        
        #PSU_N6705B.write('OUTP:STAT ON, (@3)')
        #PSU_E36312A.write('OUTP:STAT ON, (@1)')
        session.channel_active(settings.chdic['vh'])
        session.channel_active(settings.chdic['vdde'])
        session.channel_active(settings.chdic['csbias'])

        time.sleep(1)
        
        print("Release FPGA core. Sending acknoledge signal...")
        cmd("wsl ssh {} 'rm -rf {}'".format(parser.args.zedb_name, settings.VDDE_FLAG_FILE))

        if power_path:
            time.sleep(1)
            print("Running power measurement for {}".format(power_path))


        if sync_out:
            while cmd("wsl ssh zedb-diana 'test -f ~/diana-fpga-sw/CHAR_DONE'", verbose=True ):
                print ("flag is not there")
                time.sleep(1)
            print ("flag is there")
            #ssh_sync_wall(parser.args.zedb_name, settings.DONE_FLAG_FILE, session=session, process=zedb_p, timeout=5)
            print("Release FPGA core. Sending acknoledge signal...")
            cmd("wsl ssh {} 'rm -rf {}'".format(parser.args.zedb_name, settings.DONE_FLAG_FILE))
        off_procedure(session, **handlers_args_dic)
        return 0
    except Exception as e:
        print(e)
        off_procedure(session, ctrlc=True, **handlers_args_dic)
        return 1

def reset(parser):
    time.sleep(3)
    #cmd("ssh {} 'sudo halt'".format(parser.args.zedb_name))
    session = power.power()
    session.force_terminate()
    time.sleep(30)
    
    """while(cmd("ssh -q -o BatchMode=yes -o ConnectTimeout=5 {} 'exit 0'".format(parser.args.zedb_name))):
        time.sleep(5)"""
    
