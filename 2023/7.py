from base import DailyPuzzle


class Day7(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "7")
        self.custom_order = {"2": 0, "3": 1, "4": 2, "5": 3, "6": 4, "7": 5, "8": 6,
                             "9": 7, "T": 8, "J": 9, "Q": 10, "K": 11, "A": 12}
        self.custom_order_p2 = {"J": 0, "2": 1, "3": 2, "4": 3, "5": 4, "6": 5, "7": 6,
                                "8": 7, "9": 8, "T": 9, "Q": 10, "K": 11, "A": 12}

    def count_repeated_characters_with_jokers(self, input_str: str, use_jokers=False):
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
                key_with_max_value = sorted(char_count, key=lambda x: self.custom_sort_key_p2(x), reverse=True)[0]
            char_count[key_with_max_value] += jokers

        # Filter characters with counts greater than 1
        repeated_chars = {cc: count for cc, count in char_count.items() if count > 1}
        if not len(repeated_chars):
            return {"": 0}

        return repeated_chars

    def custom_sort_key(self, tuple_input):
        s = tuple_input[0]
        return [self.custom_order.get(c, float('inf')) for c in s]

    def custom_sort_key_p2(self, tuple_input):
        s = tuple_input[0]
        return [self.custom_order_p2.get(c, float('inf')) for c in s]

    def solve(self):
        hands_bids_repeats = []
        hands_bids_repeats_p2 = []
        for dd in self.data:
            hand_bid_tuple = dd.split()
            hand = hand_bid_tuple[0]
            bid = int(hand_bid_tuple[1])

            # For part 1
            repeated_char_dict = self.count_repeated_characters_with_jokers(hand)
            hands_bids_repeats.append((hand, bid, [rps for _, rps in repeated_char_dict.items()]))

            # For part 2
            repeated_char_dict_p2 = self.count_repeated_characters_with_jokers(hand, use_jokers=True)
            hands_bids_repeats_p2.append((hand, bid, [rps for _, rps in repeated_char_dict_p2.items()]))

        # First order based on points - for part 1
        sorted_pts = sorted(hands_bids_repeats, key=lambda x: (max(x[2]), len(x[2]), self.custom_sort_key(x)))
        sorted_pts_p2 = sorted(hands_bids_repeats_p2, key=lambda x: (max(x[2]), len(x[2]), self.custom_sort_key_p2(x)))

        p1 = 0
        for _idx, (_hand, _bid, _) in enumerate(sorted_pts):
            p1 += (_idx + 1) * _bid
        print(p1)

        p2 = 0
        for _idx, (_hand, _bid, _) in enumerate(sorted_pts_p2):
            p2 += (_idx + 1) * _bid
        print(p2)


if __name__ == "__main__":
    day_7 = Day7()
    day_7.solve()
