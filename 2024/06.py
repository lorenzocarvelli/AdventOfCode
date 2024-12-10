from copy import deepcopy
from typing import Tuple, Dict, List

from base import DailyPuzzle


class Day6(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "6")
        self.step_dict: Dict[str, Tuple[int, int]] = {
            "N": (-1, 0),
            "S": (1, 0),
            "E": (0, 1),
            "W": (0, -1)
        }
        self.ninety_deg_right: Dict[str, str] = {
            "N": "E",
            "S": "W",
            "E": "S",
            "W": "N"
        }

    def simulate_path(self, current_position: Tuple[int, int], current_direction: str,
                      coordinates_grid: Dict[Tuple[int, int], str]) -> Tuple[List[Tuple[int, int]], bool]:
        positions_occupied = [current_position]
        infinite_loop = True

        while True:

            # Infinite loop test
            infinite_loop_test = len(positions_occupied) / len(list(set(positions_occupied))) > 4
            if infinite_loop_test:
                return positions_occupied, infinite_loop

            new_step = self.step_dict[current_direction]
            new_position = (current_position[0] + new_step[0], current_position[1] + new_step[1])

            if new_position not in coordinates_grid:
                infinite_loop = False
                break

            if coordinates_grid[new_position] == "#":
                new_direction = self.ninety_deg_right[current_direction]
                current_direction = new_direction
                continue

            current_position = new_position
            positions_occupied.append(current_position)

        return positions_occupied, infinite_loop

    def solve(self):
        # Creating a grid of coordinates with the corresponding symbol in the input data
        coordinates_grid = dict()
        initial_position = None
        for row_idx, row in enumerate(self.data):
            for col_idx, cc in enumerate(row):
                if cc == "^":
                    initial_position = (row_idx, col_idx)
                    coordinates_grid[(row_idx, col_idx)] = "."
                    continue
                coordinates_grid[(row_idx, col_idx)] = cc

        # Solution of Part 1
        current_direction = "N"
        current_position = initial_position
        positions_occupied, _ = self.simulate_path(current_position, current_direction, coordinates_grid)
        sol_1 = len(list(set(positions_occupied)))  # This ensures to only consider the unique positions.
        print(sol_1)

        # Brute force solution for Part 2
        sol_2 = 0
        for coordinate_k, symbol in coordinates_grid.items():
            if symbol in ["#", "^"]:  # Cannot place an obstacle where the guard is or where another obstacle already is
                continue

            modified_grid = deepcopy(coordinates_grid)
            modified_grid[coordinate_k] = "#"

            current_direction = "N"
            current_position = initial_position
            _, infinite_loop = self.simulate_path(current_position, current_direction, modified_grid)
            if infinite_loop:
                sol_2 += 1

        print(sol_2-1)


if __name__ == "__main__":
    day_6 = Day6()
    day_6.solve()
