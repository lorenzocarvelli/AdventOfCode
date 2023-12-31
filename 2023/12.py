import re

from base import DailyPuzzle


class Day12(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "12")

    def solve(self):
        """data = [
            "???.### 1,1,3",
            ".??..??...?##. 1,1,3",
            "?#?#?#?#?#?#?#? 1,3,1,6",
            "????.#...#... 4,1,1",
            "????.######..#####. 1,6,5",
            "?###???????? 3,2,1"
        ]"""

        possible_arrangements_pt1 = []
        possible_arrangements_pt2 = []
        for ll in self.data:
            string_input = re.match("(.+) ", ll).group(1)
            nn = [int(n) for n in re.findall(r"\d+", ll)]

            string_input_p2 = f"{string_input}?{string_input}?{string_input}?{string_input}?{string_input}"
            nn2 = nn * 5

            # Part 1
            allowed_arrangements_pt1 = self.find_all_possible_arrangements(string_input, nn)
            possible_arrangements_pt1.append(allowed_arrangements_pt1)

            # Part 2
            # allowed_arrangements_pt2 = self.find_all_possible_arrangements(string_input_p2, nn2)
            # possible_arrangements_pt2.append(allowed_arrangements_pt2)

        print(sum(possible_arrangements_pt1))
        print(sum(possible_arrangements_pt2))

    def find_all_possible_arrangements(self, s_in: str, n_list: list) -> int:
        question_mark_positions = [idx for idx, c in enumerate(s_in) if c == "?"]

        all_possible_strings = [s_in]
        while "?" in all_possible_strings[0]:
            next_qmp = question_mark_positions[0]
            question_mark_positions.pop(0)

            new_all_possible_strings = []
            for ps in all_possible_strings:
                new_all_possible_strings.append(self.replace_char_at_position(ps, next_qmp, "."))
                new_all_possible_strings.append(self.replace_char_at_position(ps, next_qmp, "#"))

            # Pruning
            # print(1)  # TODO

            all_possible_strings = new_all_possible_strings

        out = 0
        for aps in all_possible_strings:
            cl = self.cluster_lengths(aps)
            if cl == n_list:
                out += 1

        return out

    @staticmethod
    def replace_char_at_position(input_string, position, replacement_char):
        string_list = list(input_string)
        string_list[position] = replacement_char
        return ''.join(string_list)

    @staticmethod
    def cluster_lengths(input_str):
        if not input_str:
            return []

        clusters = []
        current_length = 0

        for char in input_str:
            if char == '#':
                current_length += 1
            elif current_length > 0:
                clusters.append(current_length)
                current_length = 0

        if current_length > 0:
            clusters.append(current_length)

        return clusters


if __name__ == "__main__":
    day_12 = Day12()
    day_12.solve()
