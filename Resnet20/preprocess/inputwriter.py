import csv
import numpy as np
with open ("test.txt" , 'r') as file:
    text = file.read().splitlines()
Layers = []
output_shapes = []
i=-1
check = False
for line in text:
    if line[:8] == "IN_SHAPE":
        output_shape=(line[22:-2])
        output_shape = output_shape.split(",")
        print (output_shape)
        output_shape = [int(num) for num in output_shape]
        output_shapes.append(output_shape)
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
    Layer= np.reshape(layer, output_shapes[i])
    print (output_shapes[i])
    reshaped.append(Layer)
outputs = []
for FM, input in enumerate(reshaped):
    outputs.append([])
    k,c,x,y = input.shape
    print (k,c,x,y)
    for ki in range(k):
        for yi in range(y):
            for xi in range(x):
                for ci in range(c):
                    outputs[FM].append(input[ki][ci][yi][xi])

with open ("Activations.csv", 'w') as file:
    writer = csv.writer(file, delimiter= ',', )
    writer.writerows(reshaped)