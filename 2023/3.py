import re

from base import DailyPuzzle


class Day3(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "3")

    def solve(self):
        engine_parts_n = []

        matches_tuples = []
        for idx, data_line in enumerate(self.data):
            for m in re.finditer(r"\d+", data_line):
                n = int(m.group(0))
                start_col_idx = m.start(0)
                end_col_idx = m.end(0)

                matches_tuples.append((n, [cdx for cdx in range(start_col_idx, end_col_idx)], idx))

                previous_col_idx = start_col_idx - 1
                next_col_idx = end_col_idx + 1

                contour_pts = []
                previous_row_idx = idx - 1
                next_row_idx = idx + 1

                # Adding contour points
                if previous_col_idx >= 0:
                    contour_pts.append(data_line[previous_col_idx])
                else:
                    previous_col_idx += 1

                if end_col_idx < len(data_line):
                    contour_pts.append(data_line[end_col_idx])
                else:
                    next_col_idx -= 1

                if previous_row_idx >= 0:
                    for ii in range(previous_col_idx, next_col_idx):
                        contour_pts.append(self.data[previous_row_idx][ii])

                if next_row_idx < len(self.data):
                    for jj in range(previous_col_idx, next_col_idx):
                        contour_pts.append(self.data[next_row_idx][jj])

                if any([cp != "." for cp in contour_pts]):
                    engine_parts_n.append(n)

        print(sum(engine_parts_n))

        ratios = []
        for jdx, ll in enumerate(self.data):
            for star_match in re.finditer(r"\*", ll):
                start_col_idx_star = star_match.start(0)
                end_col_idx_star = star_match.end(0)

                above = [mt for mt in matches_tuples if mt[2] == jdx - 1 and (
                        start_col_idx_star - 1 in mt[1] or end_col_idx_star in mt[1] or start_col_idx_star in mt[1])]
                below = [mt for mt in matches_tuples if mt[2] == jdx + 1 and (
                        start_col_idx_star - 1 in mt[1] or end_col_idx_star in mt[1] or start_col_idx_star in mt[1])]
                same_line = [mt for mt in matches_tuples if
                             mt[2] == jdx and (start_col_idx_star - 1 in mt[1] or end_col_idx_star in mt[1])]

                adjacent_numbers = above + below + same_line

                if len(adjacent_numbers) == 2:
                    ratios.append(adjacent_numbers[0][0] * adjacent_numbers[1][0])

        print(sum(ratios))


if __name__ == "__main__":
    day_3 = Day3()
    day_3.solve()
