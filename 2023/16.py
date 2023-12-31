from base import DailyPuzzle


class Day16(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "16")

    def solve(self):
        energized_tiles_p1 = self.get_energized_tiles((0, 0), "left")
        print(energized_tiles_p1)

        # Get all possible starting position and directions
        # Top row
        all_possible_start_pos = [(0, x) for x in range(len(self.data[0]))]
        all_possible_start_dir = ["up" for _ in range(len(self.data[0]))]

        # Rightmost column
        all_possible_start_pos.extend([(rr, len(self.data[0]) - 1) for rr in range(len(self.data))])
        all_possible_start_dir.extend(["right" for _ in range(len(self.data))])

        # Bottom row
        all_possible_start_pos.extend([(len(self.data) - 1, cc) for cc in range(len(self.data[0]))])
        all_possible_start_dir.extend(["down" for _ in range(len(self.data[0]))])

        # Leftmost column
        all_possible_start_pos.extend([(rr, 0) for rr in range(len(self.data))])
        all_possible_start_dir.extend(["left" for _ in range(len(self.data))])

        energized_tiles_list = [self.get_energized_tiles(sp, sd) for sp, sd in
                                zip(all_possible_start_pos, all_possible_start_dir)]
        print(max(energized_tiles_list))

    @staticmethod
    def move(incoming_direction: str) -> tuple:
        if incoming_direction == "up":
            return 1, 0
        if incoming_direction == "down":
            return -1, 0
        if incoming_direction == "left":
            return 0, 1
        if incoming_direction == "right":
            return 0, -1

    @staticmethod
    def get_new_direction(input_c: str, current_direction: str) -> list:
        if input_c == ".":
            return [current_direction]

        if input_c == "\\":
            io_dict = {
                "up": ["left"],
                "down": ["right"],
                "left": ["up"],
                "right": ["down"]
            }
            return io_dict[current_direction]

        if input_c == "/":
            io_dict = {
                "up": ["right"],
                "down": ["left"],
                "left": ["down"],
                "right": ["up"]
            }
            return io_dict[current_direction]

        if input_c == "|":
            io_dict = {
                "up": ["up"],
                "down": ["down"],
                "left": ["up", "down"],
                "right": ["up", "down"]
            }
            return io_dict[current_direction]

        if input_c == "-":
            io_dict = {
                "up": ["left", "right"],
                "down": ["left", "right"],
                "left": ["left"],
                "right": ["right"]
            }
            return io_dict[current_direction]

    def get_energized_tiles(self, start_pos: tuple, start_dir: str) -> int:
        paths_tuples = []
        fail_safe = 0
        energized_tiles = []
        current_positions = [start_pos]
        coming_from_direction = [start_dir]
        while len(current_positions):

            # Updating energized tiles
            no_tiles_appended = True
            for cp in current_positions:
                if cp not in energized_tiles:
                    energized_tiles.append(cp)
                    no_tiles_appended = False
                    # fail_safe = 0
            if no_tiles_appended:
                fail_safe += 1

            if fail_safe >= 1000:
                break

            # Updating directions coming from
            new_coming_from_direction = []
            new_current_positions = []
            for c_idx, cfd in enumerate(coming_from_direction):
                cp = current_positions[c_idx]
                grid_c = self.data[cp[0]][cp[1]]
                new_dir_list = self.get_new_direction(grid_c, cfd)

                for nd in new_dir_list:
                    new_move = self.move(nd)
                    new_pos = (cp[0] + new_move[0], cp[1] + new_move[1])

                    if 0 <= new_pos[0] < len(self.data) and 0 <= new_pos[1] < len(self.data[0]) and (nd, new_pos) not in paths_tuples:
                        new_coming_from_direction.append(nd)
                        new_current_positions.append(new_pos)
                        paths_tuples.append((nd, new_pos))

            coming_from_direction = new_coming_from_direction
            current_positions = new_current_positions

        return len(energized_tiles)


if __name__ == "__main__":
    day_16 = Day16()
    day_16.solve()
