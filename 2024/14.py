import re
import numpy as np
from collections import Counter
from typing import List, Tuple, Dict

from base import DailyPuzzle


class Day14(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "14")

    def calculate_entropy(self, coordinates: List[Tuple[int, int]], xmax, ymax):
        img = self.robots_to_grid(coordinates, xmax, ymax)
        marg = np.histogramdd(np.ravel(img), bins=256)[0] / img.size
        marg = list(filter(lambda p: p > 0, np.ravel(marg)))
        entropy = -np.sum(np.multiply(marg, np.log2(marg)))
        return entropy

    @staticmethod
    def robots_to_grid(robots, xmax, ymax):
        grid = np.zeros((ymax, xmax), dtype=int)
        for x, y in robots:
            grid[y, x] += 1
        return grid

    @staticmethod
    def print_grid(robots_positions: List[Tuple[int, int]], x_bound: int, y_bound: int):
        counts = Counter(robots_positions)
        for y in range(y_bound):
            ltp = ""
            for x in range(x_bound):
                n = counts[(x, y)]
                if not n:
                    ltp += "."
                    continue
                ltp += str(n)
            print(ltp)

    @staticmethod
    def get_grid_coordinates_at_time_t(robots: List[Dict[str, Tuple[int, int]]], t: int, bound_x: int, bound_y: int) \
            -> List[Tuple[int, int]]:
        out = []
        for robot in robots:
            x0, y0 = robot["p0"][0], robot["p0"][1]
            vx0, vy0 = robot["v0"][0], robot["v0"][1]
            p = (int((x0 + t * vx0) % bound_x), int((y0 + t * vy0) % bound_y))
            out.append(p)
        return out

    def solve(self):
        # Parsing input
        robots = []
        for ll in self.data:
            x0 = int(re.match(r"p=(-*\d+),", ll).group(1))
            y0 = int(re.match(r"p=-*\d+,(-*\d+)", ll).group(1))

            vx0 = int(re.match(r"p=-*\d+,-*\d+ v=(-*\d+),", ll).group(1))
            vy0 = int(re.match(r"p=-*\d+,-*\d+ v=-*\d+,(-*\d+)", ll).group(1))
            robots.append({"p0": (x0, y0), "v0": (vx0, vy0)})

        # Part 1: positions occupied after t=100
        bound_x = 101
        bound_y = 103
        divider_x = int(bound_x/2)
        divider_y = int(bound_y/2)
        t = 100

        robots_p_100 = {"Q1": [], "Q2": [], "Q3": [], "Q4": []}
        for robot in robots:
            x0, y0 = robot["p0"][0], robot["p0"][1]
            vx0, vy0 = robot["v0"][0], robot["v0"][1]
            p100 = (int((x0+t*vx0) % bound_x), int((y0+t*vy0) % bound_y))

            if p100[0] == divider_x or p100[1] == divider_y:
                continue

            if p100[0] > divider_x and p100[1] > divider_y:
                robots_p_100["Q1"].append(p100)
            if p100[0] > divider_x and p100[1] < divider_y:
                robots_p_100["Q2"].append(p100)
            if p100[0] < divider_x and p100[1] > divider_y:
                robots_p_100["Q3"].append(p100)
            if p100[0] < divider_x and p100[1] < divider_y:
                robots_p_100["Q4"].append(p100)

        sol_1 = len(robots_p_100["Q1"]) * len(robots_p_100["Q2"]) * len(robots_p_100["Q3"]) * len(robots_p_100["Q4"])
        print(sol_1)

        # Part 2 - using entropy, implemented as in: https://stackoverflow.com/questions/50313114/what-is-the-entropy-of-an-image-and-how-is-it-calculated
        entropies = dict()
        for tt in range(10000):

            positions = []
            for robot in robots:
                x0, y0 = robot["p0"][0], robot["p0"][1]
                vx0, vy0 = robot["v0"][0], robot["v0"][1]
                ptt = (int((x0 + tt * vx0) % bound_x), int((y0 + tt * vy0) % bound_y))
                positions.append(ptt)

            entropy = self.calculate_entropy(positions, bound_x, bound_y)
            entropies[tt] = entropy

        t_with_lowest_value = min(entropies, key=entropies.get)
        ee_positions = []
        for robot in robots:
            x0, y0 = robot["p0"][0], robot["p0"][1]
            vx0, vy0 = robot["v0"][0], robot["v0"][1]
            ptt = (int((x0 + t_with_lowest_value * vx0) % bound_x), int((y0 + t_with_lowest_value * vy0) % bound_y))
            ee_positions.append(ptt)
        self.print_grid(ee_positions, bound_x, bound_y)
        print(t_with_lowest_value)


if __name__ == "__main__":
    day_14 = Day14()
    day_14.solve()
