"""
csvwriter.py

Writes two different csv-files, one for the visualization and one for the
required output.

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor Programmeren
2020
"""

import csv

class Csv:
    def __init__(self, folds):
        self.folds = folds

    def write_csv(self):
        """
        Writes a csv file with the amino and fold
        """

        # opens the file
        with open('data/folds.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Amino", "Fold"])

            # writes the information to the csv file
            for fold in self.folds:
                writer.writerow([fold[0], fold[1]])

        self.visualization_csv()

    def visualization_csv(self):
        """
        Writes a csv file with the amino and the coordinates for the visualization
        """

        # opens the file
        with open('data/visualization.csv', 'w', newline='') as file:
            writer = csv.writer(file)

            # writes the information to the csv file
            for fold in self.folds:
                writer.writerow([fold[0], fold[2], fold[3]])
