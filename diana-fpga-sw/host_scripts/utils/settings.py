################ USER DEFINED PATHS #######################

#--Paths
ROOT_MICAS_USER = "C:/zedboard/"
PULP_RISCV_GCC_TOOLCHAIN = "riscv64-unknown-elf-gdb.exe"

############### COMMON SETTINGS ##########################

#--Instruments
PSU_N6705B_addr = 'TCPIP::10.91.16.33::inst0::INSTR'
PSU_E36312A_addr = 'TCPIP::10.91.16.5::inst0::INSTR'
SCP_RTB2004_addr = 'TCPIP::10.91.16.37::INSTR'

#--Paths
C_SRC_PATH = "Z:/home/imandadras/diana-riscv-src/"
DIANA_SDK_PATH = ROOT_MICAS_USER + "diana-sdk/"
RTL_PATH = ROOT_MICAS_USER + "diana-rtl/"
#--SSH
ZEDB_SCRIPT_PATH = '~/diana-fpga-sw/'
VDDE_FLAG_FILE = ZEDB_SCRIPT_PATH + 'TURNVDDEON'
DONE_FLAG_FILE = ZEDB_SCRIPT_PATH + 'CHAR_DONE'
#--Scripts

TIME_FORMAT = '%Y_%m_%d_%H_%M_%S'

############### SH COMMANDS ##############################
#openocd
OPENOCD_BIN_PATH = "openocd"
OPENOCD_CFG_PATH = "{}fpga/pulpissimo-zedboard/openocd-zedboard-hs2.cfg".format(RTL_PATH)
openocd_df2 = "{} -f {}".format(OPENOCD_BIN_PATH,OPENOCD_CFG_PATH)
#zedb python script launch
def ZEDB_SCRIPT(ZED_TARGET): 
    return "ssh {} 'source zedb-run-soc.sh'".format(ZED_TARGET)
def KILL_ZEDB_P(ZED_TARGET): 
    return "ssh {} 'pgrep python3'".format(ZED_TARGET)
#gdb session open
def GDB_COMMAND(GDB_SCRIPT): 
    return "{} C:/zedboard/diana-riscv-src/ana_boot_ex/hwme.c/pulpissimo/hwme/hwme -x {}".format(PULP_RISCV_GCC_TOOLCHAIN, GDB_SCRIPT)

####################Power channels dictionary######################
chdic = {'plus':'SMU1/0','csbias':'SMU1/1','vh':'SMU1/2',
    'minus':'SMU1/3', 'vddio':'SMU2/0', 'vdd' :'SMU2/1', 'vddmem':'SMU2/2', 
    'vdde':'SMU2/3'}
