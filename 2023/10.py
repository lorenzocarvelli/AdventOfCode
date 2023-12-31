import math

from base import DailyPuzzle


class Day10(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "10")
        self.opposite_direction = {
            "N": "S",
            "S": "N",
            "E": "W",
            "W": "E"
        }
        self.directions = {
            "N": (-1, 0),
            "S": (1, 0),
            "E": (0, 1),
            "W": (0, -1)
        }
        self.connections = {  # Each dict is of the form {"coming_from1": "going_to1", "coming_from2": "going_to2"}
            "F": {"S": "E", "E": "S"},
            "7": {"S": "W", "W": "S"},
            "J": {"N": "W", "W": "N"},
            "L": {"N": "E", "E": "N"},
            "-": {"W": "E", "E": "W"},
            "|": {"N": "S", "S": "N"}
        }

    def solve(self):
        # Finding start position
        start_coordinates = [(r_idx, c_idx) for r_idx, r in enumerate(self.data) for c_idx, ll in enumerate(r) if ll == "S"][0]

        # The first step is taken east
        steps = 0
        loop_steps = []
        coming_from = "W"
        current_char = "-"  # "-" Needed to make the first step east
        coordinates = start_coordinates
        loop_coordinates = []

        while current_char != "S":
            steps += 1
            going_to = self.connections[current_char][coming_from]
            coordinate_update = self.directions[going_to]
            coordinates = tuple(sum(pair) for pair in zip(coordinates, coordinate_update))
            loop_coordinates.append(coordinates)
            current_char = self.data[coordinates[0]][coordinates[1]]
            coming_from = self.opposite_direction[going_to]
            loop_steps.append(steps)

        # Inverting loop to subtract opposite direction in the closed loop
        half_steps = int(math.ceil(max(loop_steps) / 2))
        print(half_steps)

        char_map = []
        for r_idx, rr in enumerate(self.data):
            current_row = ""
            for c_idx, cc in enumerate(rr):
                if (r_idx, c_idx) in loop_coordinates:
                    current_row += self.data[r_idx][c_idx]
                    continue
                current_row += "."
            print(current_row)
            char_map.append(current_row)


if __name__ == "__main__":
    day_10 = Day10()
    day_10.solve()
