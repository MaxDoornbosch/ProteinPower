"""
main.py

TODO:

"""
import timeit
from code.classes.placement import Placement
from code.classes.protein import Protein
from code.classes.stability import Stability
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.csvwriter import Csv
from code.visualization.visualization import visualize


from code.algorithms.threefoldonestep import *
from code.algorithms.threefold import *
from code.algorithms.random import *
from code.algorithms.depth_first import DepthFirst
from code.algorithms.branch_bound import BranchBound
from code.algorithms.fourfold import *


# prompts the user for an algorithm
algorithm = 0

while algorithm < 1 or algorithm > 7:
    while True:
        try:
            algorithm = int(input("Which algorithm would you like to use? Enter 1 for random algorithm, 2 for three fold one step, 3 for three fold three steps and 4 for four fold algorithm: "))
            break
        except ValueError:
            print("Invalid input")

# prompts the user for the runamount
runamount = 0
while runamount < 1:
    try:
        runamount = int(input("How many times would you like to run this algorithm? "))
        break
    except:
        print("Invalid input")

user_input = input("Please enter your protein (minimum length is 3): ").upper()

# minimum length of protein
while len(user_input) < 3:
    user_input = input("Please enter your protein (minimum length is 3): ").upper()

# checks if user_input is valid
for i in range(len(user_input)):
    while user_input[i] != "H" and user_input[i] != "P" and user_input[i] !="C":
        user_input = input("Please enter your protein (minimum length is 3): ").upper()



if algorithm == 1:
    """
    Random algorithm
    """
    random = Random(user_input, runamount)
    random.run()
    visualisation = random

    print("Final random placement: ", random.random_placement)
    # print("Best score: ", score)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)

elif algorithm == 2:
    """
    Threefold one step
    """

    start = timeit.default_timer()
    score = 0
    for z in range(runamount):

        done = False

        # Restarts the program if an error occurs
        while done == False:

            # sets first fold and adds to final
            protein = Protein(user_input)


            # splits protein sequence into chunks of three amino acids
            user_input_split = split_protein(user_input)

            # updates x,y coordinates based on most recently determined fold
            coordinate_update = CoordinateUpdate()
            coordinate_update.update_coordinates(protein.final_placement)

            amino_stability_x = []
            amino_stability_y = []

            for i in range(len(user_input_split)):

                current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)

                # extracts most recently added fold and amino and performs three fold algorithm
                current_fold = protein.final_placement[-1][1]

                # gets the current amino
                current_amino = user_input[len(protein.final_placement)]

                best_option = three_fold(protein.final_placement, user_input_split, current_fold, current_x, current_y, current_amino, i)

                # checks if an error has occured
                if best_option == False:
                    break

                # ensures no empty lists are appended
                if best_option[-2]:
                    amino_stability_x.extend(best_option[-2])
                if best_option[-1]:
                    amino_stability_y.extend(best_option[-1])

                placement = [current_amino, best_option[0], current_x, current_y]
                protein.add_amino_info(placement)

                if current_fold != 0:
                    current_x, current_y = coordinate_update.update_coordinates(protein.final_placement)

                # checks if last amino of sequence is reached
                if len(protein.final_placement) == (len(user_input) - 1):
                    protein.add_last_amino_of_chunk_without_score(current_x, current_y, user_input)

                # end of protein has been reached
                if protein.final_placement[-1][1] == 0:
                    done = True
                    stability = Stability()
                    stability_score = stability.score(protein.final_placement, user_input)

                    # checks if current score is lower than the current lowest score
                    if stability_score < score:
                            score = stability_score
                            best_placement = protein.final_placement
                            best_stability = stability.definitive_stability_score
                            best_amino_stability_x = amino_stability_x
                            best_amino_stability_y = amino_stability_y

    print("final placement: ", best_placement)
    print("Best score: ", score)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    csvwriter = Csv(best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, best_stability, best_amino_stability_x, best_amino_stability_y)

elif algorithm == 3:
    """
    Threefold algorithm
    """


    start = timeit.default_timer()
    score = 0
    for z in range(runamount):

        done = False

        # Restarts the program if an error occurs
        while done == False:

            # sets first fold and adds to final
            protein = Protein(user_input)


            # splits protein sequence into chunks of three amino acids
            user_input_split = split_protein(user_input)

            # updates x,y coordinates based on most recently determined fold
            coordinate_update = CoordinateUpdate()
            coordinate_update.update_coordinates(protein.final_placement)

            amino_stability_x = []
            amino_stability_y = []

            for i in range(len(user_input_split)):

                current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)

                # extracts most recently added fold and amino and performs three fold algorithm
                current_fold = protein.final_placement[-1][1]

                # gets the current amino
                current_amino = user_input[len(protein.final_placement)]

                best_option = three_fold(protein.final_placement, user_input_split, current_fold, current_x, current_y, current_amino, i)

                # checks if an error has occured
                if best_option == False:
                    break

                # ensures no empty lists are appended
                if best_option[-2]:
                    amino_stability_x.extend(best_option[-2])
                if best_option[-1]:
                    amino_stability_y.extend(best_option[-1])

                for i in range(len(best_option) - 3):
                    protein.add_amino_info(best_option[i])

                if current_fold != 0:
                    current_x, current_y = coordinate_update.update_coordinates(protein.final_placement)

                # checks if last amino of sequence is reached
                if len(protein.final_placement) == (len(user_input) - 1):
                    protein.add_last_amino_of_chunk_without_score(current_x, current_y, user_input)

                # end of protein has been reached
                if protein.final_placement[-1][1] == 0:
                    done = True
                    stability = Stability()
                    stability_score = stability.score(protein.final_placement, user_input)

                    # checks if current score is lower than the current lowest score
                    if stability_score < score:
                            score = stability_score
                            best_placement = protein.final_placement
                            best_stability = stability.definitive_stability_score
                            best_amino_stability_x = amino_stability_x
                            best_amino_stability_y = amino_stability_y

    print("final placement: ", best_placement)
    print("Best score: ", score)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    csvwriter = Csv(best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, best_stability, best_amino_stability_x, best_amino_stability_y)

elif algorithm == 4:
    """
    Fourfold algorithm
    """

    start = timeit.default_timer()
    score = 0
    for z in range(runamount):
        done = False

        # Restarts the program if an error occurs
        while done == False:

            # sets first fold and adds to final
            protein = Protein(user_input)


            # splits protein sequence into chunks of three amino acids
            user_input_split = split_protein(user_input)

            # updates x,y coordinates based on most recently determined fold
            coordinate_update = CoordinateUpdate()
            coordinate_update.update_coordinates(protein.final_placement)

            amino_stability_x = []
            amino_stability_y = []

            for i in range(len(user_input_split)):

                current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)

                # extracts most recently added fold and amino and performs three fold algorithm
                current_fold = protein.final_placement[-1][1]

                # gets the current amino
                current_amino = user_input[len(protein.final_placement)]

                best_option = four_fold(protein.final_placement, user_input_split, current_fold, current_x, current_y, current_amino, i)

                #checks if an error has occured
                if best_option == False:
                    break

                # ensures no empty lists are appended
                if best_option[-2]:
                    amino_stability_x.extend(best_option[-2])
                if best_option[-1]:
                    amino_stability_y.extend(best_option[-1])

                for i in range(len(best_option) - 3):
                    protein.add_amino_info(best_option[i])

                if current_fold != 0:
                    current_x, current_y = coordinate_update.update_coordinates(protein.final_placement)

                # checks if last amino of sequence is reached
                if len(protein.final_placement) == (len(user_input) - 1):
                    protein.add_last_amino_of_chunk_without_score(current_x, current_y, user_input)

                # end of protein has been reached
                if protein.final_placement[-1][1] == 0:
                    done = True
                    stability = Stability()
                    stability_score = stability.score(protein.final_placement, user_input)

                    # checks if current score is lower than the current lowest score
                    if stability_score < score:
                        score = stability_score
                        best_placement = protein.final_placement
                        best_stability = stability.definitive_stability_score
                        best_amino_stability_x = amino_stability_x
                        best_amino_stability_y = amino_stability_y

    print("final placement: ", best_placement)
    print("Best score: ", score)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    csvwriter = Csv(best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, best_stability, best_amino_stability_x, best_amino_stability_y)


elif algorithm == 5:
    """
    Runs depth first algorithm
    """

    depth = DepthFirst(user_input)
    visualisation = depth

    try:
        depth.run()
    except (KeyboardInterrupt, SystemExit):
        print("\nKeyboard Interrupt.\n")


    if depth.best_score == 0:
        print("\nLowest score: 0")
    else:
        print("\nLowest score: ", depth.best_score)
        print("\nBest protein: ", depth.best_protein)

elif algorithm == 6:
    """
    Branch and bound (depth first) algorithm
    """

    branch_bound = BranchBound(user_input)
    branch_bound.run()
    visualisation = branch_bound

    if branch_bound.best_score == 0:
        print("\nLowest score: 0")
        #print("\nTime: ", depth.time)
    else:
        print("\nLowest score: ", branch_bound.best_score)
        print("\nBest protein: ", branch_bound.best_protein)
        #print("\nTime: ", depth.time)


csvwriter = Csv(visualisation.best_protein)
csvwriter.write_csv()
csvwriter.visualization_csv()
visualize('data/visualization.csv', user_input, visualisation.best_score, visualisation.amino_stability_x, visualisation.amino_stability_y)
