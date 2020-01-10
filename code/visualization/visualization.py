import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

import numpy as np
import pandas as pd
import seaborn as sns
import csv

x = []
y = []
colors = []

# extracts amino acid x,y coordinates and determines corresponding colors
with open('example.txt','r') as csvfile:
    plots = csv.reader(csvfile, delimiter=',')
    for row in plots:
        x.append(int(row[0]))
        y.append(int(row[1]))
        print(row[2])
        if row[2] == 'H':
            colors.append('red')
        else:
            colors.append('blue')

# forces equal integer ticks
ax = plt.figure().gca()
ax.xaxis.set_major_locator(MaxNLocator(integer=True))
ax.yaxis.set_major_locator(MaxNLocator(integer=True))
plt.axis('equal')

# connects the amino acids
plt.plot(x,y,'-')

# assigns corresponding colors to individual amino acids
for i in range(len(x)):
    plt.plot(x[i], y[i], 'o', color=colors[i])
plt.plot(x,y,'-')

# draw a line between each point
plt.grid(linestyle='-')
plt.xlabel('x')
plt.ylabel('y')
plt.title('Protein\nHHHPPPPHHH')
plt.legend()
plt.show()
