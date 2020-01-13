from code.classes.check import Check
from code.classes.placement import Placement
from code.classes.protein import Protein
from code.classes.stability import Stability
from code.classes.csvwriter import Csv
from code.visualization.visualization import visualize



if __name__ == "__main__":
    user_input = input("please enter your protein: ").upper()
    while True:
        protein = Protein()
        check = Check()

            # (randomly) folds protein if user input is valid
        if check.get_protein(user_input) != False:
            placement = Placement(user_input, protein.final_placement)
            protein.add_amino(check.amino_0)
            print(protein)

        while True:

            # calculates stability score, adds values to csv and visualizes final product
            if placement.set_coordinates() == False:
                print("End of protein ------------------->>>>> :) :) :) :)")
                stability = Stability()
                print(stability.score(protein.final_placement, user_input))
                csvwriter = Csv(protein.final_placement)
                csvwriter.write_csv()
                csvwriter.visualization_csv()
                visualize('data/visualization.csv', user_input, stability.definitive_stability_score, placement.amino_stability_x, placement.amino_stability_y)
                exit()

            # checks if user input is valid
            if placement.check_empty(check.user_input):

                # checks if there aren't any possible coordinates left
                if len(placement.possible_coordinates) == 0:
                    break
                print(placement.random_amino)
                print(protein.add_amino(placement.random_amino))
                print(protein.final_placement)
