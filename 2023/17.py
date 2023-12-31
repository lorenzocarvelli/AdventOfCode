from base import DailyPuzzle


class Day17(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "17")

    def solve(self):
        """
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
            """

        data = [[int(cc) for cc in ss] for ss in self.data]

        start_p1 = (0, 0)
        end_p1 = (len(data) - 1, len(data[0]) - 1)
        min_dist = self.find_min_dist(start_p1, end_p1, data)
        print(min_dist)

    @staticmethod
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


if __name__ == "__main__":
    day_17 = Day17()
    day_17.solve()
