"""
depth_first.py

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020

"""

from code.classes.protein import Protein
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.possible_options import PossibleOptions
from code.classes.csvwriter import Csv
from code.classes.stability_score import Stability


import copy
import random

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

        self.stability = Stability()


    def get_next_path(self):
        """
        Gets the current path out of the stack of paths: the (partial) protein with
        corresponding information (fold and x,y coordinates).
        """

        current_path = self.stack.pop()
        return current_path

    def add_new_options_to_stack(self, current_path):
        """
        Determines possible options for every amino acid and appends them to stack.
        """

        possible = PossibleOptions(self.user_input)
        coordinate_update = CoordinateUpdate()

        # update coordinates for next amino based on current fold
        current_x, current_y = coordinate_update.update_coordinates(current_path)

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
                score, stability_connections = self.stability.get_stability_score(current_path)

                if score < self.best_score:
                    self.stability_coordinates = stability_connections
                    self.best_score = score
                    self.best_protein = current_path

            # creates new options if protein is not yet finished
            else:
                self.add_new_options_to_stack(current_path)

        self.stability.stability_score_coordinates(self.stability_coordinates)
        self.amino_stability_x = self.stability.amino_stability_x
        self.amino_stability_y = self.stability.amino_stability_y
