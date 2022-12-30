import argparse
import numpy as np
#import os

import utils.settings as settings
from utils.utils import cmd

class HostScriptParserClass():
    def __init__(self):
        self.parser = argparse.ArgumentParser(description='Gets options from command line.')
        self._init_parser()
        self.args = self.parser.parse_args()
        self.C_CODE_PATH = ""
        self.csbias_steps = []
        self.actv_uni_steps = []
        self.weight_pol_steps = []
        self._check_args()
        self._reduce_args()

    def _init_parser(self):
        self.parser.add_argument("-z","--zedb_name", action="store", type=str, help="Name of the ssh zedboard connected to the chip. Ex: root@10.88.18.167. Default=zedb-diana")
        self.parser.add_argument("-zs","--zedb_script", action="store", type=str, help="Script to be launched on the zedboard side. Default=")
        self.parser.add_argument("-c","--riscv_c_program", action="store", type=str, help="RISC-V c program to be executed on the chip. Check available options in {}".format(settings.C_SRC_PATH))
        self.parser.add_argument("-g","--gdb_script", action="store", type=str, help="gdb sh script to execute when launching the program")
        self.parser.add_argument("-sn","--sdk_script_name", action="store", type=str, help="sdk script name. Default MS_gen_data.py")
        self.parser.add_argument("-cb","--cs_bias", action="store", type=float, nargs="+", help="csbias value. Can be single or three (parameter sweep) float arguments")
        self.parser.add_argument("-av","--activation_val", action="store", type=int, nargs="+", help="activation value. Can be single or three (parameter sweep) int arguments")
        self.parser.add_argument("--actv_dev", action="store", type=str, help="sigma value. Can be float or int (parameter sweep) arguments")
        self.parser.add_argument("--ima_file", action="store", type=str, help="ima list of files or yaml file")
        self.parser.add_argument("--weight_sparsity", action="store", type=int, nargs="+", help="sparsity value. Can be single or three (parameter sweep) int arguments.")
        self.parser.add_argument("-wp","--weight_polarity", action="store_true", help="weight polarity, sets the experiment for both negative and positive")
        self.parser.add_argument("-i", "--starting_iteration", action="store", type=int, help="iteration to which start the main loop of experiments")
        self.parser.add_argument("--checkpoint_file", action="store", type=str, help="checkpoint file")
        self._set_defaults()

    def _set_defaults(self):
        self.parser.set_defaults(zedb_name="zedb-diana")
        self.parser.set_defaults(zedb_script="run-diana-soc.py")
        self.parser.set_defaults(riscv_c_program="ana_char_loop")
        self.parser.set_defaults(gdb_script="gdb-run-soc.sh")
        self.parser.set_defaults(sdk_script_name="MS_gen_data.py")
        self.parser.set_defaults(actv_dev="0.125")
        self.parser.set_defaults(weight_sparsity=[40])
        self.parser.set_defaults(cs_bias=[0.6])
        self.parser.set_defaults(activation_val=[1])
        self.parser.set_defaults(weight_polarity=False)
        self.parser.set_defaults(starting_iteration=0)
        self.parser.set_defaults(checkpoint_file=None)

    def _reduce_args(self):
        self.C_CODE_PATH = settings.C_SRC_PATH + self.args.riscv_c_program
        
        if len(self.args.cs_bias)==1:
            self.csbias_steps = self.args.cs_bias
        else:
            self.csbias_steps = list(np.linspace(self.args.cs_bias[0],self.args.cs_bias[1],num=int(self.args.cs_bias[2])))
        
        if len(self.args.activation_val)==1:
            self.actv_uni_steps = self.args.activation_val
        else:
            self.actv_uni_steps = list(range(self.args.activation_val[0],self.args.activation_val[1]+1,self.args.activation_val[2]))
        
        if self.args.weight_polarity:
            self.weight_pol_steps = [1,-1]
        else:
            self.weight_pol_steps = [1]

        if "." in self.args.actv_dev:
            self.actv_dev_steps = [float(self.args.actv_dev)]
        else:
            self.actv_dev_steps = list(np.logspace(-0, -8, num=int(self.args.actv_dev), base=2))

        if len(self.args.weight_sparsity)==1:
            self.weight_sparsity_steps = self.args.weight_sparsity
        else:
            self.weight_sparsity_steps = list(range(self.args.weight_sparsity[0],self.args.weight_sparsity[1]+1,self.args.weight_sparsity[2]))

        self.ima_list = [self.args.ima_file]

    def _check_args(self):
        #Check ssh connection
        zedb = self.args.zedb_name
        p = cmd("ssh -q -o BatchMode=yes -o ConnectTimeout=5 {} 'exit 0'".format(zedb))
        if not p==0:
            print("Can't reach {}".format(zedb))
            exit()
        if not len(self.args.cs_bias) in [1,3]:
            print("Wrong -cb --cs_bias argument value")
            exit
        if not len(self.args.activation_val) in [1,3]:
            print("Wrong -av --activation_val argument value")
            exit