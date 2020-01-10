from code.classes import check, placement, protein

if __name__ == "__main__":
    while True:
         user_input = input("please enter your protein: ")
         protein = protein.Protein()
         check = check.Check()

         if check.get_protein(user_input) != False:
            placement = placement.Placement(user_input, protein.final_placement)
            protein = protein.add_amino(check.amino_0)
            print(protein)

         if placement.set_coordinates() == False:
            # laat de visualisatie zien
            print("End of protein ------------------->>>>> :) :) :) :)")

         if placement.check_empty(check.user_input):
            print(placement.random_amino)
            print(protein)
            print(protein.add_amino(placement.random_amino))
