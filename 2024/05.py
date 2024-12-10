from typing import List, Tuple

from base import DailyPuzzle


class Day5(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "5")

    def parse_data(self) -> Tuple[List[Tuple[int, int]], List[List[int]]]:
        rules = []
        updates = []

        parsing_rules = True
        for ll in self.data:

            if ll == "":
                parsing_rules = False
                continue

            if parsing_rules:
                line_split = ll.split("|")
                rules.append((int(line_split[0]), int(line_split[1])))
                continue

            updates_line_split = ll.split(",")
            updates.append([int(pn) for pn in updates_line_split])

        return rules, updates

    def solve(self):

        rules, updates = self.parse_data()

        # Part 1: checking for updates that pass the rules
        updates_that_pass = []
        updates_that_do_not_pass = []
        for update in updates:
            update_passes = True

            for number in update:
                number_passes = self.check_number_in_rules(number, rules, update)
                if not number_passes:
                    update_passes = False
                    updates_that_do_not_pass.append(update)
                    break

            if update_passes:
                updates_that_pass.append(update)

        sol_1 = 0
        for ok_update in updates_that_pass:
            central_index = int(len(ok_update)/2)
            sol_1 += ok_update[central_index]

        print(sol_1)

        # Part 2: fixing the updates that do not pass
        sol_2 = 0
        main_loop_idx = 0
        while main_loop_idx < len(updates_that_do_not_pass):
            unp = updates_that_do_not_pass[main_loop_idx]
            main_loop_idx += 1

            passed = False
            relevant_rules = [r for r in rules if r[0] in unp and r[1] in unp]
            while not passed:
                passed = True
                for rr in relevant_rules:
                    index_of_first = unp.index(rr[0])
                    index_of_second = unp.index(rr[1])

                    if index_of_first > index_of_second:
                        passed = False

                        # Moving element that should be first ahead of the one that should be second
                        should_be_first = unp.pop(index_of_first)
                        unp.insert(index_of_second, should_be_first)

            unp_central_index = int(len(unp) / 2)
            sol_2 += unp[unp_central_index]

        print(sol_2)

    @staticmethod
    def check_number_in_rules(number: int, rules: List[Tuple[int, int]], update: List[int]) -> bool:
        rules_with_number_first = [rr for rr in rules if rr[0] == number]
        rules_with_number_second = [rr for rr in rules if rr[1] == number]

        for rnf in rules_with_number_first:
            other = rnf[1]
            if other not in update:
                continue
            index_of_number = update.index(number)
            index_of_other = update.index(other)
            if index_of_number > index_of_other:
                return False

        for rns in rules_with_number_second:
            other = rns[0]
            if other not in update:
                continue
            index_of_number = update.index(number)
            index_of_other = update.index(other)
            if index_of_number < index_of_other:
                return False

        return True


if __name__ == "__main__":
    day_5 = Day5()
    day_5.solve()
