class PossibleOptions:
    """
    Determines possible folds based on current fold

    """
    def __init__(self):

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

    def define_folds(self, final_placement, current_amino, user_input):
        """
        Defines folds
        """

        self.user_input = user_input
        self.final_placement = final_placement
        current_fold = self.final_placement[-1][1]

        # determines corresponding folds based on current fold
        if current_fold in self.corresponding_folds.keys():
            self.possible_folds.extend(self.corresponding_folds.get(current_fold))

        return self.possible_folds


    def define_coordinates(self, x_coordinate, y_coordinate, current_amino):

        self.possible_options = []
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate

        # saves all possible folds with corresponding amino and coordinates
        for i in self.possible_folds:

            # prevents duplicates and saves aminos with corresponding information
            if [current_amino, i, self.x_coordinate, self.y_coordinate] not in self.possible_options:
                self.possible_options.append([current_amino, i, self.x_coordinate, self.y_coordinate])

        return self.possible_options


    def check_empty(self):
        """
        Checks if possible options aren't already taken
        """

        final_possible_options = []

        for option in self.possible_options:
            is_possible = True
            fold = True
            score = 0

            # loops over all already placed aminos
            for placed_amino in self.final_placement:
                print(">>>>>", self.final_placement, ">>>>", placed_amino)

                # checks whether coordinates already exist
                if placed_amino[2] == option[2] and placed_amino[3] == option[3]:
                    is_possible = False

            # saves all possible options with corresponding stability scores
            if is_possible == True:
                final_possible_options.append([option[0], option[1], option[2], option[3]])

        return final_possible_options
