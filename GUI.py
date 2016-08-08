import tkinter
from tkinter import *
from arc_generator import get_arc
import numpy as np
import cv2
from detector_recursive import find_edges, get_middle_norm, find_intersection, get_perpendicular, get_distance, find_segments

class GUI:
    def __init__(self, width=600, height=600):
        self.window = tkinter.Tk()
        self.window.configure(background="white")
        self.width = width
        self.height = height
        self.window.geometry(str(self.width) + "x" + str(self.width))

        self.canvas = Canvas(self.window, height=600, width=600, bg="white")
        self.canvas.grid(row=0, column=0)

        self.update_period = 10
        self.window.after(self.update_period, self.loop())
        self.window.mainloop()
        while True:
            self.loop()

    def loop(self):
        self.canvas.delete(self.canvas, ALL)
        arc = get_arc(20, 140, 1000, 100, 1)

        sorted_arc = sorted(arc, key=lambda x: x[0])
        segments = find_segments(sorted_arc, 4)
        self.draw_arc(arc)
        for x, y in segments:
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill="yellow")


        radius_lines = []
        for i, (x, y) in enumerate(segments[0:]):
            x1, y1, x2, y2 = segments[i - 1][0], segments[i - 1][1], x, y
            midpoint = (x2 + x1) / 2, (y2 + y1) / 2
            try:
                A = x2 - x1
                B = y1 - y2
                C = x1*y2 - y1*x2
                k = B / -A
                b = C / -A
                r_line = get_perpendicular(k, b, midpoint[0], midpoint[1])
                radius_lines.append(r_line)
            except ZeroDivisionError:
                pass

        for k, b in radius_lines:
            self.canvas.create_line(self.get_screen_coords(-self.width,
                                                           -k*self.width + b,
                                                           self.width,
                                                           k*self.width + b), fill="green")

        self.window.after(self.update_period, self.loop)


    def draw_arc(self, arc):
        for x, y in arc:
            self.canvas.create_line(self.get_point_coords(x, y), fill="black")

    def get_point_coords(self, x, y):
        return x + int(self.width / 2), \
               y + int(self.height / 2), \
               x + int(self.width / 2) + 1, \
               y + int(self.height / 2) + 1

    def get_screen_coords(self, x1, y1, x2, y2):
        return x1 + int(self.width / 2), \
               y1 + int(self.height / 2), \
               x2 + int(self.width / 2), \
               y2 + int(self.height / 2)


if __name__ == "__main__":
    gui = GUI()

