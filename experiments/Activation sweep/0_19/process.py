import os
import csv
import matplotlib.pyplot as plt
UTs=[]
paths = next(os.walk('.'))[1]
activations_n=[int(path[5:-2]) for path in paths]
for path in paths:
    with open ('{}/7.csv'.format(path),) as file:
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
plt.plot (activations_n,activations, label= "rows 0 to 19")
plt.plot(activations_n,[-7.986328125, -29.533203125, -29.455078125, -29.556640625, -29.517578125, -29.33203125, -29.40234375, -29.09765625, -28.822265625, -28.5, -28.13671875, -27.62109375, -26.603515625, -25.921875, -25.34375, -25.015625, -24.744140625, -24.279296875, -23.94140625, -23.541015625, -22.921875, -22.17578125, -21.23046875, -20.458984375, -20.099609375, -19.974609375, -19.796875, -19.154296875, -18.208984375, -17.71484375, -17.150390625, -16.94921875, -16.599609375, -16.193359375, -15.814453125, -15.265625, -14.73046875, -13.712890625, -13.111328125, -12.98046875, -12.796875, -12.3046875, -11.791015625, -10.85546875, -9.99609375, -9.369140625, -8.720703125, -8.119140625, -8.0, -7.982421875, -7.646484375, -7.0859375, -6.28515625, -5.25, -4.669921875, -4.099609375, -4.0, -3.958984375, -3.310546875, -2.1953125, -1.74609375, -1.10546875, -0.986328125, -0.23828125, -0.017578125, 0.046875, 0.529296875, 1.04296875, 1.990234375, 2.875, 2.99609375, 3.04296875, 3.4921875, 4.046875, 4.9921875, 5.9296875, 6.474609375, 6.939453125, 7.0, 7.056640625, 7.484375, 8.1640625, 8.84765625, 9.498046875, 10.564453125, 11.146484375, 11.74609375, 11.953125, 12.005859375, 12.466796875, 13.478515625, 14.1328125, 14.666015625, 15.0625, 15.552734375, 15.91796875, 16.09375, 16.513671875, 17.080078125, 17.953125, 18.71875, 18.970703125, 19.072265625, 19.3125, 20.099609375, 20.9765625, 21.79296875, 22.33203125, 22.80859375, 23.107421875, 23.5078125, 23.869140625, 24.142578125, 24.59375, 25.267578125, 25.998046875, 26.822265625, 27.228515625, 27.65625, 27.912109375, 28.220703125, 28.51171875, 28.521484375, 28.517578125, 28.615234375, 28.490234375, 28.501953125], label= "rows 20 to 39")
plt.plot(activations_n,[-7.982421875, -29.228515625, -29.23828125, -29.205078125, -29.2421875, -29.236328125, -29.146484375, -29.00390625, -28.67578125, -28.3125, -27.857421875, -27.1328125, -26.3046875, -25.64453125, -25.21875, -24.86328125, -24.603515625, -24.201171875, -23.869140625, -23.365234375, -22.732421875, -21.845703125, -20.931640625, -20.3125, -20.03125, -19.94921875, -19.68359375, -18.8203125, -18.052734375, -17.505859375, -17.07421875, -16.90625, -16.564453125, -16.083984375, -15.71875, -15.14453125, -14.50390625, -16.529296875, -16.02734375, -15.49609375, -14.841796875, -13.931640625, -13.091796875, -12.958984375, -12.52734375, -11.982421875, -10.890625, -9.94921875, -9.263671875, -8.501953125, -8.0234375, -7.9921875, -7.681640625, -7.033203125, -5.962890625, -4.94921875, -4.2734375, -4.00390625, -3.96484375, -3.091796875, -2.017578125, -1.375, -1.005859375, -0.232421875, -0.009765625, 0.14453125, 0.810546875, 1.556640625, 2.818359375, 3.0, 3.1171875, 3.705078125, 4.46875, 5.791015625, 6.4375, 6.94921875, 7.0, 7.265625, 7.998046875, 8.740234375, 9.53515625, 10.765625, 11.353515625, 11.8984375, 12.017578125, 12.529296875, 13.669921875, 14.28125, 14.890625, 15.359375, 15.8671875, 16.126953125, 16.736328125, 17.400390625, 18.552734375, 18.9453125, 19.05859375, 19.462890625, 20.3984375, 21.46484375, 22.291015625, 22.845703125, 23.25390625, 23.662109375, 24.0703125, 24.580078125, 25.26953125, 26.265625, 26.9453125, 27.5078125, 27.85546875, 28.20703125, 28.859375, 29.70703125, 30.396484375, 30.802734375, 30.97265625, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0, 31.0], label="39 to 59")

plt.title("DIANA output value for different input activations")
plt.legend()
plt.show()
    
