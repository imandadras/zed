import numpy as np
import random as rnd
import math

"""
NAME
    input_gen
DESCRIPTION
    activation inputs generation toolkit
FILE CONTENTS
    ReLU
    get_unif_input
    get_norm_input
    get_rand_input
    gen_input
    _main (usage example)
COPYRIGHT
    author= Giuseppe Sarda
    data=   01 XII 2021
    email=  sarda74@imec.be
"""

from c_util.h_gen import gen_hdata_file

def ReLU(x):
    return x if (x>0) else 0

#TODO write functions for array generations

#single uniform integer generator
def get_unif_input(v):
    return v

#single normal distributed integer generator
def get_norm_input(loc, scale, clip, _range, signed=False):
    """get_norm_input(loc, scale, clip, _range, signed=False)

        Single normal distributed integer generator, ReLU inplace
        Parameters:
        loc     (float): center of the normal distribution
        scale   (float): sigma of the normal distribution
        clip    (float): maximum allowed number (positive and negative). All values will be clipped.
        _range  (int):  integer bitwidth
        signed  (bool):  default False. If the value generated is negative it clips to zero.
        NOTE: generated numbers will always be reranged centered to zero, regardless of distribution loc

        Returns:
        v        (int): integer number drawn according to normal distribution

        E.g.)
            a = get_norm_input( loc=0, scale=1/8, clip=1, _range=7)
    """
    v = np.random.normal(loc,scale)
    sign_v = 1 if (v<0) else -1
    #clipping
    if abs(v)>clip:
        v = -1*sign_v*clip
    #ReLU
    v = 0 if ((sign_v==1) and not signed) else v
    
    #re-range and bin
    v = math.floor(v/clip*2**(_range-1))
    return v

def get_rand_input(_range, signed=False):
    """get_norm_input(loc, scale, clip, _range, signed=False)

        Single random integer generator
        Parameters:
        _range  (int):  integer bitwidth
        signed  (bool):  default False. If the value generated is negative it clips to zero.
        NOTE: generated numbers will always be reranged centered to zero, regardless of distribution loc
        Returns:
        v        (int): integer number drawn according to normal distribution
    """
    max_v = 2**(_range-1)
    v = rnd.randint(-max_v,max_v)
    sign_v = 1 if (v<0) else -1
    #ReLU
    v = 0 if (sign_v and not signed) else v
    return v

#Dictionary translating the arguments
SINGLE_TYPE={  "UNI" : get_unif_input,
        "NOR" : get_norm_input,
        "RAN" : get_rand_input}

def _gen_input(_t, size, **kwargs):
    ig=[]
    for _ in range(size):
        ig.append(SINGLE_TYPE[_t](**kwargs)) #getting correct input generating function
    return ig

"""
start_r--> first activation non zero
range_r--> how many non zero
batch_size--> channels, the number of data paket within the range of v value falls
    e.g. gen_row active(1,2,4,2) --> 0110,0110 (list is flat)
batch_num --> numbers of pakets
"""
def gen_row_active(start_r, range_r, batch_size, batch_num, v=63):
    ig=[]
    start_r2 = start_r
    if 383<(start_r)<512:
        start_r2=512+(start_r-384)
    if 511<start_r<896:
        start_r2= start_r+128
    if 895<start_r<1024:
        start_r2=1024+128+(start_r-896)
    if 1023<start_r:
        start_r2= start_r+256
    start_r = start_r2
    end_r = start_r + range_r
    end_r2 = end_r
    if 383<(end_r)<512:
        end_r2=512+(end_r-384)
    if 511<end_r<896:
        end_r2= end_r+128
    if 895<end_r<1024:
        end_r2=1024+128+(end_r-896)
    if 1023<end_r:
        end_r2= end_r+256
    end_r=end_r2
    

    if 383<(end_r%383)<512:
        end_r=(((end_r//383)+1)*640)+(end_r%383)
    
    print (start_r,end_r)
    for _ in range(batch_num):
        for i in range(batch_size):
            if (i>=start_r and i<end_r):
                ig.append(v)
            else:
                ig.append(0)
    return ig

GEN_TYPE={  "SIN" : _gen_input,
            "ROW" : gen_row_active}

def gen_input(_type, **kwargs):
    return GEN_TYPE[_type](**kwargs)

if __name__ == '__main__':
    def _main():
        a = gen_input( "UNI", 1152, v=1)
        gen_hdata_file("../functional_test/input_memory_ania.h", a, 32, 8, "input_ania")
    _main()
