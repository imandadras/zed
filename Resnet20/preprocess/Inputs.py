import math
import numpy as np

header_32_line="__attribute__((aligned(16))) uint32_t {}[] =" #need +'{\n'
footer_line="};\n"
def activations(input_file):
    with open (input_file , 'r') as file:
        text = file.read().splitlines()
    Layers = []
    input_shapes = []
    i=-1
    check = False
    for line in text:
        if line[:8] == "IN_SHAPE":

            input_shape=(line[21:-2])
            input_shape = input_shape.split(",")
            input_shape = [int(num) for num in input_shape]
            input_shapes.append(input_shape)
        if line == "INPUT":
            check = True
            i += 1
            Layers.append([])
        if line == "OUTPUT":
            check = False

        if check == True:
            Layers[i].append(line)
    Layers_n = []
    for Layer in Layers:
        Layer = Layer[1:]
        Layer = [int(x) for x in Layer]
        Layers_n.append(Layer)
    reshaped = []
    for i, layer in enumerate(Layers_n) :
        Layer= np.reshape(layer, input_shapes[i])
        reshaped.append(Layer)

    outputs = []
    for FM, input in enumerate(reshaped):
        outputs.append([])
        k,c,x,y = input.shape
        for ki in range(k):
            for yi in range(y):
                for xi in range(x):
                    for ci in range(c):
                        outputs[FM].append(input[ki][ci][yi][xi])
    return(outputs)

def weights(input_file, bottom = True):
    with open (input_file , 'r') as file:
        text = file.read().splitlines()
    Layers = []
    weight_shapes = []
    i=-1
    for line in text:
        if line[:7] == "WEIGHT_":

            weight_shape=(line[-14:-2])
            weight_shape = weight_shape.split(",")
            weight_shape = [int(num) for num in weight_shape]
            weight_shapes.append(weight_shape)
        if line == "WEIGHT":
            check = True
            i += 1
            Layers.append([])
        if line[:4] == "NAME":
            check = False

        if check == True:
            Layers[i].append(line)
    Layers_n = []
    for Layer in Layers:
        Layer = Layer[1:]
        Layer = [int(x) for x in Layer]
        Layers_n.append(Layer)
    reshaped = []
    for i, layer in enumerate(Layers_n) :
        Layer= np.reshape(layer, weight_shapes[i])
        reshaped.append(Layer)
    outputs = []
    for wi, Weight in enumerate(reshaped):
        outputs.append([])
        k,c,x,y = Weight.shape
        for ki in range(k):
            outputs[wi].append([])
            for yi in range(y):
                for xi in range(x):
                    for ci in range(c):
                        outputs[wi][ki].append(Weight[ki][ci][yi][xi])
                    for dummy in range(64 - c):
                        outputs[wi][ki].append(0)
        for xdummies in range (512-k):
            outputs[wi].append((576*[0]))
    print (np.sum(outputs[0][19]))
    if bottom:
        for io,output in enumerate(outputs):
            dummies = (1152-len(output[0]))*[0]
            for ik,k in enumerate(output):
                outputs[io][ik] = dummies + k
    
    return(outputs)

def gen_hdata_file(f_name, sdata, out_par, in_par, data_name,endian="little"):
    """gen_hdata_file(f_name, sdata, out_par, in_par, data_name)
        Generates 
        Parameters:
        f_name      (string): .../path/name of the output file
        sdata       (list)  : list of integers (UNSIGNED!) to be exported in the h file
        out_par     (int)   : single output data parallelism
        in_par      (int)   : single input data parallelism
        data_name   (string): name of the data array to be added to header file

        Returns:
        None
    """
    word_count= out_par//in_par
    with open(f_name,"w") as fout_p:
        fout_p.write(header_32_line.format(data_name)+"{\n")
    mega_string=""
    cycles = math.ceil(len(sdata)/word_count)
    for b in range(cycles):
        num = 0
        for c in range(word_count):
            if endian=="little":
                num += 2**(in_par*c)*sdata[b*word_count+c]
            elif endian=="big":
                num += 2**(in_par*(word_count-1-c))*sdata[b*word_count+c]
        mega_string += (hex(num)+",\n")
    with open(f_name,"a") as fout_p:
        fout_p.write(mega_string)
        fout_p.write(footer_line)

def tern_to_bin(w):
    if w==1:
        return 2
    elif w==-1:
        return 1
    else:
        return 0


def mirror_Y(w):
    wg = []
    for t in range(len(w)):
        w_t = []
        for r in range( len(w[0])-1, -1, -1):
            w_t.append(w[t][r])
        wg.append(w_t)
    return wg

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



#activ = activations("test.txt")[0]
#gen_hdata_file("C:/zedboard/Resnet20/C_program/data/input_memory_ania.h", activ, 32, 8, "input_ania",endian="big")

#weights("test.txt")[0]
#weight = mirror_Y(weight)
#weight = flip_weights(weight)
#weight = map_weights(weight)
#weight = flatten_list(weight)
#
#gen_hdata_file("C:/zedboard/Resnet20/C_program/data/weight_memory_cnn_ania.h", weight, 32, 1, "w_cnn_ania",endian="big")
#
#print("Generating im file...")
#ima = InstructionMemory(yaml_file="C:/zedboard/Resnet20/preprocess/instructionmemory.yaml", yaml_template="C:/zedboard/diana-sdk/diana_rf_metadata/ima_template.yaml")
#ima.print_hfile("C:/zedboard/Resnet20/C_program/data/instruction_memory_ania.h","im_ania")