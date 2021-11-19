import random as rnd


class Command:
    op1_type: int
    op2_type: int
    comp_time: int
    mem_access: int
    timer: int
    step_timer: int
    codeRead: bool
    codeDec: bool
    op1Read: bool
    op2Read: bool
    computed: bool
    written: bool

    def __init__(self, prob1, mem_access, comp_time, prob2):
        self.op1_type = 1 if rnd.uniform(0, 1) < prob1 else 2           # 1 -- Операнд в регистре, 2 -- Операнд в памяти
        self.op2_type = 1 if rnd.uniform(0, 1) < prob1 else 2
        self.comp_time = 1 if rnd.uniform(0, 1) < prob2 else comp_time  # Определение количества тактов на вычисление результата

        self.mem_access = mem_access    # Время доступа к памяти
        self.timer = 0                  # Время с момента поступления команды на конвейер
        self.step_timer = 0             # Время с момента поступления команды на текущую ступень конвейера

        self.codeRead = False   # КОП прочитан
        self.codeDec = False    # КОП расшифрован
        self.op1Read = False    # Первый операнд прочитан
        self.op2Read = False    # Второй операнд прочитан
        self.computed = False   # Результат посчитан
        self.written = False    # Результат записан

    def process_one_tick(self, step_name):
        self.step_timer += 1
        self.timer += 1
        if step_name == "codeRead":
            if self.step_timer == self.mem_access:
                if self.op1_type == 2:  # Если операнд использует косвенную операцию
                    self.op1Read = True
                if self.op2_type == 2:
                    self.op2Read = True
                self.codeRead = True
            return self.codeRead    # True -- готов к переходу, False -- нет.

        if step_name == "deciphering":
            self.codeDec = True
            return self.codeDec

        if step_name == "opRead1":
            if self.op1Read or self.op1_type == 1 or self.step_timer == self.mem_access:
                self.op1Read = True
            return self.op1Read

        if step_name == "opRead2":
            if self.op2Read or self.op2_type == 1 or self.step_timer == self.mem_access:
                self.op2Read = True
            return self.op2Read

        if step_name == "computing":
            if self.step_timer == self.comp_time:
                self.computed = True
            return self.computed

        if step_name == "writing":
            if self.op2_type == 1:
                self.written = True
            else:
                if self.step_timer == self.mem_access:
                    self.written = True
            return self.written

    def move_to_next_step(self):
        self.step_timer = 0 # Обнуление таймера шага
