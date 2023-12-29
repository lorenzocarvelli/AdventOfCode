import re

from base import DailyPuzzle


class Day1(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "1")

    def solve(self):
        cv = []
        for ll in self.data:
            fd = re.search(r"\d", ll).group(0)
            ld = re.search(r"\d", ll[::-1]).group(0)
            cal_v = int(f"{fd}{ld}")
            cv.append(cal_v)

        print(sum(cv))

        n_dict = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7",
                  "eight": "8",
                  "nine": "9"}
        cv2 = []
        for ll in self.data:
            matches = [(match.group(), match.start()) for match in re.finditer(r"\d", ll)]
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"one", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"two", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"three", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"four", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"five", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"six", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"seven", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"eight", ll)])
            matches.extend([(match.group(), match.start()) for match in re.finditer(r"nine", ll)])

            first_tuple = min(matches, key=lambda x: x[1])
            first_n = first_tuple[0]
            if first_n in n_dict:
                first_n = n_dict[first_n]

            last_tuple = max(matches, key=lambda x: x[1])
            last_n = last_tuple[0]
            if last_n in n_dict:
                last_n = n_dict[last_n]

            nn = int(f"{first_n}{last_n}")
            cv2.append(nn)

        print(sum(cv2))


if __name__ == "__main__":
    day_1 = Day1()
    day_1.solve()
