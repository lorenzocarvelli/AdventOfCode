from base import DailyPuzzle


class Brick(object):
    def __init__(self, name, c1: str, c2: str):
        self.name: str = name
        self.cubes = self.get_cubes(c1, c2)
        self.supported_bricks = []

    @staticmethod
    def get_cubes(c1: str, c2: str):
        x1, y1, z1 = eval(c1)
        x2, y2, z2 = eval(c2)

        out = []
        for xx in range(x1, x2+1):
            out.append((xx, y1, z1))

        for yy in range(y1, y2+1):
            out.append((x1, yy, z1))

        for zz in range(z1, z2+1):
            out.append((x1, y1, zz))

        return sorted(list(set(out)))


class Day22(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "22")
        self.mock_data = [
            "1,0,1~1,2,1",
            "0,0,2~2,0,2",
            "0,2,3~2,2,3",
            "0,0,4~0,2,4",
            "2,0,5~2,2,5",
            "0,1,6~2,1,6",
            "1,1,8~1,1,9"
        ]
        # self.data = self.mock_data  # TODO: remove

    def parse_data(self) -> list:
        out = []
        for idx, ll in enumerate(self.data):
            c1, c2 = ll.split("~")
            out.append(Brick(str(idx), c1, c2))
        return out

    def solve(self):
        bricks = self.parse_data()

        sorted_by_height = sorted(bricks, key=lambda x: min([cc[2] for cc in x.cubes]))
        below = []
        for b in sorted_by_height:
            # Base case, brick already on the ground level
            if min(cc[2] for cc in b.cubes) == 1:
                below.append(b)
                continue

            can_still_fall = True
            current_positions = b.cubes
            highest_below = max([cc[2] for bb in below for cc in bb.cubes])
            idx = 1

            while can_still_fall:

                next_positions = [(cp[0], cp[1], highest_below+idx) for cp in current_positions]

                for bb in below:
                    intersection = list(set(next_positions) & set(bb.cubes))
                    if len(intersection):
                        bb.supported_bricks.append(b.name)
                        can_still_fall = False

                if can_still_fall:
                    current_positions = next_positions
                    idx += 1

            b.cubes = current_positions
            below.append(b)

        print("Done falling")

        safe_to_disintegrate = 0
        for brick in below:
            sb = brick.supported_bricks

            supported_by_others = []
            for other_brick in below:
                if other_brick == brick:
                    continue
                supported_by_others.extend(other_brick.supported_bricks)

            all_supported_by_other_bricks = all(elem in supported_by_others for elem in sb)
            if all_supported_by_other_bricks:
                safe_to_disintegrate += 1

        print(safe_to_disintegrate)


if __name__ == "__main__":
    day_22 = Day22()
    day_22.solve()
