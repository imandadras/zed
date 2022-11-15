import os
import csv
import matplotlib.pyplot as plt
Vcsbias = 0.60
Vcsbias = (int((Vcsbias - 0.6)*100))
Unit_time = 9

Vcsbias2 = 0.75
Vcsbias2 = int((Vcsbias2 - 0.6)*100)
Unit_time2 = 3


experiments = []
paths = next(os.walk('.'))[1]
for path in paths:
    with open ('{}/table.csv'.format(path),) as file:
        results = csv.reader(file, delimiter=' ')
        res = [[float(i) for i in row] for row in results]

        experiments.append(res)
x = list(range(-62,64,1))
plt.plot(x, experiments[Vcsbias][Unit_time], label="{} {}".format(paths[Vcsbias], Unit_time))
plt.plot(x, experiments[Vcsbias2][Unit_time2], label="{} {}".format(paths[Vcsbias2], Unit_time2))

plt.title("Unit Time {}".format(Unit_time))
plt.xlabel("Input")
plt.ylabel("Output")
plt.legend()
plt.show()
    
