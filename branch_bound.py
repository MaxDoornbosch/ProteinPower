"""
depth_first.py

TODO:
- Recursive functie werkend maken
- Werkend maken
- Iteraties tellen (state space?)
- Upper bound?
- Een versie maken zonder probability
- Set coordinates, define folds, etc. in classes stoppen
- Dingen boven de functie hieronder in main?
- Check of het uberhaupt mag?
"""

from code.classes.protein import Protein
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.possible_options import PossibleOptions

import random

class DepthFirst:

    def __init__(self, user_input):
        self.protein = Protein(user_input)
        self.final_placement = self.protein.final_placement
        self.user_input = user_input

        # lower bound
        self.best_score = 0

        # average of all scores of all options thus far
        self.average_score = 0


    def determine_possible_options(self, user_input):
        """
        Determines possible options for every move
        """

        possible = PossibleOptions()
        coordinate_update = CoordinateUpdate()

        # update coordinates for next amino based on current fold
        current_x, current_y = coordinate_update.update_coordinates(self.final_placement)

        # current amino
        user_input = self.user_input[1:]
        current_amino = user_input[0]

        possible.define_folds(self.final_placement, current_amino, user_input)
        possible.define_coordinates(current_x, current_y, current_amino)
        final_possible_options = possible.check_empty()

        return final_possible_options

    def pseudo_stability_score(self, final_possible_options, h_coordinates, c_coordinates):
        """
        Calculates stability scores of every possible option and appends score to list
        """

        possible_options_score = []
        current_score = self.final_placement[-1][4]

        for option in final_possible_options:

            # if two H aminos are connected or current amino is a P, keep previous score
            if option[0] == "H" and self.final_placement[-1][0] == "H" or option[0] == "P" or option[0] == "C" and self.final_placement[-1][0] == "C":
                possible_options_score.append([option[0], option[1], option[2], option[3], current_score])

            # else, checks for surrounding H aminos and calculate score
            elif option[0] == "H" or option[0] == "C":
                x_coordinate = option[2]
                y_coordinate = option[3]
                surrounding_coordinates = [[x_coordinate + 1, y_coordinate], [x_coordinate - 1, y_coordinate],
                                           [x_coordinate, y_coordinate + 1], [x_coordinate, y_coordinate - 1], [0, 0]]

                # updates score
                for coordinates in surrounding_coordinates:
                    if coordinates in h_coordinates:
                        current_score =- 1
                    elif coordinates in c_coordinates:
                        current_score =- 5

                possible_options_score.append([option[0], option[1], option[2], option[3], current_score])

        return possible_options_score


    def average_score_thus_far(self, possible_options_score):
        """
        if option[4] exists:
            sum of option[4]
        """
        average_score = 0

        for option in possible_options_score:
            average_score += option[4]

        average_score /= len(possible_options_score)

        return average_score


    def coordinates_of_H_aminos(self, key):
        """
        Extracts coordinates of all H aminos from key (i.e. current path)

        key = [[amino, fold, x, y, score]] : [a][b][c]
        key = [[amino, fold, x, y, ?], [amino, fold, x, y, ?]]
        key = [[amino, fold, x, y, ?], [amino, fold, x, y, ?], [amino, fold, x, y, ?]]
        key = [etc.]

        h_coordinates = []

        for k in key:
            if k[0] == "H":
                h_coordinates.append([k[2], k[3]])

        return h_coordinates
        """


        self.h_coordinates = []

        if amino_info[0] == "H":
            self.h_coordinates.append([amino_info[2], amino_info[3]])

        print("H COOORDINATES", self.h_coordinates)
        return self.h_coordinates


    def coordinates_of_C_aminos(self, key):
        """
        Extracts coordinates of all H aminos from key (i.e. current path)

        key = [[amino, fold, x, y, ?]]
        key = [[amino, fold, x, y, ?], [amino, fold, x, y, ?]]
        key = [[amino, fold, x, y, ?], [amino, fold, x, y, ?], [amino, fold, x, y, ?]]
        key = [etc.]

        c_coordinates = []

        for k in key:
            if k[0] == "C":
                c_coordinates.append([k[2], k[3]])

        return c_coordinates
        """

        self.c_coordinates = []

        self.c_coordinates.append([amino_info[2], amino_info[3]])

        print("C COOORDINATES", self.c_coordinates)
        return self.c_coordinates




    def run(self, current_score, user_input):
        """
        Runs algorithm until end of sequence is reached

        - Eerst alle opties overwegen: meerdere beste scores?
        - Onthoud mogelijkheid en ga vanuit daar verder: ga nog eentje dieper en kijk dan welke score het laagst is. Dan door
        """

        print("i: ", len(user_input), user_input)

        paths = {}



        #multiple_best_options = []

        final_possible_options = self.determine_possible_options(user_input)
        possible_options_score = self.pseudo_stability_score(final_possible_options, self.protein.h_coordinates, self.protein.c_coordinates)
        average_score = self.average_score_thus_far(possible_options_score)

        # while there are still options left
        if len(possible_options_score) > 0:
            for option in possible_options_score:
                final_possible_options = self.determine_possible_options(user_input)
                possible_options_score = self.pseudo_stability_score(final_possible_options, self.protein.h_coordinates, self.protein.c_coordinates)





                current_score = option[4]

                if len(user_input) == 1:
                    self.protein.add_last_amino_of_chunk(option[2], option[3], current_score, self.user_input)
                    print("End of protein. FINAL PLACEMENT: ", self.protein.final_placement)
                    exit()

                if option[0] == "H" or option[0] == "C":
                    print("current score = ", current_score)

                    # if current score is best score yet, place option
                    if current_score <= self.best_score:
                        self.best_score = current_score
                        #multiple_best_options.append(option)

                        self.protein.add_amino_info(option)
                        return self.run(current_score, user_input[1:])

                    # if current score is worse than average, low possibility (20%) of it being a good option
                    elif current_score > average_score:
                        r = random.uniform(0, 1)

                        # low possibility (20%) of it being a good option
                        if r > 0.8:
                            protein.add_amino_info(option)
                            return self.run(current_score, user_input[1:])

                    # if current score is between the best and average score, 50% chance
                    elif self.best_score < current_score < average_score:
                        r = random.uniform(0, 1)

                        # higher possibility (50%) of it being a good option
                        if r > 0.5:
                            protein.add_amino_info(option)
                            return self.run(current_score, user_input[1:])

                    else:
                        continue



                # if amino is P, or else
                else:
                    self.protein.add_amino_info(option)
                    return self.run(current_score, user_input[1:])




"""
MAIN.PY
"""

user_input = input("Please enter your protein (minimum length is 3): ").upper()

# minimum length of protein
while len(user_input) < 3:
    user_input = input("Please enter your protein (minimum length is 3): ").upper()

# checks if user_input is valid
for i in range(len(user_input)):
    while user_input[i] != "H" and user_input[i] != "P" and user_input[i] !="C":
        user_input = input("Please enter your protein (minimum length is 3): ").upper()



"""
Initialization for main.py
"""



depth = DepthFirst(user_input)
current_score = 0
depth.run(current_score, user_input[1:])
