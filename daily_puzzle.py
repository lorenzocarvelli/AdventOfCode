import os
from typing import List


class DailyPuzzle(object):
    def __init__(self, year: str, day: str):
        self.year: str = year
        self.day: str = day

        self.data_folder: str = os.path.join(os.path.dirname(__file__), "data")
        self.data_file: str = os.path.join(self.data_folder, self.year, f"{self.day}.txt")

        self.data: List[str] = self.load_data()

    def load_data(self) -> List[str]:
        with open(self.data_file, "r") as f_open:
            out = [ld.rstrip('\n') for ld in f_open.readlines()]
            f_open.close()
        return out
    