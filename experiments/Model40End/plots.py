import matplotlib.pyplot as plt
import json
output= []
with open ("Output_values_unnormal.json") as file:
    outputs = json.load(file, parse_float=None)
for unit_time in range(0,10):
    output = []
    for act in range(-62,64):
        output.append(outputs["0.65"][str(unit_time)][str(act)])
    x = list(range(-62,64))
    plt.plot(x , output)
plt.show()