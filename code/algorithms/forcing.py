"""
forcing.py

Naturally, proteins have a tendency to fold into spiral-like shapes; hence, this
heuristic forces the protein into a spiral shape in order to be able to
check and see how the stability scores produced by this program compare with
those produced by the other algorithms.

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020
"""

from code.classes.stability_score import Stability

class Force:
    def __init__(self,user_input):
        self.current_x = 0
        self.current_y = 0
        self.side_lenght = 1
        self.best_protein = [[user_input[0], 2, 0, 0]]
        self.user_input = user_input
        self.stability = Stability()
        self.end = False
        self.current_fold = 0


    def placing(self):
        """
        Places de amino's on the right place by checking if the side length is
        odd or even.
        """

        while len(self.user_input) > len(self.best_protein):

            # checks step
            for i in range(2):
                for j in range(self.side_lenght):
                    if self.end == False:
                        # checks if is odd number
                        if (self.side_lenght % 2) != 0 :
                            self.odd(i)

                        # checks if is even number
                        elif (self.side_lenght % 2) == 0:

                            # ensure the last amino isn't appended twice
                            try:
                                self.even(i)
                            except IndexError:
                                pass
            self.side_lenght += 1


    def odd(self,i):
        """
        Determines the coordinates and the fold of the amino.
        """

        # checks if is second step
        if i == 1:
            self.new_x = self.current_x + 1
            self.new_y = self.current_y

            # check if is last amino
            if len(self.user_input) -1 == len(self.best_protein):
                self.current_fold = 0
                self.end = True

        # checks if is first step
        elif i == 0:
            self.new_y = self.current_y + 1
            self.new_x = self.current_x

            # check if is last amino
            if len(self.user_input)- 1 == len(self.best_protein):
                self.current_fold = 0
                self.end = True

        self.current_x = self.new_x
        self.current_y = self.new_y

        try:
            self.current_amino = self.user_input[len(self.best_protein)]
        except IndexError:
            pass

        self.best_protein.append([self.current_amino, self.current_fold, self.new_x, self.new_y])

        return self.best_protein, self.current_x, self.current_y

    def even(self,i):
        """
        Determines the coordinates.
        """

        # checks if is first step
        if i == 0:
            self.new_x = self.current_x
            self.new_y = self.current_y -1

            # check if is last amino
            if len(self.user_input) - 1 == len(self.best_protein):
                self.current_fold = 0
                self.end = True

        # checks if is second step
        if i == 1:
            self.new_y = self.current_y
            self.new_x = self.current_x - 1

            # check if is last amino
            if len(self.user_input) - 1 == len(self.best_protein):
                self.current_fold = 0
                self.end = True

        self.current_x = self.new_x
        self.current_y = self.new_y

        try:
            self.current_amino = self.user_input[len(self.best_protein)]
        except IndexError:
            pass

        self.best_protein.append([self.current_amino, self.current_fold, self.new_x, self.new_y])

        return self.best_protein, self.current_x, self.current_y


    def fold(self):
        """
        Determines the fold.
        """

        for i in range(len(self.best_protein) - 1):
            j = i + 1

            # checks next amino and determines fold accordingly
            if self.best_protein[i][2] + 1 == self.best_protein[j][2] and self.best_protein[i][3] == self.best_protein[j][3]:
                self.fold = 1
                self.best_protein[i][1] = self.fold

            elif self.best_protein[i][2] - 1 == self.best_protein[j][2] and self.best_protein[i][3] == self.best_protein[j][3]:
                self.fold =  - 1
                self.best_protein[i][1] = self.fold

            elif self.best_protein[i][2] == self.best_protein[j][2] and self.best_protein[i][3] + 1 == self.best_protein[j][3] :
                self.fold = 2
                self.best_protein[i][1] = self.fold

            elif self.best_protein[i][2] == self.best_protein[j][2] and self.best_protein[i][3] - 1 == self.best_protein[j][3] :
                self.fold = -2
                self.best_protein[i][1] = self.fold

    def run(self):
        """
        Runs forcing algorithm until all possible protein folds have between
        evaluated; determines best fold.
        """

        self.placing()
        self.fold()
        
        self.best_score, stability_connections = self.stability.get_stability_score(self.best_protein)
        self.stability.stability_score_coordinates(stability_connections)
        self.amino_stability_x = self.stability.amino_stability_x
        self.amino_stability_y = self.stability.amino_stability_y
