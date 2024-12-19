from typing import Dict, Tuple

from base import DailyPuzzle


class Day15(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "15")
        self.moves_dict = {
            "<": (0, -1),
            ">": (0, 1),
            "^": (-1, 0),
            "v": (1, 0)
        }

    @staticmethod
    def get_sum_of_gps_coordinates_for_stones(coordinates_grid: Dict[Tuple[int, int], str]) -> int:
        out = 0
        stones_coordinates = [cc for cc, itm in coordinates_grid.items() if itm == "O"]
        for rc in stones_coordinates:
            out += rc[0]*100+rc[1]

        return out

    @staticmethod  # For debugging purposes
    def print_grid(coordinates_grid: Dict[Tuple[int, int], str], rows: int, cols: int, robot: Tuple[int, int]):
        for rr in range(rows):
            ltp = ""
            for cc in range(cols):
                if (rr, cc) == robot:
                    ltp += "@"
                    continue
                if (rr, cc) not in coordinates_grid:
                    ltp += "."
                    continue
                ltp += coordinates_grid[(rr, cc)]
            print(ltp)

    def solve(self):
        # Parsing grid first
        coordinates_grid = dict()
        robot = None
        rows = 0
        cols = len(self.data[0])
        for row_idx, ll in enumerate(self.data):
            if ll == "":
                break  # Stop parsing grid when encountering empty line
            rows += 1
            for col_idx, cc in enumerate(ll):
                if cc == ".":
                    continue

                if cc == "@":
                    robot = (row_idx, col_idx)
                    continue

                coordinates_grid[(row_idx, col_idx)] = cc

        self.print_grid(coordinates_grid, rows, cols, robot)  # Printing for debugging purposes

        # Then parsing moves
        moves = ""
        for lll in self.data[rows+1:]:
            moves += lll

        # Part 1: applying all moves
        for mm in moves:
            coordinate_update = self.moves_dict[mm]
            potential_new_coordinate = (robot[0] + coordinate_update[0], robot[1] + coordinate_update[1])

            if potential_new_coordinate not in coordinates_grid:  # If it is an empty position, then the robot coordinate is updated
                robot = potential_new_coordinate
                continue

            if coordinates_grid[potential_new_coordinate] == "#":  # If it is a wall, nothing happens
                continue

            # Third case is that the new coordinate is occupied by a box
            if not coordinate_update[0]:
                # Finding all boxes or walls with the same row coordinate as the robot
                row_obstacles = {pp: obs for pp, obs in coordinates_grid.items() if pp[0] == robot[0]}
                if coordinate_update[1] == -1:
                    left_obstacles = {pp: obs for pp, obs in row_obstacles.items() if pp[1] < robot[1]}
                    closest_left_wall_coordinates = max((key for key, value in left_obstacles.items() if value == "#"), key=lambda k: k[1])
                    coordinates_to_closest_left_wall = [(robot[0], ccc) for ccc in range(closest_left_wall_coordinates[1], robot[1])]

                    coordinates_to_be_updated = []
                    can_move = False
                    for clw in coordinates_to_closest_left_wall[::-1]:
                        if clw not in coordinates_grid:
                            can_move = True
                            break
                        if coordinates_grid[clw] == "#":
                            continue
                        coordinates_to_be_updated.append(clw)

                    if can_move:
                        for ctu in coordinates_to_be_updated:
                            coordinates_grid.pop(ctu)

                        for ctu in coordinates_to_be_updated:
                            coordinates_grid[(ctu[0], ctu[1]-1)] = "O"

                        robot = potential_new_coordinate

                else:
                    right_obstacles = {pp: obs for pp, obs in row_obstacles.items() if pp[1] > robot[1]}
                    closest_right_wall_coordinates = min((key for key, value in right_obstacles.items() if value == "#"), key=lambda k: k[1])
                    coordinates_to_closest_right_wall = [(robot[0], ccc) for ccc in range(robot[1]+1, closest_right_wall_coordinates[1])]

                    coordinates_to_be_updated = []
                    can_move = False
                    for crw in coordinates_to_closest_right_wall:
                        if crw not in coordinates_grid:
                            can_move = True
                            break
                        if coordinates_grid[crw] == "#":
                            continue
                        coordinates_to_be_updated.append(crw)

                    if can_move:
                        for ctu in coordinates_to_be_updated:
                            coordinates_grid.pop(ctu)

                        for ctu in coordinates_to_be_updated:
                            coordinates_grid[(ctu[0], ctu[1] + 1)] = "O"

                        robot = potential_new_coordinate

            else:
                # Finding all boxes or walls with the same column coordinate as the robot
                col_obstacles = {pp: obs for pp, obs in coordinates_grid.items() if pp[1] == robot[1]}
                if coordinate_update[0] == -1:
                    up_obstacles = {pp: obs for pp, obs in col_obstacles.items() if pp[0] < robot[0]}
                    closest_up_wall_coordinates = max((key for key, value in up_obstacles.items() if value == "#"), key=lambda k: k[0])
                    coordinates_to_closest_up_wall = [(ccc, robot[1]) for ccc in range(closest_up_wall_coordinates[0], robot[0])]

                    coordinates_to_be_updated = []
                    can_move = False
                    for cuw in coordinates_to_closest_up_wall[::-1]:
                        if cuw not in coordinates_grid:
                            can_move = True
                            break
                        if coordinates_grid[cuw] == "#":
                            continue
                        coordinates_to_be_updated.append(cuw)

                    if can_move:
                        for ctu in coordinates_to_be_updated:
                            coordinates_grid.pop(ctu)

                        for ctu in coordinates_to_be_updated:
                            coordinates_grid[(ctu[0] - 1, ctu[1])] = "O"

                        robot = potential_new_coordinate
                else:
                    down_obstacles = {pp: obs for pp, obs in col_obstacles.items() if pp[0] > robot[0]}
                    closest_down_wall_coordinates = min((key for key, value in down_obstacles.items() if value == "#"), key=lambda k: k[0])
                    coordinates_to_closest_down_wall = [(ccc, robot[1]) for ccc in range(robot[0]+1, closest_down_wall_coordinates[0])]

                    coordinates_to_be_updated = []
                    can_move = False
                    for cdw in coordinates_to_closest_down_wall:
                        if cdw not in coordinates_grid:
                            can_move = True
                            break
                        if coordinates_grid[cdw] == "#":
                            continue
                        coordinates_to_be_updated.append(cdw)

                    if can_move:
                        for ctu in coordinates_to_be_updated:
                            coordinates_grid.pop(ctu)

                        for ctu in coordinates_to_be_updated:
                            coordinates_grid[(ctu[0] + 1, ctu[1])] = "O"

                        robot = potential_new_coordinate

        sol_1 = self.get_sum_of_gps_coordinates_for_stones(coordinates_grid)
        print(sol_1)
        self.print_grid(coordinates_grid, rows, cols, robot)  # Printing for debugging purposes

        # Part 2 - expanded map
        coordinates_grid_pt2 = dict()


if __name__ == "__main__":
    day_15 = Day15()
    day_15.solve()
