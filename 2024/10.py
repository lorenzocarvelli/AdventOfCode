from typing import List, Tuple, Dict

from base import DailyPuzzle


class Day10(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "10")

    def solve(self):
        coordinate_dict = dict()
        n_rows = len(self.data)
        n_cols = len(self.data[0])
        for row_idx, ll in enumerate(self.data):
            for col_idx, cc in enumerate(ll):
                coordinate_dict[(row_idx, col_idx)] = int(cc)

        sol_1 = self.calculate_total_scores_for_all_trail_heads(coordinate_dict, n_rows, n_cols)
        print(sol_1)

        sol_2 = self.calculate_total_scores_for_all_trail_heads(coordinate_dict, n_rows, n_cols, part_1=False)
        print(sol_2)

    def calculate_total_scores_for_all_trail_heads(self, coordinate_dict: Dict[Tuple[int, int], int],
                                                   n_rows: int, n_cols: int, part_1=True) -> int:
        trail_heads = [coordinates for coordinates, height in coordinate_dict.items() if height == 0]
        out = 0
        for th in trail_heads:
            current_coordinates = [th]

            while len(current_coordinates):
                new_current_coordinates = []
                for cc in current_coordinates:
                    new_current_coordinates.extend(self.find_adjacent_suitable_positions(cc, coordinate_dict, n_rows, n_cols))

                # Updating current coordinates and total scores
                current_coordinates = []
                if part_1:
                    new_current_coordinates = list(set(new_current_coordinates))

                for ncc in new_current_coordinates:
                    if coordinate_dict[ncc] == 9:
                        out += 1
                        continue
                    current_coordinates.append(ncc)
        return out

    @staticmethod
    def find_adjacent_suitable_positions(position: Tuple[int, int], coordinate_dict: Dict[Tuple[int, int], int],
                                         n_rows: int, n_cols: int) -> List[Tuple[int, int]]:
        up = (-1, 0)
        down = (1, 0)
        left = (0, -1)
        right = (0, 1)

        pos_up = (position[0] + up[0], position[1] + up[1])
        pos_down = (position[0] + down[0], position[1] + down[1])
        pos_left = (position[0] + left[0], position[1] + left[1])
        pos_right = (position[0] + right[0], position[1] + right[1])

        current_n = coordinate_dict[position]
        n_up = coordinate_dict[pos_up] if pos_up[0] >= 0 else -1
        n_down = coordinate_dict[pos_down] if pos_down[0] < n_rows else -1
        n_left = coordinate_dict[pos_left] if pos_left[1] >= 0 else -1
        n_right = coordinate_dict[pos_right] if pos_right[1] < n_cols else -1

        out = []
        if n_up == current_n + 1:
            out.append(pos_up)
        if n_down == current_n + 1:
            out.append(pos_down)
        if n_left == current_n + 1:
            out.append(pos_left)
        if n_right == current_n + 1:
            out.append(pos_right)

        return out


if __name__ == "__main__":
    day_10 = Day10()
    day_10.solve()
