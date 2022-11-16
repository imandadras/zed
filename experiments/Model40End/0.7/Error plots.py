import os
import csv
import matplotlib.pyplot as plt
from scipy import stats
N_rows = 1
paths = next(os.walk('.'))[1]
activations_n=list(range(-62,64))
experiments = []
normalizers = []
xp = 20
xm = -20
for unit_time in range (0,10):
    UTs=[]
    for i in range(-62,64):
        with open ('{}/{}.csv'.format(i, unit_time),'r') as file:
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
        average =  sum(decimal)/len(decimal)

        #if i == xm:
        #    ym = average
        #if i == xp:
        #    yp = average  
        UTs.append(average)
    #m = (yp - ym)/ (xp - xm)
    #c = ((xp * ym)-(xm*yp))/ (xp - xm)
    last_point = next((x[0] for x in enumerate(UTs) if x[1]>30), 124)
    first_point = next((x[0] for x in enumerate(UTs) if x[1]>-30), 0)
    print (last_point, first_point)
    m , c, r, p ,std_err = stats.linregress (activations_n[first_point:last_point], UTs[first_point:last_point])
    print (m,c)
    normalizer = [(point*m)+c for point in activations_n]
    for i, normal in enumerate(normalizer):
        UTs[i]= UTs[i] - normal
    normalizers.append(normalizer)
    experiments.append(UTs)

experiments = [[x/N_rows for x in experiment] for experiment in experiments]
activations = []
xticks= list(range(-62,64,1))
for i, UT in enumerate(experiments):
    plt.plot(normalizers[i], UT, label = 'Unit time is {}'.format(i))
    #plt.plot(xticks, normalizers[i], label = 'Unit time is {}'.format(i))

plt.xlabel("Input Value")
plt.ylabel("Readout Value")
plt.title("Rows 0 to 19 with different activation and unit time values and weight=0")
plt.legend()
plt.grid(True)
plt.show()

