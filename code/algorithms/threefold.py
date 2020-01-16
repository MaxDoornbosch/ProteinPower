"""
threefold.py


Functies to do:
1. Checken of het mag (niet bezet): prunen
    Als je één richting niet op mag, mogen alle corresponderende moves ook niet berekend te worden
2. Als meerdere mogelijkheden: kiezen (welke is beter??)
3. Aller beste optie toevoegen aan final_placement
"""



def split_protein(user_input):
    """
    Splits user input protein into chunks of (max) three amino acids
    """


    # Zorg dat deze de eerste amino overslaat!!!
    user_input_split = [user_input[i:i+3] for i in range(0, len(user_input), 3)]
    print(user_input_split)
    return user_input_split

def three_fold(final_placement, user_input_split, current_fold, x_coordinate, y_coordinate, current_amino):
    """
    For every chunk, calculate
    """

    possible_folds = []
    final_possible_folds = []
    information_folds = []
    storage_list = []

    for i in range (len(user_input_split)):
        chunk = user_input_split[i]

        # eruit halen en hier aanroepen

        def define_folds():
            """
            Defines all possible folds for every move within
            """

            corresponding_folds = {
               1 : [1, -2, 2],
               -1 : [-1, -2, 2],
               2 : [-1, 1, 2],
               -2 : [-1, 1, -2],
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


        def set_coordinates():
            """
            Takes possible folds and attaches corresponding coordinates
            """

            # saves all possible folds with corresponding amino and coordinates
            for i in final_possible_folds:
                current_x = x_coordinate
                current_y = y_coordinate
                storage_list = []
                storage_list.append([current_amino, i[0], x_coordinate, y_coordinate])


                # updates coordinates for each individual amino


                # Simpeler maken

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
                if storage_list not in information_folds:
                    information_folds.append(storage_list)
            print("possible three folds", len(final_possible_folds))
            print("Information folds: ", information_folds)
            print("Length of information_folds: ", len(information_folds))

        def stability_score():
            """
            Calculates the stability score for every three fold
            """

            possible_options = []

            for unit in information_folds:
                checker = True
                fold = True
                score = 0

                # Loops over all the places aminos
                for i in final_placement:
                    print("i", i)

                    # Loops over all the coordinates and folds separately
                    for pos in range(len(chunk) + 1):
                        print("Hello??????")

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

            # if possible_options == []:
            #     return possible_options
            # random_amino = random.choice(possible_options)
            # current_fold = new_fold
            # if len(user_input) - 1 == len(final_placement):
                # random_amino = [user_input[len(final_placement)], 0, current_x, current_y]

            def best_options():
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

                print("Best options: ", best_options)
            best_options()

        define_folds()
        set_coordinates()
        stability_score()
