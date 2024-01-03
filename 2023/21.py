from collections import deque
from base import DailyPuzzle


class Day21(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "21")
        self.mock_data = [
            "...........",
            ".....###.#.",
            ".###.##..#.",
            "..#.#...#..",
            "....#.#....",
            ".##..S####.",
            ".##..#...#.",
            ".......##..",
            ".##.#.####.",
            ".##..##.##.",
            "..........."
        ]
        self.coordinate_grid: dict = self.create_coordinate_grid()
        self.max_row: int = len(self.data)
        self.max_col: int = len(self.data[0])

    def create_coordinate_grid(self) -> dict:
        out = dict()
        for r_idx, rr in enumerate(self.data):
            for c_idx, character in enumerate(rr):
                out[(r_idx, c_idx)] = character
        return out

    def find_start_coordinates(self):
        for k, c in self.coordinate_grid.items():
            if c == "S":
                return k

    def take_steps(self, number_of_steps: int):
        start = self.find_start_coordinates()

        current_iteration = [start]
        for _ in range(number_of_steps):
            next_iteration = []
            for step_coordinate in current_iteration:
                north = (step_coordinate[0] - 1, step_coordinate[1])
                south = (step_coordinate[0] + 1, step_coordinate[1])
                east = (step_coordinate[0], step_coordinate[1] + 1)
                west = (step_coordinate[0], step_coordinate[1] - 1)

                if north[0] >= 0 and self.data[north[0]][north[1]] in [".", "S"]:
                    next_iteration.append(north)

                if south[0] < self.max_row and self.data[south[0]][south[1]] in [".", "S"]:
                    next_iteration.append(south)

                if east[1] < self.max_col and self.data[east[0]][east[1]] in [".", "S"]:
                    next_iteration.append(east)

                if west[1] >= 0 and self.data[west[0]][west[1]] in [".", "S"]:
                    next_iteration.append(west)

            current_iteration = list(set(next_iteration))

        return len(current_iteration)

    def solve_quadratic(self, plot_counts: list[int], steps: int):
        # Credits to derailed-dash for the implementation and explanation
        # https://github.com/derailed-dash/Advent-of-Code/blob/master/src/AoC_2023/Dazbo's_Advent_of_Code_2023.ipynb
        grid = [[char for char in row] for row in self.data]
        grid_size = len(grid)

        # determine coefficients
        c = plot_counts[0]
        b = (4 * plot_counts[1] - 3 * plot_counts[0] - plot_counts[2]) // 2
        a = plot_counts[1] - plot_counts[0] - b

        x = (steps - grid_size // 2) // grid_size  # number of whole tile lengths
        return a * x ** 2 + b * x + c

    def reachable_plots(self, steps_available: int):
        grid = [[char for char in row] for row in self.data]
        grid_size = len(grid)

        print(f"Grid width={grid_size}")
        assert grid_size == len(grid[0]), "The grid should be square"
        assert grid_size % 2 == 1, "The grid size is odd"

        (start,) = [(ri, ci) for ri, row in enumerate(grid)
                    for ci, char in enumerate(row) if char == "S"]

        assert start[0] == start[1] == grid_size // 2, "Start is in the middle"

        # For each location in the original grid (tile 0,0),
        # can we reach this same location in other tiles?
        answer = self.multi_tile_bfs(grid, start, steps_available)
        print(f"We have {answer} final plots for {steps_available} steps.")

        return answer

    @staticmethod
    def multi_tile_bfs(grid, start: tuple[int, int], steps_available: int) -> int:
        """ Modified BFS that now also includes a tile coordinate as part of state.
        Args:
            grid (_type_): 2D grid of chars
            start (tuple[int,int]): start location in the grid
            steps_available (int): steps available

        Returns int: count of valid locations to land on, when we've run out of steps
        """
        steps_remaining = steps_available
        current_tile = (0, 0)
        # (tile coordinate, location in tile, steps remaining)
        queue: deque[tuple[tuple[int, int], tuple[int, int], int]] = deque([(current_tile, start, steps_remaining)])

        seen = set()  # combination of (tile, location)
        answer: set[
            tuple[tuple, tuple]] = set()  # the number of locations we can get to in the required number of steps

        side_len = len(grid)
        tiles_for_steps = (steps_available // side_len) + 1
        print(f"{tiles_for_steps=}")

        while queue:
            # When we pop, we have already updated tile and location in the tile to be valid
            current_tile, current_locn, steps_remaining = queue.popleft()

            if steps_remaining >= 0:
                if steps_remaining % 2 == 0:  # we can always get back to this location in an even number of steps
                    answer.add(
                        (current_tile, current_locn))  # so this location will be possible in our target number of steps

                if steps_remaining > 0:  # get next possible location
                    steps_remaining -= 1
                    neighbours = [(current_locn[0] + dx, current_locn[1] + dy) for dx, dy in
                                  ((0, 1), (0, -1), (1, 0), (-1, 0))]
                    for neighbour in neighbours:  # update current tile, and offset location in tile by tile width/height, as required
                        new_tile = current_tile
                        if neighbour[0] < 0:  # move to tile on the left
                            new_tile = (current_tile[0] - 1, current_tile[1])
                            neighbour = (neighbour[0] + side_len, neighbour[1])
                        if neighbour[0] >= side_len:  # move to tile on the right
                            new_tile = (current_tile[0] + 1, current_tile[1])
                            neighbour = (neighbour[0] - side_len, neighbour[1])
                        if neighbour[1] < 0:  # move to tile above
                            new_tile = (current_tile[0], current_tile[1] - 1)
                            neighbour = (neighbour[0], neighbour[1] + side_len)
                        if neighbour[1] >= side_len:  # move to tile below
                            new_tile = (current_tile[0], current_tile[1] + 1)
                            neighbour = (neighbour[0], neighbour[1] - side_len)

                        if (new_tile, neighbour) in seen or grid[neighbour[1]][neighbour[0]] == "#":
                            continue  # do nothing

                        # With max distance of 327, this is 2.5 tiles. So 3 either side should be neough.
                        # -3, -2, -1, 0, 1, 2, 3 = 7x7
                        if (abs(current_tile[0]) > tiles_for_steps or abs(current_tile[1]) > tiles_for_steps):
                            print(f"{new_tile=}")
                            assert False, "Not enough steps to move further out"

                        queue.append((new_tile, neighbour, steps_remaining))
                        seen.add((new_tile, neighbour))

        return len(answer)

    def solve(self):
        print(self.take_steps(64))

        step_counts = [64, 65, 196, 327]  # 64 is just to check it matches what we had before

        plot_counts = [(step_count, self.reachable_plots(step_count)) for step_count in step_counts[1:]]

        print(self.solve_quadratic(plot_counts=[ct[1] for ct in plot_counts], steps=26501365))


if __name__ == "__main__":
    day_21 = Day21()
    day_21.solve()
