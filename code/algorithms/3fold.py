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
            self.current_x = x_coordinate
            self.current_y = y_coordinate
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
                    self.storage_list.append([amino[j], 0, self.current_x, self.current_y])
                else:
                    self.storage_list.append([amino[j], i[j + 1], self.current_x, self.current_y])
            self.information_folds.append(self.storage_list)
        print(self.information_folds)
        print(len(self.information_folds))
        # print(self.possible_three_folds)

if __name__ == "__main__":
    test = Three_Fold()
    test.recursion_folds("PPH", 1, 1, 0)
