from code.classes import check, placement, protein
from code.classes.protein import Protein
from code.classes.stability import Stability
from code.classes.csvwriter import Csv
from code.visualization.visualization import visualize




if __name__ == "__main__":
    while True:
         visualize('data/example.txt')
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
               stability = Stability()
               print(stability.score(protein.final_placement, user_input))
               csvwriter = Csv(protein.final_placement)
               csvwriter.write_csv()
               exit()

            if placement.check_empty(check.user_input):
               print(placement.random_amino)
               print(protein.add_amino(placement.random_amino))
               print(protein.final_placement)
