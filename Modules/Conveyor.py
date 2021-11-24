from typing import *
from Modules import Command
from copy import deepcopy


class Conveyor:
    steps: Dict[str, None or Command.Command]
    p2: float
    p1: float
    m: int
    n: int
    commands_processed: int
    time_for_all_commands: int
    ticks_processed: int
    time_for_commands_wo_idle: int
    set_points: List[Tuple[int, int, int, int]]
    first_call: bool

    def __init__(self, p1, n, m, p2):
        self.p2 = p2
        self.m = m
        self.n = n
        self.p1 = p1

        self.steps = {  # Шаги конвейера
            "codeRead": None,
            "deciphering": None,
            "opRead1": None,
            "opRead2": None,
            "computing": None,
            "writing": None
        }
        self.ticks_processed = 0        # Количество обработанных тактов
        self.commands_processed = 0     # Количество обработанных команд
        self.time_for_all_commands = 0  # Сколько времени в сумме провели все команды на конвейере
        self.time_for_commands_wo_idle = 0  # Сколько времени всего провели команды на конвейере без учета простоя
        self.set_points = []
        self.first_call = True

    def process_one_tick(self):
        self.ticks_processed += 1
        if self.first_call:     # Если конвейер только что создан
            self.steps["codeRead"] = Command.Command(self.p1, self.n, self.m, self.p2)
            self.first_call = False
            return
        for step in list(self.steps.keys())[::-1]:  # Проход от конца к началу конвейера
            if self.steps[step]:
                res = self.steps[step].process_one_tick(step)
                if res:     # Если команда готова к переходу
                    if step == "writing":   # Если запись завершилась, то обновляем статистику
                        self.time_for_all_commands += self.steps[step].timer
                        self.time_for_commands_wo_idle += self.steps[step].timer - self.steps[step].idleTimer
                        self.commands_processed += 1
                        self.set_points.append((self.commands_processed, self.time_for_all_commands, self.ticks_processed, self.time_for_commands_wo_idle))
                        self.steps[step] = None
                    else:
                        next_step = list(self.steps.keys()).index(step) + 1
                        if not self.steps[list(self.steps.keys())[next_step]]:  # Если следующая ступень не занята
                            self.steps[step].move_to_next_step()    # Обнуляем таймер ступени
                            # Копируем объект, чтобы избежать проблем с ссылками
                            self.steps[list(self.steps.keys())[next_step]] = deepcopy(self.steps[step])
                            self.steps[step] = None
                        if step == "codeRead" and not self.steps[step]:     # Если первая ступень пуста, заполняем её
                            self.steps[step] = Command.Command(self.p1, self.n, self.m, self.p2)
