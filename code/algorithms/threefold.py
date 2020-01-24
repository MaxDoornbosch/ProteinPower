"""
threefold.py


Functies TO DO:
1. Checken of het mag (niet bezet): prunen
    Als je één richting niet op mag, mogen alle corresponderende moves ook niet berekend te worden
2. Als meerdere mogelijkheden: kiezen (welke is beter??)
"""

import random


def three_fold(final_placement, user_input_split, current_fold, x_coordinate, y_coordinate, current_amino, i):
    """
    Determines best possible folds and coordinates for each amino (in each chunk)
    """

    storage_list = []
    possible_options = []

    chunk = user_input_split[i]
    possible_folds, final_possible_folds, possible_options = define_folds(current_fold, x_coordinate, y_coordinate, current_amino, possible_options, storage_list, chunk)
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

def define_folds(current_fold, x_coordinate, y_coordinate, current_amino, possible_options, storage_list, chunk):
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
                final_possible_folds.append([i, j, corresponding_folds.get(current_fold)[0]])
                final_possible_folds.append([i, j, corresponding_folds.get(current_fold)[1]])
                final_possible_folds.append([i, j, corresponding_folds.get(current_fold)[2]])
        possible_folds.pop(1)

    possible_options = set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk)
    return possible_folds, final_possible_folds, possible_options

def set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk):
    """
    Takes possible folds and attaches corresponding coordinates
    """

    # saves all possible folds with corresponding amino and coordinates
    for i in final_possible_folds:
        current_x = x_coordinate
        current_y = y_coordinate
        storage_list = []
        storage_list.append([current_amino, i[0], x_coordinate, y_coordinate])

        # finds the folds
        for j in range(len(chunk)):
            if abs(i[j]) == 1:
                current_x += i[j]
            elif abs(i[j]) == 2:
                current_y += i[j] // 2

            # adds a zero fold to the last coordinates
            if j >= len(chunk) - 1:
                storage_list.append([chunk[j], 0, current_x, current_y])
            elif j < len(chunk) - 1:
                storage_list.append([chunk[j], i[j + 1], current_x, current_y])

            # prevents duplicates and saves aminos with corresponding information
            if storage_list not in possible_options:
                possible_options.append(storage_list)

    return possible_options


def stability_score(possible_options, final_placement, chunk):
    """
    Calculates the stability score for every three fold
    """

    possible_options_score = []

    # Loops over all the possible options
    for unit in possible_options:
        checker = True
        fold = True
        score = 0
        temporary_amino_stability_x = []
        temporary_amino_stability_y = []

        # Loops over all the places aminos
        for i in final_placement:

            # Loops over all the coordinates and folds separately
            for pos in range(len(chunk) + 1):

                # Checks if the coordinates aren't already taken
                if i[2] == unit[pos][2] and i[3] == unit[pos][3]:
                    checker = False

                # Checks if the coordinates overlap
                if pos != 0 and checker == True:
                    previous_fold = unit[pos - 1][1]

                    # Looks for surrounding HH and CH aminos per fold and calculates the score
                    if (i[0] == "H" and unit[pos][0] == "H") or (i[0] == "C" and unit[pos][0] == "H") or (i[0] == "H" and unit[pos][0] == "C"):
                        if i[2] == unit[pos][2] - 1 and i[3] == unit[pos][3] and previous_fold != 1:
                            score -=1
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                        if i[2] == unit[pos][2] and i[3] == unit[pos][3] + 1 and previous_fold != -2:
                            score -=1
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                        if i[2] == unit[pos][2] and i[3] == unit[pos][3] - 1 and previous_fold != 2:
                            score -=1
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                        if i[2] == unit[pos][2] + 1 and i[3] == unit[pos][3] and previous_fold != -1:
                            score -=1
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                    # Looks for surrounding CC aminos per fold and calculates the score
                    if i[0] == "C" and unit[pos][0] == "C":
                        if i[2] == unit[pos][2] - 1 and i[3] == unit[pos][3] and previous_fold != 1:
                            score -= 5
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                        if i[2] == unit[pos][2] and i[3] == unit[pos][3] + 1 and previous_fold != -2:
                            score -= 5
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                        if i[2] == unit[pos][2] and i[3] == unit[pos][3] - 1 and previous_fold != 2:
                            score -= 5
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                        if i[2] == unit[pos][2] + 1 and i[3] == unit[pos][3] and previous_fold != -1:
                            score -= 5
                            temporary_amino_stability_x.append([i[2], unit[pos][2]])
                            temporary_amino_stability_y.append([i[3], unit[pos][3]])

                    # checks whether the last amino connects to itself
                    if pos == 3 and fold == True:
                        fold = False
                        
                        # Looks for surrounding HH and CH aminos per fold and calculates the score
                        if (unit[pos][0] == "H" and unit[0][0] == "H") or (unit[pos][0] == "C" and unit[0][0] == "H") or (unit[pos][0] == "H" and unit[0][0] == "C"):
                            if unit[pos][2] + 1 == unit[0][2] and unit[pos][3] == unit[0][3]:
                                score -= 1
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                            if unit[pos][2] - 1 == unit[0][2] and unit[pos][3] == unit[0][3]:
                                score -= 1
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                            if unit[pos][2] == unit[0][2] and unit[pos][3] + 1 == unit[0][3]:
                                score -= 1
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                            if unit[pos][2] == unit[0][2] and unit[pos][3] - 1 == unit[0][3]:
                                score -= 1
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                        # Looks for surrounding CC aminos per fold and calculates the score
                        if unit[pos][0] == "C" and unit[0][0] == "C":
                            if unit[pos][2] + 1 == unit[0][2] and unit[pos][3] == unit[0][3]:
                                score -= 5
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                            if unit[pos][2] - 1 == unit[0][2] and unit[pos][3] == unit[0][3]:
                                score -= 5
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                            if unit[pos][2] == unit[0][2] and unit[pos][3] + 1 == unit[0][3]:
                                score -= 5
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

                            if unit[pos][2] == unit[0][2] and unit[pos][3] - 1 == unit[0][3]:
                                score -= 5
                                temporary_amino_stability_x.append([unit[pos][2], unit[0][2]])
                                temporary_amino_stability_y.append([unit[pos][3], unit[0][3]])

        # saves all possible options with corresponding stability scores
        if checker == True:
            try:
                possible_options_score.append([unit[0], unit[1], unit[2], score, temporary_amino_stability_x, temporary_amino_stability_y])

            except IndexError:
                possible_options_score.append([unit[0], unit[1], score, temporary_amino_stability_x, temporary_amino_stability_y])

    return possible_options_score

def best_options(possible_options_score):
    """
    Prunes possible options with lowest values
    """

    lowest_stability_score = 0
    best_options = []

    # finds lower bound
    for value in possible_options_score:
        if value[len(value) - 3] < lowest_stability_score:
            lowest_stability_score = value[len(value) - 3]

    # saves options with lower bound
    for value in possible_options_score:
        if value[len(value) - 3] == lowest_stability_score:
            best_options.append(value)

    best_option = choose_best_option(best_options)
    return best_option


def choose_best_option(best_options):
    """
    Chooses random option from best options
    """
    
    # Picks a random best option
    try:
        best_option = random.choice(best_options)
    except:
        best_option = False
        return False
    return best_option