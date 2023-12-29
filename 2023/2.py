import re

from base import DailyPuzzle


class Day2(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "2")

    def solve(self):
        allowed_cubes = {
            "red": 12,
            "green": 13,
            "blue": 14
        }

        allowed_ids = 0
        powers = 0
        for ll in self.data:
            allowed = True
            game_id = int(re.match(r"Game (\d+):", ll).group(1))

            games_str = re.match(r"Game \d+:(.+?)$", ll).group(1)
            games_list = re.findall(r"(.+?);", games_str)
            games_list.append(re.match(".+" + games_list[-1] + ";(.+)$", games_str).group(1))

            min_power = {
                "red": 0,
                "blue": 0,
                "green": 0
            }

            for game in games_list:
                red_cubes_match = re.match(r".*?(\d+) red", game)
                blue_cubes_match = re.match(r".*?(\d+) blue", game)
                green_cubes_match = re.match(r".*?(\d+) green", game)

                red_cubes = int(red_cubes_match.group(1)) if red_cubes_match else 0
                blue_cubes = int(blue_cubes_match.group(1)) if blue_cubes_match else 0
                green_cubes = int(green_cubes_match.group(1)) if green_cubes_match else 0

                if red_cubes > allowed_cubes["red"] or blue_cubes > allowed_cubes["blue"] or green_cubes > \
                        allowed_cubes[
                            "green"]:
                    allowed = False

                if red_cubes > min_power["red"]:
                    min_power["red"] = red_cubes

                if blue_cubes > min_power["blue"]:
                    min_power["blue"] = blue_cubes

                if green_cubes > min_power["green"]:
                    min_power["green"] = green_cubes

            if allowed:
                allowed_ids += game_id

            powers += min_power["red"] * min_power["blue"] * min_power["green"]

        print(allowed_ids)
        print(powers)


if __name__ == "__main__":
    day_2 = Day2()
    day_2.solve()
