"""
branch_bound.py

A branch and bound algorithm for choosing the best folds that produce the
lowest stability score for a given protein.

Using depth first search, this algorithm is inspired by Mao Chen and Wen-Qi
Huang's paper "A Branch and Bound Algorithm for the Protein Folding Problem in
the HP Lattice Model" (2005). This program keeps track of the best score
(the constantly updated lower bound) and average score for the protein on every
depth. If a fold produces a higher (worse) score than the average score of all
folds of that specific depth, there is a 70% chance of that branch being pruned
off immediately. If the score of a specific fold is between the best score and
the average score, there is a 30% chance of that branch
being pruned off, as this branch is quite promising but for time's sake, some
will be pruned. Chen and Huang suggest 80% (instead of 70%) and 50% (instead
of 30%) chance of pruning, but we have found that the inclusion of more branches
does not have a significant negative effect on the runtime of this algorithm,
but will produce more accurate results.

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
import random


class BranchBound:
    """
    Branch and Bound algorithm that folds a given protein
    3 ^ (length of user input) times to find the best possible stability score.
    """

    def __init__(self, user_input, runamount):
        self.user_input = user_input
        self.runamount = runamount
        self.very_best_score = 1

    def average_score_thus_far(self, score, current_path):
        """
        Returns the updated average score of given depth.
        """

        # calculates new average
        self.average_score_per_depth[len(current_path)].append(score)
        sum = 0
        for old_score in self.average_score_per_depth[len(current_path)]:
            sum += old_score

        average_score = sum / len(self.average_score_per_depth[len(current_path)])
        return average_score


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

        # runs the program x times depending on the runamount
        for z in range(self.runamount):

            done = False
            self.best_score = 1

            # format: [amino acid, fold, x, y]
            first_amino = [[self.user_input[0], 2, 0, 0]]
            self.stack = []
            self.stack.append(first_amino)

            self.stability = Stability()
            self.average_score_per_depth = {}

            # average score for every depth starts at 0
            for i in range(1, (len(self.user_input))):
                self.average_score_per_depth[i] = list()

            # restarts the program if an error occurs
            while done == False:

                while self.stack:
                    print(len(self.stack))
                    current_path = self.get_next_path()
                    current_amino = current_path[-1][0]

                    # calculates stability score for each protein
                    if len(current_path) == len(self.user_input):
                        score, stability_connections = self.stability.get_stability_score(current_path)


                    # if the protein is not yet finished
                    else:
                        score, stability_connections = self.stability.get_stability_score(current_path)
                        average_score = self.average_score_thus_far(score, current_path)

                        # keep all branches if score is same or better than best score
                        if score < self.best_score:
                            self.best_score = score
                            self.best_protein = current_path
                            self.add_new_options_to_stack(current_path)
                            self.amino_stability_x, self.amino_stability_y = finish_protein(score, stability_connections)

                        # if current score is worse than average score, prune 70%
                        elif score > average_score:
                            if random.uniform(0, 1) > 0.9:
                                self.add_new_options_to_stack(current_path)

                        # if current score is between the best and average score, prune 30%
                        elif self.best_score < score < average_score:
                            if random.uniform(0, 1) > 0.6:
                                self.add_new_options_to_stack(current_path)

                        # always create new options if score hasn't changed or amino is a P amino
                        else:
                            self.add_new_options_to_stack(current_path)

                if self.best_score < self.very_best_score:
                    self.very_best_score = self.best_score
                    self.very_best_protein = self.best_protein

                if z == 99 or z == 199 or z == 299 or z == 399 or z == 499 or z == 599 or z == 699 or z == 799 or z == 899 or z == 999:
                    print("Score: ", self.best_score)

                done = True
