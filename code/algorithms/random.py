from code.classes.protein import Protein
from code.classes.coordinateupdate import CoordinateUpdate
from code.classes.placement import Placement
from code.classes.stability import Stability


import timeit


class Random:
    """
    Returns a random solution to the protein folding problem
    """
    def __init__(self, user_input, runamount):
        self.user_input = user_input
        self.runamount = runamount
        self.best_placement = []



        self.stability = Stability()

        score, stability_connections = self.stability.get_stability_score(self.final_placement)
        self.stability_coordinates = stability_connections
        self.stability.stability_score_coordinates(self.stability_coordinates)
        self.amino_stability_x = self.stability.amino_stability_x
        self.amino_stability_y = self.stability.amino_stability_y


        #visualize('data/visualization.csv', user_input, depth.best_score, depth.amino_stability_x, depth.amino_stability_y)



    def run(self):
        """
        Runs random algorithm
        """
        start = timeit.default_timer()
        score = 0
        for z in range(self.runamount):

            done = False

            # restarts when there aren't any options left for the next amino
            while done == False:
                current_n = 1
                protein = Protein(self.user_input)
                placement = Placement(self.user_input, protein.final_placement)
                finished = False
                while finished == False:

                    placement.set_current(current_n)

                    # end of protein has been reached
                    if placement.set_coordinates() == False:
                        done = True
                        stability = Stability()
                        stability_score = stability.score(protein.final_placement, self.user_input)

                        # checks if current score is lower than the current lowest score
                        if stability_score < score:
                            score = stability_score
                            self.best_placement = protein.final_placement
                            best_stability = stability.definitive_stability_score
                            best_amino_stability_x = placement.amino_stability_x
                            best_amino_stability_y = placement.amino_stability_y

                        finished = True

                    # checks if the last amino has been placed
                    if finished == False:

                        placement.check_empty(self.user_input)

                        # checks if there aren't any possible coordinates left
                        if len(placement.possible_coordinates) == 0:
                            break

                        placement.random_amino
                        protein.add_amino_info(placement.random_amino)
                        protein.final_placement

        self.random_placement = protein.final_placement
        return self.random_placement
