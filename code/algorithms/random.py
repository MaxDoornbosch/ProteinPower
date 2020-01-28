"""
random.py

Random search algorithm: determines random (legal) folds for a given protein.

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020
"""

from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.protein import Protein
from code.classes.stability_score import Stability
from code.classes.possible_options import PossibleOptions


from code.helper.depth_first import finish_protein


import random


class Random:
    """
    Returns a random solution to the protein folding problem.
    """

    def __init__(self, user_input, runamount):
        self.user_input = user_input
        self.runamount = runamount

    def run(self):
        """
        Runs random algorithm as many times as the user indicated.
        """

        self.best_score = 1

        # repeat n many times
        for i in range(self.runamount):

            self.protein = Protein(self.user_input)
            self.final_placement = self.protein.final_placement
            self.stability = Stability()
            self.coordinate_update = CoordinateUpdate()
            self.possible = PossibleOptions(self.user_input)

            # while protein not yet finished
            while len(self.final_placement) < len(self.user_input):

                # determine current values
                current_x, current_y = self.coordinate_update.update_coordinates(self.final_placement)

                # finds possible options
                self.possible.define_folds(self.final_placement)
                self.possible.define_coordinates(current_x, current_y)
                final_possible_options = self.possible.check_empty()

                # starts all over if there are no possible options
                if not final_possible_options:
                    self.runamount += 1
                    break

                else:
                    self.random_amino = random.choice(final_possible_options)
                    self.protein.add_amino_info(self.random_amino)


            # calculates stability score for each protein
            if len(self.final_placement) == len(self.user_input):
                stability_score, stability_connections = self.stability.get_stability_score(self.final_placement)

                # updates current best protein option
                if stability_score < self.best_score:
                    self.best_score = stability_score
                    self.best_protein = self.final_placement
                    self.amino_stability_x, self.amino_stability_y = finish_protein(stability_score, stability_connections)
