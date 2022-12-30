import csv
import numpy as np
with open ("test.txt" , 'r') as file:
    text = file.read().splitlines()
Layers = []
output_shapes = []
i=-1
check = False
for line in text:
    if line[:8] == "OUT_SHAP":
        output_shape=(line[22:-2])
        output_shape = output_shape.split(",")
        output_shape = [int(num) for num in output_shape]
        output_shapes.append(output_shape)
    if line == "OUTPUT":
        check = True
        i += 1
        Layers.append([])
    if line == "WEIGHT":
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
        for ci in range(c):
            for yi in range(y):
                for xi in range(x):
                    outputs[FM].append(input[ki][ci][yi][xi])

with open ("outputsL2.csv", 'w') as file:
    writer = csv.writer(file, delimiter= ',', )
    writer.writerow(outputs[1])