import re

from base import DailyPuzzle


class Day15(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "15")

    def solve(self):
        data = self.data[0].split(",")
        lp1 = [self.ascii_string_helper(x) for x in data]
        print(sum(lp1))

        labels = [re.sub(r'[^a-zA-Z]', '', x) for x in data]
        box_numbers = [self.ascii_string_helper(ll) for ll in labels]
        operations = [re.sub(r'[^=\-]', '', x) for x in data]
        focal_lengths = []
        for x in data:
            try:
                focal_lengths.append(int(re.sub(r'[^\d]', '', x)))
            except ValueError:
                focal_lengths.append(None)

        boxes = [dict() for _ in range(256)]
        for idx, box in enumerate(box_numbers):
            lab = labels[idx]
            if operations[idx] == "-":
                if lab in boxes[box]:
                    del boxes[box][lab]

            else:
                focal_length = focal_lengths[idx]
                boxes[box][lab] = focal_length

        p2 = sum([self.calculate_focusing_power(b_idx, bx) for b_idx, bx in enumerate(boxes)])
        print(p2)

    @staticmethod
    def ascii_string_helper(input_string: str) -> int:
        current_value = 0
        for cc in input_string:
            ascii_val = ord(cc)
            current_value += ascii_val
            current_value *= 17
            current_value = current_value % 256
        return current_value

    @staticmethod
    def calculate_focusing_power(box_number: int, lenses: dict) -> int:
        return sum([(box_number + 1) * (l_idx + 1) * fl for l_idx, (k, fl) in enumerate(lenses.items())])


if __name__ == "__main__":
    day_15 = Day15()
    day_15.solve()
