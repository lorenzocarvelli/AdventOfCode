from typing import Tuple, List
from itertools import combinations

from base import DailyPuzzle


class Day8(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "8")

    def solve(self):
        # Parsing data into a dict where each antenna type has a list of coordinates where that antenna type is present
        n_rows = len(self.data)
        n_cols = len(self.data[0])

        antennas = dict()
        for row_idx, ll in enumerate(self.data):
            for col_idx, cc in enumerate(ll):
                if cc == ".":
                    continue

                if cc not in antennas:
                    antennas[cc] = []

                antennas[cc].append((row_idx, col_idx))

        antinodes = []
        for antenna_type, positions_list in antennas.items():
            positions_combinations = list(combinations(positions_list, 2))

            for p1, p2 in positions_combinations:
                a1, a2 = self.calculate_antinodes_coordinates(p1, p2)
                if self.check_position_within_bounds(a1, n_rows, n_cols):
                    antinodes.append(a1)
                if self.check_position_within_bounds(a2, n_rows, n_cols):
                    antinodes.append(a2)

        sol_1 = len(list(set(antinodes)))
        print(sol_1)

        # Part 2: antinodes are generated on the same line N times (as long as we are within map bounds)
        antinodes_pt2 = []
        for antenna_type, positions_list in antennas.items():
            positions_combinations = list(combinations(positions_list, 2))

            for p1, p2 in positions_combinations:
                antinodes_list = self.calculate_antinodes_coordinates_on_line(p1, p2, n_rows, n_cols)

                # If at least one antinode is created on that line, then both original antennas become antinodes
                antinodes_pt2.append(p1)
                antinodes_pt2.append(p2)

                for anc in antinodes_list:
                    antinodes_pt2.append(anc)

        sol_2 = len(list(set(antinodes_pt2)))
        print(sol_2)

    def calculate_antinodes_coordinates_on_line(self, p1: Tuple[int, int], p2: Tuple[int, int], n_rows: int, n_cols: int) -> List[Tuple[int, int]]:
        out = []

        delta_1 = (p1[0] - p2[0], p1[1] - p2[1])
        delta_2 = (p2[0] - p1[0], p2[1] - p1[1])

        current_p1 = p1
        while True:
            new_p1 = (current_p1[0] + delta_1[0], current_p1[1] + delta_1[1])
            if not self.check_position_within_bounds(new_p1, n_rows, n_cols):
                break
            out.append(new_p1)
            current_p1 = new_p1

        current_p2 = p2
        while True:
            new_p2 = (current_p2[0] + delta_2[0], current_p2[1] + delta_2[1])
            if not self.check_position_within_bounds(new_p2, n_rows, n_cols):
                break
            out.append(new_p2)
            current_p2 = new_p2

        return out

    @staticmethod
    def check_position_within_bounds(input_p: Tuple[int, int], n_rows: int, n_cols: int):
        return 0 <= input_p[0] < n_rows and 0 <= input_p[1] < n_cols

    @staticmethod
    def calculate_antinodes_coordinates(p1: Tuple[int, int], p2: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int]]:
        delta_1 = (p1[0] - p2[0], p1[1] - p2[1])
        delta_2 = (p2[0] - p1[0], p2[1] - p1[1])

        out_1 = (p1[0] + delta_1[0], p1[1] + delta_1[1])
        out_2 = (p2[0] + delta_2[0], p2[1] + delta_2[1])

        return out_1, out_2


if __name__ == "__main__":
    day_8 = Day8()
    day_8.solve()
