from typing import List

from base import DailyPuzzle


class Day9(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "9")

    def all_consecutive_indices(self, input_list: List[int]) -> bool:
        return all([elm == 1 for elm in self.derivative(input_list)])

    @staticmethod
    def derivative(input_list: List[int]) -> List[int]:
        return [input_list[idx+1] - input_list[idx] for idx in range(len(input_list) - 1)]

    def solve(self):
        # Parsing into memory representation string
        self.data = self.data[0]  # Needed for how the data is parsed in base method
        file_id_map = dict()
        spaces_map = []
        memory_representation = []
        file_id = 0
        for idx, block in enumerate(self.data):
            memory_length_before_addition = len(memory_representation)
            if idx % 2:
                memory_representation.extend(["."] * int(block))   # Parsing space
                memory_length_after_addition = len(memory_representation)
                spaces_map.append([ii for ii in range(memory_length_before_addition, memory_length_after_addition)])
            else:
                memory_representation.extend([f"{file_id}"] * int(block))  # Parsing file
                memory_length_after_addition = len(memory_representation)
                file_id_map[file_id] = [ii for ii in range(memory_length_before_addition, memory_length_after_addition)]
                file_id += 1

        # Part 1: no need to rearrange memory, just using some logic with the indices of file blocks and spaces
        file_indices = [idx for idx, cc in enumerate(memory_representation) if cc != "."]

        checksum = 0
        for idx, block in enumerate(memory_representation):
            if idx > file_indices[-1]:
                break
            if block == ".":
                checksum += idx*int(memory_representation[file_indices[-1]])
                file_indices.pop(-1)
                continue
            checksum += idx*int(block)
        print(checksum)

        # Part 2: similar logic to Part 1, using maps (i.e. dictionaries) instead of lists
        checksum_2 = 0
        current_file_id = [k for k in file_id_map.keys()][-1]
        while current_file_id > 0:
            file_block = file_id_map[current_file_id]
            block_length = len(file_block)

            # Finding first index of space block that can contain whole file length
            spaces_idx = None
            for si, sl in enumerate(spaces_map):
                if not len(sl):
                    continue
                if sl[-1] >= file_block[0]:
                    break
                if len(sl) >= block_length:
                    spaces_idx = si
                    break

            if spaces_idx is None:
                for p_idx in file_block:
                    checksum_2 += current_file_id*p_idx
                current_file_id -= 1
                continue

            spaces_block = spaces_map[spaces_idx]
            for _ in range(block_length):
                s_idx = spaces_block.pop(0)  # Popping elements from the left
                checksum_2 += current_file_id*s_idx

            current_file_id -= 1
        print(checksum_2)


if __name__ == "__main__":
    day_9 = Day9()
    day_9.solve()
