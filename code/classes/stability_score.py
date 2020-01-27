class Stability:
    """
    Calculates stability score of a (finished) protein.
    """

    def __init__(self):
        pass

    def get_stability_score(self, current_path):

        # finds coordinates of C and H amino acids
        self.coordinates_of_C_H_aminos(current_path)

        score = 0
        i = 0
        stability_connections = []

        for amino in current_path:
            if amino[0] == "H" or amino[0] == "C":
                surrounding_coordinates, x, y = self.surrounding_coordinates(amino, current_path, i)

                # checks and calculates score
                for coordinates in surrounding_coordinates:
                    potential_connection = [coordinates, [x, y]]

                    # ensures stability connections aren't calculated twice
                    score, stability_connections = self.calculate_score(amino, stability_connections, potential_connection, coordinates, score)

            i += 1

        return score, stability_connections


    def surrounding_coordinates(self, amino, current_path, i):
        """
        Returns surrounding coordinates of a given amino acid, whilst excluding
        the coordinates of connected amino acids.
        """

        x = amino[2]
        y = amino[3]
        surrounding_coordinates = [[x + 1, y], [x - 1, y], [x, y + 1], [x, y - 1]]

        if amino != current_path[0]:
            connected_x = current_path[i - 1][2]
            connected_y = current_path[i - 1][3]
            surrounding_coordinates.remove([connected_x, connected_y])

        if amino != current_path[-1]:
            connected_x = current_path[i + 1][2]
            connected_y = current_path[i + 1][3]
            surrounding_coordinates.remove([connected_x, connected_y])

        return surrounding_coordinates, x, y


    def calculate_score(self, amino, stability_connections, potential_connection, coordinates, score):
        """
        Calculates score and ensures stability connections aren't calculated twice.
        """

        if self.already_calculated(stability_connections, potential_connection, score):
            return score, stability_connections

        if amino[0] == "H":
            if coordinates in self.h_coordinates or coordinates in self.c_coordinates:
                score -= 1
                stability_connections.append(potential_connection)

        elif amino[0] == "C":
            if coordinates in self.h_coordinates:
                score -= 1
                stability_connections.append(potential_connection)
            elif coordinates in self.c_coordinates:
                score -= 5
                stability_connections.append(potential_connection)

        return score, stability_connections


    def already_calculated(self, stability_connections, potential_connection, score):
        """
        True if stability between two amino acids was already calculated.
        """

        if stability_connections:
            for connection in stability_connections:
                if sorted(connection) == sorted(potential_connection):
                    return True

        return False


    def coordinates_of_C_H_aminos(self, current_path):
        """
        Extracts coordinates of all H and C aminos from current path.
        """
        self.h_coordinates = []
        self.c_coordinates = []

        for path in current_path:
            if path[0] == "H" and [path[2], path[3]] not in self.h_coordinates:
                self.h_coordinates.append([path[2], path[3]])
            elif path[0] == "C" and [path[2], path[3]] not in self.c_coordinates:
                self.c_coordinates.append([path[2], path[3]])


    def stability_score_coordinates(self, stability_coordinates):
        """
        Creates coordinate lists for the visualisation of the stability score.
        """

        self.amino_stability_x = []
        self.amino_stability_y = []

        for i in stability_coordinates:
            self.amino_stability_x.append([i[0][0], i[1][0]])
            self.amino_stability_y.append([i[0][1], i[1][1]])
