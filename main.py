import re

def aoc17():

    input_file_path = "/Users/lorenzocarvelli/Desktop/aoc_2023_data/17/17.txt"
    with open(input_file_path, "r") as f_open:
        data = [ld.rstrip('\n') for ld in f_open.readlines()]
        f_open.close()



if __name__ == "__main__":
    aoc17()
