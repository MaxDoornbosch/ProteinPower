"""
protein.py

Saves each amino acid of the protein sequence with corresponding coordinates.

"""

class Protein:
    """
    Fold and coordinates of first amino are predetermined
    """

    def __init__(self, user_input):

        self.h_coordinates = []
        self.c_coordinates = []

        fold = 2
        x_coordinate = 0
        y_coordinate = 0

        self.user_input = user_input

        first_amino = [user_input[0], fold, x_coordinate, y_coordinate]
        self.final_placement = [first_amino]

        if user_input[0] == "H":
            self.coordinates_of_H_aminos(first_amino)
        elif user_input[0] == "C":
            self.coordinates_of_C_aminos(first_amino)


    def add_last_amino_of_chunk(self, x_coordinate, y_coordinate, current_score, user_input):
        """
        Fold of last amino is always 0
        """

        fold = 0

        last_amino = [user_input[-1], fold, x_coordinate, y_coordinate, current_score]
        self.final_placement.append(last_amino)


    def add_amino_info(self, amino_info):
        """
        Adds amino
        """

        self.final_placement.append(amino_info)

        if amino_info[0] == "H":
            self.coordinates_of_H_aminos(amino_info)
        elif amino_info[0] == "C":
            self.coordinates_of_C_aminos(amino_info)


    def coordinates_of_H_aminos(self, amino_info):
        """
        Saves coordinates of H aminos to calculate stability score
        """

        if amino_info[0] == "H":
            self.h_coordinates.append([amino_info[2], amino_info[3]])


    def coordinates_of_C_aminos(self, amino_info):
        """
        Saves coordinates of C aminos to calculate stability score
        """

        self.c_coordinates.append([amino_info[2], amino_info[3]])

    def add_last_amino_of_chunk_without_score(self, x_coordinate, y_coordinate, user_input):
        """
        Fold of last amino is always 0
        """

        fold = 0

        last_amino = [user_input[-1], fold, x_coordinate, y_coordinate]
        self.final_placement.append(last_amino)


    def random_try_again(self):

        self.h_coordinates = []
        self.c_coordinates = []

        fold = 2
        x_coordinate = 0
        y_coordinate = 0

        first_amino = [self.user_input[0], fold, x_coordinate, y_coordinate]
        self.final_placement = [first_amino]

        if self.user_input[0] == "H":
            self.coordinates_of_H_aminos(first_amino)
        elif self.user_input[0] == "C":
            self.coordinates_of_C_aminos(first_amino)
