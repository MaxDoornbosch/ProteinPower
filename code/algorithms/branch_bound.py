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

from classes.protein import Protein
from classes.coordinateupdate import CoordinateUpdate
from classes.possible_options import PossibleOptions

import random

class DepthFirst:

    def __init__(self, user_input):
        self.protein = Protein(user_input)
        self.final_placement = self.protein.final_placement
        self.user_input = user_input
        self.depth_first_dict = {}

        # ensures first key has a length of 1
        first = tuple([user_input[0], 2, 0, 0, 0]),

        # creates first branch (first amino with three options)
        final_possible_options = self.determine_possible_options(user_input, self.final_placement)
        possible_options_score = self.pseudo_stability_score(final_possible_options, self.protein.h_coordinates, self.protein.c_coordinates)
        for option in possible_options_score:
            self.depth_first_dict.setdefault(first, []).append(option)

        # average of all scores of all options thus far
        self.average_score = 0

        # lower bound
        self.best_score = 0


    def determine_possible_options(self, user_input, pseudo_placement):
        """
        Determines possible options for every move
        """

        possible = PossibleOptions()
        coordinate_update = CoordinateUpdate()

        # update coordinates for next amino based on current fold
        current_x, current_y = coordinate_update.update_coordinates(pseudo_placement)

        # current amino
        user_input = self.user_input[1:]
        current_amino = user_input[0]

        possible.define_folds(pseudo_placement, current_amino, user_input)
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


    def get_current_keys(self, current_depth):
        """
        Gets all keys of current depth
        """

        current_keys = []
        pseudo_placement = []

        for key in self.depth_first_dict.keys():
            if len(key) == current_depth:

                # saves all keys of current depth
                current_keys.append(key)

                # pseudo_placement of every key as part of current path
                for k in key:
                    print("lalalalalal", k)
                    pseudo_placement.append([val for sublist in key for val in sublist])

        #print("pseudo_placement:::::::", pseudo_placement)

        return current_keys, pseudo_placement


    def run(self, current_score, user_input):
        """
        Runs algorithm until end of sequence is reached


        - Eerst alle opties overwegen: meerdere beste scores? dan gewoon alles.
        - Onthoud mogelijkheid en ga vanuit daar verder: ga nog eentje dieper en kijk dan welke score het laagst is. Dan door
        """

        current_depth = len(self.user_input) - len(user_input)


        #print("depth:", current_depth, "amino:",user_input)



        """
        Of all the keys of this current length, the current key is the last amino of the key
        """
        # for key in self.depth_first_dict.keys():
        #     if len(key) == current_depth:
        #         current_key = list(key[-1])



        current_keys, pseudo_placement = self.get_current_keys(current_depth)


        # for every key in current path
        for key in current_keys:

            # to get the last key of current path????? not necessary???
            #current_keys.append(list(key[-1]))
            #print("Every current key: ", list(key[-1]))


            # for every option, generate three new options
            for option in self.depth_first_dict.get(key):

                if option[0] == "H" or option[0] == "C":
                    current_score = option[-1]

                    if len(user_input) == 1:

                        # x, y, score is same for every option, so the first one will do
                        self.depth_first_dict[tuple([self.user_input[-1], 0, option[2], option[3], current_score])] = []
                        print("---->>>> End of protein. FINAL PLACEMENT: ", self.depth_first_dict)
                        for y in self.depth_first_dict.keys():
                            print("---->>>> FINAL PLACEMENT KEYS: ", y)
                        for z in self.depth_first_dict.values():
                            print("---->>>> FINAL PLACEMENT VALUES: ", z)
                        exit()

                    # pseudo place current path
                    """
                    pseudo placement of first key
                    TODO:
                    - Place all keys in current_key by default
                    """

    #
    #                 if current_score < self.best_score:
    #                     self.best_score = current_score
    #                     #multiple_best_options.append(option)
    #
    #                     self.protein.add_amino_info(option)
    #                     return self.run(current_score, user_input[1:])
    #
    #                 # if current score is worse than average, low possibility (20%) of it being a good option
    #                 elif current_score > average_score:
    #                     r = random.uniform(0, 1)
    #
    #                     # low possibility (20%) of it being a good option
    #                     if r > 0.8:
    #                         protein.add_amino_info(option)
    #                         return self.run(current_score, user_input[1:])
    #
    #                 # if current score is between the best and average score, 50% chance
    #                 elif self.best_score < current_score < average_score:
    #                     r = random.uniform(0, 1)
    #
    #                     # higher possibility (50%) of it being a good option
    #                     if r > 0.5:
    #                         protein.add_amino_info(option)
    #                         return self.run(current_score, user_input[1:])
    #
    #             else:
    #                 continue
    #
    # def pseudo_place(self, pseudo_placement):
    #


                    #pseudo_placement = [list(i) for i in current_keys[0]]
                    pseudo_placement.append(option)
                    print("pseudo placement final placement", pseudo_placement)

                    final_possible_options = self.determine_possible_options(user_input, pseudo_placement)
                    print("Final possible optionsss00000000000>>>", final_possible_options)
                    possible_options_score = self.pseudo_stability_score(final_possible_options, self.protein.h_coordinates, self.protein.c_coordinates)
                    #average_score = self.average_score_thus_far(possible_options_score)

                    # new key is current path + each of the options
                    new_key = tuple(tuple(x) for x in pseudo_placement)

                    # saves current path with corresponding next three options in new tuple
                    for new_option in possible_options_score:
                        self.depth_first_dict.setdefault(new_key, []).append(new_option)

                    # ensures this option is not part of next path
                    pseudo_placement.remove(option)

        return self.run(current_score, user_input[1:])



        """
        new_key = (user_input[0], 6, 0, 0, 0),
        new_key += previous_key

        first = (user_input[0], 2, 0, 0, 0),
        sec = (user_input[0], 6, 0, 0, 0),
        first = first + sec + first
        """


            # current_score = option[-1]
            #
            # if len(user_input) == 1:
            #     self.protein.add_last_amino_of_chunk(option[2], option[3], current_score, self.user_input)
            #     print("End of protein. FINAL PLACEMENT: ", self.protein.final_placement)
            #     exit()
            #
            # if option[0] == "H" or option[0] == "C":
            #     #print("current score = ", current_score)
            #
            #     # if current score is best score yet, place option
            #     if current_score <= self.best_score:
            #         self.best_score = current_score
            #         #multiple_best_options.append(option)
            #
            #         self.protein.add_amino_info(option)
            #         return self.run(current_score, user_input[1:])
            #
            #     # if current score is worse than average, low possibility (20%) of it being a good option
            #     elif current_score > average_score:
            #         r = random.uniform(0, 1)
            #
            #         # low possibility (20%) of it being a good option
            #         if r > 0.8:
            #             protein.add_amino_info(option)
            #             return self.run(current_score, user_input[1:])
            #
            #     # if current score is between the best and average score, 50% chance
            #     elif self.best_score < current_score < average_score:
            #         r = random.uniform(0, 1)
            #
            #         # higher possibility (50%) of it being a good option
            #         if r > 0.5:
            #             protein.add_amino_info(option)
            #             return self.run(current_score, user_input[1:])
            #
            #     else:
            #         continue
            #
            #
            #
            # # if amino is P, or else
            # else:
            #     self.protein.add_amino_info(option)
            #     return self.run(current_score, user_input[1:])
            #
            #
            #


        #multiple_best_options = []

        #
        # final_possible_options = self.determine_possible_options(user_input)
        # possible_options_score = self.pseudo_stability_score(final_possible_options, self.protein.h_coordinates, self.protein.c_coordinates)
        # average_score = self.average_score_thus_far(possible_options_score)

        # while there are still options left


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
