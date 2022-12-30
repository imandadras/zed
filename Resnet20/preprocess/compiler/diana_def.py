from collections import OrderedDict
import math
from recordtype import recordtype

Register = recordtype( 'Register', ['index','fields'])
Field    = recordtype( 'Field',    ['value','bit','default'])

DIANAInstruction = OrderedDict()
DIANAInstruction['REG0'] = Register( index   = 0,
                                fields  = OrderedDict([
                                            ('SKIP_POOL' , Field(value=0, bit=1, default=1)),
                                            ('SKIP_QUANT', Field(value=0, bit=1, default=1)),
                                            ('SKIP_ACT'  , Field(value=0, bit=1, default=1)),
                                            ('SKIP_RES'  , Field(value=0, bit=1, default=1)),
                                            ('SKIP_BN'   , Field(value=0, bit=1, default=1)),
                                            ('POOL'      , Field(value=0, bit=2, default=0)),
                                            ('RELU_TYPE' , Field(value=0, bit=1, default=0)),
                                            ('RESERVED'  , Field(value=0, bit=7, default=0))
                                        ]))

DIANAInstruction['REG1'] = Register( index   = 1,
                                fields  = OrderedDict([
                                            ('RESERVED'  , Field(value=0, bit=16, default=0))
                                        ]))

DIANAInstruction['REG2'] = Register( index   = 2,
                                fields  = OrderedDict([
                                            ('ACT_START_ADDRESS'    , Field(value=0, bit=14, default=0)),
                                            ('RESERVED'             , Field(value=0, bit=2, default=0))
                                        ]))

DIANAInstruction['REG3'] = Register( index   = 3,
                                fields  = OrderedDict([
                                            ('OUT_START_ADDRESS'    , Field(value=0, bit=14, default=0)),
                                            ('RESERVED'             , Field(value=0, bit=2, default=0))
                                        ]))

DIANAInstruction['REG4'] = Register( index   = 4,
                                fields  = OrderedDict([
                                            ('PS_START_ADDRESS'    , Field(value=0, bit=14, default=0)),
                                            ('RESERVED'            , Field(value=0, bit=2, default=0))
                                        ]))

DIANAInstruction['REG5'] = Register( index   = 5,
                                fields  = OrderedDict([
                                            ('RES_START_ADDRESS'    , Field(value=0, bit=14, default=0)),
                                            ('RESERVED'             , Field(value=0, bit=2, default=0))
                                        ]))

DIANAInstruction['REG6'] = Register( index   = 6,
                                fields  = OrderedDict([
                                            ('BN_START_ADDRESS'     , Field(value=0, bit=13, default=0)),
                                            ('RESERVED'             , Field(value=0, bit=3, default=0))
                                        ]))

DIANAInstruction['REG7'] = Register( index   = 7,
                                fields  = OrderedDict([
                                            ('IN_CHANNEL'   , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG8'] = Register( index   = 8,
                                fields  = OrderedDict([
                                            ('OUT_CHANNEL'  , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG9'] = Register( index   = 9,
                                fields  = OrderedDict([
                                            ('IF_FMAP_X'    , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG10'] = Register( index  = 10,
                                fields  = OrderedDict([
                                            ('IF_FMAP_Y'    , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG11'] = Register( index  = 11,
                                fields  = OrderedDict([
                                            ('PRECISION'    , Field(value=0, bit=4, default=7)),
                                            ('FP_INT_N'     , Field(value=0, bit=1, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=11, default=0))
                                        ]))

DIANAInstruction['REG12'] = Register( index  = 12,
                                fields  = OrderedDict([
                                            ('KERNEL_X'     , Field(value=0, bit=4, default=0)),
                                            ('KERNEL_Y'     , Field(value=0, bit=4, default=0)),
                                            ('POOLING_SIZE' , Field(value=0, bit=5, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=3, default=0))
                                        ]))

DIANAInstruction['REG13'] = Register( index   = 13,
                                fields  = OrderedDict([
                                            ('OF_FMAP_X'    , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG14'] = Register( index  = 14,
                                fields  = OrderedDict([
                                            ('OF_FMAP_Y'    , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG15'] = Register( index  = 15,
                                fields  = OrderedDict([
                                            ('OX_UNROLL'        , Field(value=0, bit=4, default=1)),
                                            ('RES_WORD_SIZE'    , Field(value=0, bit=4, default=0)),
                                            ('RESERVED'         , Field(value=0, bit=8, default=0))
                                        ]))
                                    
DIANAInstruction['REG16'] = Register( index  = 16,
                                fields  = OrderedDict([
                                            ('STRIDE'   , Field(value=0, bit=2, default=1)),
                                            ('RESERVED' , Field(value=0, bit=14, default=0))
                                        ]))

DIANAInstruction['REG17'] = Register( index  = 17,
                                fields  = OrderedDict([
                                            ('PADDING_DOWN'     , Field(value=0, bit=2, default=0)),
                                            ('PADDING_UP'       , Field(value=0, bit=2, default=0)),
                                            ('PADDING_RIGHT'    , Field(value=0, bit=2, default=0)),
                                            ('PADDING_LEFT'     , Field(value=0, bit=2, default=0)),
                                            ('RESERVED'         , Field(value=0, bit=8, default=0))
                                        ]))

DIANAInstruction['REG18'] = Register( index  = 18,
                                fields  = OrderedDict([
                                            ('PROCESSING_BLOCK' , Field(value=0, bit=4, default=1)),
                                            ('RESERVED'         , Field(value=0, bit=14, default=0))
                                        ]))

DIANAInstruction['REG19'] = Register( index  = 19,
                                fields  = OrderedDict([
                                            ('PS_PREC'      , Field(value=0, bit=2, default=1)),
                                            ('OUT_PREC'     , Field(value=0, bit=2, default=1)),
                                            ('OUT_OFFSET'   , Field(value=0, bit=5, default=0)),
                                            ('BUF_OFFSET'   , Field(value=0, bit=4, default=0)),
                                            ('WEIGHT_INIT'  , Field(value=0, bit=1, default=0)),
                                            ('SIMD_INIT'    , Field(value=0, bit=1, default=0)),
                                            ('RESERVED'     , Field(value=0, bit=1, default=0))
                                        ]))

DIANAInstruction['REG20'] = Register( index  = 20,
                                fields  = OrderedDict([
                                            ('USE_BLK_COL' , Field(value=0, bit=16, default=1))
                                        ]))

DIANAInstruction['REG21'] = Register( index  = 21,
                                fields  = OrderedDict([
                                            ('UNIT_TIME'    , Field(value=0, bit=8, default=1)),
                                            ('DELAY_SYNC'   , Field(value=0, bit=2, default=1)),
                                            ('RESERVED'     , Field(value=0, bit=6, default=0))
                                        ]))

DIANAInstruction['REG22'] = Register( index  = 22,
                                fields  = OrderedDict([
                                            ('STOP'         , Field(value=0, bit=1, default=0)),
                                            ('ANIA_INIT'    , Field(value=0, bit=1, default=0)),
                                            ('AVG_POOL_DIV' , Field(value=0, bit=8, default=0)),
                                            ('ANIA_INIT_V'  , Field(value=0, bit=2, default=0)),
                                            ('MEM_LAYOUT'   , Field(value=0, bit=4, default=15))
                                        ]))

DIANAInstruction['REG23'] = Register( index  = 23,
                                fields  = OrderedDict([
                                            ('CSBIAS_DRIVER'    , Field(value=0, bit=4, default=0)),
                                            ('ADC_OUT_RANGE'    , Field(value=0, bit=1, default=0)),
                                            ('OF_POOL_SIZE'     , Field(value=0, bit=10, default=0)),
                                            ('RESERVED'         , Field(value=0, bit=1, default=0))
                                        ]))

DIANAInstruction['REG24'] = Register( index  = 24,
                                fields  = OrderedDict([
                                            ('RESERVED' , Field(value=0, bit=16, default=0x0084))
                                        ]))

DIANAInstruction['REG25'] = Register( index  = 25,
                                fields  = OrderedDict([
                                            ('WGT_PAKET_S' , Field(value=0, bit=16, default=0))
                                        ]))
                                        
DIANAInstruction['REG26'] = Register( index  = 26,
                                fields  = OrderedDict([
                                            ('BN_PAKET_S' , Field(value=0, bit=16, default=0))
                                        ]))

DIANAInstruction['REG27'] = Register( index  = 27,
                                fields  = OrderedDict([
                                            ('QUANT_SCALE'  , Field(value=0, bit=8, default=0)),
                                            ('RES_SCALE'    , Field(value=0, bit=4, default=0)),
                                            ('BETA_SCALE'   , Field(value=0, bit=4, default=0))
                                        ]))

DIANAInstruction['REG28'] = Register( index  = 28,
                                fields  = OrderedDict([
                                            ('LRELU_THRLD' , Field(value=0, bit=16, default=0))
                                        ]))

DIANAInstruction['REG29'] = Register( index  = 29,
                                fields  = OrderedDict([
                                            ('WAIT_CS_LDO'  , Field(value=0, bit=1, default=0)),
                                            ('CSBIAS_DELAY' , Field(value=0, bit=15, default=0))
                                        ]))

DIANAInstruction['REG30'] = Register( index  = 30,
                                fields  = OrderedDict([
                                            ('RESERVED' , Field(value=0, bit=16, default=0))
                                        ]))

DIANAInstruction['REG31'] = Register( index  = 31,
                                fields  = OrderedDict([
                                            ('RESERVED' , Field(value=0, bit=16, default=0))
                                        ]))


def skip_pool(layer):
    print("WARNING! SKIP_POOL support not available!")
    return 1

def skip_quant(layer):
    print("WARNING! PSUM support not available!")
    return 0

def skip_act(layer):
    print("WARNING! PSUM & RES support not available!")
    return 0

def skip_res(layer):
    print("WARNING! RES support not available!")
    return 1

def skip_bn(layer):
    print("WARNING! BN always active!")
    return 0

def pool_type(layer):
    print("WARNING! POOL_TYPE support not available!")
    return 0

def relu_type(layer):
    print("WARNING! RELU_TYPE support not available!")
    return 0

def act_start_address(layer):
    print("WARNING! Mapping for ACTIVATION START ADDRESS support not available!")
    return 0

def out_start_address(layer):
    print("WARNING! Mapping for OUTPUT START ADDRESS support not available!")
    return 0

def ps_start_address(layer):
    print("WARNING! Mapping for PSUM START ADDRESS support not available!")
    return 0

def res_start_address(layer):
    print("WARNING! Mapping for RES START ADDRESS support not available!")
    return 0

def bn_start_address(layer):
    print("WARNING! Mapping for BN START ADDRESS support not available!")
    return 0

def in_channel(layer):
    C = list(layer.w.shape)[1]
    print("IN_CHANNEL : {}".format(C))
    return C

def out_channel(layer):
    K = list(layer.w.shape)[0]
    print("IN_CHANNEL : {}".format(K))
    return K

def if_fmap_x(layer):
    print("WARNING! Input feature map size support not available!")
    return 0
    
def if_fmap_y(layer):
    print("WARNING! Input feature map size support not available!")
    return 0

def precision(layer):
    return 7 #only default precision available

def fp_int_n(layer):
    return 1 #only default integer supported

def kernel_x(layer):
    FX = list(layer.w.shape)[3]
    print("IN_CHANNEL : {}".format(FX))
    return FX

def kernel_y(layer):
    FY = list(layer.w.shape)[2]
    print("IN_CHANNEL : {}".format(FY))
    return FY

def pooling_size(layer):
    print("WARNING! POOLING SIZE support not available!")
    return 0

def of_fmap_x(layer):
    print("WARNING! Output feature map size support not available!")
    return 0

def of_fmap_y(layer):
    print("WARNING! Output feature map size support not available!")
    return 0

def ox_unroll(layer):
    print("WARNING! Mapping for OX UNROLLING support not available!")
    return 0

def res_word_size(layer):
    print("WARNING! RESIDUAL WORD SIZE support not available")
    return 0

def stride(layer):
    print("WARNING! Mapping for STRIDE support not available!")
    return 1

def padding_down(layer):
    print("WARNING! Mapping for PADDING support not available!")
    return 0

def padding_up(layer):
    print("WARNING! Mapping for PADDING support not available!")
    return 0

def padding_right(layer):
    print("WARNING! Mapping for PADDING support not available!")
    return 0

def padding_left(layer):
    print("WARNING! Mapping for PADDING support not available!")
    return 0

def processing_block(layer):
    K = list(layer.w.shape)[0] #Note! K should be "virtual"--> after mapping
    PB = math.ceil(K/64)
    print("PROCESSIN BLOCKS : {}".format(PB))
    return PB

def ps_prec(layer):
    print("WARNING! Mapping for PSUM PRECISION support not available!")
    return 0

def out_prec(layer):
    print("WARNING! Mapping for OUT PRECISION support not available!")
    return 0

def out_offset(layer):
    print("WARNING! Mapping for OUT REGISTER OFFSET support not available!")
    return 0

def buf_offset(layer):
    print("WARNING! Mapping for BUFFER OFFSET support not available!")
    return 0

def weight_init(layer):
    return 1    #No weight_init by default

def simd_init(layer):
    return 1    #By default is 1

def use_blk_col(layer):
    K = list(layer.w.shape)[0]
    ubc = math.ceil(K/32)
    UBC = 2**ubc -1
    print("USE_BLOCK_COLUMN : {}".format(UBC))
    return UBC

def unit_time(layer):
    print("WARNING! UNIT_TIME support not available!")
    return 10
    
def delay_sync(layer):
    return 1 #By default is 1 

def stop(layer):
    return 0 #never a stop instruction. Compiler will always have to add a stop instruction

def ania_init(layer):
    return 0 #never a init instruction

def avg_pool_div(layer):
    print("WARNING! AVG_POOL_DIV support not available!")
    return 1

def ania_init_v(layer):
    return 0 #by default is 0. Never use a different value

def mem_layout(layer):
    return 15 #don't mess up with this field

def csbias_driver(layer):
    return 0 #not active field at this time

def adc_out_range(layer):
    return 0 #default value, different value should be set at model level

def of_pool_size(layer):
    print("WARNING! OUTPUT POOL SIZE support not available!")
    return 1

def wgt_paket_s(layer):
    print("WARNING! WEIGHT PAKET SIZE with OX UNROLLING support not available!")
    print("WARNING! WEIGHT PAKET SIZE must be better implemented with mapping information!")
    K = list(layer.w.shape)[0]
    C = list(layer.w.shape)[0]
    FX = list(layer.w.shape)[0]
    FY = list(layer.w.shape)[0]
    B = math.ceil(K/256)
    WPS = C*FX*FY*B
    print("WGT_PAKET_S : {}".format(WPS))
    return WPS

def bn_paket_s(layer):
    K = list(layer.w.shape)[0]
    BPS =math.ceil(K/16)
    print("BN_PAKET_S : {}".format(BPS))
    return BPS

def quant_scale(layer):
    QS = layer.q_s
    print("QUANT_SCAL : {}".format(QS))
    return QS

def res_scale(layer):
    RS = layer.r_s
    print("RES_SCAL : {}".format(RS))
    return RS

def beta_scale(layer):
    BS = layer.bn_bs
    print("BETA_SCAL : {}".format(BS))
    return BS

def lrelu_thrld(layer):
    print("WARNING! LEAKY RELU support not available!")
    return 0

def wait_cs_ldo(layer):
    return 0 #never wait for LDO

def csbias_delay(layer):
    return 0 #never specify a delay


FieldCompilerDict = {
    "SKIP_POOL"         : skip_pool,
    "SKIP_QUANT"        : skip_quant,
    "SKIP_ACT"          : skip_act,
    "SKIP_RES"          : skip_res,
    "SKIP_BN"           : skip_bn,
    "POOL"              : pool_type,
    "RELU_TYPE"         : relu_type,
    "ACT_START_ADDRESS" : act_start_address, 
    "OUT_START_ADDRESS" : out_start_address, 
    "PS_START_ADDRESS"  : ps_start_address, 
    "RES_START_ADDRESS" : res_start_address, 
    "BN_START_ADDRESS"  : bn_start_address, 
    "IN_CHANNEL"        : in_channel, 
    "OUT_CHANNEL"       : out_channel, 
    "IF_FMAP_X"         : if_fmap_x, 
    "IF_FMAP_Y"         : if_fmap_y, 
    "PRECISION"         : precision, 
    "FP_INT_N"          : fp_int_n, 
    "KERNEL_X"          : kernel_x, 
    "KERNEL_Y"          : kernel_y, 
    "POOLING_SIZE"      : pooling_size, 
    "OF_FMAP_X"         : of_fmap_x, 
    "OF_FMAP_Y"         : of_fmap_y, 
    "OX_UNROLL"         : ox_unroll, 
    "RES_WORD_SIZE"     : res_word_size, 
    "STRIDE"            : stride, 
    "PADDING_DOWN"      : padding_down, 
    "PADDING_UP"        : padding_up, 
    "PADDING_RIGHT"     : padding_right, 
    "PADDING_LEFT"      : padding_left, 
    "PROCESSING_BLOCK"  : processing_block, 
    "PS_PREC"           : ps_prec, 
    "OUT_PREC"          : out_prec, 
    "OUT_OFFSET"        : out_offset, 
    "BUF_OFFSET"        : buf_offset, 
    "WEIGHT_INIT"       : weight_init, 
    "SIMD_INIT"         : simd_init, 
    "USE_BLK_COL"       : use_blk_col, 
    "UNIT_TIME"         : unit_time, 
    "DELAY_SYNC"        : delay_sync, 
    "STOP"              : stop, 
    "ANIA_INIT"         : ania_init, 
    "AVG_POOL_DIV"      : avg_pool_div, 
    "ANIA_INIT_V"       : ania_init_v, 
    "MEM_LAYOUT"        : mem_layout,    
    "CSBIAS_DRIVER"     : csbias_driver, 
    "ADC_OUT_RANGE"     : adc_out_range, 
    "OF_POOL_SIZE"      : of_pool_size, 
    "WGT_PAKET_S"       : wgt_paket_s, 
    "BN_PAKET_S"        : bn_paket_s, 
    "QUANT_SCALE"       : quant_scale, 
    "RES_SCALE"         : res_scale, 
    "BETA_SCALE"        : beta_scale, 
    "LRELU_THRLD"       : lrelu_thrld, 
    "WAIT_CS_LDO"       : wait_cs_ldo, 
    "CSBIAS_DELAY"      : csbias_delay, 
}