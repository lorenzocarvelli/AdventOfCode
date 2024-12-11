from typing import List, Dict

from base import DailyPuzzle


class Day11(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "11")

    @staticmethod
    def apply_rules(input_n: int) -> List[int]:
        if input_n == 0:
            return [1]

        n_digits = len(str(input_n))
        if not n_digits % 2:
            half_length = int(n_digits / 2)
            n1 = int(str(input_n)[:half_length])
            n2 = int(str(input_n)[half_length:])
            return [n1, n2]

        return [input_n * 2024]

    def blink_n_times(self, n: int, stones_dict: Dict[int, int]) -> int:
        for _ in range(n):
            updated_dict = dict()
            for stone, count in stones_dict.items():
                updated_stones = self.apply_rules(stone)
                for us in updated_stones:
                    if us not in updated_dict:
                        updated_dict[us] = count
                        continue
                    updated_dict[us] += count
            stones_dict = updated_dict

        out = 0
        for _, count in stones_dict.items():
            out += count
        return out

    def solve(self):
        # Parsing data into a dict of number engraved into the stone and corresponding count
        stones = [int(s) for s in self.data[0].split(" ")]
        stones_dict = dict()
        for s in stones:
            if s not in stones_dict:
                stones_dict[s] = 1
                continue
            stones_dict[s] += 1

        print(self.blink_n_times(25, stones_dict))
        print(self.blink_n_times(75, stones_dict))


if __name__ == "__main__":
    day_11 = Day11()
    day_11.solve()
