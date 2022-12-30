import math
import numpy

################# UTIL FUNCTIONS ################
def convert_scale(scale):
    s = math.log(numpy.round(1/scale),2)
    if (s%1 != 0):
        raise ValueError
    return s