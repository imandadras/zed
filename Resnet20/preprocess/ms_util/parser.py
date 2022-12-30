import argparse
from ms_util.input_gen import SINGLE_TYPE as ACTV_TYPE
from ms_util.input_gen import GEN_TYPE as GEN_TYPE
from ms_util.weight_gen import TYPE as WGHT_TYPE
import ms_util.parser_util as pu

class MeasurementParser():
    def __init__(self) -> None:
        self.parser = argparse.ArgumentParser(description='Gets options from command line.')
        self.weight_options = list(WGHT_TYPE.keys())
        self.weight_gen_dic = {}
        self.actv_sin_options   = list(ACTV_TYPE.keys())
        self.actv_gen_options   = list(GEN_TYPE.keys())
        self.actv_options       = self.actv_sin_options + self.actv_gen_options
        self.actv_gen_dic       = {}
        self.bn_gen_dic       = {}
        self._init_parser()
        self.args = self.parser.parse_args()
        self._reduce_args()
        self._check_args()

    def _init_parser(self):
        #-----------SCRIPT TYPE (kind HERE) SELECTION-----------------------------------//
        self.parser.add_argument("-p", "--c_code_path", action="store", type=str, help="C code directory name. Ex: ana_base")
        self.parser.add_argument("-A", "--all", action="store_true")
        #------------INSTRUCTION ARGUMENTS---------------------------------------------//
        self.parser.add_argument("-imp","--ana_instr_mem_path", action="store", type=str, help="Path to the instruction memory YAML configuration file")
        self.parser.add_argument("-ima","--ana_instr_mem", action="store_true")
        self.parser.add_argument("-ut", "--unit_time", action="store", type=int, help="IMA unit time value to over-ride")        
        #----------ACTIVATION ARGUMENTS------------------------------------------------//
        self.parser.add_argument("-a", "--activation", action="store", type=str, help="Type of weight\n OPTIONS:{}".format("\t"+"\t".join(self.actv_options)))
        self.parser.add_argument("-as", "--activation_size", action="store", type=int, help="Size of activations")
        self.parser.add_argument("--actv_sign", action="store_true", help="NOR-RAN: Activation signed (True) or unsigned (False)")
        self.parser.add_argument("-v", "--actv_val", action="store", type=int, help="UNI: Activation uniform value")
        self.parser.add_argument("--actv_loc", action="store", type=float, help="NOR: Center of the normal distribution")
        self.parser.add_argument("--actv_scale", action="store", type=float, help="NOR: Sigma of the normal distribution")
        self.parser.add_argument("--actv_clip", action="store",type=float, help="NOR: Maximum value of the normal distribution")
        self.parser.add_argument("--actv_range", action="store",type=float, help="NOR-RAN: Integer bitwidth")
        self.parser.add_argument("--actv_start_row", action="store", type=int, help="ROW: position of first non-zero activation")
        self.parser.add_argument("--actv_range_row", action="store", type=int, help="ROW: burst of non-zero activations")
        self.parser.add_argument("--actv_batch_size", action="store", type=int, help="ROW: channels, the number of data paket within the burst of v value falls")
        self.parser.add_argument("--actv_batch_num", action="store", type=int, help="ROW: numbers of pakets")
        #----------WEIGHT ARGUMENTS---------------------------------------------------//
        self.parser.add_argument("-w", "--weight", action="store", type=str, help="Type of weight.\n OPTIONS:{}".format("\t"+"\t".join(self.weight_options)))
        self.parser.add_argument("-wz", "--weight_zero", action="store_true")
        self.parser.add_argument("--weight_tiles", action="store", type=int, help="RPD-STR-CLM: Number of tiles of weight to generate")
        self.parser.add_argument("--weight_pd", action="store", type=int, help="RPD: Positive probability per column of the RPD weight distribution")
        self.parser.add_argument("--weight_nd", action="store", type=int, help="RPD: Negative probability per column of the RPD weight distribution")
        self.parser.add_argument("--weight_pol", action="store", type=int, help="STR-CLM: Polarity of the weights")       
        self.parser.add_argument("--weight_str_val", action="store", type=int, help="STR: Starting value of active rows")
        self.parser.add_argument("--weight_step", action="store", type=int, help="STR: Increasing step of active rows")
        self.parser.add_argument("--weight_col_blocks", action="store", type=int, nargs="+", help="BLK: List of blocks where to set the weights as polarity")
        self.parser.add_argument("--weight_row_blocks", action="store", type=int, nargs="+", help="BLK: List of blocks where to set the weights as polarity")
        self.parser.add_argument("--weight_start_row", action="store", type=int, help="CLM: Starting value of [polarity] weight row")
        self.parser.add_argument("--weight_batch_row", action="store", type=int, help="CLM: Batching value of [polarity] weight row")
        self.parser.add_argument("--weight_start_col", action="store", type=int, help="CLM: Starting value of [polarity] weight col")
        self.parser.add_argument("--weight_batch_col", action="store", type=int, help="CLM: Batching value of [polarity] weight col")
        #---------BATCH NORM ARGUMENTS---------------------------------------------//
        self.parser.add_argument("-bn", "--bn", action="store", type=str, help="Type of bn\n OPTIONS:{}".format("\tRAN\t"))
        self.parser.add_argument("-bns", "--bn_size", action="store", type=int, help="BN size")
        #---------CONFIGURATION ARGUMENTS---------------------------------------------//
        self.parser.add_argument("-crp","--ana_config_reg_path", action="store", type=str, help="Path to the configuration register YAML configuration file")
        self.parser.add_argument("-cra","--ana_config_reg", action="store_true")
        #----------------------------------------------------------------------------//
        self._set_defaults()

    def _set_defaults(self):
        #-----------MAIN--------------------------------------------------------------//
        self.parser.set_defaults(all=False)
        self.parser.set_defaults(c_code_path="")
        #----------ACTIVATION ARGUMENTS-----------------------------------------------//
        self.parser.set_defaults(activation=None)
        self.parser.set_defaults(actv_sign=False)
        #----------WEIGHT ARGUMENTS---------------------------------------------------//
        self.parser.set_defaults(weight=None)
        self.parser.set_defaults(weight_zero=False)
        self.parser.set_defaults(weight_tiles=1)
        #----------CONFIGURATION ARGUMENTS--------------------------------------------//
        self.parser.set_defaults(ana_config_reg=False)
        #------------INSTRUCTION ARGUMENTS--------------------------------------------//
        self.parser.set_defaults(ana_instr_mem=False)

    def _reduce_args(self):
        if self.args.all:
            self.args.activation= self.actv_options[0] if (self.args.activation == None) else self.args.activation
            self.args.weight=self.weight_options[0] if (self.args.weight == None) else self.args.weight
            self.args.ana_config_reg=True
            self.args.ana_instr_mem=True
        #TODO put this if in reduce arguments...
        if (self.args.unit_time!=None):
            self.args.ana_instr_mem=True
        self._reduce_actv()
        self._reduce_weight()
        self._reduce_bn()

    def _reduce_actv(self):

        if self.args.activation in self.actv_sin_options:
            self.actv_gen_dic["_type"] = "SIN"
            self.actv_gen_dic["size"] = self.args.activation_size
            self.actv_gen_dic["_t"] = self.args.activation
        else:
            self.actv_gen_dic["_type"] = self.args.activation
        if self.args.activation == "UNI":
            self.actv_gen_dic["v"] = self.args.actv_val
        elif self.args.activation == "NOR":
            self.actv_gen_dic["loc"]    = self.args.actv_loc
            self.actv_gen_dic["scale"]  = self.args.actv_scale
            self.actv_gen_dic["clip"]   = self.args.actv_clip
            self.actv_gen_dic["_range"] = self.args.actv_range
            self.actv_gen_dic["signed"] = self.args.actv_sign
        elif self.args.activation == "RAN":
            self.actv_gen_dic["_range"] = self.args.actv_range
            self.actv_gen_dic["signed"] = self.args.actv_sign
        elif self.args.activation == "ROW":
            self.actv_gen_dic["v"] = self.args.actv_val
            self.actv_gen_dic["start_r"] = self.args.actv_start_row
            self.actv_gen_dic["range_r"] = self.args.actv_range_row
            self.actv_gen_dic["batch_size"] = self.args.actv_batch_size
            self.actv_gen_dic["batch_num"] = self.args.actv_batch_num

    def _reduce_bn(self):
        try:
            if self.args.bn == 'RAN':
                self.bn_gen_dic['type'] = 'RAN'
                self.bn_gen_dic['size'] = self.args.bn_size
                self.bn_gen_dic['signed'] = True
        except KeyError:
            print("Missing keys for BN parser")
            exit()


    def _reduce_weight(self):
        if self.args.weight == "RPD":
            self.weight_gen_dic["pos_dist"] = self.args.weight_pd
            self.weight_gen_dic["neg_dist"] = self.args.weight_nd
            self.weight_gen_dic["tiles"]    = self.args.weight_tiles           
        elif self.args.weight == "STR":
            self.weight_gen_dic["polarity"]     = self.args.weight_pol
            self.weight_gen_dic["start_val"]    = self.args.weight_str_val
            self.weight_gen_dic["step"]         = self.args.weight_step
            self.weight_gen_dic["tiles"]        = self.args.weight_tiles
        elif self.args.weight == "BLK":
            self.weight_gen_dic["colb"]     = self.args.weight_col_blocks
            self.weight_gen_dic["rowb"]     = self.args.weight_row_blocks
            self.weight_gen_dic["polarity"] = self.args.weight_pol
            self.weight_gen_dic["tiles"]    = self.args.weight_tiles
        elif self.args.weight == "CLM":
            self.weight_gen_dic["start_r"]  = self.args.weight_start_row
            self.weight_gen_dic["batch_r"]  = self.args.weight_batch_row
            self.weight_gen_dic["start_c"]  = self.args.weight_start_col
            self.weight_gen_dic["batch_c"]  = self.args.weight_batch_col
            self.weight_gen_dic["polarity"] = self.args.weight_pol
            self.weight_gen_dic["tiles"]    = self.args.weight_tiles
        elif self.args.weight == "CSS":
            print("Only default values supported for CSS weight-gen mode...")
        elif self.args.weight == "ONE":
            self.weight_gen_dic["tiles"]    = self.args.weight_tiles
        else:
            raise NotImplementedError

    def _check_args(self):
        pu.check_options(self.args.activation, self.actv_options)
        pu.check_options(self.args.weight,self.weight_options)
