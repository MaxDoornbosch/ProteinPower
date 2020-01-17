def three_fold(final_placement, amino, current_fold, x_coordinate, y_coordinate, current_amino):
    possible_three_folds = []
    possible_folds = []
    information_folds = []
    storage_list = []

    """
    Functies:
    1. User input in stukken van 3 hakken (of 2 of 1 voor laatste)
    2. Checken of het mag (niet bezet): prunen
        Als je één richting niet op mag, mogen alle corresponderende moves ook niet berekend te worden
    """

    def define_folds():
        """
        Defines all possible folds for every move
        """

        # Checks the previous fold
        if current_fold == 1:
            possible_folds.append([1, -2, 2])
        elif current_fold == -1:
            possible_folds.append([-1, -2, 2])
        elif current_fold == 2:
            possible_folds.append([-1, 1, 2])
        elif current_fold == -2:
            possible_folds.append([-1, 1, -2])

        # Loop over all the possible folds
        for i in (possible_folds[0]):

            # Checks which folds are possible
            if i == 1:
                possible_folds.append([1, -2, 2])
            elif i == -1:
                possible_folds.append([-1, -2, 2])
            elif i == 2:
                possible_folds.append([-1, 1, 2])
            elif i == -2:
                possible_folds.append([-1, 1, -2])

            # Loops over all the previous possible folds
            for j in (possible_folds[1]):

                # Adds the folds to a list
                if j == 1:
                    possible_three_folds.append([i, j, 1])
                    possible_three_folds.append([i, j, -2])
                    possible_three_folds.append([i, j, 2])
                elif j == -1:
                    possible_three_folds.append([i, j, -1])
                    possible_three_folds.append([i, j, -2])
                    possible_three_folds.append([i, j, 2])
                elif j == 2:
                    possible_three_folds.append([i, j, 1])
                    possible_three_folds.append([i, j, -1])
                    possible_three_folds.append([i, j, 2])
                elif j == -2:
                    possible_three_folds.append([i, j, 1])
                    possible_three_folds.append([i, j, -2])
                    possible_three_folds.append([i, j, -1])
            possible_folds.pop(1)

    def set_coordinates():
        """
        Takes possible folds and attaches corresponding coordinates
        """

        # Loops over all the possible three folds
        for i in possible_three_folds:
            current_x = x_coordinate
            current_y = y_coordinate
            storage_list = []
            storage_list.append([current_amino, i[0], x_coordinate, y_coordinate])

            # Loops over the folds separately
            for j in range(len(amino)):

                # Changes the coordinates
                if i[j] == 1:
                    current_x += 1
                elif i[j] == -1:
                    current_x -= 1
                elif i[j]== 2:
                    current_y += 1
                elif i[j] == -2:
                    current_y -= 1

                # Adds a dummy fold to the last coordinates
                if j >= len(amino) - 1:
                    storage_list.append([amino[j], 0, current_x, current_y])
                elif j < len(amino) - 1:
                    storage_list.append([amino[j], i[j + 1], current_x, current_y])

            if storage_list not in information_folds:
                information_folds.append(storage_list)
        print(information_folds)
        print(len(information_folds))

    def stability_score():
        """
        Calculates the stability score for every three fold
        """

        
        print(information_folds)

        # Loops over all the three folds
        for possible_folds in information_folds:
            checker = True
            fold = True
            score = 0
            possible_options = []

            # Loops over all the places amino's
            for i in (final_placement):

                # Loops over all the coordinates and folds separately
                for pos in range(len(amino)+1):

                    # Checks if the coordinates aren't already taken
                    if i[2] == possible_folds[pos][2] and i[3] == possible_folds[pos][3]:
                        print(i[2], i[3])
                        print(possible_folds[pos][2], possible_folds[pos][3])
                        checker = False

                    # Checks if the coordinates overlap
                    if pos != 0 and checker == True:
                        previous_fold = possible_folds[pos - 1][1]

                        # Looks for surrounding H amino's per fold and calculates the score
                        if i[0] == "H" and possible_folds[pos][0] == "H":
                            if i[2] == possible_folds[pos][2] - 1 and i[3] == possible_folds[pos][3] and previous_fold != 1:
                                    score -=1

                            if i[2] == possible_folds[pos][2] and i[3] == possible_folds[pos][3] + 1 and previous_fold != -2:
                                    score -=1

                            if i[2] == possible_folds[pos][2] and i[3] == possible_folds[pos][3] - 1 and previous_fold != 2:
                                    score -=1

                            if i[2] == possible_folds[pos][2] + 1 and i[3] == possible_folds[pos][3] and previous_fold != -1:
                                    score -=1

                        if pos == 3 and fold == True:
                            fold = False
                            if possible_folds[pos][0] == "H" and possible_folds[0][0] == "H":
                                if possible_folds[pos][2] + 1 == possible_folds[0][2] and possible_folds[pos][3] == possible_folds[0][3]:
                                    score -= 1

                                if possible_folds[pos][2] - 1 == possible_folds[0][2] and possible_folds[pos][3] == possible_folds[0][3]:
                                    score -= 1

                                if possible_folds[pos][2] == possible_folds[0][2] and possible_folds[pos][3] + 1 == possible_folds[0][3]:
                                    score -= 1

                                if possible_folds[pos][2] == possible_folds[0][2] and possible_folds[pos][3] - 1 == possible_folds[0][3]:
                                    score -= 1


            # saves all possible options with corresponding stability scores
            if checker == True:
                try:
                    possible_options.append([possible_folds[0], possible_folds[1], possible_folds[2], score])
                except IndexError:
                    possible_options.append([possible_folds[0], possible_folds[1], score])

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

            lower_bound = 0
            best_options = []

            # finds lower bound
            for value in possible_options:
                if value[len(value) - 1] < lower_bound:
                    lower_bound = value[len(value)- 1]
                    print("Lower bound is: ", lower_bound)

            # saves options with lower bound
            for value in possible_options:
                if value[len(value) - 1] == lower_bound:
                    best_options.append(value)

            print("Best options: ", best_options)
            def choose_option():
                counter = 0
                best = best_options[0][0][1]
                best_folds = []
                for option in best_options:
                    best_folds.append(option[0][1])
                for option in best_folds:
                    current_frequency = best_folds.count(option)
                    if (current_frequency > counter):
                        counter = current_frequency 
                        best = option
                print("The best fold is ", best)

                def new_placement():
                    placement = []
                    placement.append(amino)
                    placement.append(best)
                    placement.append(x_coordinate)
                    placement.append(y_coordinate)
                new_placement()
            choose_option()
        best_options()
    define_folds()
    set_coordinates()
    stability_score()
