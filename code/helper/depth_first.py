"""
depth_first.py

Helper function for depth first search algorithms (depth_first.py and branch_bound.py)

Florien Altena, Emily van Veen, Max Doornbosch
UvA, minor programmeren
2020
"""

from code.classes.stability_score import Stability


def finish_protein(score, stability_connections):
    """
    Calculates final stability score for each protein, checks for new best
    scores and prepares data for the visualization of the final best protein
    folds.
    """

    stability = Stability()

    stability_coordinates = stability_connections

    # creates needed lists for the visualisation of the final protein
    stability.stability_score_coordinates(stability_coordinates)
    amino_stability_x = stability.amino_stability_x
    amino_stability_y = stability.amino_stability_y

    return amino_stability_x, amino_stability_y
