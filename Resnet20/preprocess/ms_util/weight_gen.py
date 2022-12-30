import random as rnd
from typing import List

from c_util.h_gen import gen_hdata_file
from hw_lib.hw_def import DIANA_AiMC
import hw_lib.hw_def
"""
NAME
    weight_gen
DESCRIPTION
    weights generation toolkit
FILE CONTENTS
    get_rand_weight
    gen_pd
    tern_to_bin
    flip_weights
    gen_input
    flatten_list
    gen_hw_test_weights
    _main (usage example)
COPYRIGHT
    author= Giuseppe Sarda
    data=   01 XII 2021
    email=  sarda74@imec.be
"""

def get_rand_weight(distrs,values):
    p = rnd.randint(0,99)
    for i,d in enumerate(distrs[::-1]):
        if p>=d:
            return values[-i]
    return values[0]

def gen_pd(distrs):
    d = [distrs[0]]
    for i in distrs[1:]:
        d.append(d[-1]+i)
    return d

def _transpose(wg):
    # iterate over list l1 to the length of an item
    wg_t = []
    for t in range(len(wg)):
        tile = []
        for i in range(len(wg[t][0])):
            # print(i)
            row =[]
            for item in wg[t]:
                # appending to new list with values and index positions
                # i contains index position and item contains values
                row.append(item[i])
            tile.append(row)
        wg_t.append(tile)
    return wg_t

def gen_rpd_weights(pos_dist, neg_dist, tiles=1, aimc=DIANA_AiMC):
    
    n_rows = aimc.n_rows 
    n_cols = aimc.n_cols 
    values = aimc.w_values    
    
    wg = []
    zero_dist = 100-pos_dist-neg_dist
    distrs = [neg_dist,zero_dist,pos_dist]
    for i in range(tiles):
        w_t = []
        for r in range(n_rows):
            w_r = []
            for c in range(n_cols):
                w_r.append( get_rand_weight(    distrs=gen_pd(distrs),
                                                values=values))
            w_t.append(w_r)
        wg.append(w_t)
    return wg

"""
gen stair weights
11111111
01110111
00110011
00010001
"""
def gen_stair_weights(polarity, start_val, step, tiles=1, aimc=DIANA_AiMC):

    n_rows = aimc.n_rows
    n_cols = aimc.n_cols
        
    wg = []
    values = n_cols if (start_val) else n_cols-1
    res = start_val
    for _ in range(tiles):
        w_t = []
        for r in range(n_rows):
            w_r = []
            for c in range(n_cols):
                if c<values:
                    w_r.append(polarity)
                else:
                    w_r.append(0)
            res -= 1
            if (res < 1): 
                values -= 1
                res = step
            w_t.append(w_r)
        wg.append(w_t)
    return wg

def gen_chess_weights(polarity=1, right=False, tiles=1, aimc=DIANA_AiMC): 
    
    n_rows = aimc.n_rows 
    n_cols = aimc.n_cols
    rows_per_blk = aimc.rows_per_block
    cols_per_blk = aimc.cols_per_block
    row_blocks = aimc.row_blocks
    
    wg = []
    for _ in range(tiles): #all tiles the same
        w_t = []
        for r in range(n_rows):
            rb = r//rows_per_blk
            w_r = []
            for c in range(n_cols):
                cb = c//cols_per_blk
                if (rb==abs(int(right)*row_blocks-cb)):
                    w_r.append(polarity)
                else:
                    w_r.append(0)
            w_t.append(w_r)
        wg.append(w_t)
    return wg

def gen_column_weights(start_r, batch_r, start_c, batch_c, polarity=1, tiles=1, aimc=DIANA_AiMC): 
    
    n_rows=aimc.n_rows 
    n_cols=aimc.n_cols
    
    wg = []
    end_r = start_r + batch_r
    end_c = start_c + batch_c
    for _ in range(tiles): #all tiles the same
        w_t = []
        for r in range(n_rows):
            w_r = []
            for c in range(n_cols):
                if (c>=start_c and c<end_c and r>=start_r and r<end_r):
                    w_r.append(polarity)
                else:
                    w_r.append(0)
            w_t.append(w_r)
        wg.append(w_t)
    return wg

def gen_block_weights(colb: List[int], rowb: List[int], polarity=1, tiles=1, aimc=DIANA_AiMC): 
    
    n_rows=aimc.n_rows 
    n_cols=aimc.n_cols
    rows_per_blk = aimc.rows_per_block
    cols_per_blk = aimc.cols_per_block

    wg = []
    for _ in range(tiles): #all tiles the same
        w_t = []
        for r in range(n_rows):
            rb = r//rows_per_blk
            w_r = []
            for c in range(n_cols):
                cb = c//cols_per_blk
                if ((rb in rowb) and (cb in colb)):
                    w_r.append(polarity)
                else:
                    w_r.append(0)
            w_t.append(w_r)
        wg.append(w_t)
    return wg

def mirror_X(w):
    wg = []
    for t in range(len(w)):
        for r in range(len(w[0])):
            wg.append(w[t][r][::-1])
    return wg

def mirror_Y(w):
    wg = []
    for t in range(len(w)):
        w_t = []
        for r in range( len(w[0])-1, -1, -1):
            w_t.append(w[t][r])
        wg.append(w_t)
    return wg

def mirror_XY(w):
    wg = []
    for t in range(len(w)):
        w_t = []
        for r in range( len(w[0])-1, -1, -1):
            w_t.append(w[t][r][::-1])
        wg.append(w_t)
    return wg

def tern_to_bin(w):
    if w==1:
        return 2
    elif w==-1:
        return 1
    else:
        return 0

def flip_weights(w,toBin=False):
    for t in range(len(w)):
        for r in range(len(w[0])):
            for c in range(len(w[0][0])):
                b = r//64
                if ((c%2==0) and not (b in [6, 7, 8, 9, 10, 11])): #if odd column
                    w[t][r][c]=-w[t][r][c]
                elif ((c%2) and (b<=8)):
                    w[t][r][c]=-w[t][r][c]
                if toBin:
                    w[t][r][c]=tern_to_bin(w[t][r][c])
    return w

def map_weights(w):
    ww = []
    for t in range(len(w)):
        w_t = []
        for r in range(len(w[0])):
            w_p = []
            w_m = []
            for c in range(len(w[0][0])):
                if w[t][r][c]==1:
                    w_p.append(1)
                    w_m.append(0)
                elif w[t][r][c]==-1:
                    w_p.append(0)
                    w_m.append(1)
                else:
                    w_p.append(0)
                    w_m.append(0)
            w_t.append(w_p)
            w_t.append(w_m)
        ww.append(w_t)
    return ww

def flatten_list(l):
    if not (type(l[0]) == list):
        return l
    else:
        flat_l = []
        for e in l:
            for i in e:
                flat_l.append(i)
        return flatten_list(flat_l)

#def gen_ones(tiles):
#    return tiles*[1152*[512*[1]]]

def gen_ones(tiles=1, aimc=DIANA_AiMC):

    n_rows = aimc.n_rows
    n_cols = aimc.n_cols
        
    wg = []
    for _ in range(tiles):
        w_t = []
        for r in range(n_rows):
            w_r = []
            for c in range(n_cols):
                w_r.append(1)
            w_t.append(w_r)
        wg.append(w_t)
    return wg

TYPE={  "RPD" : gen_rpd_weights,# residual 
        "STR" : gen_stair_weights,
        "CLM" : gen_column_weights,
        "CSS" : gen_chess_weights,
        "BLK" : gen_block_weights,
        "ONE" : gen_ones}


def gen_hw_test_weights(_type, hardwarize=True, serialize=True, **kwargs):
    w = TYPE[_type](**kwargs)
    #visualize = hw_lib.hw_def.AiMC(1152,512,list(range(-1,2)),32,64)
    #visualize.list2d_fdisplay(w,"weightVisualize.txt")
    if hardwarize:
        w = mirror_Y(w)
        w = flip_weights(w)
        w = map_weights(w)
    if serialize:
        w = flatten_list(w)
    return w

if __name__ == '__main__':
    def _main():
        w = gen_rpd_weights(20, 20, 1)
        w = flip_weights(w)
        flw = flatten_list(w)
        gen_hdata_file("try.h", flw, 32, 2, "w_cnn_ania")
    _main()
