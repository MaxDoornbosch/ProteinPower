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

class BranchBound:
    """
    Branch and Bound algorithm that folds a given protein
    3 ^ (length of user input) times to find the best possible stability score.
    """

    def __init__(self, user_input):
        self.user_input = user_input

        # format: [amino acid, fold, x, y]
        first_amino = [[self.user_input[0], 2, 0, 0]]
        self.stack = []
        self.stack.append(first_amino)

        self.stability = Stability()

        self.best_score = 1
        self.best_protein = []

        self.average_score_per_depth = {}

        # average score for every depth starts at 0
        for i in range(1, (len(self.user_input))):
            self.average_score_per_depth[i] = list()


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


    def prepare_visualisation(self):
        """
        Creates needed lists for the visualisation of the final protein.
        """

        self.stability.stability_score_coordinates(self.stability_coordinates)
        self.amino_stability_x = self.stability.amino_stability_x
        self.amino_stability_y = self.stability.amino_stability_y


    def finish_protein(self, current_path):
        """
        Calculates final stability score for each protein, checks for new best
        scores and prepares data for the visualization of the final best protein
        folds.
        """

        score, stability_connections = self.stability.get_stability_score(current_path)

        # updates current best protein option
        if score < self.best_score:
            self.best_score = score
            self.best_protein = current_path
            self.stability_coordinates = stability_connections
            self.prepare_visualisation()


    def run(self):
        """
        Runs depth-first algorithm until all possible protein folds have between
        evaluated; determines best fold.
        """

        while self.stack:
            current_path = self.get_next_path()
            current_amino = current_path[-1][0]

            # calculates stability score for each protein
            if len(current_path) == len(self.user_input):
                self.finish_protein(current_path)

            # if the protein is not yet finished
            elif len(current_path) < len(self.user_input):
                score, stability_connections = self.stability.get_stability_score(current_path)
                average_score = self.average_score_thus_far(score, current_path)

                # keep all branches if score is same or better than best score
                if score < self.best_score:
                    self.best_score = score
                    self.add_new_options_to_stack(current_path)

                # if current score is worse than average score, prune 70%
                elif score > average_score:
                    r = random.uniform(0, 1)

                    if r > 0.7:
                        self.add_new_options_to_stack(current_path)

                # if current score is between the best and average score, prune 30%
                elif self.best_score < score < average_score:
                    r = random.uniform(0, 1)

                    if r > 0.3:
                        self.add_new_options_to_stack(current_path)

                # always create new options if score hasn't changed or amino is a P amino
                self.add_new_options_to_stack(current_path)
