def inputs(input_file):
    import numpy as np
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
    print (len(Layers_n))
    print (len(input_shapes))
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