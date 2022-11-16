import os
import csv
import json
Vcs_out ={}
rows_n=1
Vcs = [V/100 for V in list(range(51,81))]
UT = list(range(0,10))
actvation = list(range(-62,64))
for V in Vcs:
    UT_out = {}
    for Unit_time in UT:
        actvation_out = {}
        for act in actvation:
            with open ('{}/{}/{}.csv'.format(V,act,Unit_time),'r') as file:
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
            average = sum(decimal)/len(decimal)
            normalized = average/rows_n
            actvation_out[act] = normalized
        UT_out[Unit_time] = actvation_out
    Vcs_out[V] = UT_out
with open('output_values_unnormal.json', 'w') as model:
    json.dump(Vcs_out, model)