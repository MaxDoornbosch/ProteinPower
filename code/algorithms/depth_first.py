"""
depth_first.py

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020

"""

from classes.protein import Protein
from classes.coordinateupdate import CoordinateUpdate
from classes.possible_options import PossibleOptions
from classes.csvwriter import Csv


import copy
import random
from timeit import default_timer as timer


import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd
import seaborn as sns
import csv

class DepthFirst:
    """
    Depth first search algorithm that folds a given protein
    3 ^ (length of user input) times to find the best possible stability score.
    """

    def __init__(self, user_input):

        self.user_input = user_input

        # format: [amino, fold, x, y]
        first_amino = [[self.user_input[0], 2, 0, 0]]
        self.stack = []
        self.stack.append(first_amino)

        self.best_score = 1


    def get_next_path(self):
        """
        Gets the current path out of the stack of paths: the (partial) protein with
        corresponding information (fold and x,y coordinates).
        """

        current_path = self.stack.pop()
        return current_path


    def stability(self, current_path):
        """
        Calculates stability score of protein.
        """

        # finds coordinates of C and H amino acids
        self.coordinates_of_C_H_aminos(current_path)

        score = 0
        i = 0
        stability_connections = []

        for amino in current_path:
            if amino[0] == "H" or amino[0] == "C":
                surrounding_coordinates, x, y = self.surrounding_coordinates(amino, current_path, i)

                # checks and calculates score
                for coordinates in surrounding_coordinates:
                    potential_connection = [coordinates, [x, y]]

                    # ensures stability connections aren't calculated twice
                    score, stability_connections = self.calculate_score(amino, stability_connections, potential_connection, coordinates, score)

            i += 1

        return score, stability_connections


    def surrounding_coordinates(self, amino, current_path, i):
        """
        Returns surrounding coordinates of a given amino acid, whilst excluding
        the coordinates of connected amino acids.
        """

        x = amino[2]
        y = amino[3]
        surrounding_coordinates = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]

        if amino != current_path[0]:
            connected_x = current_path[i - 1][2]
            connected_y = current_path[i - 1][3]
            surrounding_coordinates.remove([connected_x, connected_y])

        if amino != current_path[-1]:
            connected_x = current_path[i + 1][2]
            connected_y = current_path[i + 1][3]
            surrounding_coordinates.remove([connected_x, connected_y])

        return surrounding_coordinates, x, y


    def calculate_score(self, amino, stability_connections, potential_connection, coordinates, score):
        """
        Calculates score and ensures stability connections aren't calculated twice.
        """

        if self.already_calculated(stability_connections, potential_connection, score):
            return score, stability_connections

        if amino[0] == "H":
            if coordinates in self.h_coordinates or coordinates in self.c_coordinates:
                score -= 1
                stability_connections.append(potential_connection)

        elif amino[0] == "C":
            if coordinates in self.h_coordinates:
                score -= 1
                stability_connections.append(potential_connection)
            elif coordinates in self.c_coordinates:
                score -= 5
                stability_connections.append(potential_connection)

        return score, stability_connections


    def already_calculated(self, stability_connections, potential_connection, score):
        """
        True if stability between two amino acids was already calculated.
        """

        if stability_connections:
            for connection in stability_connections:
                if sorted(connection) == sorted(potential_connection):
                    return True

        return False


    def coordinates_of_C_H_aminos(self, current_path):
        """
        Extracts coordinates of all H and C aminos from current path.
        """
        self.h_coordinates = []
        self.c_coordinates = []

        for path in current_path:
            if path[0] == "H" and [path[2], path[3]] not in self.h_coordinates:
                self.h_coordinates.append([path[2], path[3]])
            elif path[0] == "C" and [path[2], path[3]] not in self.c_coordinates:
                self.c_coordinates.append([path[2], path[3]])


    def add_new_options_to_stack(self, current_path):
        """
        Determines possible options for every amino acid and appends them to stack.
        """

        possible = PossibleOptions(self.user_input)
        coordinate_update = CoordinateUpdate()

        # update coordinates for next amino based on current fold
        current_x, current_y = coordinate_update.update_coordinates_path(current_path)

        possible.define_folds(current_path)
        possible.define_coordinates(current_x, current_y)
        final_possible_options = possible.check_empty()

        for option in final_possible_options:
            new_path = copy.deepcopy(current_path)
            new_path.append(option)

            if new_path not in self.stack:
                self.stack.append(new_path)


    def run(self):
        """
        Runs depth-first algorithm until all possible protein folds have between
        evaluated; determines best fold.
        """

        while self.stack:
            current_path = self.get_next_path()

            # calculates stability score for each protein
            if len(current_path) == len(self.user_input):
                score, stability_connections = self.stability(current_path)

                if score < self.best_score:
                    self.stability_coordinates = stability_connections
                    self.best_score = score
                    self.best_protein = current_path

            # creates new options if protein is not yet finished
            else:
                self.add_new_options_to_stack(current_path)


        self.stability_score_coordinates(self.stability_coordinates)


    def stability_score_coordinates(self, stability_coordinates):
        """
        Creates coordinate lists for the visualisation of the stability score.
        """

        self.amino_stability_x = []
        self.amino_stability_y = []

        for i in stability_coordinates:
            self.amino_stability_x.append([i[0][0], i[1][0]])
            self.amino_stability_y.append([i[0][1], i[1][1]])


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
            elif row[0] == "C":
                colors.append('green')
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



"""
MAIN.PY
"""

user_input = input("Please enter your protein (minimum length is 3): ").upper()

# minimum length of protein
while len(user_input) < 3:
    user_input = input("Please enter your protein (minimum length is 3): ").upper()

# checks if user_input is valid
for i in range(len(user_input)):
    while user_input[i] != "H" and user_input[i] != "P" and user_input[i] !="C":
        user_input = input("Please enter your protein (minimum length is 3): ").upper()






"""
Initialization for main.py
"""

depth = DepthFirst(user_input)

try:
    depth.run()
except (KeyboardInterrupt, SystemExit):
    print("\nKeyboard Interrupt.\n")


if depth.best_score == 0:
    print("\nLowest score: 0")
else:
    print("\nLowest score: ", depth.best_score)
    print("\nBest protein: ", depth.best_protein)



# csvwriter = Csv(depth.best_protein)
# csvwriter.write_csv()
# csvwriter.visualization_csv()
#
# visualize('data/visualization.csv', user_input, depth.best_score, depth.amino_stability_x, depth.amino_stability_y)
