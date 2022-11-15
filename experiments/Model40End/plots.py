import matplotlib.pyplot as plt
import json

with open ("Output_values.json") as file:
    outputs = json.load(file, parse_float=None)
V = []
output = []
for Vcs in outputs.keys():
    
        V.append(float(Vcs))
        output.append(outputs[Vcs]["9"]["63"])
print (V)
plt.plot(V , output)
plt.show()