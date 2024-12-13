import re

from base import DailyPuzzle


class Day13(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "13")

    @staticmethod
    def is_almost_integer(number, tolerance=1e-15):
        decimal_part = abs(number - round(number))
        return decimal_part < tolerance

    def solve(self):
        sol_1 = 0
        sol_2 = 0

        part_2_addition = 10000000000000

        ax, ay = None, None
        bx, by = None, None
        x, y = None, None
        for ll in self.data:

            if ll.startswith("Button A"):
                ax = int(re.match(r".+X\+(\d+),", ll).group(1))
                ay = int(re.match(r".+, Y\+(\d+)$", ll).group(1))

            if ll.startswith("Button B"):
                bx = int(re.match(r".+X\+(\d+),", ll).group(1))
                by = int(re.match(r".+, Y\+(\d+)$", ll).group(1))

            if ll.startswith("Prize"):
                x = int(re.match(r".+X=(\d+),", ll).group(1))
                y = int(re.match(r".+, Y=(\d+)$", ll).group(1))

            if all([ax, ay, bx, by, x, y]):
                # Resolving the system of equation of 2 equations and 2 unknowns for Part 1
                a = (bx*y-by*x) / (bx*ay-ax*by)
                b = (x-ax*a) / bx

                # Doing the same for Part 2 but after the addition
                x_pt2 = x + part_2_addition
                y_pt2 = y + part_2_addition
                a_pt2 = (bx*y_pt2-by*x_pt2) / (bx*ay-ax*by)
                b_pt2 = (x_pt2-ax*a_pt2) / bx

                if self.is_almost_integer(a) and self.is_almost_integer(b):
                    sol_1 += a*3 + b

                if self.is_almost_integer(a_pt2) and self.is_almost_integer(b_pt2):
                    sol_2 += a_pt2 * 3 + b_pt2

                # Resetting after calculation
                ax, ay = None, None
                bx, by = None, None
                x, y = None, None

        print(int(sol_1))
        print(int(sol_2))


if __name__ == "__main__":
    day_13 = Day13()
    day_13.solve()
