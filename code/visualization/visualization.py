import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import seaborn as sns
import csv

def visualize(visualization_data, user_input, stability_score, amino_stability_x, amino_stability_y):
    x = []
    y = []
    colors = []

    print("VISUAL", amino_stability_x, amino_stability_y)

    # extracts amino acid x,y coordinates and determines corresponding colors
    with open(visualization_data,'r') as csvfile:
        plots = csv.reader(csvfile, delimiter=',')
        for row in plots:
            if row[0] == 'H':
                colors.append('red')
            else:
                colors.append('blue')
            x.append(int(row[1]))
            y.append(int(row[2]))


    # forces equal integer ticks
    ax = plt.figure().gca()
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    plt.axis('equal')

    # connects the amino acids
    plt.plot(x,y,'-', label='Folds')

    # stability score visualisatie
    for i in range(len(amino_stability_x)):
        plt.plot(amino_stability_x[i], amino_stability_y[i], ':', color='r')

    # assigns corresponding colors to individual amino acids
    for i in range(len(x)):
        plt.plot(x[i], y[i], 'o', color=colors[i])

    # draws a line between each point
    plt.grid(linestyle='-')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title('Protein: ' + user_input.upper() + '\nStability score: ' + str(stability_score))
    plt.legend()
    plt.show()