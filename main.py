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
from code.algorithms.fourfold import *
from code.algorithms.threefold import *
from code.algorithms.Threefoldonestep import *
from code.algorithms.threefold import *
from code.algorithms.random import *
from code.algorithms.depth_first import DepthFirst
from code.algorithms.branch_bound import BranchBound
from code.algorithms.fourfold import *
from code.algorithms.forcing import Force


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
if algorithm > 0 and algorithm < 5:
    while runamount < 1:
        try:
            runamount = int(input("How many times would you like to run this algorithm? "))
            break
        except ValueError:
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

    print("Final random placement: ", random.random_placement)
    # print("Best score: ", score)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    csvwriter = Csv(random.best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, random.best_stability, random.best_amino_stability_x, random.best_amino_stability_y)

elif algorithm == 2:
    """
    Threefold one step
    """

    three_fold_one_step = ThreeFoldOneStep(user_input, runamount)
    three_fold_one_step.run()

    print("final placement: ", three_fold_one_step.best_placement)
    # print("Best score: ", score)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    csvwriter = Csv(three_fold_one_step.best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, three_fold_one_step.best_stability, three_fold_one_step.best_amino_stability_x, three_fold_one_step.best_amino_stability_y)

elif algorithm == 3:
    """
    Threefold algorithm
    """

    three_fold = ThreeFold(user_input, runamount)
    three_fold.run()    

    print("final placement: ", three_fold.best_placement)
    # print("Best score: ", score)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    csvwriter = Csv(three_fold.best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, three_fold.best_stability, three_fold.best_amino_stability_x, three_fold.best_amino_stability_y)

elif algorithm == 4:
    """
    Fourfold algorithm
    """
    
    four_fold = FourFold(user_input, runamount)
    four_fold.run() 

    print("final placement: ", four_fold.best_placement)
    # print("Best score: ", score)
    # stop = timeit.default_timer()
    # print('Time: ', stop - start)
    csvwriter = Csv(four_fold.best_placement)
    csvwriter.write_csv()
    csvwriter.visualization_csv()
    visualize('data/visualization.csv', user_input, four_fold.best_stability, four_fold.best_amino_stability_x, four_fold.best_amino_stability_y)



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

    if branch_bound.best_score == 1:
        print("\nLowest score: 0")
        exit()

    else:
        print("\nLowest score: ", branch_bound.best_score)
        print("\nBest protein: ", branch_bound.best_protein)
        #print("\nTime: ", depth.time)




if algorithm == 7:
    """
    Runs forcing algorithm

    """
    force = Force(user_input)
    visualisation = force
    try:
        force.run()
    except (KeyboardInterrupt, SystemExit):
        print("\nKeyboard Interrupt.\n")

    print("final placement: ", force.placing())

csvwriter = Csv(visualisation.best_protein)
csvwriter.write_csv()
csvwriter.visualization_csv()
visualize('data/visualization.csv', user_input, visualisation.best_score, visualisation.amino_stability_x, visualisation.amino_stability_y)
