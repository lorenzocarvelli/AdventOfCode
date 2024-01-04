from copy import deepcopy

from base import DailyPuzzle


class Day14(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "14")

    def solve(self):
        round_rocks = []
        square_rocks = []
        for r_idx, row in enumerate(self.data):
            for c_idx, ccc in enumerate(row):
                if ccc == "O":
                    round_rocks.append((r_idx, c_idx))
                    continue
                if ccc == "#":
                    square_rocks.append((r_idx, c_idx))

        # Round rocks will go north
        tr = len(self.data)
        tc = len(self.data[0])
        round_rocks1 = deepcopy(round_rocks)
        round_rocks1 = self.tilt(round_rocks1, square_rocks, "north", tr, tc)

        p1 = self.get_total_load(round_rocks1, tr)
        print(p1)

        one_cycle_configuration = []
        configurations = []
        ii = 0
        cycles = 1000000000
        while ii < cycles:
            round_rocks = self.tilt(round_rocks, square_rocks, "north", tr, tc)
            round_rocks = self.tilt(round_rocks, square_rocks, "west", tr, tc)
            round_rocks = self.tilt(round_rocks, square_rocks, "south", tr, tc)
            round_rocks = self.tilt(round_rocks, square_rocks, "east", tr, tc)

            if ii == 0:
                one_cycle_configuration = sorted(round_rocks)

            if ii > 0 and all(rrk in one_cycle_configuration for rrk in sorted(round_rocks)):
                break

            configurations.append(round_rocks)

        out_i = cycles % ii
        p2 = self.get_total_load(configurations[out_i], tr)
        print(p2)

    @staticmethod
    def get_total_load(round_rocks_in: list, total_rows: int):
        out = 0
        for ri in range(total_rows):
            round_rocks_in_row = len([rrk for rrk in round_rocks_in if rrk[0] == ri])
            out += (total_rows - ri) * round_rocks_in_row
        return out

    @staticmethod
    def tilt(round_rks: list, square_rks: list, direction: str, total_rows: int, total_cols: int):
        idx = 0
        while idx < len(round_rks):
            rr_row, rr_col = round_rks[idx]

            objects_in_same_column = [rrr for rrr in round_rks if rrr[1] == rr_col and rrr != (rr_row, rr_col)]
            objects_in_same_column.extend([srr for srr in square_rks if srr[1] == rr_col])
            objects_in_same_column.append((-1, rr_col) if direction == "north" else (total_rows, rr_col))

            objects_in_same_row = [rrr for rrr in round_rks if rrr[0] == rr_row and rrr != (rr_row, rr_col)]
            objects_in_same_row.extend([srr for srr in square_rks if srr[0] == rr_row])
            objects_in_same_row.append((rr_row, -1) if direction == "west" else (rr_row, total_cols))

            new_row_coordinate = rr_row
            if direction == "north":
                closest_object_north = max([osc for osc in objects_in_same_column if osc[0] < rr_row])
                new_row_coordinate = closest_object_north[0] + 1
            elif direction == "south":
                closest_object_south = min([osc for osc in objects_in_same_column if osc[0] > rr_row])
                new_row_coordinate = closest_object_south[0] - 1
            elif direction == "west":
                pass
            elif direction == "east":
                pass

            round_rks[idx] = (new_row_coordinate, rr_col)
            idx += 1
        return round_rks


if __name__ == "__main__":
    day_14 = Day14()
    day_14.solve()
