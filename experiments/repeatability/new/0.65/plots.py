import matplotlib.pyplot as plt
import json
output= []
with open ("Output_values_unnormal.json") as file:
    outputs = json.load(file, parse_float=None)

for test in range(10):
    for unit_time in range(10):
        output=[]
        for activation in range(-62,64):

            output.append(outputs[str(test)][str(unit_time)][str(activation)])
        plt.plot(list(range(-62,64)),output)
plt.title("Experiment repeatability on the same row")
plt.xlabel("Activation")
plt.ylabel("Output")
plt.show()