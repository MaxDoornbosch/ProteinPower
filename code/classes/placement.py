import random


class Placement:
    def __init__(self, user_input, final_placement):
        self.final_placement = final_placement
        self.user_input = user_input
        self.possible_folds = []
        self.possible_coordinates = []
        self.new_x = 0
        self.new_y = 0
        self.amino_stability_x = []
        self.amino_stability_y = []

    def set_coordinates(self):
        self.current_fold = self.final_placement[-1][1]
        self.current_x = self.final_placement[-1][2]
        self.current_y = self.final_placement[-1][3]

        if self.current_fold == 1:
            self.current_x += 1
            self.possible_folds = [1, -2, 2]
        elif self.current_fold == -1:
            self.current_x -= 1
            self.possible_folds = [-1, -2, 2]
        elif self.current_fold == 2:
            self.current_y += 1
            self.possible_folds = [-1, 1, 2]
        elif self.current_fold == -2:
            self.current_y -= 1
            self.possible_folds = [-1, 1, -2]

        # end of user_input is reached
        elif self.current_fold == 0:
            return False
        return True

    def check_empty(self, user_input):

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
                    if i[0] == "H" and user_input[len(self.final_placement)] == "H":
                        stability_x = [self.current_x, i[2]]
                        stability_y = [self.current_y, i[3]]
                        self.amino_stability_x.append(stability_x)
                        self.amino_stability_y.append(stability_y)
                        print("APPEEEEEEENNNDNDNDNDNDNDNDN")
                        print(self.amino_stability_x, self.amino_stability_y)

            if checker == True:
                self.possible_coordinates.append([user_input[len(self.final_placement)], self.new_fold, self.current_x, self.current_y])

        print("/////////")
        print(self.possible_coordinates)
        self.random_amino = random.choice(self.possible_coordinates)
        self.possible_coordinates.clear()
        self.current_fold = self.new_fold
        if len(user_input) - 1 == len(self.final_placement):
            self.random_amino = [user_input[len(self.final_placement)], 0, self.current_x, self.current_y]
        return self.random_amino, self.amino_stability_x, self.amino_stability_y
