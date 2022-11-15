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
x = list(range(-62,64,1))
plot= []
for i, experiment in enumerate(experiments):
    plot.append(experiment[78])
plt.plot([x/100 for x in list(range(61, 76,1))] ,plot)
plt.title("Unit Time {}".format(unit_time))
plt.xlabel("Vcsbias")
plt.ylabel("Output for activation=30")
plt.legend()
plt.show()
    
