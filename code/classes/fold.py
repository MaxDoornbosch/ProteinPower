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
