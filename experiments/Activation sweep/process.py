import os
import csv
import matplotlib.pyplot as plt


unit_time = 9
experiments = []
paths = next(os.walk('.'))[1]
for path in paths:
    with open ('{}/table.csv'.format(path),) as file:
        results = csv.reader(file, delimiter=' ')
        res = [[float(i) for i in row] for row in results]

        experiments.append(res[unit_time])
x = list(range(-63,64,1))
for experiment in experiments:
    plt.plot(x, experiment)
plt.show()
    
