import csv
from subprocess import Popen

class Csv:
    def __init__(self, folds):
        self.folds = folds

    def write_csv(self):

        # Opens the file
        with open('folds.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amino", "Fold", "X coordinate", "Y Coordinate"])

            # Writes the information to the csv file
            for fold in self.folds:
                writer.writerow([fold[0], fold[1], fold[2], fold[3]])
            p = Popen('folds.csv', shell=True)

if __name__ == "__main__":
    listcheck = [['P', 2, 0, 0], ['H', 2, 0 , 1]]
    test = Csv(listcheck)
    test.write_csv()