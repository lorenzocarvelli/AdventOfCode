import re
import math
from copy import deepcopy
from itertools import combinations


def aoc1():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/1/1.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    cv = []
    for ll in data:
        fd = re.search(r"\d", ll).group(0)
        ld = re.search(r"\d", ll[::-1]).group(0)
        cal_v = int(f"{fd}{ld}")
        cv.append(cal_v)

    print(sum(cv))

    n_dict = {"one": "1", "two": "2", "three": "3", "four": "4", "five": "5", "six": "6", "seven": "7", "eight": "8",
              "nine": "9"}
    cv2 = []
    for ll in data:
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


def aoc2():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/2/2.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    allowed_cubes = {
        "red": 12,
        "green": 13,
        "blue": 14
    }

    allowed_ids = 0
    powers = 0
    for ll in data:
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

            if red_cubes > allowed_cubes["red"] or blue_cubes > allowed_cubes["blue"] or green_cubes > allowed_cubes[
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


def aoc3():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/3/3.txt"
    with open(input_file_path, "r") as fopen:
        data = fopen.readlines()
        fopen.close()

    polished_data = [d.strip() for d in data]
    engine_parts_n = []

    matches_tuples = []
    for idx, data_line in enumerate(polished_data):
        for m in re.finditer(r"\d+", data_line):
            n = int(m.group(0))
            start_col_idx = m.start(0)
            end_col_idx = m.end(0)

            matches_tuples.append((n, [cdx for cdx in range(start_col_idx, end_col_idx)], idx))

            previous_col_idx = start_col_idx - 1
            next_col_idx = end_col_idx + 1

            contour_pts = []
            previous_row_idx = idx - 1
            next_row_idx = idx + 1

            # Adding contour points
            if previous_col_idx >= 0:
                contour_pts.append(data_line[previous_col_idx])
            else:
                previous_col_idx += 1

            if end_col_idx < len(data_line):
                contour_pts.append(data_line[end_col_idx])
            else:
                next_col_idx -= 1

            if previous_row_idx >= 0:
                for ii in range(previous_col_idx, next_col_idx):
                    contour_pts.append(polished_data[previous_row_idx][ii])

            if next_row_idx < len(polished_data):
                for jj in range(previous_col_idx, next_col_idx):
                    contour_pts.append(polished_data[next_row_idx][jj])

            if any([cp != "." for cp in contour_pts]):
                engine_parts_n.append(n)

    print(sum(engine_parts_n))

    ratios = []
    for jdx, ll in enumerate(polished_data):
        for star_match in re.finditer(r"\*", ll):
            start_col_idx_star = star_match.start(0)
            end_col_idx_star = star_match.end(0)

            above = [mt for mt in matches_tuples if mt[2] == jdx - 1 and (
                        start_col_idx_star - 1 in mt[1] or end_col_idx_star in mt[1] or start_col_idx_star in mt[1])]
            below = [mt for mt in matches_tuples if mt[2] == jdx + 1 and (
                        start_col_idx_star - 1 in mt[1] or end_col_idx_star in mt[1] or start_col_idx_star in mt[1])]
            same_line = [mt for mt in matches_tuples if
                         mt[2] == jdx and (start_col_idx_star - 1 in mt[1] or end_col_idx_star in mt[1])]

            adjacent_numbers = above + below + same_line

            if len(adjacent_numbers) == 2:
                ratios.append(adjacent_numbers[0][0] * adjacent_numbers[1][0])

    print(sum(ratios))


def aoc4():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/4/4.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    points = []
    cards_matches = dict()
    for idx, ll in enumerate(data):
        card_number = idx + 1

        winning_numbers_str = re.match(r".+:(.+)\|", ll).group(1)
        my_numbers_str = re.match(r".+\|(.+)$", ll).group(1)

        winning_numbers = [int(wn) for wn in re.findall(r"\d+", winning_numbers_str)]
        my_numbers = [int(mn) for mn in re.findall(r"\d+", my_numbers_str)]

        matches = len(list(set(winning_numbers) & set(my_numbers)))
        if matches > 0:
            points.append(2 ** (matches - 1))

        cards_matches[card_number] = matches

    print(sum(points))

    card_copies = [1] * len(cards_matches)
    for c_number, c_matches in cards_matches.items():
        for j in range(c_number, c_number + c_matches):
            card_copies[j] += card_copies[c_number - 1]

    print(sum(card_copies))


def aoc5():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/5/5.txt"
    # input_file_path = "/Users/lorenzocarvelli/Library/Application Support/JetBrains/PyCharmCE2022.2/scratches/test.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    seeds = []
    seed_to_soil = []
    soil_to_fertilizer = []
    fertilizer_to_water = []
    water_to_light = []
    light_to_temperature = []
    temperature_to_humidity = []
    humidity_to_location = []

    parsing_seed_to_soil = False
    parsing_soil_to_fertilizer = False
    parsing_fertilizer_to_water = False
    parsing_water_to_light = False
    parsing_light_to_temperature = False
    parsing_temperature_to_humidity = False
    parsing_humidity_to_location = False
    parsing = False

    range_tuple = ()
    seeds_pt2 = []

    for ll in data:
        if ll.startswith("seeds"):
            seeds = [int(ss) for ss in re.findall(r"\d+", ll.strip())]
            seeds_pt2 = [(seeds[idx], seeds[idx + 1]) for idx in range(0, len(seeds), 2)]
            continue

        if ll.startswith("seed-to-soil map"):
            parsing_seed_to_soil = True
            parsing = True
            continue

        if ll.startswith("soil-to-fertilizer map"):
            parsing_soil_to_fertilizer = True
            parsing = True
            continue

        if ll.startswith("fertilizer-to-water map"):
            parsing_fertilizer_to_water = True
            parsing = True
            continue

        if ll.startswith("water-to-light map"):
            parsing_water_to_light = True
            parsing = True
            continue

        if ll.startswith("light-to-temperature map"):
            parsing_light_to_temperature = True
            parsing = True
            continue

        if ll.startswith("temperature-to-humidity map"):
            parsing_temperature_to_humidity = True
            parsing = True
            continue

        if ll.startswith("humidity-to-location map"):
            parsing_humidity_to_location = True
            parsing = True
            continue

        if ll == "\n":
            parsing_seed_to_soil = False
            parsing_soil_to_fertilizer = False
            parsing_fertilizer_to_water = False
            parsing_water_to_light = False
            parsing_light_to_temperature = False
            parsing_temperature_to_humidity = False
            parsing_humidity_to_location = False
            parsing = False

        if parsing:
            nns = [int(n) for n in re.findall(r"\d+", ll)]
            destination_range_start = nns[0]
            source_range_start = nns[1]
            range_length = nns[2]
            range_tuple = (source_range_start, range_length, destination_range_start)

        if parsing_seed_to_soil:
            seed_to_soil.append(range_tuple)

        if parsing_soil_to_fertilizer:
            soil_to_fertilizer.append(range_tuple)

        if parsing_fertilizer_to_water:
            fertilizer_to_water.append(range_tuple)

        if parsing_water_to_light:
            water_to_light.append(range_tuple)

        if parsing_light_to_temperature:
            light_to_temperature.append(range_tuple)

        if parsing_temperature_to_humidity:
            temperature_to_humidity.append(range_tuple)

        if parsing_humidity_to_location:
            humidity_to_location.append(range_tuple)

    def convert_through_map(input_value: int, map_tuples_list: list) -> int:
        for tpl in map_tuples_list:
            source_start, r_length, destination_start = tpl
            if source_start <= input_value < source_start + r_length:
                increment = input_value - source_start
                return destination_start + increment

        return input_value

    def reverse_through_map(input_value: int, map_tuples_list: list) -> int:
        for tpl in map_tuples_list:
            source_start, r_length, destination_start = tpl
            if destination_start <= input_value < destination_start + r_length:
                increment = input_value - destination_start
                return source_start + increment

        return input_value

    locations = []
    for ss in seeds:
        soil = convert_through_map(ss, seed_to_soil)
        fertilizer = convert_through_map(soil, soil_to_fertilizer)
        water = convert_through_map(fertilizer, fertilizer_to_water)
        light = convert_through_map(water, water_to_light)
        temperature = convert_through_map(light, light_to_temperature)
        humidity = convert_through_map(temperature, temperature_to_humidity)
        location = convert_through_map(humidity, humidity_to_location)

        locations.append(location)

    print(min(locations))

    do_end = False
    max_seed = max(seeds)  # Should be enough...
    for i in range(max_seed):
        location = i
        humidity = reverse_through_map(location, humidity_to_location)
        temperature = reverse_through_map(humidity, temperature_to_humidity)
        light = reverse_through_map(temperature, light_to_temperature)
        water = reverse_through_map(light, water_to_light)
        fertilizer = reverse_through_map(water, fertilizer_to_water)
        soil = reverse_through_map(fertilizer, soil_to_fertilizer)
        seed = reverse_through_map(soil, seed_to_soil)

        for start_seed, range_seeds in seeds_pt2:
            if start_seed <= seed <= start_seed + range_seeds:
                print(i)
                do_end = True
                break

        if do_end:
            break


def aoc6():
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/6/6.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    times = []
    distances = []
    times_puzzle_2 = 0
    distance_puzzle_2 = 0
    for ll in data:
        if ll.startswith("Time"):
            times = [int(ss) for ss in re.findall(r"\d+", ll.strip())]
            t_str_p2 = ""
            for t in times:
                t_str_p2 += str(t)
            times_puzzle_2 = int(t_str_p2)

        if ll.startswith("Distance"):
            distances = [int(ss) for ss in re.findall(r"\d+", ll.strip())]
            d_str_p2 = ""
            for d in distances:
                d_str_p2 += str(d)
            distance_puzzle_2 = int(d_str_p2)

    record_multiplier = 1
    for idx, tt in enumerate(times):
        max_d = distances[idx]
        possible_distances_for_race = [hold * (tt - hold) for hold in range(tt + 1)]

        record_multiplier *= sum([pd > max_d for pd in possible_distances_for_race])

    print(record_multiplier)

    possible_distances_for_race_p2 = [hold * (times_puzzle_2 - hold) for hold in range(times_puzzle_2 + 1)]
    print(sum([pd > distance_puzzle_2 for pd in possible_distances_for_race_p2]))


def aoc7():
    def count_repeated_characters_with_jokers(input_str: str, use_jokers=False):
        char_count = {}
        jokers = 0

        # Count occurrences of each character in the string
        for cc in input_str:
            if use_jokers and cc == "J":
                jokers += 1
                continue
            if cc in char_count:
                char_count[cc] += 1
            else:
                char_count[cc] = 1

        # Adding jokers
        if use_jokers:
            try:
                key_with_max_value = max(char_count, key=char_count.get)
            except ValueError:
                return {"J": 5}  # Only case in which the above line throws a value error

            # If the max is one, then take the highest card
            if max(char_count) == 1:
                key_with_max_value = sorted(char_count, key=lambda x: custom_sort_key_p2(x), reverse=True)[0]
            char_count[key_with_max_value] += jokers

        # Filter characters with counts greater than 1
        repeated_chars = {cc: count for cc, count in char_count.items() if count > 1}
        if not len(repeated_chars):
            return {"": 0}

        return repeated_chars

    custom_order = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6, "9": 7, "T": 8, "J": 9, "Q": 10, "K": 11,
                    "A": 12}
    custom_order_p2 = {"J": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6, "8": 7, "9": 8, "T": 9, "Q": 10, "K": 11,
                       "A": 12}

    def custom_sort_key(tuple_input):
        s = tuple_input[0]
        return [custom_order.get(c, float('inf')) for c in s]

    def custom_sort_key_p2(tuple_input):
        s = tuple_input[0]
        return [custom_order_p2.get(c, float('inf')) for c in s]

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/7/7.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    hands_bids_repeats = []
    hands_bids_repeats_p2 = []
    for dd in data:
        hand_bid_tuple = dd.split()
        hand = hand_bid_tuple[0]
        bid = int(hand_bid_tuple[1])

        # For part 1
        repeated_char_dict = count_repeated_characters_with_jokers(hand)
        hands_bids_repeats.append((hand, bid, [rps for _, rps in repeated_char_dict.items()]))

        # For part 2
        repeated_char_dict_p2 = count_repeated_characters_with_jokers(hand, use_jokers=True)
        hands_bids_repeats_p2.append((hand, bid, [rps for _, rps in repeated_char_dict_p2.items()]))

    # First order based on points - for part 1
    sorted_pts = sorted(hands_bids_repeats, key=lambda x: (max(x[2]), len(x[2]), custom_sort_key(x)))
    sorted_pts_p2 = sorted(hands_bids_repeats_p2, key=lambda x: (max(x[2]), len(x[2]), custom_sort_key_p2(x)))

    p1 = 0
    for _idx, (_hand, _bid, _) in enumerate(sorted_pts):
        p1 += (_idx + 1) * _bid
    print(p1)

    p2 = 0
    for _idx, (_hand, _bid, _) in enumerate(sorted_pts_p2):
        p2 += (_idx + 1) * _bid
    print(p2)


def aoc8():
    def gcd_of_list(numbers):
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = math.gcd(result, numbers[i])
        return result

    def lcm(a, b):
        return (a * b) // math.gcd(a, b)

    def lcm_of_list(numbers):
        result = numbers[0]
        for i in range(1, len(numbers)):
            result = lcm(result, numbers[i])
        return result

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/8/8.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    instructions = data[0].strip()
    coordinates = dict()
    for dd in data[2:]:
        k, t = dd.split("=")
        left = re.match(r" \((.+),", t).group(1)
        right = re.match(r".+, (.+)\)", t).group(1)
        coordinates[k.strip()] = {
            "L": left,
            "R": right
        }

    # Part 1
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


def aoc9():
    def diff_list(input_list):
        return [input_list[i + 1] - input_list[i] for i in range(len(input_list) - 1)]

    def predict_next_value(input_sequence: list):
        current_seq = input_sequence
        sequences = [current_seq]
        while any(current_seq):
            next_seq = diff_list(current_seq)
            sequences.append(next_seq)
            current_seq = next_seq

        for idx, sq in enumerate(sequences[::-1]):

            if idx == 0:
                sq.append(0)
                continue

            last_elm_idx = len(sq) - 1
            prediction = sq[last_elm_idx] + sequences[len(sequences) - idx][last_elm_idx]
            sq.append(prediction)

        return sequences[0][-1]

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/9/9.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    # Parsing
    input_sequences = []
    for dd in data:
        input_sequences.append([int(n) for n in re.findall(r"-*\d+", dd.strip())])

    p1 = []
    p2 = []
    for isq in input_sequences:
        p1.append(predict_next_value(isq))
        p2.append(predict_next_value((isq[::-1])))

    print(sum(p1))
    print(sum(p2))


def aoc10():
    opposite_direction = {
        "N": "S",
        "S": "N",
        "E": "W",
        "W": "E"
    }
    directions = {
        "N": (-1, 0),
        "S": (1, 0),
        "E": (0, 1),
        "W": (0, -1)
    }
    connections = {  # Each dict is of the form {"coming_from1": "going_to1", "coming_from2": "going_to2"}
        "F": {"S": "E", "E": "S"},
        "7": {"S": "W", "W": "S"},
        "J": {"N": "W", "W": "N"},
        "L": {"N": "E", "E": "N"},
        "-": {"W": "E", "E": "W"},
        "|": {"N": "S", "S": "N"}
    }
    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/10/10.txt"
    with open(input_file_path, "r") as f_open:
        data = f_open.readlines()
        f_open.close()

    # Finding start position
    start_coordinates = [(r_idx, c_idx) for r_idx, r in enumerate(data) for c_idx, ll in enumerate(r) if ll == "S"][0]

    # The first step is taken east
    steps = 0
    loop_steps = []
    coming_from = "W"
    current_char = "-"  # "-" Needed to make the first step east
    coordinates = start_coordinates
    loop_coordinates = []

    while current_char != "S":
        steps += 1
        going_to = connections[current_char][coming_from]
        coordinate_update = directions[going_to]
        coordinates = tuple(sum(pair) for pair in zip(coordinates, coordinate_update))
        loop_coordinates.append(coordinates)
        current_char = data[coordinates[0]][coordinates[1]]
        coming_from = opposite_direction[going_to]
        loop_steps.append(steps)

    # Inverting loop to subtract opposite direction in the closed loop
    half_steps = int(math.ceil(max(loop_steps) / 2))
    print(half_steps)

    char_map = []
    for r_idx, rr in enumerate(data):
        current_row = ""
        for c_idx, cc in enumerate(rr):
            if (r_idx, c_idx) in loop_coordinates:
                current_row += data[r_idx][c_idx]
                continue
            current_row += "."
        print(current_row)
        char_map.append(current_row)


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
