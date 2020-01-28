"""
depth_first.py

A depth first search algorithm for choosing the best folds that produce the
lowest stability score for a given protein. This algorithm defines all the
possible folds and calculates every possible stability score in order to
return the best possible solution.

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor programmeren
2020
"""

from code.classes.protein import Protein
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.possible_options import PossibleOptions
from code.classes.csvwriter import Csv
from code.classes.stability_score import Stability

from code.helper.depth_first import finish_protein

import copy


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

        self.stability = Stability()
        self.possible = PossibleOptions(user_input)
        self.coordinate_update = CoordinateUpdate()


    def get_next_path(self, stack):
        """
        Gets the current path out of the stack of paths: the (partial) protein with
        corresponding information (fold and x,y coordinates).
        """

        current_path = stack.pop()
        return current_path, stack


    def add_new_options_to_stack(self, current_path):
        """
        Determines possible options for every amino acid and appends them to stack.
        """

        # updates coordinates for next amino based on current fold
        current_x, current_y = self.coordinate_update.update_coordinates(current_path)

        # finds possible options
        self.possible.define_folds(current_path)
        self.possible.define_coordinates(current_x, current_y)
        final_possible_options = self.possible.check_empty()

        # adds new option to stack if not appended already
        for option in final_possible_options:
            new_option = copy.deepcopy(current_path)
            new_option.append(option)

            if new_option not in self.stack:
                self.stack.append(new_option)


    def run(self):
        """
        Runs depth-first algorithm until all possible protein folds have between
        evaluated; determines best fold.
        """

        self.best_score = 1

        while self.stack:
            current_path = self.get_next_path()

            # calculates stability score for each protein
            if len(current_path) == len(self.user_input):
                score, stability_connections = self.stability.get_stability_score(current_path)

                # updates current best protein option
                if score < self.best_score:
                    self.best_score = score
                    self.best_protein = current_path
                    self.amino_stability_x, self.amino_stability_y = finish_protein(score, stability_connections)

            # creates new options if protein is not yet finished
            else:
                self.add_new_options_to_stack(current_path)
