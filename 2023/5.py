import re

from base import DailyPuzzle


class Day5(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "5")

    def solve(self):
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

        for ll in self.data:
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

            if ll == "":
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

        locations = []
        for ss in seeds:
            soil = self.convert_through_map(ss, seed_to_soil)
            fertilizer = self.convert_through_map(soil, soil_to_fertilizer)
            water = self.convert_through_map(fertilizer, fertilizer_to_water)
            light = self.convert_through_map(water, water_to_light)
            temperature = self.convert_through_map(light, light_to_temperature)
            humidity = self.convert_through_map(temperature, temperature_to_humidity)
            location = self.convert_through_map(humidity, humidity_to_location)

            locations.append(location)

        print(min(locations))

        do_end = False
        max_seed = max(seeds)  # Should be enough...
        for i in range(max_seed):
            location = i
            humidity = self.reverse_through_map(location, humidity_to_location)
            temperature = self.reverse_through_map(humidity, temperature_to_humidity)
            light = self.reverse_through_map(temperature, light_to_temperature)
            water = self.reverse_through_map(light, water_to_light)
            fertilizer = self.reverse_through_map(water, fertilizer_to_water)
            soil = self.reverse_through_map(fertilizer, soil_to_fertilizer)
            seed = self.reverse_through_map(soil, seed_to_soil)

            for start_seed, range_seeds in seeds_pt2:
                if start_seed <= seed <= start_seed + range_seeds:
                    print(i)
                    do_end = True
                    break

            if do_end:
                break

    @staticmethod
    def convert_through_map(input_value: int, map_tuples_list: list) -> int:
        for tpl in map_tuples_list:
            source_start, r_length, destination_start = tpl
            if source_start <= input_value < source_start + r_length:
                increment = input_value - source_start
                return destination_start + increment

        return input_value

    @staticmethod
    def reverse_through_map(input_value: int, map_tuples_list: list) -> int:
        for tpl in map_tuples_list:
            source_start, r_length, destination_start = tpl
            if destination_start <= input_value < destination_start + r_length:
                increment = input_value - destination_start
                return source_start + increment

        return input_value


if __name__ == "__main__":
    day_5 = Day5()
    day_5.solve()
