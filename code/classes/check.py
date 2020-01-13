class Check:
    def __init__(self):
        pass

    def get_protein(self, user_input):

        # checks if user_input exists
        if len(user_input) != 0:
            self.user_input = user_input

            # checks if user_input is valid
            for i in range(len(self.user_input)):
                if self.user_input[i] != "H" and self.user_input[i] != "P" and  self.user_input[i] !="C":
                    return False
            self.amino_0 = [self.user_input[0], 2, 0, 0]
            return self.amino_0, self.user_input
        return False
