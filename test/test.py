import matplotlib.pyplot as plt

# data
personnel = ['Scientists', 'Engineers', 'Managers']
phd = [20, 0, 0]
count = [50, 20, 8]
phd = [20, 0, 2]

# create the bar chart
plt.bar(personnel, phd, bottom=count, color='b', edgecolor='k',label= "Ph.D. holders")
plt.bar(personnel, count, color='r', edgecolor='k')
plt.legend()

# show the chart
plt.show()