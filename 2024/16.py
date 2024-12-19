from math import inf
from copy import deepcopy
from typing import List, Tuple, Dict

from base import DailyPuzzle


TURN_90_CLOCKWISE = {
    "N": "E",
    "S": "W",
    "E": "S",
    "W": "N"
}
TURN_90_ANTICLOCKWISE = {
    "N": "W",
    "S": "E",
    "E": "N",
    "W": "S"
}


class LabyrinthPath(object):
    def __init__(self, initial_positions: List[Tuple[int, int]], initial_orientation: str, initial_score: int):
        self.positions: List[Tuple[int, int]] = initial_positions
        self.current_orientation: str = initial_orientation
        self.current_position: Tuple[int, int] = self.positions[-1]
        self.score: int = initial_score
        self.completed: bool = False

    def add_position(self, new_pos: Tuple[int, int]):
        self.positions.append(new_pos)
        self.current_position = self.positions[-1]
        self.score += 1

    def turn_90_degrees(self, direction: str):
        if direction == "clockwise":
            self.current_orientation = TURN_90_CLOCKWISE[self.current_orientation]
            self.score += 1000
            return
        if direction == "anticlockwise":
            self.current_orientation = TURN_90_ANTICLOCKWISE[self.current_orientation]
            self.score += 1000
            return
        raise RuntimeError(f"Unknown direction {direction}")


class Day16(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "16")

    @staticmethod
    def print_grid_and_best_paths_pos(coordinates_grid: Dict[Tuple[int, int], str], n_rows: int, n_cols: int, best_positions: List[Tuple[int, int]]):
        for r in range(n_rows):
            ltp = ""
            for c in range(n_cols):
                coordinate = (r, c)
                if coordinate in best_positions:
                    ltp += "O"
                    continue
                ltp += coordinates_grid[coordinate]
            print(ltp)

    @staticmethod
    def get_neighbor_positions(input_position: Tuple[int, int]) -> Tuple[Tuple[int, int], Tuple[int, int], Tuple[int, int], Tuple[int, int]]:
        up = (input_position[0]-1, input_position[1])
        down = (input_position[0]+1, input_position[1])
        left = (input_position[0], input_position[1]-1)
        right = (input_position[0], input_position[1]+1)
        return up, down, left, right  # No need to worry about being outside the map, cause the labyrinth is fenced

    def solve(self):
        # Parsing input
        coordinates_grid = dict()
        start_pos = None
        target_pos = None
        n_rows, n_cols = len(self.data), len(self.data[0])
        for row_idx, ll in enumerate(self.data):
            for col_idx, cc in enumerate(ll):
                if cc == "S":
                    start_pos = (row_idx, col_idx)
                    coordinates_grid[(row_idx, col_idx)] = "."
                    continue
                if cc == "E":
                    target_pos = (row_idx, col_idx)
                    coordinates_grid[(row_idx, col_idx)] = "."
                    continue

                coordinates_grid[(row_idx, col_idx)] = cc

        positions_lowest_cost = {pc: inf for pc, smb in coordinates_grid.items() if smb == "."}
        positions_lowest_cost[start_pos] = 0
        paths = [LabyrinthPath([start_pos], "E", 0)]
        completed_paths = []
        completion_scores = [inf]
        while len(paths):
            updated_paths = []
            for l_path in paths:
                up, down, left, right = self.get_neighbor_positions(l_path.current_position)

                if coordinates_grid[up] == "." and (not l_path.current_orientation == "S"):  # If true, then it can move up
                    new_path = deepcopy(l_path)
                    if new_path.current_orientation == "N":  # Then no need to turn
                        new_path.add_position(up)
                    elif new_path.current_orientation == "E":
                        new_path.turn_90_degrees("anticlockwise")
                        new_path.add_position(up)
                    elif new_path.current_orientation == "W":
                        new_path.turn_90_degrees("clockwise")
                        new_path.add_position(up)

                    if up == target_pos:
                        completed_paths.append(new_path)
                        completion_scores.append(new_path.score)
                    elif new_path.score <= min(completion_scores):  # positions_lowest_cost[up]:
                        # positions_lowest_cost[up] = new_path.score
                        updated_paths.append(new_path)

                if coordinates_grid[down] == "." and (not l_path.current_orientation == "N"):  # If true, then it can move down
                    new_path = deepcopy(l_path)
                    if new_path.current_orientation == "S":  # Then no need to turn
                        new_path.add_position(down)
                    elif new_path.current_orientation == "E":
                        new_path.turn_90_degrees("clockwise")
                        new_path.add_position(down)
                    elif new_path.current_orientation == "W":
                        new_path.turn_90_degrees("anticlockwise")
                        new_path.add_position(down)

                    if down == target_pos:
                        completed_paths.append(new_path)
                        completion_scores.append(new_path.score)
                    elif new_path.score <= min(completion_scores):  # positions_lowest_cost[down]:
                        # positions_lowest_cost[down] = new_path.score
                        updated_paths.append(new_path)

                if coordinates_grid[left] == "." and (not l_path.current_orientation == "E"):  # If true, then it can move left
                    new_path = deepcopy(l_path)
                    if new_path.current_orientation == "W":  # Then no need to turn
                        new_path.add_position(left)
                    elif new_path.current_orientation == "N":
                        new_path.turn_90_degrees("anticlockwise")
                        new_path.add_position(left)
                    elif new_path.current_orientation == "S":
                        new_path.turn_90_degrees("clockwise")
                        new_path.add_position(left)

                    if left == target_pos:
                        completed_paths.append(new_path)
                        completion_scores.append(new_path.score)
                    elif new_path.score <= min(completion_scores):  # positions_lowest_cost[left]:
                        # positions_lowest_cost[left] = new_path.score
                        updated_paths.append(new_path)

                if coordinates_grid[right] == "." and (not l_path.current_orientation == "W"):  # If true, then it can move right
                    new_path = deepcopy(l_path)
                    if new_path.current_orientation == "E":  # Then no need to turn
                        new_path.add_position(right)
                    elif new_path.current_orientation == "N":
                        new_path.turn_90_degrees("clockwise")
                        new_path.add_position(right)
                    elif new_path.current_orientation == "S":
                        new_path.turn_90_degrees("anticlockwise")
                        new_path.add_position(right)

                    if right == target_pos:
                        completed_paths.append(new_path)
                        completion_scores.append(new_path.score)
                    elif new_path.score <= min(completion_scores):  # positions_lowest_cost[right]:
                        # positions_lowest_cost[right] = new_path.score
                        updated_paths.append(new_path)

            paths = updated_paths

        completed_paths.sort(key=lambda x: x.score)
        sol_1 = completed_paths[0].score
        print(sol_1)

        best_paths = [cp for cp in completed_paths if cp.score == sol_1]
        tiles = []
        for bp in best_paths:
            tiles.extend(bp.positions)
        self.print_grid_and_best_paths_pos(coordinates_grid, n_rows, n_cols, tiles)
        sol_2 = len(list(set(tiles)))
        print(sol_2)


if __name__ == "__main__":
    day_16 = Day16()
    day_16.solve()
