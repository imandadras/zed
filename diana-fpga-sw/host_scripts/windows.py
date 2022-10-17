import utils.power as power
import time
from utils.utils import cmd, non_blocking_cmd
from utils.settings import chdic

#making the result directory on zedboard
cmd ("wsl ssh zedb-diana mkdir /root/char_data")

print ("starting the loop experiment ...")

session = power.power()
session.power_set()
session.channel_active(chdic['plus'])
session.channel_active(chdic['minus'])
session.channel_active(chdic['vddio'])
session.channel_active(chdic['vdd'])
session.channel_active(chdic['vddmem'])

_ = input("zedboard")

#cmd ("wsl ssh zedb-diana source zedb-run-soc.sh")

print ("openocd")

_ = input ("run openocd")
#non_blocking_cmd ("openocd -f C:/zedboard/diana-rtl/fpga/pulpissimo-zedboard/openocd-zedboard-hs2.cfg")

print ("gdb")

_ = input ("run gdb")
#non_blocking_cmd ("riscv64-unknown-elf-gdb.exe Z:/home/imandadras/diana-riscv-src/ana_boot_ex/build/hwme.c/pulpissimo/hwme/hwme -x C:/zedboard/diana-fpga-sw/host_scripts/templates/gdb-run-soc.sh")

time.sleep (2)

while cmd("wsl ssh zedb-diana 'test -f ~/diana-fpga-sw/TURNVDDEON'", verbose=True ):
    print ("flag is not there")
    time.sleep(1)
print ("flag is there")

session.channel_active(chdic['vh'])
session.channel_active(chdic['vdde'])
session.channel_active(chdic['csbias'])

time.sleep(1)
        
print("Release FPGA core. Sending acknoledge signal...")
time.sleep(1)


cmd("ssh zedb-diana 'rm -f ~/diana-fpga-sw/TURNVDDEON'")

cmd("ssh zedb-diana 'rm -f ~/diana-fpga-sw/TURNVDDEON'")



while cmd("wsl ssh zedb-diana 'test -f ~/diana-fpga-sw/CHAR_DONE'", verbose=True ):
    print ("flag is not there")
    time.sleep(1)
print ("flag is there")
cmd("zedb-diana 'rm -f ~/diana-fpga-sw/CHAR_DONE'")