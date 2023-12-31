import re

from base import DailyPuzzle


class Day9(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "9")

    def solve(self):
        input_sequences = []
        for dd in self.data:
            input_sequences.append([int(n) for n in re.findall(r"-*\d+", dd.strip())])

        p1 = []
        p2 = []
        for isq in input_sequences:
            p1.append(self.predict_next_value(isq))
            p2.append(self.predict_next_value((isq[::-1])))

        print(sum(p1))
        print(sum(p2))

    def predict_next_value(self, input_sequence: list):
        current_seq = input_sequence
        sequences = [current_seq]
        while any(current_seq):
            next_seq = self.diff_list(current_seq)
            sequences.append(next_seq)
            current_seq = next_seq

        for idx, sq in enumerate(sequences[::-1]):

            if idx == 0:
                sq.append(0)
                continue

            last_elm_idx = len(sq) - 1
            prediction = sq[last_elm_idx] + sequences[len(sequences) - idx][last_elm_idx]
            sq.append(prediction)

        return sequences[0][-1]

    @staticmethod
    def diff_list(input_list):
        return [input_list[i + 1] - input_list[i] for i in range(len(input_list) - 1)]


if __name__ == "__main__":
    day_9 = Day9()
    day_9.solve()
