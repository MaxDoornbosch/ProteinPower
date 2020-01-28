"""
depth_first.py

Helper function for the n fold algorithms (threefold, fourfold, threefoldonestep)

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor programmeren
2020
"""

def creating_folds(current_fold):
    """
    Creates all the possible fold combinations
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

    return possible_folds, final_possible_folds

def creating_coordinates(final_possible_folds, x_coordinate, y_coordinate, current_amino, possible_options, chunk):
    """
    Creates all coordinates
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

def calculate_best_options(possible_options_score):
    """
    Finds all the best options
    """
    lowest_stability_score = 0
    best_options = []

    # finds lower bound
    for value in possible_options_score:
        if value[len(value) - 1] < lowest_stability_score:
            lowest_stability_score = value[len(value) - 1]

    # saves options with lower bound
    for value in possible_options_score:
        if value[len(value) - 1] == lowest_stability_score:
            best_options.append(value)
    return best_options