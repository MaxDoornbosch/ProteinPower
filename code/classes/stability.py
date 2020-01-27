"""
stability.py

Calculates stability score based on the final protein sequence list.
"""

class Stability:
    def __init__(self):
        self.possible_stability_coordinates = []
        self.stability_score = 0
        self.amino_value = 0

    def score(self, final_placement, user_input):
        for amino_properties in final_placement:

            # checks if amino is H
            if amino_properties[0] != "P":

                # creates surrounding coordinates
                stability_x_plus = amino_properties[2] + 1
                self.possible_stability_coordinates.append([stability_x_plus, amino_properties[3]])
                stability_x_min = amino_properties[2] - 1
                self.possible_stability_coordinates.append([stability_x_min, amino_properties[3]])
                stability_y_plus = amino_properties[3] + 1
                self.possible_stability_coordinates.append([amino_properties[2],stability_y_plus])
                stability_y_min = amino_properties[3] - 1
                self.possible_stability_coordinates.append([amino_properties[2],stability_y_min])

                # total connections
                for coordinates in final_placement:

                    if amino_properties[0] == "H":

                        # checks if it is the same amino
                        if coordinates[0] == "H" or coordinates[0] == "C":
                            # print(self.possible_stability_coordinates)s
                            for possible_coordinates in self.possible_stability_coordinates:

                                # checks if the coordinates are the same
                                if coordinates[2] == possible_coordinates[0] and coordinates[3] == possible_coordinates[1]:
                                    self.stability_score -= 1

                    if amino_properties[0] == "C":

                        # checks if it is the same amino
                        if coordinates[0] == "C":
                            # print(self.possible_stability_coordinates)s
                            for possible_coordinates in self.possible_stability_coordinates:

                                # checks if the coordinates are the same
                                if coordinates[2] == possible_coordinates[0] and coordinates[3] == possible_coordinates[1]:
                                    self.stability_score -= 5

                        # checks if it is the same amino
                        if coordinates[0] == "H":
                            # print(self.possible_stability_coordinates)s
                            for possible_coordinates in self.possible_stability_coordinates:

                                # checks if the coordinates are the same
                                if coordinates[2] == possible_coordinates[0] and coordinates[3] == possible_coordinates[1]:
                                    self.stability_score -= 1
                self.possible_stability_coordinates.clear()


        # checks for adjacent amino acid
        for amino in range(len(user_input)):

            # checks if is beginning of the string
            if amino == 0:
                if user_input[amino + 1] == "H" and user_input[amino] == "H":
                    self.amino_value -= 1
                elif (user_input[amino + 1] == "H" and user_input[amino] == "C") or (user_input[amino + 1] == "C" and user_input[amino] == "H"):
                    self.amino_value -= 1
                if user_input[amino + 1] == "C" and user_input[amino] == "C":
                        self.amino_value -= 5

            # checks if is the end of the string
            elif amino == len(user_input)-1:
                if (user_input[amino - 1] == "H" and user_input[amino] == "H"):
                    self.amino_value -= 1
                elif (user_input[amino - 1] == "C" and user_input[amino] == "H") or (user_input[amino - 1] == "H" and user_input[amino] == "C"):
                    self.amino_value -= 1
                if (user_input[amino - 1] == "C" and user_input[amino] == "C"):
                    self.amino_value -= 5

            # checks if the current amino is an H
            elif user_input[amino] == "H":

                # looks for HH connections or CH connections
                if user_input[amino + 1] == "H" or user_input[amino + 1] == "C":
                    self.amino_value -= 1

                # looks for HH coneections and CH connections
                if user_input[amino - 1] == "H" or user_input[amino - 1] == "C":
                    self.amino_value -= 1

            # checks if the current amino is a C
            elif user_input[amino] == "C": 
                    if user_input[amino + 1] == "H":
                        self.amino_value -= 1

                    if user_input[amino - 1] == "H":
                        self.amino_value -= 1

                    # looks for CC connections
                    if user_input[amino + 1] == "C":
                        self.amino_value -= 5

                    # looks for CC connections
                    if user_input[amino - 1] == "C":
                        self.amino_value -= 5

        self.definitive_stability_score =  (self.stability_score - self.amino_value)/2
        return self.definitive_stability_score