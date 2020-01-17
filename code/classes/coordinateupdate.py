"""
coordinateupdate.py

Returns coordinates based on folds
"""


class CoordinateUpdate:
    def __init__(self, final_placement):
        self.final_placement = final_placement

    def update_coordinates(self, final_placement):
        """
        Updates coordinates based on folds
        """

        self.final_placement = final_placement
        self.current_x = self.final_placement[-1][2]
        self.current_y = self.final_placement[-1][3]
        self.current_fold = self.final_placement[-1][1]

        if self.current_fold == 1:
            self.current_x += 1
        elif self.current_fold == -1:
            self.current_x -= 1
        elif self.current_fold == 2:
            self.current_y += 1
        elif self.current_fold == -2:
            self.current_y -= 1

        return self.current_x, self.current_y
