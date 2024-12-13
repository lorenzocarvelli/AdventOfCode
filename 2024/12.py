from typing import Dict, Tuple, List

from base import DailyPuzzle


class Day12(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "12")

    def solve(self):
        coordinates_dict = dict()
        n_rows = len(self.data)
        n_cols = len(self.data[0])
        for row_idx, row in enumerate(self.data):
            for col_idx, cc in enumerate(row):
                coordinates_dict[(row_idx, col_idx)] = cc

        sol_1 = 0
        already_examined_coordinates = []
        total_length = len(list(coordinates_dict.keys()))
        coordinates_keys = sorted(list(coordinates_dict.keys()))
        while len(already_examined_coordinates) < total_length:

            perimeter = 0
            area = 0
            adjacent_identical_coordinates = [coordinates_keys[0]]

            while len(adjacent_identical_coordinates):
                current_coordinates = adjacent_identical_coordinates[0]

                n_diff_neighbors, identical_neighbors_coordinates = self.count_different_neighbors(coordinates_dict, already_examined_coordinates, current_coordinates, n_rows, n_cols)
                adjacent_identical_coordinates.pop(0)

                # Updating area and perimeter
                area += 1
                perimeter += n_diff_neighbors

                adjacent_identical_coordinates.extend(identical_neighbors_coordinates)
                adjacent_identical_coordinates = list(set(adjacent_identical_coordinates))  # Ensuring unicity

                already_examined_coordinates.append(current_coordinates)
                coordinates_keys.remove(current_coordinates)

            sol_1 += area * perimeter

        print(sol_1)

    @staticmethod
    def count_different_neighbors(coordinates_dict: Dict[Tuple[int, int], str], already_examined_coordinates: List[Tuple[int, int]],
                                  input_coordinates: Tuple[int, int], n_rows: int, n_cols: int) -> Tuple[int, List[Tuple[int, int]]]:
        up = (-1, 0)
        down = (1, 0)
        left = (0, -1)
        right = (0, 1)

        coordinates_up = (input_coordinates[0] + up[0], input_coordinates[1] + up[1])
        coordinates_down = (input_coordinates[0] + down[0], input_coordinates[1] + down[1])
        coordinates_left = (input_coordinates[0] + left[0], input_coordinates[1] + left[1])
        coordinates_right = (input_coordinates[0] + right[0], input_coordinates[1] + right[1])

        current_letter = coordinates_dict[input_coordinates]

        out = 0
        identical_coordinates = []

        # Considering edges of the map as different neighbors (fence must be put up there)
        if coordinates_up[0] < 0:
            out += 1
        elif coordinates_dict[coordinates_up] != current_letter:
            out += 1
        else:
            identical_coordinates.append(coordinates_up)

        if coordinates_down[0] >= n_rows:
            out += 1
        elif coordinates_dict[coordinates_down] != current_letter:
            out += 1
        else:
            identical_coordinates.append(coordinates_down)

        if coordinates_left[1] < 0:
            out += 1
        elif coordinates_dict[coordinates_left] != current_letter:
            out += 1
        else:
            identical_coordinates.append(coordinates_left)

        if coordinates_right[1] >= n_cols:
            out += 1
        elif coordinates_dict[coordinates_right] != current_letter:
            out += 1
        else:
            identical_coordinates.append(coordinates_right)

        identical_coordinates = [ic for ic in identical_coordinates if ic not in already_examined_coordinates]

        return out, identical_coordinates


if __name__ == "__main__":
    day_12 = Day12()
    day_12.solve()
