class Three_Fold():
    def __init__(self):
        self.possible_three_folds = []
        self.possible_folds = []
        self.information_folds = []
        self.storage_list = []

    def define_folds(self, amino, current_fold, x_coordinate, y_coordinate):
        """
        Defines all possible folds for every move
        """
        self.amino = amino
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        if current_fold == 1:
            self.possible_folds.append([1, -2, 2])
        elif current_fold == -1:
           self.possible_folds.append([-1, -2, 2])
        elif current_fold == 2:
            self.possible_folds.append([-1, 1, 2])
        elif current_fold == -2:
            self.possible_folds.append([-1, 1, -2])

        for i in (self.possible_folds[0]):
            if i == 1:
                self.possible_folds.append([1, -2, 2])
            elif i == -1:
                self.possible_folds.append([-1, -2, 2])
            elif i == 2:
                self.possible_folds.append([-1, 1, 2])
            elif i == -2:
                self.possible_folds.append([-1, 1, -2])

            for j in (self.possible_folds[1]):
                print(j, i)
                if j == 1:
                    self.possible_three_folds.append([i, j, 1])
                    self.possible_three_folds.append([i, j, -2])
                    self.possible_three_folds.append([i, j, 2])
                elif j == -1:
                    self.possible_three_folds.append([i, j, -1])
                    self.possible_three_folds.append([i, j, -2])
                    self.possible_three_folds.append([i, j, 2])
                elif j == 2:
                    self.possible_three_folds.append([i, j, 1])
                    self.possible_three_folds.append([i, j, -1])
                    self.possible_three_folds.append([i, j, 2])
                elif j == -2:
                    self.possible_three_folds.append([i, j, 1])
                    self.possible_three_folds.append([i, j, -2])
                    self.possible_three_folds.append([i, j, -1])
            self.possible_folds.pop(1)

    def set_coordinates(self):
        """
        Takes possible folds and attaches corresponding coordinates
        """
        for i in self.possible_three_folds:
            self.current_x = self.x_coordinate
            self.current_y = self.y_coordinate
            self.storage_list = []

            for j in range(3):
                if i[j] == 1:
                    self.current_x += 1
                elif i[j] == -1:
                    self.current_x -= 1
                elif i[j]== 2:
                    self.current_y += 1
                elif i[j] == -2:
                    self.current_y -= 1
                if j == 2:
                    self.storage_list.append([self.amino[j], 0, self.current_x, self.current_y])
                else:
                    self.storage_list.append([self.amino[j], i[j + 1], self.current_x, self.current_y])
            self.information_folds.append(self.storage_list)
        print(self.information_folds)
        print(len(self.information_folds))

    def stability_score(self, final_placement):
        self.possible_coordinates = []
        self.final_placement = final_placement
        print(self.information_folds)

        for possible_folds in self.information_folds:
            checker = True
            score = 0

            # checks and saves possible folds
            for i in (self.final_placement):
                
                for pos in range(3):
                    if i[2] == possible_folds[pos][2] and i[3] == possible_folds[pos][3]:
                        print(i[2], i[3])
                        print(possible_folds[pos][2], possible_folds[pos][3])
                        checker = False

                        # save coordinates for visualization
                        if i[0] == "H" and possible_folds[pos][0]:
                            score -= 1
                            

            if checker == True:
                self.possible_coordinates.append([possible_folds[0], possible_folds[1], possible_folds[2], score])

        print("/////////")
        print(self.possible_coordinates)
        print(len(self.possible_coordinates))
        # if self.possible_coordinates == []:
        #     return self.possible_coordinates
        # self.random_amino = random.choice(self.possible_coordinates)
        # self.current_fold = self.new_fold
        # if len(user_input) - 1 == len(self.final_placement):
            # self.random_amino = [user_input[len(self.final_placement)], 0, self.current_x, self.current_y]
        for value in self.possible_coordinates:
            if value[3] != 0:
                print("-------------------------------------------------")
                print(value)
        return True

if __name__ == "__main__":
    test = Three_Fold()
    test.define_folds("HHH", 2, 0, 2)
    test.set_coordinates()
    final_placement = [["H", 1, -1, 0], ["H", 2, 0, 0], ["H", 2, 0, 1]]
    test.stability_score(final_placement)
