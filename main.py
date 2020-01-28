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

from code.algorithms.random import Random
from code.algorithms.fourfold import *
from code.algorithms.threefold import *
from code.algorithms.Threefoldonestep import *
from code.algorithms.depth_first import DepthFirst
from code.algorithms.branch_bound import BranchBound
from code.algorithms.forcing import Force

from code.visualization.visualization import visualize

def main():
    """
    Prompts user to choose an algorithm, runs chosen algorithm.
    """

    algorithm = 0

    while algorithm < 1 or algorithm > 7:
        while True:
            try:
                algorithm = int(input("Which algorithm would you like to use? \n1 for random algorithm \n2 for three fold one step \n3 for three fold three steps \n4 for four fold algorithm \n5 for depth first searh algorithm \n6 for branch and bound algorithm \n7 for the forcing algorithm\n"))
                break
            except ValueError:
                print("Invalid input")

    # prompts the user for the runamount for algorithms 1-4
    if algorithm > 0 and algorithm < 5:
        runamount = 0
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
        visualisation = random

        print("Random placement: ", random.best_protein)
        print("Score: ", random.best_score)

    elif algorithm == 2:
        """
        Threefold one step
        """

        three_fold_one_step = ThreeFoldOneStep(user_input, runamount)
        three_fold_one_step.run()
        visualisation = three_fold_one_step

        print("final placement: ", three_fold_one_step.best_placement)
        print("Best score: ", three_fold_one_step.best_score)


        """


        Hoiiiii

        Dit moet nog even gebeurd worden:

        .best_placement vervangen door .best_protein
        Scheelt weer regels code, dan hoeft visualisatie niet overal.
        Heb nu dit gedaan (hij werkt ook gewoon nu):

        self.best_score = score
        self.best_protein = self.best_placement

        Maar beter om dit in 1 keer te doen natuurlijk.
        oh en self.variabelen hoeven niet gereturned :)


        Oh en fourfold doet nog een beetje gek, best_placement kent 'ie niet en
        de visualisatie gaat ook niet goed.. weird


        Mag

        groetjes


        """

    elif algorithm == 3:
        """
        Threefold algorithm
        """

        three_fold = ThreeFold(user_input, runamount)
        three_fold.run()
        visualisation = three_fold

        print("final placement: ", three_fold.best_placement)
        print("Best score: ", three_fold.best_score)


    elif algorithm == 4:
        """
        Fourfold algorithm
        """

        four_fold = FourFold(user_input, runamount)
        four_fold.run()
        visualisation = four_fold

        print("final placement: ", four_fold.best_placement)
        print("Best score: ", four_fold.best_score)

    elif algorithm == 5:
        """
        Runs depth first algorithm
        """

        depth = DepthFirst(user_input)
        visualisation = depth

        # ensures results are still printed when algorithm is cut off
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

    elif algorithm == 7:
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

    # visualizes results of every algorithm
    csvwriter = Csv(visualisation.best_protein)
    csvwriter.write_csv()
    print(visualisation.amino_stability_x)
    print(visualisation.amino_stability_y)
    visualize('data/visualization.csv', user_input, visualisation.best_score, visualisation.amino_stability_x, visualisation.amino_stability_y)


if __name__ == "__main__":
    main()
