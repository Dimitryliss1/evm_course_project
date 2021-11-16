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
        self.p1 = DoubleVar()
        self.n = IntVar()
        self.m = IntVar()
        self.p2 = DoubleVar()
        self.draw()
        self.mainloop()

    def draw(self):
        Label(self, text="Select P1: ").grid(column=0, row=0, sticky=W)
        for cnt_col, i in enumerate([0.6, 0.8, 0.9]):
            Radiobutton(text=i, value=i, variable=self.p1).grid(row=0, column=cnt_col + 1, sticky=W)

        Label(self, text="Select N: ").grid(column=0, row=1, sticky=W)
        for cnt_col, i in enumerate([2, 5, 10]):
            Radiobutton(text=i, value=i, variable=self.n).grid(row=1, column=cnt_col + 1, sticky=W)

        Label(self, text="Select M: ").grid(column=0, row=2, sticky=W)
        for cnt_col, i in enumerate([4, 8, 16]):
            Radiobutton(text=i, value=i, variable=self.m).grid(row=2, column=cnt_col + 1, sticky=W)

        Label(self, text="Select P2: ").grid(column=0, row=3, sticky=W)
        for cnt_col, i in enumerate([0.5, 0.7, 0.9]):
            Radiobutton(text=i, value=i, variable=self.p2).grid(row=3, column=cnt_col + 1, sticky=W)

        Button(self, text='Simulate!', command=self.simulate).grid(row=4, column=0, columnspan=4)

    def simulate(self):
        if not self.p1.get() or not self.p2.get() or not self.m.get() or not self.n.get():
            messagebox.showerror("Ошибка", "Выберите значения каждого поля, пожалуйста")
            return
        conv = Conveyor.Conveyor(self.p1.get(), self.n.get(), self.m.get(), self.p2.get())
        while conv.commands_processed != 1000:
            conv.process_one_tick()
        xs = [x[0] for x in conv.set_points]
        ys = [x[1] for x in conv.set_points]
        for i in range(len(ys)):
            ys[i] = ys[i] / xs[i]
        plt.plot(xs, ys)
        plt.grid()
        plt.xlabel("N of operations")
        plt.ylabel("Mean ticks per operation")
        plt.title(
            f"p1 = {self.p1.get()}, n = {self.n.get()}, m = {self.m.get()}, p2 = {self.p2.get()}")
        plt.show()
