class PossibleOptions:
    """
    Determines possible options based on current amino acid
    """

    def __init__(self, user_input):
        self.user_input = user_input

        # fold and coordinates of first amino are predetermined
        self.possible_folds = []
        self.final_possible_folds = []
        self.storage_list = []
        self.corresponding_folds = {
           1 : [1, -2, 2],
           -1 : [-1, -2, 2],
           2 : [-1, 1, 2],
           -2 : [-1, 1, -2]
        }

    def define_folds(self, current_path):
        """
        Defines folds
        """

        self.current_path = current_path
        current_fold = self.current_path[-1][1]

        # last amino of sequence has a fold of 0
        if len(current_path) == len(self.user_input) - 1:
            self.possible_folds = [0, 0, 0]

        # determines corresponding folds based on current fold
        elif current_fold in self.corresponding_folds.keys():
            self.possible_folds.extend(self.corresponding_folds.get(current_fold))


    def define_coordinates(self, x_coordinate, y_coordinate):
        """
        Determines x, y coordinates based on possible folds
        """

        self.possible_options = []
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

        current_amino = self.user_input[len(self.current_path)]

        # saves all possible folds with corresponding amino and coordinates
        for fold in self.possible_folds:

            # prevents duplicates and saves aminos with corresponding information
            if [current_amino, fold, self.x_coordinate, self.y_coordinate] not in self.possible_options:
                self.possible_options.append([current_amino, fold, self.x_coordinate, self.y_coordinate])


    def check_empty(self):
        """
        Checks if possible options aren't already taken
        """

        final_possible_options = []
        full_coordinates = []

        for path in self.current_path:
            full_coordinates.append([path[2], path[3]])

        for option in self.possible_options:
            is_possible = True
            fold = True
            score = 0

            option_coordinates = [option[2], option[3]]

            # checks whether coordinates already exist
            if option_coordinates in full_coordinates:
                is_possible = False

            # saves all possible options: amino, fold, x, y
            if is_possible == True:
                final_possible_options.append([option[0], option[1], option[2], option[3]])

        return final_possible_options
