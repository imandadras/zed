from compiler.inspectors import ModelInspector, ModelInputClass
from brevitas.aimc.nn.analog import AimcConv2d
from compiler.util import convert_scale
from compiler.data_class import ConvLayerClass

from math import log, ceil

import numpy

"""
NAME
    BrevitasModelCompiler (class)
DESCRIPTION
    Pytorch to Diana compilation functions
FILE CONTENTS
    BrevitasModelCompiler (class)
COPYRIGHT
    author= Giuseppe Sarda
    data=   17 I 2022
    email=  sarda74@imec.be
"""

class BrevitasModelCompiler():
    def __init__(self, model):
        self.model = model
        self.inspector = ModelInspector(model, True, True)
        self.analogConvList = self._gen_convList()
        self.analogConvLayers = []
    
    def _populate_convLayers(self,image : ModelInputClass = None):
        self.inspector._fw_p(image)
        for i in self.analogConvList:
            #initialize
            ds = False
            r_s2=1
            w   = self.inspector.inspectors[i].extract_param()
            bn  = self.inspector.inspectors[i+1].extract_param()
            if "downsample" in self.inspector.inspectors[i].name: #if this is a 1x1 layer
                ds = True
                r_s = 1
                q_s = self.inspector.inspectors[i+1].outputs.scale.to('cpu').detach().numpy().copy() #save bn output scale
            elif "downsample" in self.inspector.inspectors[i+3].name: #if there is residual at the end with a 1x1 in the shortcut
                q_s = self.inspector.inspectors[i+2].outputs.scale.to('cpu').detach().numpy().copy() #save final relu scale
                r_s = self.inspector.inspectors[i+1].outputs.scale.to('cpu').detach().numpy().copy() #save bn output scale
                ds = True
            elif "residual" in self.inspector.inspectors[i+3].name: #if normal residual
                q_s = self.inspector.inspectors[i+2].outputs.scale.to('cpu').detach().numpy().copy() #save final relu scale
                r_s = self.inspector.inspectors[i+3].inputs[0].scale.to('cpu').detach().numpy().copy() #same as bottlneck branch scale
                r_s2 = self.inspector.inspectors[i+3].inputs[1].scale.to('cpu').detach().numpy().copy()
            elif "relu" in self.inspector.inspectors[i+2].name: #normal layers
                r_s = 1
                q_s = self.inspector.inspectors[i+2].outputs.scale.to('cpu').detach().numpy().copy() #save relu output scale
            self.analogConvLayers.append(ConvLayerClass( tag     = self.inspector.inspectors[i].name,
                                                        w       = w.weight,
                                                        ws      = w.weight_scale, #convert_scale(o_s/i_s),
                                                        bn_w    = bn.weight,
                                                        bn_ws   = convert_scale(bn.weight_scale),
                                                        bn_b    = bn.bias,
                                                        bn_bs   = convert_scale(bn.bias_scale),
                                                        r_s     = convert_scale(r_s)-convert_scale(r_s2),
                                                        q_s     = convert_scale(q_s),
                                                        ds = ds))

    def _gen_convList(self):
        l = []
        for i, m in enumerate(self.inspector.inspectors):
            if (type(m.module) == AimcConv2d):
                l.append(i)
        return l

    def _process_scales(self, i):
        #as it is now, it is not possible to process a single layer because of state save (bn_s)
        pass
    
    def _process_weights(self, i):
        self.analogConvLayers[i].w = self.analogConvLayers[i].w/self.analogConvLayers[i].ws 


    def _process_convLayers(self):
        for i in range(len(self.analogConvLayers)):
            if (self.analogConvLayers[i].r_s == 0 and self.analogConvLayers[i].ds == False): #Normal layers
                self.analogConvLayers[i].set_qs(self.analogConvLayers[i].bn_bs-self.analogConvLayers[i].q_s)
            elif (self.analogConvLayers[i].r_s != 0 and self.analogConvLayers[i].ds == True): 
                bn_s = self.analogConvLayers[i].r_s
                if (self.analogConvLayers[i].r_s>self.analogConvLayers[i+1].q_s):
                    self.analogConvLayers[i].set_rs(bn_s-self.analogConvLayers[i+1].q_s)
                    self.analogConvLayers[i].set_qs(bn_s-self.analogConvLayers[i].q_s)
                else:
                    self.analogConvLayers[i].set_rs(0)
                    self.analogConvLayers[i].set_qs(bn_s-self.analogConvLayers[i].q_s)
            elif (self.analogConvLayers[i].r_s == 0 and self.analogConvLayers[i].ds == True):
                if (self.analogConvLayers[i].q_s>bn_s):
                    self.analogConvLayers[i].set_qs(self.analogConvLayers[i].q_s-bn_s)
                else:
                    self.analogConvLayers[i].set_qs(0)
            elif (self.analogConvLayers[i].r_s != 0 and self.analogConvLayers[i].ds == False):
                self.analogConvLayers[i].set_qs(self.analogConvLayers[i].bn_bs-self.analogConvLayers[i].q_s)
            
            self._process_weights(i)

    def compile(self, image : ModelInputClass = None):
        self._populate_convLayers(image)
        del self.inspector
        self._process_convLayers()

    def print_model(self):
        print(self.inspector)

    def report_scales(self, fname=None):
        fname = fname if fname else "scales.rpt"
        with open(fname, "w") as fpointer:
            for l in self.analogConvLayers:
                fpointer.write("LAYER: {}\n".format(l.tag))
                fpointer.write("\tIS: {}\n".format(l.ws))
                fpointer.write("\tBN_WS: {}\n".format(l.bn_ws))
                fpointer.write("\tBN_BS: {}\n".format(l.bn_bs))
                fpointer.write("\tR_S: {}\n".format(l.r_s))
                fpointer.write("\tQ_S: {}\n".format(l.q_s))
                fpointer.write("\n")