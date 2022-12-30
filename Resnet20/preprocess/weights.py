def weights(input_file, bottom = True):
    import numpy as np
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
    print (len(Layers_n))
    print (len(weight_shapes))
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
    if bottom:
        for io,output in enumerate(outputs):
            dummies = (1152-len(output[0]))*[0]
            for ik,k in enumerate(output):
                outputs[io][ik] = dummies + k
                print (len(k))
    
    return(outputs)


