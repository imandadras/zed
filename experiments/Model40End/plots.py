import matplotlib.pyplot as plt
import json
output= []
with open ("Output_values_unnormal.json") as file:
    outputs = json.load(file, parse_float=None)
output = []

for Vcs in [x/100 for x in list(range(51,80))]:
        output.append(outputs[str(Vcs)]["1"][str(40)])
x = [x/100 for x in list(range(51,80))]
plt.plot(x , output)
plt.xlabel("Vcsb")
plt.ylabel("output")
plt.title("Output variation according to unit time index = 1")
plt.show()