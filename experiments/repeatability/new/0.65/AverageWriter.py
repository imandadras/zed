import os
import csv
import json
test_out ={}
rows_n=1
test_n =list(range(10))
UT = list(range(0,10))
actvation = list(range(-62,64))
for test in test_n:
    UT_out = {}
    for Unit_time in UT:
        actvation_out = {}
        for act in actvation:
            with open ('{}/{}/{}.csv'.format(test,act,Unit_time),'r') as file:
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
    test_out[test] = UT_out
with open('output_values_unnormal.json', 'w') as model:
    json.dump(test_out, model)