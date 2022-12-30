import numpy as np
import csv

def MAC (kernel , activation):
    return np.sum (np.multiply(kernel , activation))

def get_activation (file,L):
    with open (file , 'r') as file:
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

    return(np.squeeze(reshaped[L],axis=0))


def get_weights (file, L, bottom = False):
    with open (file , 'r') as file:
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
    return(reshaped[L])

def pad (activation,width=1):
    return (np.pad(activation, width))

def act_slicing(act, weight_shape, x,y):
    return act[:,y:y+weight_shape[2],x:x+weight_shape[3]]

def make_out_array (file, L):
    with open (file , 'r') as file:
        text = file.read().splitlines()
    output_shapes = []
    i=-1
    for line in text:
        if line[:8] == "OUT_SHAP":
            output_shape=(line[22:-2])
            output_shape = output_shape.split(",")
            output_shape = [int(num) for num in output_shape]
            output_shapes.append(output_shape)
    return (np.zeros(output_shapes[L][1:]))

def get_scale (file, L):
    with open (file , 'r') as file:
        text = file.read().splitlines()
    scales = []
    i=-1
    for line in text:
        if line[:5] == "SCALE":
            scale=(line[14:-2])
            scale = float(scale)
            scales.append(scale)  
    return(scales[L])

layer = 2
out = make_out_array("test.txt",layer)
act = get_activation("test.txt",layer)
weight = get_weights("test.txt",layer)
scale = get_scale("test.txt",layer)
weight_shape = weight.shape
print (act.shape)
act = pad(act, width=((0,0),(1,1),(1,1)))
print (act.shape)
print (out.shape[2])
for c in range (out.shape[0]):
    for y in range (out.shape[1]):
        for x in range (out.shape[2]):
            sliced = act_slicing(act, weight_shape=weight_shape, x=x, y=y)
            out[c,y,x] = MAC(weight[c],sliced)
out = out/scale
out = np.floor (out)
out = np.reshape(out,(1,-1))
with open ("outputL2.csv", 'w') as file:
    writer = csv.writer(file, delimiter= ',', )
    writer.writerows(out)