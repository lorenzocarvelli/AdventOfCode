import re
from typing import List, Tuple
from base import DailyPuzzle


class Day4(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "4")
        self.word_to_search: str = "XMAS"
        self.word_to_search_pt2: str = "MAS"

    def find_all_matches(self, input_data: List[str]) -> int:
        out = 0
        for ll in input_data:
            forward_matches = re.findall(self.word_to_search, ll)
            backward_matches = re.findall(self.word_to_search[::-1], ll)
            out += (len(forward_matches) + len(backward_matches))
        return out

    def find_all_matches_and_central_coordinate(self, input_data: List[str], coordinates_data: List[List[Tuple[int, int]]]) -> list:
        out = []
        for line_idx, line in enumerate(input_data):
            coordinates_data_line = coordinates_data[line_idx]
            forward_matches_central_idx = [match.start() + 1 for match in re.finditer(self.word_to_search_pt2, line)]
            backward_matches_central_idx = [match.start() + 1 for match in re.finditer(self.word_to_search_pt2[::-1], line)]

            forward_coordinates = [coordinates_data_line[idx] for idx in forward_matches_central_idx]
            backward_coordinates = [coordinates_data_line[idx] for idx in backward_matches_central_idx]
            out.extend(forward_coordinates + backward_coordinates)
        return out

    def solve(self):

        # Solution to Part 1: search for horizontal, vertical, left & right diagonal matches
        # Horizontal matches first
        horizontal_matches = self.find_all_matches(self.data)

        # Transpose data to check for vertical matches
        transposed_data = [""] * len(self.data[0])
        for ll in self.data:
            for letter_idx, letter in enumerate(ll):
                transposed_data[letter_idx] += letter

        vertical_matches = self.find_all_matches(transposed_data)

        # Right diagonal rearrangement
        right_diagonal_data = [""] * (2 * len(self.data[0]) - 1)
        for l_idx, ll in enumerate(self.data):
            for r_letter_idx, r_letter in enumerate(ll):
                right_diagonal_data[r_letter_idx + l_idx] += r_letter

        right_diagonal_matches = self.find_all_matches(right_diagonal_data)

        # Left diagonal rearrangement
        left_diagonal_data = [""] * (2 * len(self.data[0]) - 1)
        for l_idx, ll in enumerate(self.data):
            for l_letter_idx, l_letter in enumerate(ll[::-1]):
                left_diagonal_data[l_letter_idx + l_idx] += l_letter

        left_diagonal_matches = self.find_all_matches(left_diagonal_data)

        sol_1 = horizontal_matches + vertical_matches + right_diagonal_matches + left_diagonal_matches
        print(sol_1)

        # Creating a map of coordinates for the grid of input data, for left and right diagonal rearrangements
        coordinates_grid = []
        for row_idx, ll in enumerate(self.data):
            coordinates_grid.append([(row_idx, col_idx) for col_idx, _ in enumerate(ll)])

        right_diagonal_coordinates = [[] for _ in range(2 * len(coordinates_grid[0]) - 1)]
        for row_idx, row in enumerate(coordinates_grid):
            for col_idx, coordinates in enumerate(row):
                right_diagonal_coordinates[col_idx + row_idx].append(coordinates)

        left_diagonal_coordinates = [[] for _ in range(2 * len(coordinates_grid[0]) - 1)]
        for row_idx, row in enumerate(coordinates_grid):
            for col_idx, coordinates in enumerate(row[::-1]):
                left_diagonal_coordinates[col_idx + row_idx].append(coordinates)

        # To solve Part 2, we find the matches in the diagonally rearranged data, both left and right, save the central
        # coordinate of the match (i.e. the coordinate of the "A" in "MAS") and then find the intersection of the two
        # lists of central coordinates
        right_matches_central_coordinates = self.find_all_matches_and_central_coordinate(right_diagonal_data, right_diagonal_coordinates)
        left_matches_central_coordinates = self.find_all_matches_and_central_coordinate(left_diagonal_data, left_diagonal_coordinates)
        intersection = [rmc for rmc in right_matches_central_coordinates if rmc in left_matches_central_coordinates]
        sol_2 = len(intersection)

        print(sol_2)


if __name__ == "__main__":
    day_4 = Day4()
    day_4.solve()
