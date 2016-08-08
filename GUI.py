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
        segments = find_segments(sorted_arc, 5)
        self.draw_arc(arc)
        for x, y in segments:
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill="yellow")
        # self.canvas.create_line(self.get_screen_coords(edges[0][0],
        #                                                edges[0][1],
        #                                                edges[1][0],
        #                                                edges[1][1]))
        #
        # self.canvas.create_line(self.get_screen_coords(-self.width,
        #                                                arc_line[0] * -self.width + arc_line[1],
        #                                                self.width,
        #                                                arc_line[0] * self.width + arc_line[1]), fill="green")
        #
        # self.canvas.create_line(self.get_screen_coords(-self.width,
        #                                                norm[0] * -self.width + norm[1],
        #                                                self.width,
        #                                                norm[0] * self.width + norm[1]), fill="red")
        #
        #
        # self.canvas.create_oval(self.get_screen_coords(midpoint[0] - 5, midpoint[1] - 5, midpoint[0] + 5, midpoint[1] + 5),
        #                         fill="green")
        #
        # self.canvas.create_oval(self.get_screen_coords(arc_midpoint[0] - 5, arc_midpoint[1] - 5, arc_midpoint[0] + 5, arc_midpoint[1] + 5),
        #                         fill="red")

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

    def get_screen_coords(self, x1, y1, x2, y2):
        return x1 + int(self.width / 2), \
               y1 + int(self.height / 2), \
               x2 + int(self.width / 2), \
               y2 + int(self.height / 2)


if __name__ == "__main__":
    gui = GUI()

