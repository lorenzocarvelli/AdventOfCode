import re

from base import DailyPuzzle


class Day6(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "6")

    def solve(self):
        times = []
        distances = []
        times_puzzle_2 = 0
        distance_puzzle_2 = 0
        for ll in self.data:
            if ll.startswith("Time"):
                times = [int(ss) for ss in re.findall(r"\d+", ll.strip())]
                t_str_p2 = ""
                for t in times:
                    t_str_p2 += str(t)
                times_puzzle_2 = int(t_str_p2)

            if ll.startswith("Distance"):
                distances = [int(ss) for ss in re.findall(r"\d+", ll.strip())]
                d_str_p2 = ""
                for d in distances:
                    d_str_p2 += str(d)
                distance_puzzle_2 = int(d_str_p2)

        record_multiplier = 1
        for idx, tt in enumerate(times):
            max_d = distances[idx]
            possible_distances_for_race = [hold * (tt - hold) for hold in range(tt + 1)]

            record_multiplier *= sum([pd > max_d for pd in possible_distances_for_race])

        print(record_multiplier)

        possible_distances_for_race_p2 = [hold * (times_puzzle_2 - hold) for hold in range(times_puzzle_2 + 1)]
        print(sum([pd > distance_puzzle_2 for pd in possible_distances_for_race_p2]))


if __name__ == "__main__":
    day_6 = Day6()
    day_6.solve()
