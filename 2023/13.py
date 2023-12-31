from base import DailyPuzzle


class Day13(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "13")

    def solve(self):
        blocks = []
        block = []
        for idx, ll in enumerate(self.data):
            if ll == "" or idx == len(self.data) - 1:
                blocks.append(block)
                block = []
                continue
            block.append(ll)

        p1 = 0
        p2 = 0
        for block in blocks:
            columns = [[] for _ in range(len(block[0]))]
            for r_idx, rr in enumerate(block):

                # Updating columns for next step
                for ci in range(len(block[0])):
                    columns[ci].append(rr[ci])

            hs, hs_pt2 = self.find_symmetry(block)
            vs, vs_pt2 = self.find_symmetry(columns)

            # Summarizing for part 1
            if len(hs) + len(vs) > 1:  # The last line has 2 symmetry axes... Might it be a bug in the input data?
                hs = []

            for hh in hs:
                p1 += hh[0] * 100

            for vv in vs:
                p1 += vv[0]

            # Summarizing for part 2
            if len(hs_pt2) + len(vs_pt2) > 1 or len(hs_pt2) + len(
                    vs_pt2) == 0:  # The last line has 2 symmetry axes... Might it be a bug in the input data?
                raise

            for hh2 in hs_pt2:
                p2 += hh2[0] * 100

            for vv2 in vs_pt2:
                p2 += vv2[0]

        print(p1)
        print(p2)

    @staticmethod
    def find_symmetry(input_list: list) -> (list, list):
        out = []
        output_pt2 = []
        for index, _ in enumerate(input_list):
            lines_before_axis = index + 1
            lines_after_axis = len(input_list) - (index + 1)
            lines_to_consider = min(lines_before_axis, lines_after_axis)

            if lines_to_consider == 0:
                break

            symmetry = True
            d_idx = 0
            for ltc in range(lines_to_consider):
                lb = input_list[index - ltc]
                la = input_list[index + ltc + 1]

                if lb != la:
                    symmetry = False
                    for c_idx, cc in enumerate(lb):
                        if cc != la[c_idx]:
                            d_idx += 1

            if symmetry:
                out.append((index + 1, index + 2))

            if d_idx == 1:
                output_pt2.append((index + 1, index + 2))

        return out, output_pt2


if __name__ == "__main__":
    day_13 = Day13()
    day_13.solve()
