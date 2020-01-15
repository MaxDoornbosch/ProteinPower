from code.classes.placement import Placement
from code.classes.protein import Protein
from code.classes.stability import Stability
from code.classes.csvwriter import Csv
from code.visualization.visualization import visualize
from code.algorithms.threefold import Three_Fold


if __name__ == "__main__":
    user_input = input("Please enter your protein (minimum length is 3): ").upper()

    # minimum length of protein
    while len(user_input) <= 3:
        user_input = input("Please enter a valid protein (minimum length is 3): ").upper()

    # checks if user_input is valid
    for i in range(len(user_input)):
        while user_input[i] != "H" and user_input[i] != "P" and user_input[i] !="C":
            user_input = input("Please enter a valid protein (minimum length is 3): ").upper()

    amino_0 = [user_input[0], 2, 0, 0]
    protein = Protein()
    protein.add_amino(amino_0)
    print(protein)
    current_n = 1
    three_fold = Three_Fold()
    three_fold.define_folds("HHH", 2, 0, 1)
    three_fold.set_coordinates("P")
    three_fold.stability_score(protein.final_placement)
    three_fold.best_options()



"""
    while True:
        placement.set_current(current_n)

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



"""
