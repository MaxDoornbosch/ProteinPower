"""
protein.py

Saves each amino acid of the protein sequence with corresponding coordinates.
"""

class Protein:
    def __init__(self, user_input):

        # fold and coordinates of first amino are predetermined
        self.final_placement = [[user_input[0], 2, 0, 0]]

    def add_last_amino_of_chunk(self, x_coordinate, y_coordinate, user_input):
        self.final_placement.append([user_input[-1], 0, x_coordinate, y_coordinate])

    def add_amino_info(self, amino_info):
        self.final_placement.append(amino_info)
        return self.final_placement
