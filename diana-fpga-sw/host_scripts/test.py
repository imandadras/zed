l1 =[2,5,7]
l2=['a', 'b', 'c']

dic = {x[1]:l1[x[0]] for x in enumerate (l2)}
print (str(dic))