from copy import deepcopy
from itertools import combinations

from base import DailyPuzzle


class Day11(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "11")

    def solve(self):
        unexpanded_data = deepcopy(self.data)

        # Find rows and columns with no galaxies
        no_galaxies_rows = []
        columns = ["" for _ in range(len(self.data[0]))]
        no_galaxies_columns = []
        for r_idx, rr in enumerate(self.data):

            for c_idx, ch in enumerate(rr):
                columns[c_idx] += ch

            if all(ch == "." for ch in rr):
                no_galaxies_rows.append(r_idx)

        for c_idx, cc in enumerate(columns):

            if all(ch == "." for ch in cc):
                no_galaxies_columns.append(c_idx)

        # Inserting rows and columns where there are no galaxies
        for idx_sum, r_insert_idx in enumerate(no_galaxies_rows):
            self.data.insert(r_insert_idx + idx_sum, "." * len(self.data[0]))

        for idx_sum_c, c_insert_idx in enumerate(no_galaxies_columns):
            for r_idx, _ in enumerate(self.data):
                self.data[r_idx] = self.data[r_idx][:(c_insert_idx + idx_sum_c)] + "." + self.data[r_idx][(c_insert_idx + idx_sum_c):] 

        # Find coordinates of galaxies
        galaxies_coordinates = []
        for r_idx, rr in enumerate(self.data):
            for c_idx, c in enumerate(rr):
                if c == "#":
                    galaxies_coordinates.append((r_idx, c_idx))

        galaxies_indices = [gg for gg, _ in enumerate(galaxies_coordinates)]
        pair_combinations = list(combinations(galaxies_indices, 2))

        closest_paths = []
        for g1, g2 in pair_combinations:
            min_distance = abs(galaxies_coordinates[g1][0] - galaxies_coordinates[g2][0]) + abs(
                galaxies_coordinates[g1][1] - galaxies_coordinates[g2][1])
            closest_paths.append(min_distance)
        print(sum(closest_paths))

        # Find coordinates of galaxies
        unexpanded_galaxies_coordinates = []
        for r_idx, rr in enumerate(unexpanded_data):
            for c_idx, c in enumerate(rr):
                if c == "#":
                    unexpanded_galaxies_coordinates.append((r_idx, c_idx))

        expansion_factor = 1000000 - 1
        paths = []
        for g1, g2 in pair_combinations:
            min_r = min(unexpanded_galaxies_coordinates[g1][0], unexpanded_galaxies_coordinates[g2][0])
            max_r = max(unexpanded_galaxies_coordinates[g1][0], unexpanded_galaxies_coordinates[g2][0])
            min_c = min(unexpanded_galaxies_coordinates[g1][1], unexpanded_galaxies_coordinates[g2][1])
            max_c = max(unexpanded_galaxies_coordinates[g1][1], unexpanded_galaxies_coordinates[g2][1])

            expansion_rows = len([r for r in no_galaxies_rows if min_r <= r <= max_r])
            expansion_cols = len([c for c in no_galaxies_columns if min_c <= c <= max_c])

            min_distance = abs(unexpanded_galaxies_coordinates[g1][0] - unexpanded_galaxies_coordinates[g2][0]) + \
                abs(unexpanded_galaxies_coordinates[g1][1] - unexpanded_galaxies_coordinates[g2][1]) + \
                expansion_factor * expansion_rows + expansion_factor * expansion_cols
            paths.append(min_distance)
        print(sum(paths))


if __name__ == "__main__":
    day_11 = Day11()
    day_11.solve()
