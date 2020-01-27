"""
random.py

Random search algorithm: determines random (legal) folds for a given protein.

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020
"""

from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.placement import Placement
from code.classes.protein import Protein
from code.classes.stability_score import Stability


class Random:
    """
    Returns a random solution to the protein folding problem.
    """

    def __init__(self, user_input, runamount):
        self.best_placement = []

        self.user_input = user_input
        self.runamount = runamount

        self.protein = Protein(self.user_input)
        self.placement = Placement(self.user_input, self.protein.final_placement)
        self.stability = Stability()

    def run(self):
        """
        Runs random algorithm as many times as the user indicated.
        """

        score = 1

        for i in range(self.runamount):

            done = False

            # restarts when there aren't any options left for the next amino
            while done == False:
                current_n = 1
                finished = False

                while finished == False:
                    self.placement.set_current(current_n)

                    # end of protein has been reached
                    if self.placement.set_coordinates() == False:
                        done = True

                        stability_score, stability_connections = self.stability.get_stability_score(self.protein.final_placement)
                        self.stability_coordinates = stability_connections
                        self.stability.stability_score_coordinates(self.stability_coordinates)
                        self.amino_stability_x = self.stability.amino_stability_x
                        self.amino_stability_y = self.stability.amino_stability_y

                        # checks if current score is lower than the current lowest score
                        if stability_score < score:
                            score = stability_score
                            self.best_placement = self.protein.final_placement
                            self.best_stability = stability_score
                            self.best_amino_stability_x = self.placement.amino_stability_x
                            self.best_amino_stability_y = self.placement.amino_stability_y

                        finished = True

                    # checks if the last amino has been placed
                    if finished == False:

                        self.placement.check_empty(self.user_input)

                        # checks if there aren't any possible coordinates left
                        if len(self.placement.possible_coordinates) == 0:
                            break

                        self.placement.random_amino
                        self.protein.add_amino_info(self.placement.random_amino)
                        self.protein.final_placement

        self.best_protein = self.protein.final_placement
        self.best_score = score
