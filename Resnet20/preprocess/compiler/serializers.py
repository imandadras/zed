from hw_lib.hw_def import DIANA_AiMC
from compiler.data_class import BinaryLayerClass, SerialTensor, WeightSerialTensor, ActivationSerialTensor
from c_util.h_gen import gen_hdata_file
from ms_util.aim_gen import gen_reg_list

class Serializer():
    def __init__(self):
        self.serial_data = SerialTensor([],None)
    
    def __call__(self):
        return self.serial_data()
    
    def serialize(self):
        raise NotImplementedError
    
    def pad(self):
        raise NotImplementedError

    def tile(self):
        raise NotImplementedError

    def process(self):
        raise NotImplementedError

    def gen_hbinary(self, path, data_name):
        raise NotImplementedError

class AiMCWeightSerializer(Serializer):
    def __init__(self, weight):
        super(AiMCWeightSerializer,self).__init__()
        self._weight = weight

    @staticmethod
    def tern_to_bin(w):
        if w==1:
            return 2
        elif w==-1:
            return 1
        else:
            return 0

    def serialize(self,AiMC=DIANA_AiMC):
        """
        serialize(self)
            Serializes Pytorch weight tensor (K,C,X,Y order) to Diana L2 data ordering for AiMC 
            INPUT PARAMS
            inplace (bool)
            RETURN
            wg (SerialTensor): SerialTensor containing the weights in the order Y,X,C,K
        """
        shape = list(self._weight.shape)
        K  = shape[0]
        C  = shape[1]
        FX = shape[3]
        FY = shape[2]
        wg = []
        for y in range(FY):
            for x in range(FX):
                for c in range(C):
                    for k in range(K):
                        wg.append(int(self._weight[k][c][y][x]))
        self.serial_data = WeightSerialTensor(shape,wg,AiMC)

    def _padd_C(self):
        K  = self.serial_data.virtual_size[0]
        C  = self.serial_data.virtual_size[1]
        FX = self.serial_data.virtual_size[3]
        FY = self.serial_data.virtual_size[2]
        #padding along C in case less than 64 in channels
        if (C<64):
            wg=[]
            print("Need for padding along C detected...")
            self.serial_data.virtual_size[1] = 64
            for i in range(FX*FY):
                for c in range(64):
                    for k in range(K):
                        if (c<C):
                            wg.append(self.serial_data.data[i*C*K+c*K+k])
                        else:
                            wg.append(0)
            self.serial_data.data = wg
    
    def _padd_K(self):
        K  = self.serial_data.virtual_size[0]
        C  = self.serial_data.virtual_size[1]
        FX = self.serial_data.virtual_size[3]
        FY = self.serial_data.virtual_size[2]
        if (K<64):
            wg=[]
            print("Need for padding along K detected...")
            self.serial_data.virtual_size[0] = 64
            for c in range(C*FX*FY):    #total amount of lines
                for i in range(64):     #single line
                    if (i<K):
                        wg.append(self.serial_data.data[c*K+i])
                    else:
                        wg.append(0)
            self.serial_data.data = wg

    #always pad after tiling
    def pad(self, C=True, K=True):
        if C:
            self._padd_C()
        if K:
            self._padd_K()

    def _tile_C(self, AiMC):
        TY = self.serial_data.tile_Y
        if (TY>1):
            raise NotImplementedError

    def _tile_R(self, AiMC):
        TX = self.serial_data.tile_X
        if (TX>1):
            print("Need for tiling along rows detected...")
            print("{} tiles will be created".format(TX))
            print("WARNING: kernel tiling not supported!")
            K  = self.serial_data.virtual_size[0]
            C  = self.serial_data.virtual_size[1]
            R  = AiMC.n_rows
            FX = self.serial_data.virtual_size[3]
            FY = self.serial_data.virtual_size[2]
            iC = C//TX #need to change this, in case we need to tile also along FX and FY
            #iC = C//(R//(FX*FY)) #need to change this, in case we need to tile also along FX and FY

            self.serial_data.virtual_size[1]
            wt=[]
            for t in range(TX):
                wt_=[]
                for y in range(FY):
                    for x in range(FX):
                        for c in range(iC):
                            for k in range(K):
                                wt_.append(self.serial_data.data[(((t*FY+y)*FX+x)*iC+c)*K+k])
                wt.append(wt_)
            self.serial_data.data = wt

    def _tile(self):
        try:
            _ = self.serial_data.data[0][0]
        except TypeError:
            self.serial_data.data = [self.serial_data.data]
        except IndexError:
            pass

    def tile(self, AiMC, R=True, C=True):
        if R:
            self._tile_R(AiMC)
        if C:
            self._tile_C(AiMC)
        self._tile()

    def line_twist(self,toBin=True):
        T=self.serial_data.get_tiling()
        R=self.serial_data.get_rows()
        C=self.serial_data.get_cols()
        for t in range(T):
            for r in range(R):
                b = r//64
                for c in range(C):
                    if ((c%2) and (b in [6, 7, 8, 9, 10, 11])): #if odd column
                        self.serial_data.data[t][r*C+c]=-self.serial_data.data[t][r*C+c]
                    elif ((c%2==0) and (b>8)):
                        self.serial_data.data[t][r*C+c]=-self.serial_data.data[t][r*C+c]
                    if toBin:
                        self.serial_data.data[t][r*C+c]=self.tern_to_bin(self.serial_data.data[t][r*C+c])


    def process(self, AiMC=DIANA_AiMC):
        print("Serializing the weights...")
        self.serialize(AiMC)
        print("Adding padding to the serial weights...")
        self.pad()
        print("Tiling the serial weights...")
        self.tile(AiMC)
        print("Serialization of weights complete!")
        print("Twisting the lines and binarizing...")
        self.line_twist()

    def gen_hbinary(self, path, data_name):
        for t in self.serial_data.data:
            gen_hdata_file( path, 
                            t, 
                            32, 
                            2, 
                            data_name,
                            endian="big")

class AiMCActivationSerializer(Serializer):
    def __init__(self, actv):
        super(AiMCActivationSerializer,self).__init__()
        self._actv = actv

    @property
    def actv(self):
        return self.serial_data.data

    @actv.setter
    def actv(self, actv):
        self._actv = actv
    
    def serialize(self):
        shape = list(self._actv.shape)
        B  = shape[0]
        C  = shape[1]
        X = shape[3]
        Y = shape[2]
        ag = []
        for b in range(B):
            at=[]
            for y in range(Y):
                for x in range(X):
                    for c in range(C):
                        at.append(int(self._actv[b][c][y][x]))
            ag.append(at)
        self.serial_data = ActivationSerialTensor(shape, ag)

    def pad(self): #TODO test
        C  = self.serial_data.virtual_size[1]
        _C = self.serial_data.min_C
        if (C<_C):
            B = self.serial_data.virtual_size[0]
            X = self.serial_data.virtual_size[3]
            Y = self.serial_data.virtual_size[2]
            ag = []
            for b in range(B):
                at = []
                for i in range(X*Y):
                    for c in range(_C):
                        if (c<C):
                            at.append(self.serial_data.data[b][_C*i+c])
                        else:
                            at.append(0)
                ag.append(at)
            self.serial_data.data = ag
    
    def process(self):
        print("Serializing the weights...")
        self.serialize()
        print("Adding padding to the serial weights...")
        self.pad()
    
    def gen_hbinary(self, path, data_name):
        for b in self.serial_data.data:
            gen_hdata_file( path, 
                            b, 
                            32, 
                            8, 
                            data_name)

class AiMCInstructionMemorySerializer(Serializer):
    def __init__(self, ima):
        super(AiMCInstructionMemorySerializer,self).__init__()
        self._ima = ima
    
    def serialize(self):
        self.serial_data = gen_reg_list(self._ima.rf_to_yaml(),self._ima.yaml_template)
    
    def gen_hbinary(self, path, data_name):
        gen_hdata_file( path, 
                        self.serial_data, 
                        32, 
                        16, 
                        data_name)

class DIANASerializer():
    """
    NAME
        DIANASerializer
    DESCRIPTION
        List of functions which Serialize data for Diana HW
    FILE CONTENTS
        __init__
        AiMC_weight_serializer
    """
    def __init__(self, layer, AiMC=DIANA_AiMC):
        self.AiMC = AiMC
        self.clayer = layer
        self.blayer = BinaryLayerClass(None, None)