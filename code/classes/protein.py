class Protein:
    def __init__(self):
        self.final_placement = []

    def add_amino(self, amino):
        self.final_placement.append(amino)
        return self.final_placement
