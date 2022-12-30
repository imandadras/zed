import os
import csv
import matplotlib.pyplot as plt
UTs=[]
paths = list(range(-62,64))
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

activations = []
for i, UT in enumerate(UTs):
    activations.append(sum(UT)/len(UT)) 
    plt.plot(UT, label = 'activation is {}'.format(paths[i]))
plt.xlabel("Column number")
plt.ylabel("Readout value")
plt.title("ACTIVATION = 5, UNIT TIME INDEX {} , Vcs_BIAS = 0.61")
plt.legend()
plt.grid(True)
plt.show()
Activ=[(Act/40) for Act in activations]
plt.plot (paths, Activ)
plt.xlabel("Input")
plt.ylabel("Output")
plt.title("UNIT TIME INDEX = 1 , Vcs_BIAS = 0.79")

plt.show()
print (activations)
    
