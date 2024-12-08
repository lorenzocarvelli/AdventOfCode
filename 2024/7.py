from itertools import product
from typing import List, Tuple

from base import DailyPuzzle


class Day7(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "7")

    def solve(self):
        sol_1 = 0
        combination_found = []
        for ll in self.data:

            left_side, right_side_list = self.get_left_and_right_side_integers(ll)

            bits = len(right_side_list) - 1
            combinations = list(product([self._mul, self._sum], repeat=bits))

            for combination in combinations:
                result = right_side_list[0]
                for func, num in zip(combination, right_side_list[1:]):
                    result = func(result, num)
                if result == left_side:
                    sol_1 += result
                    combination_found.append(ll)
                    break

        print(sol_1)

        # Part 2: one more operator to be added to the picture
        sol_2 = sol_1
        for ll in self.data:
            if ll in combination_found:
                continue

            left_side, right_side_list = self.get_left_and_right_side_integers(ll)

            bits = len(right_side_list) - 1
            combinations = list(product([self._mul, self._sum, self._concat], repeat=bits))

            for combination in combinations:
                result = right_side_list[0]
                for func, num in zip(combination, right_side_list[1:]):
                    result = func(result, num)
                if result == left_side:
                    sol_2 += result
                    break
        print(sol_2)

    @staticmethod
    def _mul(n1: int, n2: int) -> int:
        return n1 * n2

    @staticmethod
    def _sum(n1: int, n2: int) -> int:
        return n1 + n2

    @staticmethod
    def _concat(n1: int, n2: int) -> int:
        return int(f"{n1}{n2}")

    @staticmethod
    def get_left_and_right_side_integers(ll: str) -> Tuple[int, List[int]]:
        line_split = ll.split(": ")
        left_side = int(line_split[0])
        right_side_str = line_split[1]
        right_side_list = [int(nn) for nn in right_side_str.split(" ")]
        return left_side, right_side_list


if __name__ == "__main__":
    day_7 = Day7()
    day_7.solve()
