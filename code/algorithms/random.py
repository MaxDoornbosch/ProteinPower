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

import random


class Random:
    """
    Returns a random solution to the protein folding problem.
    """

    def __init__(self, user_input, runamount):
        self.best_placement = []

        self.user_input = user_input
        self.runamount = runamount

        self.protein = Protein(self.user_input)
        self.stability = Stability()

        self.final_placement = self.protein.final_placement

        self.possible_folds = []
        self.possible_coordinates = []
        self.new_x = 0
        self.new_y = 0
        self.amino_stability_x = []
        self.amino_stability_y = []

    def set_current(self):
        """
        Recursive function to set current values
        """

        self.current_fold = self.final_placement[-1][1]
        self.current_x = self.final_placement[-1][2]
        self.current_y = self.final_placement[-1][3]

    def set_coordinates(self):
        """
        Sets current coordinates and calculates possible folds
        """
        self.corresponding_folds = {
           1 : [1, -2, 2],
           -1 : [-1, -2, 2],
           2 : [-1, 1, 2],
           -2 : [-1, 1, -2]
        }

        # last amino of sequence can only have a fold of 0
        if self.current_fold == 0:
            self.possible_folds = [0, 0, 0]
            return False

        # determines corresponding folds based on current fold
        elif self.current_fold in self.corresponding_folds.keys():
            self.possible_folds.extend(self.corresponding_folds.get(self.current_fold))
            return True

    def check_empty(self, user_input):
        """
        Checks if possible folds are legal, sets possible coordinates, and picks random fold.
        """

        self.possible_coordinates.clear()

        # determines possible folds and coordinates
        for i in range(len(self.possible_folds)):
            self.new_fold = self.possible_folds[i]
            self.new_x = self.current_x
            self.new_y = self.current_y

            if self.new_fold == 1:
                self.new_x += 1
                self.new_y = self.current_y
            elif self.new_fold == -1:
                self.new_x -= 1
                self.new_y = self.current_y
            elif self.new_fold == 2:
                self.new_y += 1
                self.new_x = self.current_x
            elif self.new_fold == -2:
                self.new_y -= 1
                self.new_x = self.current_x

            checker = True

            # checks and saves possible folds
            for i in (self.final_placement):
                # print(i)
                if i[2] == self.new_x and i[3] == self.new_y:
                    checker = False

                    # save coordinates for visualization
                    if (i[0] == "H" or i[0] == "C") and (user_input[len(self.final_placement)] == "H" or user_input[len(self.final_placement)] == "C"):
                        stability_x = [self.current_x, i[2]]
                        stability_y = [self.current_y, i[3]]
                        self.amino_stability_x.append(stability_x)
                        self.amino_stability_y.append(stability_y)

            if checker == True:
                self.possible_coordinates.append([user_input[len(self.final_placement)], self.new_fold, self.current_x, self.current_y])

        if not self.possible_coordinates:
            return self.possible_coordinates
        self.random_amino = random.choice(self.possible_coordinates)
        self.current_fold = self.new_fold
        if len(user_input) - 1 == len(self.final_placement):
            self.random_amino = [user_input[len(self.final_placement)], 0, self.current_x, self.current_y]


    def run(self):
        """
        Runs random algorithm as many times as the user indicated.
        """

        self.best_score = 1

        # repeat n many times
        for i in range(self.runamount):

            done = False
            finished = False

            # restarts when there aren't any options left for the next amino
            while done == False:
                while finished == False:
                    self.set_current()

                    # end of protein has been reached
                    if self.set_coordinates() == False:
                        done = True
                        print(">???", self.protein.final_placement)
                        stability_score, stability_connections = self.stability.get_stability_score(self.protein.final_placement)
                        self.stability_coordinates = stability_connections
                        self.stability.stability_score_coordinates(self.stability_coordinates)
                        self.amino_stability_x = self.stability.amino_stability_x
                        self.amino_stability_y = self.stability.amino_stability_y

                        # checks if current score is lower than the current lowest score
                        if stability_score < self.best_score:
                            self.best_score = stability_score
                            self.best_protein = self.protein.final_placement

                        finished = True

                    # checks if the last amino has been placed
                    if finished == False:
                        self.check_empty(self.user_input)

                        # checks if there aren't any possible coordinates left
                        if len(self.possible_coordinates) == 0:
                            break

                        self.random_amino
                        self.protein.add_amino_info(self.random_amino)
                        self.protein.final_placement
