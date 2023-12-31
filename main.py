import re
from copy import deepcopy


def aoc14():

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/14/14.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()




def aoc15():
    def ascii_string_helper(input_string: str) -> int:
        current_value = 0
        for cc in input_string:
            ascii_val = ord(cc)
            current_value += ascii_val
            current_value *= 17
            current_value = current_value % 256
        return current_value

    def calculate_focusing_power(box_number: int, lenses: dict) -> int:
        return sum([(box_number + 1) * (l_idx + 1) * fl for l_idx, (k, fl) in enumerate(lenses.items())])

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/15/15.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()

    data = data[0].split(",")
    lp1 = [ascii_string_helper(x) for x in data]
    print(sum(lp1))

    labels = [re.sub(r'[^a-zA-Z]', '', x) for x in data]
    box_numbers = [ascii_string_helper(ll) for ll in labels]
    operations = [re.sub(r'[^=\-]', '', x) for x in data]
    focal_lengths = []
    for x in data:
        try:
            focal_lengths.append(int(re.sub(r'[^\d]', '', x)))
        except ValueError:
            focal_lengths.append(None)

    boxes = [dict() for _ in range(256)]
    for idx, box in enumerate(box_numbers):
        lab = labels[idx]
        if operations[idx] == "-":
            if lab in boxes[box]:
                del boxes[box][lab]

        else:
            focal_length = focal_lengths[idx]
            boxes[box][lab] = focal_length

    p2 = sum([calculate_focusing_power(b_idx, bx) for b_idx, bx in enumerate(boxes)])
    print(p2)


def aoc16():
    def move(incoming_direction: str) -> tuple:
        if incoming_direction == "up":
            return 1, 0
        if incoming_direction == "down":
            return -1, 0
        if incoming_direction == "left":
            return 0, 1
        if incoming_direction == "right":
            return 0, -1

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

    def get_energized_tiles(start_pos: tuple, start_dir: str) -> int:
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
                grid_c = data[cp[0]][cp[1]]
                new_dir_list = get_new_direction(grid_c, cfd)

                for nd in new_dir_list:
                    new_move = move(nd)
                    new_pos = (cp[0] + new_move[0], cp[1] + new_move[1])

                    if 0 <= new_pos[0] < len(data) and 0 <= new_pos[1] < len(data[0]) and (
                    nd, new_pos) not in paths_tuples:
                        new_coming_from_direction.append(nd)
                        new_current_positions.append(new_pos)
                        paths_tuples.append((nd, new_pos))

            coming_from_direction = new_coming_from_direction
            current_positions = new_current_positions

        return len(energized_tiles)

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/16/16.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()

    energized_tiles_p1 = get_energized_tiles((0, 0), "left")
    print(energized_tiles_p1)

    # Get all possible starting position and directions
    # Top row
    all_possible_start_pos = [(0, x) for x in range(len(data[0]))]
    all_possible_start_dir = ["up" for _ in range(len(data[0]))]

    # Rightmost column
    all_possible_start_pos.extend([(rr, len(data[0]) - 1) for rr in range(len(data))])
    all_possible_start_dir.extend(["right" for _ in range(len(data))])

    # Bottom row
    all_possible_start_pos.extend([(len(data) - 1, cc) for cc in range(len(data[0]))])
    all_possible_start_dir.extend(["down" for _ in range(len(data[0]))])

    # Leftmost column
    all_possible_start_pos.extend([(rr, 0) for rr in range(len(data))])
    all_possible_start_dir.extend(["left" for _ in range(len(data))])

    energized_tiles_list = [get_energized_tiles(sp, sd) for sp, sd in
                            zip(all_possible_start_pos, all_possible_start_dir)]
    print(max(energized_tiles_list))


def aoc17():
    def find_min_dist(start_coordinates: tuple, end_coordinates: tuple, input_grid: list) -> int:
        t_set = [(rr, cc) for rr in range(len(input_grid)) for cc in range(len(input_grid[0]))]

        cn = start_coordinates
        cn_dist = 0
        distances = dict()
        temporary_distances = {start_coordinates: cn_dist}
        while len(t_set):
            adjacent_nodes = [(cn[0] + 1, cn[1] + 1), (cn[0] + 1, cn[1]), (cn[0] + 1, cn[1] - 1),
                              (cn[0] - 1, cn[1] + 1),
                              (cn[0] - 1, cn[1]), (cn[0] - 1, cn[1] - 1), (cn[0], cn[1] - 1), (cn[0], cn[1] + 1)]
            adjacent_nodes = list(set(adjacent_nodes) & set(t_set))

            distances[cn] = temporary_distances[cn]
            t_set.remove(cn)

            if not len(adjacent_nodes):
                break

            for xx, yy in adjacent_nodes:
                if (xx, yy) not in temporary_distances:
                    temporary_distances[(xx, yy)] = cn_dist + input_grid[xx][yy]
                    continue
                temporary_distances[(xx, yy)] = min(cn_dist + temporary_distances[(xx, yy)],
                                                    cn_dist + input_grid[xx][yy])

            next_node = None
            next_node_dist = 100000000000
            for ajn in adjacent_nodes:
                if temporary_distances[ajn] < next_node_dist:
                    next_node_dist = temporary_distances[ajn]
                    next_node = ajn

            cn = next_node
            cn_dist = next_node_dist

        return distances[end_coordinates]

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/17/17.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()

    data = [
        "2413432311323",
        "3215453535623",
        "3255245654254",
        "3446585845452",
        "4546657867536",
        "1438598798454",
        "4457876987766",
        "3637877979653",
        "4654967986887",
        "4564679986453",
        "1224686865563",
        "2546548887735",
        "4322674655533"
    ]

    data = [[int(cc) for cc in ss] for ss in data]

    start_p1 = (0, 0)
    end_p1 = (len(data) - 1, len(data[0]) - 1)
    min_dist = find_min_dist(start_p1, end_p1, data)
    print(min_dist)


if __name__ == "__main__":
    aoc17()
