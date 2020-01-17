"""
threefold.py


Functies TO DO:
1. Checken of het mag (niet bezet): prunen
    Als je één richting niet op mag, mogen alle corresponderende moves ook niet berekend te worden
2. Als meerdere mogelijkheden: kiezen (welke is beter??)
3. Aller beste optie toevoegen aan final_placement
"""


def three_fold(final_placement, user_input_split, current_fold, x_coordinate, y_coordinate, current_amino):
    """
    Determines best possible folds and coordinates for each amino (in each chunk)
    """
    amino_info = []
    storage_list = []

    for i in range(len(user_input_split)):
        chunk = user_input_split[i]
        possible_folds, final_possible_folds, amino_info = define_folds(current_fold, x_coordinate, y_coordinate, current_amino, amino_info, storage_list, chunk)
        possible_options = stability_score(amino_info, final_placement, chunk)
        best_options(possible_options)


def split_protein(user_input):
    """
    Splits user input protein sequence into chunks of (max) three amino acids while ignoring
    the first amino as the first fold and coordinates are predefined.
    """

    user_input = user_input[1:]
    user_input_split = [user_input[i:i+3] for i in range(0, len(user_input), 3)]
    return user_input_split

def define_folds(current_fold, x_coordinate, y_coordinate, current_amino, amino_info, storage_list, chunk):
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
        if i in corresponding_folds.keys():
            possible_folds.append(corresponding_folds.get(current_fold))

        # saves every possible fold for each amino
        for j in (possible_folds[1]):
            if j in corresponding_folds.keys():
                final_possible_folds.append([i, j, corresponding_folds.get(current_fold)[0]])
                final_possible_folds.append([i, j, corresponding_folds.get(current_fold)[1]])
                final_possible_folds.append([i, j, corresponding_folds.get(current_fold)[2]])
        print("possible folds", possible_folds)
        possible_folds.pop(1)

    amino_info = set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, amino_info, chunk)
    return possible_folds, final_possible_folds, amino_info

def set_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, amino_info, chunk):
    """
    Takes possible folds and attaches corresponding coordinates
    """

    # saves all possible folds with corresponding amino and coordinates
    for i in final_possible_folds:
        current_x = x_coordinate
        current_y = y_coordinate
        storage_list = []
        storage_list.append([current_amino, i[0], x_coordinate, y_coordinate])

        # Simpeler maken !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! (class???)
        for j in range(len(chunk)):
            if i[j] == 1:
                current_x += 1
            elif i[j] == -1:
                current_x -= 1
            elif i[j]== 2:
                current_y += 1
            elif i[j] == -2:
                current_y -= 1

            # adds a dummy fold of 0 to the last coordinates
            if j >= len(chunk) - 1:
                storage_list.append([chunk[j], 0, current_x, current_y])
            elif j < len(chunk) - 1:
                storage_list.append([chunk[j], i[j + 1], current_x, current_y])

            # prevents duplicates and saves aminos with corresponding information
            if storage_list not in amino_info:
                amino_info.append(storage_list)

    print("Length of amino_info: ", len(amino_info))
    print("All possible options (amino_info): ", amino_info)

    return amino_info


def stability_score(amino_info, final_placement, chunk):
    """
    Calculates the stability score for every three fold
    """

    possible_options = []

    for unit in amino_info:
        checker = True
        fold = True
        score = 0

        # Loops over all the places aminos
        for i in final_placement:

            # Loops over all the coordinates and folds separately
            for pos in range(len(chunk) + 1):

                # Checks if the coordinates aren't already taken
                if i[2] == unit[pos][2] and i[3] == unit[pos][3]:
                    print(i[2], i[3])
                    print(unit[pos][2], unit[pos][3])
                    checker = False

                # Checks if the coordinates overlap
                if pos != 0 and checker == True:
                    previous_fold = unit[pos - 1][1]

                    # Looks for surrounding H aminos per fold and calculates the score
                    if i[0] == "H" and unit[pos][0] == "H":
                        if i[2] == unit[pos][2] - 1 and i[3] == unit[pos][3] and previous_fold != 1:
                            score -=1

                        if i[2] == unit[pos][2] and i[3] == unit[pos][3] + 1 and previous_fold != -2:
                            score -=1

                        if i[2] == unit[pos][2] and i[3] == unit[pos][3] - 1 and previous_fold != 2:
                            score -=1

                        if i[2] == unit[pos][2] + 1 and i[3] == unit[pos][3] and previous_fold != -1:
                            score -=1

                    if pos == 3 and fold == True:
                        fold = False
                        if unit[pos][0] == "H" and unit[0][0] == "H":
                            if unit[pos][2] + 1 == unit[0][2] and unit[pos][3] == unit[0][3]:
                                score -= 1

                            if unit[pos][2] - 1 == unit[0][2] and unit[pos][3] == unit[0][3]:
                                score -= 1

                            if unit[pos][2] == unit[0][2] and unit[pos][3] + 1 == unit[0][3]:
                                score -= 1

                            if unit[pos][2] == unit[0][2] and unit[pos][3] - 1 == unit[0][3]:
                                score -= 1


        # saves all possible options with corresponding stability scores
        if checker == True:
            try:
                possible_options.append([unit[0], unit[1], unit[2], score])
            except IndexError:
                possible_options.append([unit[0], unit[1], score])

    print("////////////////")
    print("All possible options: ", possible_options)
    print("Length of all possible options: ", len(possible_options))

    return possible_options

    # if possible_options == []:
    #     return possible_options
    # random_amino = random.choice(possible_options)
    # current_fold = new_fold
    # if len(user_input) - 1 == len(final_placement):
        # random_amino = [user_input[len(final_placement)], 0, current_x, current_y]

def best_options(possible_options):
    """
    Prunes possible options with lowest values
    """

    lowest_stability_score = 0
    best_options = []

    # finds lower bound
    for value in possible_options:
        if value[len(value) - 1] < lowest_stability_score:
            lowest_stability_score = value[len(value)- 1]
            print("Lowest stability score is: ", lowest_stability_score)

    # saves options with lower bound
    for value in possible_options:
        if value[len(value) - 1] == lowest_stability_score:
            best_options.append(value)

    print("Length of best options: ", len(best_options))
    print("Best options: ", best_options)
