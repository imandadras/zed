import json
from scipy import stats

with open ("Output_values.json") as file:
    outputs = json.load(file, parse_float=None)
activations_n = list(range(-62,64))
scale = {}

for Vcs in outputs.keys():
    for unit_time in outputs[Vcs].keys():
        output = []
        for activation in outputs[Vcs][unit_time].keys():
            output.append(outputs[Vcs][unit_time][activation])
        last_point = next((x[0] for x in enumerate(output) if x[1]>20), 124)
        first_point = next((x[0] for x in enumerate(output) if x[1]>-20), 0)
        m , c, r, p ,std_err = stats.linregress (activations_n[first_point:last_point], output[first_point:last_point])
        scale[m]=(float(Vcs), int(unit_time) , c)

with open('scales.json', 'w') as scales:
    json.dump(scale, scales)