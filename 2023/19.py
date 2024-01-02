import re
from typing import Dict, List

from base import DailyPuzzle


class Workflow(object):
    def __init__(self, input_dict: Dict[str, str], wf_name: str):
        self.name: str = wf_name
        self.input_dict: Dict[str, str] = input_dict
        self.conditions_tree: List[Dict[str, str]] = self.initialize()

    def initialize(self) -> List[Dict[str, str]]:
        out = []
        for condition, destination in self.input_dict.items():
            level_conditions = {
                condition: destination
            }
            if condition != "True":
                reversed_condition = self.reverse_condition(condition)
                level_conditions[reversed_condition] = "continue"
            out.append(level_conditions)

        return out

    @staticmethod
    def reverse_condition(cc: str) -> str:
        param = cc[0]
        comparison = cc[1]
        vl = int(cc[2:])

        if comparison == ">":
            reversed_c = f"{param}<{vl + 1}"
        else:
            reversed_c = f"{param}>{vl - 1}"
        return reversed_c


class Node(object):
    def __init__(self, parent_node: 'Node' or None, node_condition: str, node_destination: str):
        self.parent_node = parent_node
        self.node_condition: str = node_condition
        self.node_destination: str = node_destination


class Day19(DailyPuzzle):
    def __init__(self):
        super().__init__("2023", "19")

    def parse_data(self) -> (list, list):
        workflows, parts = dict(), []
        parsing_workflows = True

        for ll in self.data:
            if ll == "":
                parsing_workflows = False
                continue

            if parsing_workflows:
                workflow_name = re.match(r"(.+)\{", ll).group(1)
                all_rules = re.match(r".+\{(.+)}$", ll).group(1)
                rules = all_rules.split(",")

                set_of_rules = dict()
                for rr in rules:
                    if ":" in rr:
                        rl = rr.split(":")
                        condition = rl[0]
                        destination = rl[1]
                        set_of_rules[condition] = destination
                    else:
                        set_of_rules["True"] = rr

                workflows[workflow_name] = set_of_rules

            else:
                parts.append(eval(ll.replace("=", ":").replace("{", "{'").replace(":", "':").replace(",", ",'")))

        return workflows, parts

    def solve(self):
        workflows, parts = self.parse_data()

        accepted = []
        for pp in parts:
            current_workflow_key = "in"
            while True:
                current_workflow = workflows[current_workflow_key]
                for cdt_k, des in current_workflow.items():

                    try:
                        param = cdt_k[0]
                        comparison = cdt_k[1]
                        vl = int(cdt_k[2:])
                    except ValueError:
                        current_workflow_key = des
                        break

                    condition_is_verified = pp[param] < vl if comparison == "<" else pp[param] > vl
                    if condition_is_verified:
                        current_workflow_key = des
                        break

                if current_workflow_key == "A":
                    accepted.append(sum(vv for _, vv in pp.items()))
                    break

                if current_workflow_key == "R":
                    break

        # Part 1
        print(sum(accepted))

        # Part 2
        wf_list = []
        for wfk, wf in workflows.items():
            wf_list.append(Workflow(wf, wfk))

        nodes = [Node(None, "True", "in")]
        keep_expanding = True
        accepted = []
        while keep_expanding:
            next_level = []
            for nn in nodes:
                cwf = [w for w in wf_list if w.name == nn.node_destination][0]

                previous_level_condition = ""
                for depth_idx, depth_level in enumerate(cwf.conditions_tree):
                    for condition, destination in depth_level.items():

                        if destination != "continue":
                            next_level.append(Node(parent_node=nn, node_condition=previous_level_condition+condition, node_destination=destination))

                        else:
                            previous_level_condition += f"{condition},"

            idx_to_pop = []
            for idx, nnl in enumerate(next_level):
                if nnl.node_destination == "R":
                    idx_to_pop.append(idx)

                if nnl.node_destination == "A":
                    accepted_condition = nnl.node_condition
                    current_node = nnl
                    while current_node.parent_node is not None:
                        accepted_condition += f",{current_node.parent_node.node_condition}"
                        current_node = current_node.parent_node
                    accepted.append(accepted_condition)
                    idx_to_pop.append(idx)

            nodes = [nl for ni, nl in enumerate(next_level) if ni not in idx_to_pop]
            keep_expanding = any([aa for aa in nodes if aa not in ["A", "R"]])

        p2 = 0
        for accepted_c in accepted:
            range_dict = self.reset_range_dict()
            cond_list = accepted_c.split(",")
            for c in cond_list:
                if c == "True":
                    continue

                # Extract condition parameter etc
                param = c[0]
                comparison = c[1]
                nn = int(c[2:])

                # Update min/max
                if comparison == ">":
                    range_dict[param]["min"] = max(range_dict[param]["min"], nn+1)

                else:
                    range_dict[param]["max"] = min(range_dict[param]["max"], nn-1)

            n_accepted = 1
            for kk, min_max in range_dict.items():
                range_n = min_max["max"] - min_max["min"] + 1
                n_accepted *= range_n
            p2 += n_accepted

        print(p2)

    @staticmethod
    def reset_range_dict() -> Dict[str, Dict[str, int]]:
        return {
                "a": {
                    "min": 1,
                    "max": 4000
                },
                "s": {
                    "min": 1,
                    "max": 4000
                },
                "m": {
                    "min": 1,
                    "max": 4000
                },
                "x": {
                    "min": 1,
                    "max": 4000
                },
            }


if __name__ == "__main__":
    day_19 = Day19()
    day_19.solve()
