"""
main.py

TODO:

- Uiteindelijke stability berekenen
"""
import timeit
from code.classes.placement import Placement
from code.classes.protein import Protein
from code.classes.stability import Stability
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.csvwriter import Csv
from code.visualization.visualization import visualize

algorithm = 0
while algorithm < 1 or algorithm > 4:
    while True:
        try:
            algorithm = int(input("Which algorithm would you like to use? Enter 1 for three fold one step, 2 for three fold three steps, 3 for four fold four steps and 4 is random algorithm: "))
            break
        except:
            print("Invalid input")

runamount = 0
while runamount < 1:
    while True:
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
    Threefold one step
    """

    from code.algorithms.Threefoldonestep import *
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

            # quits updating once end of sequence has been reached
            if coordinate_update == False:
                exit()

            amino_stability_x = []
            amino_stability_y = []

            for i in range(len(user_input_split)):

                current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)

                # extracts most recently added fold and amino and performs three fold algorithm
                current_fold = protein.final_placement[-1][1]

                # -1 want user input begint bij 0 en len van lijst niet
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
                    
                if protein.final_placement[-1][1] == 0:
                    done = True
                    print("End of protein ------------------->>>>> :) :) :) :)")
                    stability = Stability()
                    stability_score = stability.score(protein.final_placement, user_input)
                    if stability_score < score:
                            score = stability_score
                            best_placement = protein.final_placement
                            best_stability = stability.definitive_stability_score
                            best_amino_stability_x = amino_stability_x
                            best_amino_stability_y = amino_stability_y
                    # csvwriter = Csv(protein.final_placement)
                    # csvwriter.write_csv()
                    # csvwriter.visualization_csv()
                    # visualize('data/visualization.csv', user_input, stability.definitive_stability_score, amino_stability_x, amino_stability_y)

            print("check final placement", protein.final_placement)
    print("Best score: ", score)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    csvwriter = Csv(best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, best_stability, best_amino_stability_x, best_amino_stability_y)
    
if algorithm == 2:
    """
    Threefold algorithm
    """

    from code.algorithms.threefold import *
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

            # quits updating once end of sequence has been reached
            if coordinate_update == False:
                exit()

            amino_stability_x = []
            amino_stability_y = []

            for i in range(len(user_input_split)):

                current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)

                # extracts most recently added fold and amino and performs three fold algorithm
                current_fold = protein.final_placement[-1][1]

                # -1 want user input begint bij 0 en len van lijst niet
                current_amino = user_input[len(protein.final_placement)]

                best_option = three_fold(protein.final_placement, user_input_split, current_fold, current_x, current_y, current_amino, i)

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

                if protein.final_placement[-1][1] == 0:
                    done = True
                    print("End of protein ------------------->>>>> :) :) :) :)")
                    stability = Stability()
                    stability_score = stability.score(protein.final_placement, user_input)
                    if stability_score < score:
                            score = stability_score
                            best_placement = protein.final_placement
                            best_stability = stability.definitive_stability_score
                            best_amino_stability_x = amino_stability_x
                            best_amino_stability_y = amino_stability_y
                    print(stability_score)
                    # csvwriter = Csv(protein.final_placement)
                    # csvwriter.write_csv()
                    # csvwriter.visualization_csv()
                    # visualize('data/visualization.csv', user_input, stability.definitive_stability_score, amino_stability_x, amino_stability_y)

            print("check final placement", protein.final_placement)
    print("Best score: ", score)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    csvwriter = Csv(best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, best_stability, best_amino_stability_x, best_amino_stability_y)

if algorithm == 3:
    """
    Fourfold algorithm
    """
    from code.algorithms.fourfold import *

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
            print(protein.final_placement)
            # updates x,y coordinates based on most recently determined fold
            coordinate_update = CoordinateUpdate()
            coordinate_update.update_coordinates(protein.final_placement)

            # quits updating once end of sequence has been reached
            if coordinate_update == False:
                exit()

            amino_stability_x = []
            amino_stability_y = []

            for i in range(len(user_input_split)):

                current_x, current_y  = coordinate_update.update_coordinates(protein.final_placement)

                # extracts most recently added fold and amino and performs three fold algorithm
                current_fold = protein.final_placement[-1][1]

                # -1 want user input begint bij 0 en len van lijst niet
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

                if protein.final_placement[-1][1] == 0:
                    done = True
                    print("End of protein ------------------->>>>> :) :) :) :)")
                    stability = Stability()
                    stability_score = stability.score(protein.final_placement, user_input)
                    if stability_score < score:
                        score = stability_score
                        best_placement = protein.final_placement
                        best_stability = stability.definitive_stability_score
                        best_amino_stability_x = amino_stability_x
                        best_amino_stability_y = amino_stability_y

                    print(stability_score)
                    # csvwriter = Csv(protein.final_placement)
                    # csvwriter.write_csv()
                    # csvwriter.visualization_csv()
                    # visualize('data/visualization.csv', user_input, stability.definitive_stability_score, amino_stability_x, amino_stability_y)

            print("check final placement", protein.final_placement)

    print("Best score: ", score)
    stop = timeit.default_timer()
    print('Time: ', stop - start)
    csvwriter = Csv(best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, best_stability, best_amino_stability_x, best_amino_stability_y)

if algorithm == 4:
    """
    Random algorithm
    """
    current_n = 1
    protein = Protein(user_input)
    placement = Placement(user_input, protein.final_placement)
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

            # checks if there aren't any possible coordinates left
            if len(placement.possible_coordinates) == 0:
                break
            print(placement.random_amino)
            print(protein.add_amino_info(placement.random_amino))
            print(protein.final_placement)

