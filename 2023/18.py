import re

from base import DailyPuzzle


class Day18(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "18")

        self.direction_dict: dict = {
            "U": (-1, 0),
            "D": (1, 0),
            "L": (0, -1),
            "R": (0, 1)
        }

    @staticmethod
    def solve_pt2(h_lines: list, v_lines: list):
        # Credits to tmo1 - see: https://github.com/tmo1/adventofcode/blob/main/2023/18b.py
        h_bars = sorted({h_line[2] for h_line in h_lines})
        v_bars = sorted({v_line[2] for v_line in v_lines})
        total = 0
        cells = []
        for y in range(len(h_bars) - 1):
            cell_row = []
            h_bar_prev = h_bars[y]
            h_bar = h_bars[y + 1]
            for x in range(len(v_bars) - 1):
                v_bar_left = False
                for v_line in v_lines:
                    if h_bar_prev >= v_line[0] and h_bar <= v_line[1] and v_bars[x] == v_line[2]:
                        v_bar_left = True
                        break
                prev_in = False if (x == 0 or not cell_row[x - 1]) else True
                if prev_in != v_bar_left:
                    cell_row.append(True)
                    total += (h_bar - h_bar_prev - 1) * (v_bars[x + 1] - v_bars[x] - 1)
                    if prev_in:
                        total += h_bar - h_bar_prev - 1
                    if y > 0 and cells[y - 1][x]:
                        total += v_bars[x + 1] - v_bars[x] - 1
                    if prev_in and not v_bar_left and y > 0 and cells[y - 1][x] and cells[y - 1][x - 1]:
                        total += 1
                else:
                    cell_row.append(False)
            cells.append(cell_row)
        print(total + sum([v_line[1] - v_line[0] + 1 for v_line in v_lines]) + sum(
            [h_line[1] - h_line[0] + 1 for h_line in h_lines]) - len(v_lines) - len(h_lines))

    def solve(self):

        current_coordinate = (0, 0)
        x, y = 0, 0
        trench_coordinates = [current_coordinate]
        h_lines = []
        v_lines = []
        for ll in self.data:
            direction = ll[0]
            steps = int(re.match(r".+ (\d+) \(", ll).group(1))
            new_dir = self.direction_dict[direction]

            hex_d = re.match(r".+ \(#(.+)\)$", ll).group(1)
            steps_pt2 = int(hex_d[:-1], 16)
            if hex_d[-1] == "0":
                h_lines.append((x, x + steps_pt2, y))
                x += steps_pt2
            if hex_d[-1] == "1":
                v_lines.append((y, y + steps_pt2, x))
                y += steps_pt2
            if hex_d[-1] == "2":
                h_lines.append((x - steps_pt2, x, y))
                x -= steps_pt2
            if hex_d[-1] == "3":
                v_lines.append((y - steps_pt2, y, x))
                y -= steps_pt2

            for _ in range(steps):
                current_coordinate = (current_coordinate[0] + new_dir[0], current_coordinate[1] + new_dir[1])
                trench_coordinates.append(current_coordinate)

        self.solve_pt2(h_lines, v_lines)

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
