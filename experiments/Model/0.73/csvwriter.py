import os
import csv
experiments = []
number_rows = 6
paths = next(os.walk('.'))[1]
activations_n=[int(path[:-2]) for path in paths]
for path in paths:
    UTs= []
    for i in range (10):
        with open ('{}/{}.csv'.format(path, i),'r') as file:
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
        decimal = [(ex-256)/number_rows if ex>32 else ex/number_rows for ex in decimal]
        UTs.append(sum(decimal)/len(decimal))
    experiments.append(UTs)

zipped = list(zip(activations_n,experiments))
zipped.sort(key=lambda tup: tup[0])
experiments = [tup[1] for tup in zipped]
activations_n = [tup[0] for tup in zipped]
experiments=[list(i) for i in zip(*experiments)]
with open ("table.csv" , 'w', newline="") as file:
    table = csv.writer (file, delimiter= " ")
    table.writerows(experiments)