import re
import math
from copy import deepcopy
from itertools import combinations


def aoc10():

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/10/10.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()



def aoc11():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/11/11.txt"
    with open(input_file_path, "r") as f_open:
        data = [ll.strip() for ll in f_open.readlines()]
        f_open.close()

    unexpanded_data = deepcopy(data)

    # Find rows and columns with no galaxies
    no_galaxies_rows = []
    columns = ["" for _ in range(len(data[0]))]
    no_galaxies_columns = []
    for r_idx, rr in enumerate(data):

        for c_idx, ch in enumerate(rr):
            columns[c_idx] += ch

        if all(ch == "." for ch in rr):
            no_galaxies_rows.append(r_idx)

    for c_idx, cc in enumerate(columns):

        if all(ch == "." for ch in cc):
            no_galaxies_columns.append(c_idx)

    # Inserting rows and columns where there are no galaxies
    for idx_sum, r_insert_idx in enumerate(no_galaxies_rows):
        data.insert(r_insert_idx + idx_sum, "." * len(data[0]))

    for idx_sum_c, c_insert_idx in enumerate(no_galaxies_columns):
        for r_idx, _ in enumerate(data):
            data[r_idx] = data[r_idx][:(c_insert_idx + idx_sum_c)] + "." + data[r_idx][(
                                                                                                   c_insert_idx + idx_sum_c):]  # TODO: an issue might be here

    # Find coordinates of galaxies
    galaxies_coordinates = []
    for r_idx, rr in enumerate(data):
        for c_idx, c in enumerate(rr):
            if c == "#":
                galaxies_coordinates.append((r_idx, c_idx))

    galaxies_indices = [gg for gg, _ in enumerate(galaxies_coordinates)]
    pair_combinations = list(combinations(galaxies_indices, 2))

    closest_paths = []
    for g1, g2 in pair_combinations:
        min_distance = abs(galaxies_coordinates[g1][0] - galaxies_coordinates[g2][0]) + abs(
            galaxies_coordinates[g1][1] - galaxies_coordinates[g2][1])
        closest_paths.append(min_distance)
    print(sum(closest_paths))

    # Find coordinates of galaxies
    unexpanded_galaxies_coordinates = []
    for r_idx, rr in enumerate(unexpanded_data):
        for c_idx, c in enumerate(rr):
            if c == "#":
                unexpanded_galaxies_coordinates.append((r_idx, c_idx))

    expansion_factor = 1000000 - 1
    paths = []
    for g1, g2 in pair_combinations:
        min_r = min(unexpanded_galaxies_coordinates[g1][0], unexpanded_galaxies_coordinates[g2][0])
        max_r = max(unexpanded_galaxies_coordinates[g1][0], unexpanded_galaxies_coordinates[g2][0])
        min_c = min(unexpanded_galaxies_coordinates[g1][1], unexpanded_galaxies_coordinates[g2][1])
        max_c = max(unexpanded_galaxies_coordinates[g1][1], unexpanded_galaxies_coordinates[g2][1])
        expansion_rows = len([r for r in no_galaxies_rows if min_r <= r <= max_r])
        expansion_cols = len([c for c in no_galaxies_columns if min_c <= c <= max_c])
        min_distance = abs(unexpanded_galaxies_coordinates[g1][0] - unexpanded_galaxies_coordinates[g2][0]) + \
                       abs(unexpanded_galaxies_coordinates[g1][1] - unexpanded_galaxies_coordinates[g2][1]) + \
                       expansion_factor * (expansion_rows) + expansion_factor * (expansion_cols)
        paths.append(min_distance)
    print(sum(paths))


def aoc12():
    def find_all_possible_arrangements(s_in: str, n_list: list) -> int:
        question_mark_positions = [idx for idx, c in enumerate(s_in) if c == "?"]

        all_possible_strings = [s_in]
        while "?" in all_possible_strings[0]:
            next_qmp = question_mark_positions[0]
            question_mark_positions.pop(0)

            new_all_possible_strings = []
            for ps in all_possible_strings:
                new_all_possible_strings.append(replace_char_at_position(ps, next_qmp, "."))
                new_all_possible_strings.append(replace_char_at_position(ps, next_qmp, "#"))

            # Pruning
            print(1)

            all_possible_strings = new_all_possible_strings

        out = 0
        for aps in all_possible_strings:
            cl = cluster_lengths(aps)
            if cl == n_list:
                out += 1

        return out

    def replace_char_at_position(input_string, position, replacement_char):
        string_list = list(input_string)
        string_list[position] = replacement_char
        return ''.join(string_list)

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

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/12/12.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()

    data = [
        "???.### 1,1,3",
        ".??..??...?##. 1,1,3",
        "?#?#?#?#?#?#?#? 1,3,1,6",
        "????.#...#... 4,1,1",
        "????.######..#####. 1,6,5",
        "?###???????? 3,2,1"
    ]

    possible_arrangements_pt1 = []
    possible_arrangements_pt2 = []
    for ll in data:
        string_input = re.match("(.+) ", ll).group(1)
        nn = [int(n) for n in re.findall(r"\d+", ll)]

        string_input_p2 = f"{string_input}?{string_input}?{string_input}?{string_input}?{string_input}"
        nn2 = nn * 5

        # Part 1
        allowed_arrangements_pt1 = find_all_possible_arrangements(string_input, nn)
        possible_arrangements_pt1.append(allowed_arrangements_pt1)

        # Part 2
        allowed_arrangements_pt2 = find_all_possible_arrangements(string_input_p2, nn2)
        possible_arrangements_pt2.append(allowed_arrangements_pt2)

    print(sum(possible_arrangements_pt1))
    print(sum(possible_arrangements_pt2))


def aoc13():
    def find_symmetry(input_list: list) -> (list, list):
        out = []
        output_pt2 = []
        for index, _ in enumerate(input_list):
            lines_before_axis = index + 1
            lines_after_axis = len(input_list) - (index + 1)
            lines_to_consider = min(lines_before_axis, lines_after_axis)

            if lines_to_consider == 0:
                break

            symmetry = True
            d_idx = 0
            for ltc in range(lines_to_consider):
                lb = input_list[index - ltc]
                la = input_list[index + ltc + 1]

                if lb != la:
                    symmetry = False
                    for c_idx, cc in enumerate(lb):
                        if cc != la[c_idx]:
                            d_idx += 1

            if symmetry:
                out.append((index + 1, index + 2))

            if d_idx == 1:
                output_pt2.append((index + 1, index + 2))

        return out, output_pt2

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/13/13.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()

    blocks = []
    block = []
    for idx, ll in enumerate(data):
        if ll == "" or idx == len(data) - 1:
            blocks.append(block)
            block = []
            continue
        block.append(ll)

    p1 = 0
    p2 = 0
    for block in blocks:
        columns = [[] for _ in range(len(block[0]))]
        for r_idx, rr in enumerate(block):

            # Updating columns for next step
            for ci in range(len(block[0])):
                columns[ci].append(rr[ci])

        hs, hs_pt2 = find_symmetry(block)
        vs, vs_pt2 = find_symmetry(columns)

        # Summarizing for part 1
        if len(hs) + len(vs) > 1:  # The last line has 2 symmetry axes... Might it be a bug in the input data?
            hs = []

        for hh in hs:
            p1 += hh[0] * 100

        for vv in vs:
            p1 += vv[0]

        # Summarizing for part 2
        if len(hs_pt2) + len(vs_pt2) > 1 or len(hs_pt2) + len(
                vs_pt2) == 0:  # The last line has 2 symmetry axes... Might it be a bug in the input data?
            raise  # TODO: remove

        for hh2 in hs_pt2:
            p2 += hh2[0] * 100

        for vv2 in vs_pt2:
            p2 += vv2[0]

    print(p1)
    print(p2)


def aoc14():
    def get_total_load(round_rocks_in: list, total_rows: int):
        out = 0
        for ri in range(total_rows):
            round_rocks_in_row = len([rrk for rrk in round_rocks_in if rrk[0] == ri])
            out += (tr - ri) * round_rocks_in_row
        return out

    def tilt(round_rks: list, square_rks: list, direction: str, total_rows: int, total_cols: int):
        idx = 0
        while idx < len(round_rks):
            rr_row, rr_col = round_rks[idx]

            objects_in_same_column = [rrr for rrr in round_rks if rrr[1] == rr_col and rrr != (rr_row, rr_col)]
            objects_in_same_column.extend([srr for srr in square_rks if srr[1] == rr_col])
            objects_in_same_column.append((-1, rr_col) if direction == "north" else (total_rows, rr_col))

            objects_in_same_row = [rrr for rrr in round_rks if rrr[0] == rr_row and rrr != (rr_row, rr_col)]
            objects_in_same_row.extend([srr for srr in square_rks if srr[0] == rr_row])
            objects_in_same_row.append((rr_row, -1) if direction == "west" else (rr_row, total_cols))

            new_row_coordinate = rr_row
            if direction == "north":
                closest_object_north = max([osc for osc in objects_in_same_column if osc[0] < rr_row])
                new_row_coordinate = closest_object_north[0] + 1
            elif direction == "south":
                closest_object_south = min([osc for osc in objects_in_same_column if osc[0] > rr_row])
                new_row_coordinate = closest_object_south[0] - 1
            elif direction == "west":
                pass
            elif direction == "east":
                pass

            round_rks[idx] = (new_row_coordinate, rr_col)
            idx += 1
        return round_rks

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/14/14.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()

    round_rocks = []
    square_rocks = []
    for r_idx, row in enumerate(data):
        for c_idx, ccc in enumerate(row):
            if ccc == "O":
                round_rocks.append((r_idx, c_idx))
                continue
            if ccc == "#":
                square_rocks.append((r_idx, c_idx))

    # Round rocks will go north
    tr = len(data)
    tc = len(data[0])
    round_rocks1 = deepcopy(round_rocks)
    round_rocks1 = tilt(round_rocks1, square_rocks, "north", tr, tc)

    p1 = get_total_load(round_rocks1, tr)
    print(p1)  # 108857

    one_cycle_configuration = []
    configurations = []
    ii = 0
    cycles = 1000000000
    while ii < cycles:
        round_rocks = tilt(round_rocks, square_rocks, "north", tr, tc)
        round_rocks = tilt(round_rocks, square_rocks, "west", tr, tc)
        round_rocks = tilt(round_rocks, square_rocks, "south", tr, tc)
        round_rocks = tilt(round_rocks, square_rocks, "east", tr, tc)

        if ii == 0:
            one_cycle_configuration = round_rocks

        if ii > 0 and all(rrk in one_cycle_configuration for rrk in round_rocks):
            break

        configurations.append(round_rocks)

    out_i = cycles % ii
    p2 = get_total_load(configurations[out_i], tr)
    print(p2)


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
