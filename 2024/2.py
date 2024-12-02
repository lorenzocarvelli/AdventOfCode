from base import DailyPuzzle


class Day2(DailyPuzzle):
    def __init__(self):
        super().__init__("2024", "2")

    def solve(self):
        # Parsing data into lists ("reports") of integers ("levels")
        reports_list = []
        for line_str in self.data:
            reports_list.append([int(lvl) for lvl in line_str.split(" ")])

        # Counting how many reports are "safe" - Solution to Part 1
        safe_reports = 0
        safe_idx_list = []
        for idx, report in enumerate(reports_list):
            delta_report = [report[idx+1]-report[idx] for idx in range(len(report)-1)]

            # Safety rule 1: all increasing or all decreasing
            sr1 = all([delta_lvl > 0 for delta_lvl in delta_report]) or all([delta_lvl < 0 for delta_lvl in delta_report])

            # Safety rule 2: all adjacent levels must differ in absolute value by at least 1 and at most 3
            sr2 = all([1 <= abs(delta_lvl) <= 3 for delta_lvl in delta_report])

            if sr1 and sr2:
                safe_reports += 1
                safe_idx_list.append(idx)

        print(safe_reports)

        # Counting how many reports are "safe" after the Problem Dampener - Solution to Part 2
        safe_reports_pt2 = 0
        for idx, report in enumerate(reports_list):

            # If found to be safe in Part 1, then it is still safe
            if idx in safe_idx_list:
                safe_reports_pt2 += 1
                continue

            # Brute force solution - trying to remove one index at the time each of the levels in the report and checking again
            for report_idx in range(len(report)):
                updated_report = [lvl for l_idx, lvl in enumerate(report) if l_idx != report_idx]
                updated_delta_report = [updated_report[idx + 1] - updated_report[idx] for idx in range(len(updated_report) - 1)]

                # Safety rule 1: all increasing or all decreasing
                u_sr1 = all([u_delta_lvl > 0 for u_delta_lvl in updated_delta_report]) or all([u_delta_lvl < 0 for u_delta_lvl in updated_delta_report])

                # Safety rule 2: all adjacent levels must differ in absolute value by at least 1 and at most 3
                u_sr2 = all([1 <= abs(u_delta_lvl) <= 3 for u_delta_lvl in updated_delta_report])
                if u_sr1 and u_sr2:
                    safe_reports_pt2 += 1
                    break

        print(safe_reports_pt2)


if __name__ == "__main__":
    day_2 = Day2()
    day_2.solve()
