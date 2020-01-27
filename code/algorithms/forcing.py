"""
forcing.py
Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020
"""
from code.classes.stability_score import Stability

class Force:
    def __init__(self,user_input):
        self.current_x = 0
        self.current_y = 0
        self.zijde_lengte = 1
        self.final_placement = []
        self.user_input = user_input[0]
        self.final_placement.append([self.user_input,2,self.current_x,self.current_y])

    def placing(self, user_input):
            for i in range(2):
                print("i",i)
                for j in range(self.zijde_lengte):
                    print("j",j)
                    print("m",self.zijde_lengte % 2)
                    if (self.zijde_lengte % 2) != 0 :
                        """ oneven """
                        self.oneven(i)
                    if (self.zijde_lengte % 2) == 0:
                        """ even """
                        print("even")
                        self.even(i)
            self.zijde_lengte += 1

    def oneven(self,i):
        if i == 0:
            print("HOOII")
            self.new_y = self.current_y + 1
            self.new_x = self.current_x
            self.current_fold = 1
        if i == 1:
            print("HIEERR")
            self.new_x = self.current_x + 1
            self.new_y = self.current_y
            self.current_fold = -2
        self.current_x = self.new_x
        self.current_y = self.new_y
        self.current_amino = user_input[len(self.final_placement)]
        self.final_placement.append([self.current_amino,self.current_fold,self.new_x,self.new_y])
        print(self.final_placement)
        return self.final_placement, self.current_x, self.current_y

    def even (self,i):
        if i == 0:
            self.new_x = self.current_x
            self.new_y = self.current_y -1
            self.current_fold = -1
        if i == 1:
            self.new_y = self.current_y
            self.new_x = self.current_x - 1
            self.current_fold = 2
        self.current_x = self.new_x
        self.current_y = self.new_y
        self.current_amino = user_input[len(self.final_placement)]
        self.final_placement.append([self.current_amino,self.current_fold,self.new_x,self.new_y])
        print(self.final_placement)
        return self.final_placement, self.current_x, self.current_y

    def run(self):
        """
        Runs forcing algorithm until all possible protein folds have between
        evaluated; determines best fold.
        """
        self.stability = Stability()

        score, stability_connections = self.stability.get_stability_score(self.final_placement)
        self.stability_coordinates = stability_connections
        self.stability.stability_score_coordinates(self.stability_coordinates)
        self.amino_stability_x = self.stability.amino_stability_x
        self.amino_stability_y = self.stability.amino_stability_y

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



force = Force(user_input)
force.placing(user_input)
