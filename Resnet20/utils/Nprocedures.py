import utils.settings as settings
from utils.utils import cmd, is_alive, non_blocking_cmd, gen_file_from_template, check_return_zero, cd
import time 





def c_compile(parser, i_loop=1, gen_data_h=True):
    if gen_data_h:
        data_h_template_dict={}
        data_h_template_dict["I_CYCLES"] = i_loop
        gen_file_from_template("C:/zedboard/diana-fpga-sw/host_scripts/templates/data.h", parser.C_CODE_PATH + "/data/data.h", data_h_template_dict)

    script_template_dict={}
    script_template_dict["C_CODE_PATH"] = "~/diana-riscv-src/"+parser.args.riscv_c_program
    SCRIPT_PATH = settings.C_SRC_PATH + "compile.sh"
    gen_file_from_template("//wsl$/Ubuntu/home/imandadras/diana-fpga-sw/host_scripts/templates/compile.sh",SCRIPT_PATH, script_template_dict)
    with cd ("//wsl$/Ubuntu/home/imandadras/diana-riscv-src/") :
        cmd ("wsl sed -i 's/\r//' compile.sh")

        p = cmd ("wsl source compile.sh", verbose=True)
        check_return_zero(p)
        p = cmd("wsl rm -rf ./compile.sh")






def kill_zedb_python(parser):
    ZEDB_TARGET = parser.args.zedb_name
    KILL_ZEDB_P = settings.KILL_ZEDB_P(ZEDB_TARGET)

    PPROCESS = True
    while(PPROCESS):
        pid_p = non_blocking_cmd(KILL_ZEDB_P)
        pid = pid_p.stdout.readline()
        if pid:
            cmd("ssh {} 'kill -2 {}'".format(ZEDB_TARGET, pid))
        else:
            PPROCESS = False


#zedb_p handlers
def spawn_zedb_p(parser, dump_path, i_loop=1, **kwargs): #kwargs only to avoid python complaining
    ZEDB_PSCRIPT_NAME = parser.args.zedb_script
    ZEDB_TARGET = parser.args.zedb_name
    ZEDB_SCRIPT = settings.ZEDB_SCRIPT(ZEDB_TARGET)
    with open("C:/zedboard/diana-fpga-sw/host_scripts/templates/zedb-run-soc.sh","r") as inp, open("temp","w") as outp:
        for l in inp:
            if ("SCRIPT_NAME=" in l):
                outp.write("SCRIPT_NAME={}\n".format(ZEDB_PSCRIPT_NAME))
            elif("SCRIPT_ARGS=" in l):
                outp.write("SCRIPT_ARGS='-p {} --rx_packet_num {}'\n".format(dump_path, i_loop)) #TODO exted here for more support rx_packet_num
            else:
                outp.write(l)
    cmd("scp temp {}:~/zedb-run-soc.sh".format(ZEDB_TARGET))
    cmd("ssh zedb-diana sed -i 's/\r//' zedb-run-soc.sh")
    cmd("del temp", shell= True)
    _ = input ("run the fpga program")
    #zedb_p = non_blocking_cmd(ZEDB_SCRIPT)
    time.sleep(3)


def spawn_gdb_p(parser):
    C_CODE_PATH = "~/diana-riscv-src/{}".format(parser.args.riscv_c_program)
    GDB_COMMAND = settings.GDB_COMMAND(parser.args.gdb_script)
    cmd("wsl cp ~/diana-fpga-sw/host_scripts/templates/gdb-run-soc.sh {}/{}".format(C_CODE_PATH,parser.args.gdb_script), verbose=True)
    with cd(parser.C_CODE_PATH):
        gdb_session_p = non_blocking_cmd(GDB_COMMAND)
    return gdb_session_p



def run_diana_experiment(parser, session , sync_out=True, **kwargs):
    #registering off handler
    session.channel_active(settings.chdic['plus'])
    session.channel_active(settings.chdic['minus'])


    handlers_args_dic = {"parser":parser}

    print("Starting the digital supplies...")
    session.channel_active(settings.chdic['vddio'])
    session.channel_active(settings.chdic['vdd'])
    session.channel_active(settings.chdic['vddmem'])
    print("Starting the FPGA program...")

    zedb_p = spawn_zedb_p(parser, **kwargs)

    _ = input("Please start up the chip program.")

    print ("openocd ...")
    _ = input ("press enter to shutdown")
    cmd ("ssh zedb-diana killall python3")
    cmd ("openocd -c shutdown")

    cmd("ssh {} 'rm -rf {}'".format(parser.args.zedb_name, settings.VDDE_FLAG_FILE))

    session.force_terminate()
    