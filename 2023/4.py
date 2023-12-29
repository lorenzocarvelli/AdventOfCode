import re

from base import DailyPuzzle


class Day4(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "4")

    def solve(self):
        points = []
        cards_matches = dict()
        for idx, ll in enumerate(self.data):
            card_number = idx + 1

            winning_numbers_str = re.match(r".+:(.+)\|", ll).group(1)
            my_numbers_str = re.match(r".+\|(.+)$", ll).group(1)

            winning_numbers = [int(wn) for wn in re.findall(r"\d+", winning_numbers_str)]
            my_numbers = [int(mn) for mn in re.findall(r"\d+", my_numbers_str)]

            matches = len(list(set(winning_numbers) & set(my_numbers)))
            if matches > 0:
                points.append(2 ** (matches - 1))

            cards_matches[card_number] = matches

        print(sum(points))

        card_copies = [1] * len(cards_matches)
        for c_number, c_matches in cards_matches.items():
            for j in range(c_number, c_number + c_matches):
                card_copies[j] += card_copies[c_number - 1]

        print(sum(card_copies))


if __name__ == "__main__":
    day_4 = Day4()
    day_4.solve()
