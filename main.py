from code.classes import check, placement, protein
from code.classes.protein import Protein
from code.visualization.visualization import visualization


if __name__ == "__main__":
    while True:
         user_input = input("please enter your protein: ")
         protein = Protein()
         check = check.Check()

         if check.get_protein(user_input) != False:
            placement = placement.Placement(user_input, protein.final_placement)
            protein.add_amino(check.amino_0)
            print(protein)

         while True:
            if placement.set_coordinates() == False:
               # laat de visualisatie zien
               print("End of protein ------------------->>>>> :) :) :) :)")
               # return False
               exit()

            if placement.check_empty(check.user_input):
               print(placement.random_amino)
               print(protein.add_amino(placement.random_amino))
               print(protein.final_placement)
