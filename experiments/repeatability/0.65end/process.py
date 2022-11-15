import os
import csv
import matplotlib.pyplot as plt
N_rows = 10
paths = next(os.walk('.'))[1]
activations_n=[int(path[:-2]) for path in paths]
experiments = []
unit_time = 9
for test in range (3):
    UTs=[]
    for path in paths:
        with open ('{}/{}.csv'.format(path, unit_time),) as file:
            results = csv.reader(file, delimiter='\t')
            res = [row for row in results]
            res = res [test*32 : (test+1)*32]
        for row in res:
            del row[0]
        res = [i for row in res for i in row]
        decimal = []
        for r in res:
            decimal.append(int(r[-8:-6] , base=16))
            decimal.append(int(r[-6:-4] , base=16))
            decimal.append(int(r[-4:-2] , base=16))
            decimal.append(int(r[-2:  ] , base=16))
        decimal = [ex-256 if ex>32 else ex for ex in decimal]  
        if test == 0 :
            decimal = [d*(1.65) for d in decimal]
        UTs.append(sum(decimal)/len(decimal))
    zipped = list(zip(activations_n,UTs))
    zipped.sort(key=lambda tup: tup[0])
    UTs = [tup[1] for tup in zipped]    
    experiments.append(UTs)

activations_n = [tup[0] for tup in zipped]
experiments = [[x/N_rows for x in experiment] for experiment in experiments]
activations = []
xticks= list(range(-62,64,1))
for i, UT in enumerate(experiments):
    plt.plot( UT, label = 'Unit time is {}'.format(i))
plt.xlabel("Input Value")
plt.ylabel("Readout Value")
plt.title("Rows 0 to 19 with different activation and unit time values and weight=0")
plt.legend()
plt.grid(True)
plt.show()

