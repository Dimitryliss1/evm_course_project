from tkinter import *
from tkinter import messagebox
import matplotlib.pyplot as plt
from Modules import Conveyor


class GUI(Tk):
    p1: DoubleVar
    p2: DoubleVar
    n: IntVar
    m: IntVar

    def __init__(self):
        super(GUI, self).__init__()
        self.title("Курсовая по ОЭВМ")

        self.p1 = DoubleVar()   # Определение переменных, в которые будут записываться значения флажков
        self.n = IntVar()
        self.m = IntVar()
        self.p2 = DoubleVar()
        self.draw()
        self.mainloop()

    def draw(self):
        # Подпись, затем справа три флажка со своими значениями.
        Label(self, text="Выберите P1: ").grid(column=0, row=0, sticky=W)
        for cnt_col, i in enumerate([0.6, 0.8, 0.9]):
            Radiobutton(text=i, value=i, variable=self.p1).grid(row=0, column=cnt_col + 1, sticky=W)

        Label(self, text="Выберите N: ").grid(column=0, row=1, sticky=W)
        for cnt_col, i in enumerate([2, 5, 10]):
            Radiobutton(text=i, value=i, variable=self.n).grid(row=1, column=cnt_col + 1, sticky=W)

        Label(self, text="Выберите M: ").grid(column=0, row=2, sticky=W)
        for cnt_col, i in enumerate([4, 8, 16]):
            Radiobutton(text=i, value=i, variable=self.m).grid(row=2, column=cnt_col + 1, sticky=W)

        Label(self, text="Выберите P2: ").grid(column=0, row=3, sticky=W)
        for cnt_col, i in enumerate([0.5, 0.7, 0.9]):
            Radiobutton(text=i, value=i, variable=self.p2).grid(row=3, column=cnt_col + 1, sticky=W)

        # Подсказка пользователю
        Label(self, text="P1 - вероятность регистровой адресации для операнда\n"
                         "N - время обращения к памяти в тактах\n"
                         "M - время вычисления для команд второго типа\n"
                         "P2 - вероятность, что текущая команда является командой первого типа", justify=CENTER)\
            .grid(row=4, column=0, columnspan=4)

        # Кнопка запуска симуляции
        Button(self, text='Симулировать!', command=self.simulate).grid(row=5, column=0, columnspan=4)

    def simulate(self):
        """
        Функция, формирующая конвейер с заданными условиями и выполняющая на нем тысячу команд.
        В конце работы график отрисовывается и выводится на экран.
        """

        # Если хотя бы одно из полей не заполнено, выдать ошибку
        if not self.p1.get() or not self.p2.get() or not self.m.get() or not self.n.get():
            messagebox.showerror("Ошибка", "Выберите значения каждого поля, пожалуйста")
            return

        # Инициализация конвейера
        conv = Conveyor.Conveyor(self.p1.get(), self.n.get(), self.m.get(), self.p2.get())
        while conv.commands_processed != 1000:
            conv.process_one_tick()
        xs = [x[0] for x in conv.set_points]    # Массив координат по оси X -- количество выполненных команд

        # Массив координат по оси Y -- суммарное время всех n команд
        ys = [float(x[1]) for x in conv.set_points]

        # Вычисление среднего арифметического времени для одной команды при условии n исполненных.
        for i in range(len(ys)):
            ys[i] = ys[i] / xs[i]

        # Отрисовка графика и выведение его на экран.
        plt.figure(1)
        plt.plot(xs, ys)
        plt.grid()
        plt.xlabel("Количество обработанных команд")
        plt.ylabel("Среднее количество тактов на команду")
        plt.title(f"p1 = {self.p1.get()}, n = {self.n.get()}, m = {self.m.get()}, p2 = {self.p2.get()}")

        plt.figure(2)
        plt.plot(xs, [x[1] for x in conv.set_points], 'b', label='Без конвейера')
        plt.plot(xs, [x[2] for x in conv.set_points], 'g', label='С применением конвейера')
        plt.legend()
        plt.grid()
        plt.title("Демонстрация эффективности применения конвейера")
        plt.xlabel("Количество обработанных команд")
        plt.ylabel("Количество тактов")
        plt.show()
