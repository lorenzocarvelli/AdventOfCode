import re
from typing import Dict, List

from base import DailyPuzzle


class Day17(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "17")
        self.output: str = ""
        self.instruction_pointer: int = 0
        self.did_jump: bool = False
        self.a_register: int = 0
        self.b_register: int = 0
        self.c_register: int = 0
        self.combo_operands: Dict[int, int] = {
            0: 0,
            1: 1,
            2: 2,
            3: 3,
            4: self.a_register,
            5: self.b_register,
            6: self.c_register
        }

    def execute_instruction(self, opcode: int, operand: int):
        if opcode == 0:
            self.a_register = int(self.a_register / 2**self.combo_operands[operand])
            self.combo_operands[4] = self.a_register
            return
        if opcode == 1:
            self.b_register = int(self.b_register ^ operand)
            self.combo_operands[5] = self.b_register
            return
        if opcode == 2:
            self.b_register = self.combo_operands[operand] % 8
            self.combo_operands[5] = self.b_register
            return
        if opcode == 3:
            if self.a_register == 0:
                return
            self.instruction_pointer = operand
            self.did_jump = True
            return
        if opcode == 4:
            self.b_register = int(self.b_register ^ self.c_register)  # operand is not used here
            self.combo_operands[5] = self.b_register
            return
        if opcode == 5:
            self.output += f"{int(self.combo_operands[operand] % 8)},"
            return
        if opcode == 6:
            self.b_register = int(self.a_register / 2 ** self.combo_operands[operand])
            self.combo_operands[5] = self.b_register
            return
        if opcode == 7:
            self.c_register = int(self.a_register / 2 ** self.combo_operands[operand])
            self.combo_operands[6] = self.c_register
            return
        raise RuntimeError(f"Unknown opcode {opcode}")

    def run_execution_loop(self, instructions_list: List[int]):
        while self.instruction_pointer < len(instructions_list) - 1:
            opcode = instructions_list[self.instruction_pointer]
            operand = instructions_list[self.instruction_pointer + 1]

            self.execute_instruction(opcode, operand)

            if self.did_jump:
                self.did_jump = False
                continue

            self.instruction_pointer += 2

    def solve(self):
        instructions_str = ""
        instructions_list = []
        for ll in self.data:
            if ll.startswith("Register A"):
                self.a_register = int(re.match(r"Register A: (\d+)$", ll).group(1))
                continue
            if ll.startswith("Register B"):
                self.b_register = int(re.match(r"Register B: (\d+)$", ll).group(1))
                continue
            if ll.startswith("Register C"):
                self.c_register = int(re.match(r"Register C: (\d+)$", ll).group(1))
                continue
            if ll.startswith("Program"):
                instructions_str = re.match(r"Program: (.+)$", ll).group(1)
                instructions_list = [int(n) for n in instructions_str.split(",")]
                continue

        # Updating combo operands
        self.combo_operands[4] = self.a_register
        self.combo_operands[5] = self.b_register
        self.combo_operands[6] = self.c_register

        # Part 1 - running the program and printing its output
        self.run_execution_loop(instructions_list)
        print(self.output[:-1])

        # Part 2 - brute force
        for i in range(100000000, 1000000000):
            self.a_register = i
            self.b_register = 0
            self.c_register = 0
            self.instruction_pointer = 0
            self.output = ""
            self.run_execution_loop(instructions_list)

            if self.output[:-1] == instructions_str:
                break

        print(i)

        # 2,4,1,5,7,5,1,6,4,1,5,5,0,3,3,0

        # First operation: 2, 4
        # This will set self.b_register = A_REGISTER % 8

        # Second operation: 1, 5
        # This will set self.b_register to bitwise XOR (A_REGISTER % 8) ^ 5

        # Third operation 7, 5
        # self.c_register = int(A_REGISTER / 2 ** ((A_REGISTER % 8) ^ 5))

        # Fourth operation: 1, 6
        # self.b_register = int( ( (A_REGISTER % 8) ^ 5 ) ^ 6)

        # Fifth operation 4, 1
        # self.b_register = int(int( ( (A_REGISTER % 8) ^ 5 ) ^ 6) ^ int(A_REGISTER / 2 ** ((A_REGISTER % 8) ^ 5)))

        # Sixth operation 5, 5
        # This will output self.b_register to screen, so first clue we have is
        # int(int( ( (A_REGISTER % 8) ^ 5 ) ^ 6) ^ int(A_REGISTER / 2 ** ((A_REGISTER % 8) ^ 5))) = 2


if __name__ == "__main__":
    day_17 = Day17()
    day_17.solve()
