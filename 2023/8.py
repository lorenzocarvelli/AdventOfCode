import re
import math

from base import DailyPuzzle


class Day8(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "8")

    def solve(self):
        instructions = self.data[0].strip()
        coordinates = dict()
        for dd in self.data[2:]:
            k, t = dd.split("=")
            left = re.match(r" \((.+),", t).group(1)
            right = re.match(r".+, (.+)\)", t).group(1)
            coordinates[k.strip()] = {
                "L": left,
                "R": right
            }

        kk = "AAA"
        end_kk = "ZZZ"
        steps = 0
        idx = 0
        while kk != end_kk:
            single_instruction = instructions[idx]
            kk = coordinates[kk][single_instruction]
            steps += 1
            if kk == end_kk:
                break
            idx = (idx + 1) % len(instructions)
        print(steps)

        current_coordinates = [c for c in coordinates if c.endswith("A")]
        end_points_indices = [[] for _ in range(len(current_coordinates))]
        i_idx = 0
        increment = 0
        while not all(len(ep) for ep in end_points_indices):
            ii = instructions[i_idx]
            current_coordinates = [coordinates[cc][ii] for cc in current_coordinates]
            increment += 1

            for c_idx, ccc in enumerate(current_coordinates):
                if ccc.endswith("Z"):
                    end_points_indices[c_idx].append(increment)

            i_idx = (i_idx + 1) % len(instructions)

        count = [epl[0] for epl in end_points_indices]
        print(math.lcm(*count))

    @staticmethod
    def lcm(a, b):
        return (a * b) // math.gcd(a, b)


if __name__ == "__main__":
    day_8 = Day8()
    day_8.solve()
