from base import DailyPuzzle


class Day1(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "1")

    def solve(self):
        # Parsing text data into two lists
        l1 = []
        l2 = []
        for txt_line in self.data:
            line_split = txt_line.split("   ")
            l1.append(int(line_split[0]))
            l2.append(int(line_split[1]))

        # Sorting lists
        sl1 = sorted(l1)
        sl2 = sorted(l2)

        # Solution to part 1 - sum of absolute distances
        distances = [abs(elm_1 - elm_2) for elm_1, elm_2 in zip(sl1, sl2)]
        print(sum(distances))

        # Solution to part 2 - "similarity score", i.e. addition of each number in the left list multiplied by its n
        # of occurrences in the right list.
        sol2 = 0
        for elm_1 in l1:
            sol2 += elm_1 * l2.count(elm_1)
        print(sol2)


if __name__ == "__main__":
    day_1 = Day1()
    day_1.solve()
