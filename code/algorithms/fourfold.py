"""
fourfold.py

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020

The algorithm looks at all the possibilities for the upcoming 4 moves, all the possibilities are 3^4 = 81.
Then the score per possibility will be calculated. This algorithm will take four steps and will look at
all the best possibilities. It chooses a random best possibility and the four amino's will be placed at those
coordinates. This method will reapeat itself until the end of the protein has been reached. If there are less
than four amino's remaining it will look at all the remaining possibilities.
 """

from code.classes.protein import Protein
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.stability_score import Stability
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.possible_options import PossibleOptions
from code.helper.nfold import creating_coordinates, calculate_best_options, surrounding, connects_to_itself
import random
import copy

class FourFold:
    """
    Looks 4 steps forward and then takes 4 steps
    """
    def __init__(self, user_input, runamount):
        self.user_input = user_input
        self.runamount = runamount
        self.best_placement = []

    def run(self):
        """
        Runs three fold one step
        """

        self.best_score = 1

        # runs the program x times depending on the runamount
        for z in range(self.runamount):
            done = False

            # restarts the program if an error occurs
            while done == False:

                # sets first fold and adds to final
                protein = Protein(self.user_input)

                # splits protein sequence into chunks of three amino acids
                user_input_split = split_protein(self.user_input)

                # updates x,y coordinates based on most recently determined fold
                coordinate_update = CoordinateUpdate()
                coordinate_update.update_coordinates(protein.final_placement)

                for i in range(len(user_input_split)):

                    current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)
                    current_fold = protein.final_placement[-1][1]
                    current_amino = self.user_input[len(protein.final_placement)]
                    best_option = four_fold(protein.final_placement, user_input_split, current_fold, current_x, current_y, current_amino, i, self.user_input)

                    # checks if an error has occured
                    if best_option == False:
                        break

                    # adds the amino's the final placement
                    for i in range(len(best_option) - 1):
                        protein.add_amino_info(best_option[i])

                    # checks if the end of protein hasn't been reached
                    if current_fold != 0:
                        current_x, current_y = coordinate_update.update_coordinates(protein.final_placement)

                    # checks if last amino of sequence is reached
                    if len(protein.final_placement) == (len(self.user_input) - 1):
                        protein.add_last_amino_of_chunk_without_score(current_x, current_y, self.user_input)

                    # end of protein has been reached
                    if protein.final_placement[-1][1] == 0:
                        done = True
                        self.stability = Stability()

                        stability_score, stability_connections = self.stability.get_stability_score(protein.final_placement)
                        self.stability_coordinates = stability_connections
                        self.stability.stability_score_coordinates(self.stability_coordinates)
                        amino_stability_x = self.stability.amino_stability_x
                        amino_stability_y = self.stability.amino_stability_y

                        # checks if current score is lower than the current lowest score
                        if stability_score < self.best_score:
                            self.best_score = stability_score
                            self.best_protein = protein.final_placement
                            self.best_stability = stability_score
                            self.amino_stability_x = amino_stability_x
                            self.amino_stability_y = amino_stability_y

def four_fold(final_placement, user_input_split, current_fold, x_coordinate, y_coordinate, current_amino, i, user_input):
    """
    Determines best possible folds and coordinates for each amino (in each chunk)
    """

    possible_options = []

    chunk = user_input_split[i]
    # possible_folds, final_possible_folds, possible_options = define_folds(current_fold, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    
    possible = PossibleOptions(user_input)
    coordinate_update = CoordinateUpdate()
    current_x, current_y = coordinate_update.update_coordinates(final_placement)

    # finds possible options
    possible.define_folds(final_placement)
    possible.define_coordinates(current_x, current_y)
    final_possible_options = possible.check_empty()

    possible_options_score = stability_score(final_possible_options, final_placement, chunk)
    best_option = best_options(possible_options_score)
    return best_option


def split_protein(user_input):
    """
    Splits user input protein sequence into chunks of (max) three amino acids while ignoring
    the first amino as the first fold and coordinates are predefined.
    """

    user_input = user_input[2:]
    user_input_split = [user_input[i:i+4] for i in range(0, len(user_input), 4)]
    return user_input_split

def define_folds(current_fold, x_coordinate, y_coordinate, current_amino, possible_options, chunk):
    """
    Defines all possible folds for every move within
    """
    possible_folds = []
    final_possible_folds = []
    corresponding_folds = {
       1 : [1, -2, 2],
       -1 : [-1, -2, 2],
       2 : [-1, 1, 2],
       -2 : [-1, 1, -2]
    }

    # determines corresponding folds based on current fold
    if current_fold in corresponding_folds.keys():
        possible_folds.append(corresponding_folds.get(current_fold))

    for i in (possible_folds[0]):
        current_fold = i
        if i in corresponding_folds.keys():
            possible_folds.append(corresponding_folds.get(current_fold))

        # saves every possible fold for each amino
        for j in (possible_folds[1]):
            current_fold = j
            if j in corresponding_folds.keys():
                possible_folds.append(corresponding_folds.get(current_fold))

            # saves every possible fold for each amino
            for k in possible_folds[2]:
                current_fold = k
                if k in corresponding_folds.keys():
                    final_possible_folds.append([i, j, k, corresponding_folds.get(current_fold)[0]])
                    final_possible_folds.append([i, j, k, corresponding_folds.get(current_fold)[1]])
                    final_possible_folds.append([i, j, k, corresponding_folds.get(current_fold)[2]])
            possible_folds.pop(2)
        possible_folds.pop(1)

    possible_options = set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    return possible_folds, final_possible_folds, possible_options

def set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk):
    """
    Takes possible folds and attaches corresponding coordinates
    """

    # goes to a helper function
    possible_options = creating_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    return possible_options


def stability_score(possible_options, final_placement, chunk):
    """
    Calculates the stability score for every three fold
    """

    possible_options_score = []

    # loops over all the possible options
    for unit in possible_options:
        new_option = copy.deepcopy(final_placement)

        for option in unit:
            new_option.append(option)

        stability = Stability()
        score, stability_connections = stability.get_stability_score(new_option)

        # saves all possible options with corresponding stability scores
        try:
            possible_options_score.append([unit[0], unit[1], unit[2], unit[3], score])
        except IndexError:
            try:
                possible_options_score.append([unit[0], unit[1], unit[2], score])
            except IndexError:
                possible_options_score.append([unit[0], unit[1], score])

    return possible_options_score

def best_options(possible_options_score):
    """
    Prunes possible options with lowest values
    """

    # goes to a helper function
    best_options = calculate_best_options(possible_options_score)

    best_option = choose_best_option(best_options)
    return best_option


def choose_best_option(best_options):
    """
    Chooses random option from best options
    """

    # picks a random best option
    try:
        best_option = random.choice(best_options)
    except:
        best_option = False
        return False
    return best_option
