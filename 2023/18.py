import re

from base import DailyPuzzle


class Day18(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "18")
        self.mock_data = [
            "R 6 (#70c710)",
            "D 5 (#0dc571)",
            "L 2 (#5713f0)",
            "D 2 (#d2c081)",
            "R 2 (#59c680)",
            "D 2 (#411b91)",
            "L 5 (#8ceee2)",
            "U 2 (#caa173)",
            "L 1 (#1b58a2)",
            "U 2 (#caa171)",
            "R 2 (#7807d2)",
            "U 3 (#a77fa3)",
            "L 2 (#015232)",
            "U 2 (#7a21e3)"
        ]

        self.direction_dict: dict = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1)
        }

    def solve(self):

        current_coordinate = (0, 0)
        trench_coordinates = [current_coordinate]
        for ll in self.data:
            direction = ll[0]
            steps = int(re.match(r".+ (\d+) \(", ll).group(1))
            new_dir = self.direction_dict[direction]

            for _ in range(steps):
                current_coordinate = (current_coordinate[0] + new_dir[0], current_coordinate[1] + new_dir[1])
                trench_coordinates.append(current_coordinate)

        filled_trench = self.fill_grid(trench_coordinates)
        p1 = self.draw_grid_and_count_m3_lava(filled_trench)
        print(p1)

    def fill_grid(self, trench_coordinates):
        out = []
        min_row, min_col = self.get_min_row_col(trench_coordinates)
        max_row, max_col = self.get_max_row_col(trench_coordinates)
        for rr in range(min_row, max_row):
            for cc in range(min_col, max_col):
                coordinates = (rr, cc)

                if coordinates in trench_coordinates:
                    out.append(coordinates)
                    continue

                if self.is_inside_polygon(coordinates, trench_coordinates):
                    out.append(coordinates)
        return out

    def draw_grid_and_count_m3_lava(self, trench_coordinates: list) -> int:
        out = 0
        min_row, min_col = self.get_min_row_col(trench_coordinates)
        max_row, max_col = self.get_max_row_col(trench_coordinates)
        for rr in range(min_row, max_row):
            ll = ""
            for cc in range(min_col, max_col):
                coordinates = (rr, cc)
                if coordinates in trench_coordinates:
                    ll += "#"
                    out += 1
                    continue
                ll += "."
            print(ll)
        return out

    @staticmethod
    def is_inside_polygon(point, polygon):
        x, y = point
        n = len(polygon)
        inside = False

        p1x, p1y = polygon[0]
        for i in range(n + 1):
            p2x, p2y = polygon[i % n]
            if y > min(p1y, p2y):
                if y <= max(p1y, p2y):
                    if x <= max(p1x, p2x):
                        if p1y != p2y:
                            x_inters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or x <= x_inters:
                                inside = not inside
            p1x, p1y = p2x, p2y

        return inside

    @staticmethod
    def get_max_row_col(trench_coordinates: list) -> tuple:
        max_row = max(item[0] for item in trench_coordinates) + 1
        max_col = max(item[1] for item in trench_coordinates) + 1
        return max_row, max_col

    @staticmethod
    def get_min_row_col(trench_coordinates: list) -> tuple:
        max_row = min(item[0] for item in trench_coordinates)
        max_col = min(item[1] for item in trench_coordinates)
        return max_row, max_col


if __name__ == "__main__":
    day_18 = Day18()
    day_18.solve()
