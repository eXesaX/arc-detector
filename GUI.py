import tkinter
from tkinter import *
from arc_generator import get_arc


class GUI:
    def __init__(self, width=600, height=600):
        self.window = tkinter.Tk()
        self.window.configure(background="white")
        self.width = width
        self.height = height
        self.window.geometry(str(self.width) + "x" + str(self.width))

        self.canvas = Canvas(self.window, height=600, width=600, bg="white")
        self.canvas.grid(row=0, column=0)

        self.update_period = 15
        self.window.after(self.update_period, self.loop())
        self.window.mainloop()

    def loop(self):
        self.canvas.delete(self.canvas, ALL)
        arc = get_arc(-120, 120, 500, 2000, 5)
        self.draw_arc(self.normalize(arc))

        self.window.after(self.update_period, self.loop)

    def normalize(self, arc):
        max_x = max(arc, key=lambda point: point[0])[0]
        max_y = max(arc, key=lambda point: point[1])[1]

        normalized_arc = []

        for x, y in arc:
            nx = int(x / max_x * int(self.width / 2))
            ny = int(y / max_y * int(self.height / 2))
            normalized_arc.append((nx, ny))
        return normalized_arc

    def draw_arc(self, arc):
        for x, y in arc:
            self.canvas.create_line(self.get_point_coords(x, y), fill="black")

    def get_point_coords(self, x, y):
        return x + int(self.width / 2), \
               y + int(self.height / 2), \
               x + int(self.width / 2) + 1, \
               y + int(self.height / 2) + 1


if __name__ == "__main__":
    gui = GUI()

