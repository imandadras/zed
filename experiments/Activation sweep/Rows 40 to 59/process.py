import os
import csv
import matplotlib.pyplot as plt
UTs=[]
paths = next(os.walk('.'))[1]
activations_n=[int(path[5:-2]) for path in paths]
for path in paths:
    with open ('{}/1.csv'.format(path),) as file:
        results = csv.reader(file, delimiter='\t')

        res = [row for row in results]
        del res[32:]
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
    UTs.append(decimal)

zipped = list(zip(activations_n,UTs))
print (zipped)
zipped.sort(key=lambda tup: tup[0])
UTs = [tup[1] for tup in zipped]
activations_n = [tup[0] for tup in zipped]
activations = []
for i, UT in enumerate(UTs):
    activations.append(sum(UT)/len(UT)) 
    plt.plot(UT, label = 'activation is {}'.format(activations_n[i]))
plt.xlabel("Column number")
plt.ylabel("Readout value")
plt.title("ACTIVATION = 5, UNIT TIME INDEX {} , Vcs_BIAS = 0.61")
plt.legend()
plt.grid(True)
plt.show()
plt.plot (activations_n, activations)
plt.show()
print (activations)
    
