from typing import *
from Modules import Command
from copy import deepcopy


class Conveyor:
    steps: dict[str, None or Command.Command]
    p2: float
    p1: float
    m: int
    n: int
    commands_processed: int
    time_for_all_commands: int
    set_points: List[Tuple[int, int]]
    first_call: bool

    def __init__(self, p1, n, m, p2):
        self.p2 = p2
        self.m = m
        self.n = n
        self.p1 = p1

        self.steps = {
            "codeRead": None,
            "deciphering": None,
            "opRead1": None,
            "opRead2": None,
            "computing": None,
            "writing": None
        }
        self.commands_processed = 0
        self.time_for_all_commands = 0
        self.set_points = []
        self.first_call = True

    def process_one_tick(self):
        if self.first_call:
            self.steps["codeRead"] = Command.Command(self.p1, self.n, self.m, self.p2)
            self.first_call = False
            return
        for step in list(self.steps.keys())[::-1]:
            if self.steps[step]:
                res = self.steps[step].process_one_tick(step)
                if res:
                    if step == "writing":
                        self.time_for_all_commands += self.steps[step].timer
                        self.commands_processed += 1
                        self.set_points.append((self.commands_processed, self.time_for_all_commands))
                        self.steps[step] = None
                    else:
                        next_step = list(self.steps.keys()).index(step) + 1
                        if not self.steps[list(self.steps.keys())[next_step]]:
                            self.steps[step].move_to_next_step()
                            self.steps[list(self.steps.keys())[next_step]] = deepcopy(self.steps[step])
                            self.steps[step] = None
                        if step == "codeRead" and not self.steps[step]:
                            self.steps[step] = Command.Command(self.p1, self.n, self.m, self.p2)
