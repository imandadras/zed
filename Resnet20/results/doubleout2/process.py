import os
import csv
import matplotlib.pyplot as plt
UTs=[]
paths = next(os.walk('.'))[1]
#activations_n=[float(path) for path in paths]
for path in paths:
    with open ('{}/1.csv'.format(path),) as file:
        results = csv.reader(file, delimiter='\t')

        res = [row for row in results]
    for row in res:
        del row[0]
    res = [i for row in res for i in row]
    decimal = []
    for r in res:
        decimal.append(int(r[-8:-6] , base=16))
        decimal.append(int(r[-6:-4] , base=16))
        decimal.append(int(r[-4:-2] , base=16))
        decimal.append(int(r[-2:  ] , base=16))
    decimal = [ex-256 if ex>128 else ex for ex in decimal]      
    UTs.append(decimal)

zipped = list(zip(paths,UTs))
#print (zipped)
zipped.sort(key=lambda tup: tup[0])
UTs = [tup[1] for tup in zipped]
activations_n = [tup[0] for tup in zipped]
activations = []
with open ("outputL0.csv", 'r') as file:
    reader = csv.reader(file, delimiter=",")
    output = list(reader)
print (output)
output = [float(out) for out in output[0]]
for i, UT in enumerate(UTs):    
    plt.plot(UT, label = 'activation is {}'.format(activations_n[i]))
plt.plot(output, label = 'output', linewidth = 2)
plt.xlabel("Column number")
plt.ylabel("Readout value")
plt.title("ACTIVATION = 1, UNIT TIME INDEX {} , Vcs_BIAS = 0.61")
plt.legend()
plt.grid(True)
plt.show()
#plt.plot (activations_n, activations)
#plt.show()
#print (activations)
    
