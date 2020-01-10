class Stability:
    def __init__(self):
        self.possible_stability_coordinates = []
        self.stability_score = 0
        self.amino_H = 0

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
                for  coordinates in final_placement:

                    # checks if it is the same amino
                    if amino_properties[0] == coordinates[0]:
                        for possible_coordinates in self.possible_stability_coordinates:

                            # checks if the coordinates are the same
                            if coordinates[2] == possible_coordinates[0] and coordinates[3] == possible_coordinates[1]:
                                self.stability_score -= 1
                self.possible_stability_coordinates.clear()


        # checks for adjacent aminozuur
        for amino in range(len(user_input)):
            if user_input[amino] == "H":

                # checks if is beginning of the string
                if amino == 0 and user_input[amino + 1]:
                    self.amino_H -= 1

                # checks if is the end of the string
                elif amino == len(user_input)-1 and user_input[amino - 1]:
                    self.amino_H -= 1
                else:

                    # looks for H
                    if user_input[amino + 1] == "H":
                        self.amino_H -= 1

                    # looks for H
                    if user_input[amino - 1] == "H":
                        self.amino_H -= 1
        print(self.stability_score)
        print(self.amino_H)
        definitieve_stability_score =  (self.stability_score - self.amino_H)/2
        return definitieve_stability_score
