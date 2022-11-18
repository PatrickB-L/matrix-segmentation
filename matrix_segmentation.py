import numpy as np
import pandas as pd


class Matrix:
    def __init__(self):
        self.change_was_made = None
        self.matrix = None
        self.label = None
        self.x_len = None
        self.x_right_edge_idx = None
        self.y_len = None
        self.y_lower_edge_idx = None

    def set_label(self, _label):
        self.label = _label

    def set_matrix_and_dynamic_bounds(self, _df):
        _df = pd.DataFrame(_df)
        self.matrix = _df

        self.x_len = len(_df)
        self.y_len = len(_df.columns)

        self.x_right_edge_idx = len(_df) - 1
        self.y_lower_edge_idx = len(_df.columns) - 1

    def if_needed_change_cell_and_all_followers(self, _x, _y):
        """
        If the value of the cell is 1, change it to a new label, and recursively
        give the same label to all his neighbors and neighbors and so on, that
        also have 1 for their value
        """
        cell_value = self.matrix.iloc[_x, _y]
        adjacents = self.coordinates_of_adjacents(_x, _y)

        if cell_value == 1:
            self.matrix.iloc[_x, _y] = self.label
            self.change_was_made = True

            for neighbors_coord in adjacents:
                _x, _y = neighbors_coord[0], neighbors_coord[1]
                if self.matrix.iloc[_x, _y] == 1:
                    self.if_needed_change_cell_and_all_followers(_x, _y)
        return

    def coordinates_of_adjacents(self, row_idx, col_idx):
        """
        return the coordinates of each adjacent cells, for a given cell,
        by a list of the tuple of their row and col indexes
        """
        coord_adjacents = []
        if row_idx == 0:
            if col_idx == 0:
                coord_adjacents = [(0, 1),
                                   (1, 0),
                                   (1, 1)]
            elif col_idx == self.x_right_edge_idx:
                coord_adjacents = [(0, self.x_right_edge_idx - 1),
                                   (1, self.x_right_edge_idx - 1),
                                   (1, self.x_right_edge_idx)]
            else:
                coord_adjacents = [(row_idx, col_idx - 1),
                                   (row_idx, col_idx + 1),
                                   (row_idx + 1, col_idx - 1),
                                   (row_idx + 1, col_idx),
                                   (row_idx + 1, col_idx + 1)]

        elif row_idx == self.y_lower_edge_idx:
            if col_idx == 0:
                coord_adjacents = [(self.y_lower_edge_idx - 1, 0),
                                   (self.y_lower_edge_idx - 1, 1),
                                   (self.y_lower_edge_idx, 1)]
            elif col_idx == self.x_len - 1:
                coord_adjacents = [(self.y_lower_edge_idx - 1,
                                    self.x_right_edge_idx - 1),
                                   (self.y_lower_edge_idx - 1,
                                    self.x_right_edge_idx),
                                   (self.y_lower_edge_idx,
                                    self.x_right_edge_idx - 1)]
            else:
                coord_adjacents = [(self.y_lower_edge_idx - 1, col_idx - 1),
                                   (self.y_lower_edge_idx - 1, col_idx),
                                   (self.y_lower_edge_idx - 1, col_idx + 1),
                                   (self.y_lower_edge_idx, col_idx - 1),
                                   (self.y_lower_edge_idx, col_idx + 1)]

        else:
            if col_idx == 0:
                coord_adjacents = [(row_idx + 1, 0),
                                   (row_idx + 1, 1),
                                   (row_idx, 1),
                                   (row_idx - 1, 0),
                                   (row_idx - 1, 1)]

            elif col_idx == self.x_right_edge_idx:
                coord_adjacents = [(row_idx + 1, self.x_right_edge_idx - 1),
                                   (row_idx + 1, self.x_right_edge_idx),
                                   (row_idx, self.x_right_edge_idx - 1),
                                   (row_idx - 1, self.x_right_edge_idx - 1),
                                   (row_idx - 1, self.x_right_edge_idx)]

            else:
                coord_adjacents = [(row_idx + 1, col_idx - 1),
                                   (row_idx + 1, col_idx),
                                   (row_idx + 1, col_idx + 1),
                                   (row_idx, col_idx - 1),
                                   (row_idx, col_idx + 1),
                                   (row_idx - 1, col_idx -1),
                                   (row_idx - 1, col_idx),
                                   (row_idx - 1, col_idx + 1)]

        return coord_adjacents

    def print_coordinates_of_items(self):
        """
        For each unique number in a matrix, print a Serie with the coordinates
        of every occurence of said number
        """
        unique = np.unique(np.array(self.matrix))
        unique_no_zero = np.delete(unique, np.where(unique == 0))
        for ele in unique_no_zero:
            coord = self.matrix.rename_axis(index='index',
                                            columns='col'
                                            ).stack().loc[lambda x: x == ele]
            print(f"\nCoordinates for the item represented by {ele}:")
            print(coord)


if __name__ == '__main__':
    mat = [[1, 1, 0, 1, 1, 1, 0, 1],
           [1, 1, 0, 1, 0, 1, 0, 1],
           [1, 1, 1, 1, 0, 0, 0, 1],
           [0, 0, 0, 0, 0, 0, 0, 1],
           [1, 1, 1, 1, 0, 1, 0, 1],
           [0, 0, 0, 1, 0, 1, 0, 1],
           [1, 1, 1, 1, 0, 0, 0, 1],
           [1, 1, 1, 1, 0, 1, 1, 1]]

    matrix = Matrix()

    matrix.set_matrix_and_dynamic_bounds(mat)
    matrix.set_label(2)

    for x in range(matrix.x_len):
        for y in range(matrix.y_len):

            if matrix.change_was_made:
                matrix.label += 1

            matrix.change_was_made = False
            matrix.if_needed_change_cell_and_all_followers(x, y)

    matrix.print_coordinates_of_items()
    print(f'\nTransformed matrix:\n{matrix.matrix}')

