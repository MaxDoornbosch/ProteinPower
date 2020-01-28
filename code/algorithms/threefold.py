"""
threefold.py

The algorithm looks at all the possibilities for the upcoming 3 moves, all the possibilities are 3^3 = 27.
Then the score per possibility will be calculated. This algorithm will take three steps and will look at
all the best possibilities. It chooses a random best possibility and the three amino's will be placed those
coordinates. This method will reapeat itself until the end of the protein has been reached. If there are less
than three amino's remaining it will look at all the remaining possibilities.

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020
"""

from code.classes.protein import Protein
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.stability_score import Stability
from code.helper.nfold import *
import random

class ThreeFold:
    """
    Looks 3 steps forward and then takes three steps.
    """

    def __init__(self, user_input, runamount):
        self.user_input = user_input
        self.runamount = runamount

        self.best_placement = []
        self.best_score = 1

        self.coordinate_update = CoordinateUpdate()
        self.stability = Stability()


    def set_best_options(self, i):
        """
        Sets coordinates, folds, and determines best options for three fold
        algorithm.
        """

        # updates x,y coordinates based on most recently determined fold
        self.current_x, self.current_y = self.coordinate_update.update_coordinates(self.protein.final_placement)
        self.current_fold = self.protein.final_placement[-1][1]
        self.current_amino = self.user_input[len(self.protein.final_placement)]
        self.best_option = three_fold(self.protein.final_placement, self.user_input_split, self.current_fold, self.current_x, self.current_y, self.current_amino, i)

    def run(self):
        """
        Runs three fold one step.
        """

        # runs the program x times depending on the runamount
        for times in range(self.runamount):
            done = False

            # sets first fold and adds to final
            self.protein = Protein(self.user_input)

            # restarts the program if an error occurs
            while done == False:

                # splits protein sequence into chunks of three amino acids
                self.user_input_split = split_protein(self.user_input)

                for i in range(len(self.user_input_split)):
                    self.set_best_options(i)

                    # checks if an error has occured
                    if self.best_option == False:
                        break

                    # places the amino acids
                    for i in range(len(self.best_option) - 1):
                        self.protein.add_amino_info(self.best_option[i])

                    # adds last amino of sequence
                    if len(self.protein.final_placement) == (len(self.user_input) - 1):
                        self.protein.add_last_amino_of_chunk_without_score(self.current_x, self.current_y, self.user_input)

                    # determines stability after each protein is finished
                    if len(self.protein.final_placement) == len(self.user_input):
                        done, self.protein.final_placement, self.best_score, self.best_protein, self.best_stability, self.amino_stability_x, self.amino_stability_y, self.stability_score = set_stability(self.best_score, self.protein.final_placement)


def three_fold(final_placement, user_input_split, current_fold, x_coordinate, y_coordinate, current_amino, i):
    """
    Determines best possible folds and coordinates for each amino (in each chunk).
    """

    possible_options = []

    chunk = user_input_split[i]
    possible_folds, final_possible_folds, possible_options = define_folds(current_fold, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    possible_options_score = stability_score(possible_options, final_placement, chunk)
    best_option = best_options(possible_options_score)
    return best_option

def split_protein(user_input):
    """
    Splits user input protein sequence into chunks of (max) three amino acids while ignoring
    the first amino as the first fold and coordinates are predefined.
    """

    user_input = user_input[2:]
    user_input_split = [user_input[i:i+3] for i in range(0, len(user_input), 3)]
    return user_input_split

def define_folds(current_fold, x_coordinate, y_coordinate, current_amino, possible_options, chunk):
    """
    Defines all possible folds for every move within.
    """

    # goes to a helper function
    possible_folds, final_possible_folds = creating_folds(current_fold)
    possible_options = set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    return possible_folds, final_possible_folds, possible_options

def set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk):
    """
    Takes possible folds and attaches corresponding coordinates.
    """

    # helper function for determining the possible options
    possible_options = creating_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    return possible_options

def stability_score(possible_options, final_placement, chunk):
    """
    Calculates the stability score for every three fold.
    """

    possible_options_score = []

    # loops over all the possible options
    for unit in possible_options:
        checker = True
        score = 0

        # loops over all the places aminos
        for i in final_placement:

            # loops over all the coordinates and folds separately
            for pos in range(len(chunk) + 1):

                # checks if the coordinates aren't already taken
                if i[2] == unit[pos][2] and i[3] == unit[pos][3]:
                    checker = False

                # checks if the coordinates overlap
                if pos != 0 and checker == True:
                    previous_fold = unit[pos - 1][1]

                    # goes to a helpers function that looks for surrounding amino's
                    score = surrounding(i, unit, pos, previous_fold, score)

                    # checks whether the last amino connects to itself
                    if pos == 3:

                        # goes te a helpers functions
                        score = connects_to_itself(i, unit, pos, previous_fold, score)

        # saves all possible options with corresponding stability scores
        if checker == True:
            try:
                possible_options_score.append([unit[0], unit[1], unit[2], score])
            except IndexError:
                possible_options_score.append([unit[0], unit[1], score])

    return possible_options_score

def best_options(possible_options_score):
    """
    Prunes possible options with lowest values.
    """

    # goes to a helper function
    best_options = calculate_best_options(possible_options_score)
    best_option = choose_best_option(best_options)

    return best_option

def choose_best_option(best_options):
    """
    Chooses random option from best options.
    """

    # picks a random best option
    try:
        best_option = random.choice(best_options)
    except:
        best_option = False
        return False

    return best_option
