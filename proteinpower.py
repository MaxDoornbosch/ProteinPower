class Fold:
    def __init__(self):
        self.final_path = {}

    def get_protein(self, protein):

        # checks if protein exists
        if len(protein) != 0:
            self.protein = protein.upper()

            # checks if protein is valid
            for i in range(len(self.protein)):
                if self.protein[i] != "H" and self.protein[i] != "P" and  self.protein[i] !="C":
                    return False

            # set first amino
            self.final_path[0] = [self.protein[0], 2, 0, 0, 0]
            return True
        return False

class Placement:
    def __init__(self, protein, final_path):
        self.final_path = final_path
        self.protein = protein
        self.possible_folds = []
        self.possible_coordinates = []
        self.new_x = None
        self.new_y = None

    def set_coordinates(self):
        current_key = max(self.final_path, key=int)
        current_values = self.final_path[current_key]
        self.current_fold = current_values[1]
        self.current_x = current_values[2]
        self.current_y = current_values[3]

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

        # end of protein is reached
        elif self.current_fold == 0:
            return True

    def check_empty(self):

        # determine possible folds and coordinates
        for i in range(len(self.possible_folds)):
            self.new_fold == self.possible_folds[i]

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

            # checks and saves possible folds
            for value in self.final_path.values():
                if value[2] != self.new_x and value[3] != self.new_y:
                    self.possible_coordinates.append([self.new_x, self.new_y])

        self.current_fold = self.new_fold






if __name__ == "__main__":
    while True:
         protein = str(input("please enter your protein: "))
         # print(protein)
         fold = Fold()
         if fold.get_protein(protein) == True:
             # print(case.get_protein(protein))
             # print("error")
         placement = Placement(protein, fold.final_path)
         if placement == True:
             print("goed")
