from dataclasses import dataclass
import os
import math
from typing import List
import yaml
import copy

from compiler.diana_def import DIANAInstruction, FieldCompilerDict

from ms_util.aim_gen import gen_reg_list
from c_util.h_gen import gen_hdata_file

################# DATA CLASSES ################
#------------ SerialTensor Classes --------
@dataclass
class SerialTensor():
    def __init__(self,size,data):
        self.size = size
        self.virtual_size = size
        self.data = data
    
    def __call__(self):
        return self.data

class WeightSerialTensor(SerialTensor):
    def __init__(self, size, data, AiMC=None):
        super(WeightSerialTensor,self).__init__(size, data)
        self.tile_X = 1
        self.tile_Y = 1
        if (AiMC!=None):
            self.def_tile_size(AiMC)

    def get_tiling(self):
        return self.tile_X*self.tile_Y
    
    def get_rows(self):
        return self.virtual_size[1]*self.virtual_size[2]*self.virtual_size[3]
    
    def get_cols(self):
        return self.virtual_size[0]

    def def_tile_size(self,AiMC):
        K  = self.size[0]
        C  = self.size[1]
        FX = self.size[3]
        FY = self.size[2]
        print("--------------------------------------")
        print("Elaborated weight tensor:")
        print("\t K:{} ".format(K))
        print("\t C:{} ".format(C))
        print("\t FX:{}".format(FX))
        print("\t FY:{}".format(FY))

        self.tile_X = math.ceil(C*FX*FY/AiMC.n_rows)
        self.tile_Y = math.ceil(K/AiMC.n_cols)
        print("Given AiMC ROWS:{}\t COLS:{}".format(AiMC.n_rows,AiMC.n_cols))
        print("X tile(s):{}\t Y tile(s):{}".format(self.tile_X, self.tile_Y))
        print("--------------------------------------\n")
        return self.tile_X*self.tile_Y

class ActivationSerialTensor(SerialTensor):
    def __init__(self, size, data, min_C = 16):
        super(WeightSerialTensor,self).__init__(size, data)
        self.min_C = min_C

#--------------------------------------
#------------ Layer Classes -----------
@dataclass
class ConvLayerClass():
    def __init__(self, tag, w, ws, bn_w, bn_ws, bn_b, bn_bs, r_s, q_s, ds=False, a=None):
        self.tag    = tag
        self.w      = w
        self.ws     = ws
        self.bn_w   = bn_w
        self.bn_ws  = bn_ws
        self.bn_b   = bn_b
        self.bn_bs  = bn_bs
        self.r_s    = r_s
        self.q_s    = q_s
        self.ds     = ds
        self.a      = a
    def set_qs(self,qs):
        self.q_s = qs
    def set_rs(self,rs):
        self.r_s = rs

@dataclass
class BinaryLayerClass():
    def __init__(self, weight, bn_wgt, actv=None, imem=None):
        self.weight = weight
        self.bn_wgt = bn_wgt
        self.actv   = actv
        self.imem   = imem

#--------------------------------------
#------------ RF Classes --------------
@dataclass
class RegisterFileClass():
    def __init__(self, bitwidth):
        self.file = []
        self.bitwidth = bitwidth
        self.template = None #to be specified

    def _init_self_register(self,i):
        for r in self.file[i].keys():
            for f in self.file[i][r].fields.keys():
                self.file[i][r].fields[f].value = self.file[i][r].fields[f].default
    
    def new_instruction(self):
        self.file.append(copy.deepcopy(self.template))
        i = len(self.file)-1
        self._init_self_register(i)
        print("New instruction with index {} created!".format(i))
        return i
    
    def rf_to_yaml(self, reg_name="REGNS"):
        l = []
        for i,n in enumerate(self.file):
            print("RF-TO-YAML. Processing instruction {}".format(i))
            d = {}
            _d= {}
            for r in self.file[i].keys():
                for f in self.file[i][r].fields.keys():
                    if (self.file[i][r].fields[f].value != self.file[i][r].fields[f].default):
                        print("\tField {} will be dumped with value {}".format(f,self.file[i][r].fields[f].value))
                        _d[f] = self.file[i][r].fields[f].value
            d[reg_name+str(i)]=_d
            l.append(d)
        return l

    def yaml_to_rf(self, l):
        for i in l:
            ima_name = list(i.keys())[0] #getting instruction name!
            ima_k = i[ima_name]
            print("YAML-TO-RF. Processing instruction {}".format(ima_name))
            j = self.new_instruction()
            for r in self.file[j].keys():
                for f in self.file[j][r].fields.keys():
                    if f in ima_k:
                        print("\tField {} will be dumped with value {}".format(f,ima_k[f]))
                        self.file[j][r].fields[f].value = ima_k[f]

    def yaml_dump(self, file_name, reg_name="REGNS"):
        l = self.rf_to_yaml(reg_name)
        with open(file_name, 'w') as fout:
            _ = yaml.dump(l,fout)

    def yaml_load(self, file_name):
        with open(file_name, 'r') as fin:
            ima_db = yaml.load( fin, Loader=yaml.CLoader)
            self.yaml_to_rf(ima_db)

    def set_field(self, file_index, field, value):
        i = file_index
        for r in self.file[i].keys():
            for f in self.file[i][r].fields.keys():
                if f == field:
                    print("\tField {} will be set with value {}".format(f,value))
                    self.file[i][r].fields[f].value = value

    def print_hfile(self, out_file, data_name):
        ima = gen_reg_list( self.rf_to_yaml(), self.yaml_template)
        gen_hdata_file( out_file, ima, 32, self.bitwidth, data_name)

@dataclass
class InstructionMemory(RegisterFileClass):
    def __init__(self, bitwidth=16, yaml_file=None, yaml_template="../diana_rf_metadata/ima_template.yaml"):
        super(InstructionMemory,self).__init__(bitwidth)
        self.template = DIANAInstruction
        self.yaml_template = yaml_template
        if os.path.isfile(yaml_file):
            self.yaml_load(yaml_file)
    
    def compile(self, conv_layers: List[ConvLayerClass]):
        for layer in conv_layers:
            j = self.new_instruction(self.template)
            for r in self.file[j].keys():
                for f in self.file[j][r].fields.keys():
                    if f in FieldCompilerDict.keys():
                        self.file[j][r].fields[f].value = FieldCompilerDict[f](layer)
                    else:
                        self.file[j][r].fields[f].value = self.file[j][r].fields[f].default