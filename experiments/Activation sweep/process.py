import os
import csv
import matplotlib.pyplot as plt


unit_time = 1
experiments = []
paths = next(os.walk('.'))[1]
for path in paths:
    with open ('{}/table.csv'.format(path),) as file:
        results = csv.reader(file, delimiter=' ')
        res = [[float(i) for i in row] for row in results]

        experiments.append(res[unit_time])
x = list(range(-63,64,1))
for i, experiment in enumerate(experiments):
    plt.plot(x, experiment, label=paths[i])
plt.title("Unit Time {}".format(unit_time))
plt.xlabel("Input")
plt.ylabel("Output")
plt.legend()
plt.show()
    
