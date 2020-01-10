import csv
from subprocess import Popen

class Csv:
    def __init__(self, folds):
        self.folds = folds

    def write_csv(self):

        # Opens the file
        with open('data/folds.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amino", "Fold"])

            # Writes the information to the csv file
            for fold in self.folds:
                writer.writerow([fold[0], fold[1]])
            # p = Popen('data/folds.csv', shell=True)
        return True

    def visualization(self):
        # Opens the file
        with open('data/visualization.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # Writes the information to the csv file
            for fold in self.folds:
                writer.writerow([fold[0], fold[2], fold[3]])
        return True