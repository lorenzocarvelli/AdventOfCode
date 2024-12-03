import re
from base import DailyPuzzle


class Day3(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "3")

    def solve(self):
        # Solution of Part 1 through reg ex
        multiplication_pattern = r"mul\(\d+,\d+\)"
        mul_str_list = []
        for ll in self.data:
            mul_str_list.extend(re.findall(multiplication_pattern, ll))

        mul_sum = 0
        for mul_str in mul_str_list:
            mul_sum += self.perform_multiplication_from_string(mul_str)

        print(mul_sum)

        # Solution of Part 2 through creation of a map of coordinates of each statement
        one_input_str = "".join(self.data)
        mul_matches = [(match.group(), match.start()) for match in re.finditer(multiplication_pattern, one_input_str)]
        do_matches = [(match.group(), match.start()) for match in re.finditer(r"do\(\)", one_input_str)]
        dont_matches = [(match.group(), match.start()) for match in re.finditer(r"don\'t\(\)", one_input_str)]

        instruction_list = mul_matches + do_matches + dont_matches
        sorted_instruction_list = sorted(instruction_list, key=lambda x: x[1])

        mul_sum_2 = 0
        mul_enabled = True
        idx = 0
        while idx < len(sorted_instruction_list):
            current_instruction = sorted_instruction_list[idx][0]
            idx += 1

            if current_instruction.startswith("don't"):
                mul_enabled = False
                continue

            if current_instruction.startswith("do("):
                mul_enabled = True
                continue

            if not mul_enabled:
                continue

            mul_sum_2 += self.perform_multiplication_from_string(current_instruction)

        print(mul_sum_2)

    @staticmethod
    def perform_multiplication_from_string(input_string: str) -> int:
        match_object = re.match(r"mul\((\d+),(\d+)\)", input_string)
        int_1 = int(match_object.group(1))
        int_2 = int(match_object.group(2))
        return int_1 * int_2


if __name__ == "__main__":
    day_3 = Day3()
    day_3.solve()
