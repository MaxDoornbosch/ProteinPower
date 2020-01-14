class Three_Fold():
    def __init__(self):
        self.possible_three_folds = []
        self.possible_folds = []
        self.information_folds = []
        self.storage_list = []

    def recursion_folds(self, amino, current_fold, x_coordinate, y_coordinate):
            if current_fold == 1:
                self.possible_folds.append([1, -2, 2])
            elif current_fold == -1:
               self.possible_folds.append([-1, -2, 2])
            elif current_fold == 2:
                self.possible_folds.append([-1, 1, 2])
            elif current_fold == -2:
                self.possible_folds.append([-1, 1, -2])
            for j in (self.possible_folds[0]):
                if j == 1:
                    self.possible_folds.append([1, -2, 2])
                elif j == -1:
                    self.possible_folds.append([-1, -2, 2])
                elif j == 2:
                    self.possible_folds.append([-1, 1, 2])
                elif j == -2:
                    self.possible_folds.append([-1, 1, -2])
                for k in (self.possible_folds[1]):
                    print(k, j)
                    if k == 1:
                        self.possible_three_folds.append([j, k, 1])
                        self.possible_three_folds.append([j, k, -2])
                        self.possible_three_folds.append([j, k, 2])
                    elif k == -1:
                        self.possible_three_folds.append([j, k, -1])
                        self.possible_three_folds.append([j, k, -2])
                        self.possible_three_folds.append([j, k, 2])
                    elif k == 2:
                        self.possible_three_folds.append([j, k, 1])
                        self.possible_three_folds.append([j, k, -1])
                        self.possible_three_folds.append([j, k, 2])
                    elif k == -2:
                        self.possible_three_folds.append([j, k, 1])
                        self.possible_three_folds.append([j, k, -2])
                        self.possible_three_folds.append([j, k, -1])
                self.possible_folds.pop(1)
            for m in self.possible_three_folds:
                self.current_x = x_coordinate
                self.current_y = y_coordinate
                self.storage_list = []
                for n in range(3):
                    if m[n] == 1:
                        self.current_x += 1
                    elif m[n] == -1:
                        self.current_x -= 1
                    elif m[n]== 2:
                        self.current_y += 1
                    elif m[n] == -2:
                        self.current_y -= 1
                    if n == 2:
                        self.storage_list.append([amino[n], 0, self.current_x, self.current_y])
                    else:
                        self.storage_list.append([amino[n], m[n + 1], self.current_x, self.current_y])
                self.information_folds.append(self.storage_list)
            print(self.information_folds)
            print(len(self.information_folds))
            # print(self.possible_three_folds)

if __name__ == "__main__":
    test = Three_Fold()
    test.recursion_folds("PPH", 1, 1, 0)


        
        


