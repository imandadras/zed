import csv
import matplotlib.pyplot as plt

UTs = []
for UT in range (10):
    with open('{}.csv'.format(UT) , 'r') as file:
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

    devide = int(len(decimal)/512)

    diff = 0
    experiments = []
    for d in range(devide):
        experiments.append(decimal[d*512:(d+1)*512])
    """print ("One and two")
    for i , j in enumerate (experiments[0]):
        if j > experiments[1][i]:
            print ("{} and {}".format(j, experiments[1][i]))
    print ("Two and three")
    for i , j in enumerate (experiments[1]):
        if j > experiments[2][i]:
            print ("{} and {}".format(j, experiments[2][i]))
    print ("three and four")
    for i , j in enumerate (experiments[2]):
        if j < experiments[3][i]:
            print ("{} and {}".format(j, experiments[3][i]))
    """
    #print ("index {} is different, {} against {} against {} against {} ".format(i, j, experiments[1][i], experiments[2][i], experiments[3][i]))
    experiments = [[0 if ex==255 else ex for ex in experiment] for experiment in experiments]        
    """for i, experiment in enumerate(experiments):
        for j, output in enumerate (experiment):
            if output !=0:
                print (output, i, j )"""

    averages = [sum(experiment)/len(experiment) for experiment in experiments]
    UTs.append(averages)






x = [100 , 200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1152]
for i, UT in enumerate(UTs): 
    plt.plot(x, UT, label = 'unit time is index is: {}'.format(i))
plt.xlabel("Number of activated rows")
plt.ylabel("Readout value")
plt.title("bottom, 5, 0, 0.6")
plt.legend()
plt.show()
    
#print (len(decimal))