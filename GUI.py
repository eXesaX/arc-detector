import tkinter
from tkinter import *
from arc_generator import get_arc
from detector_cv import make_picture, find_circle
import numpy as np
import cv2


class GUI:
    def __init__(self, width=600, height=600):
        # self.window = tkinter.Tk()
        # self.window.configure(background="white")
        # self.width = width
        # self.height = height
        # self.window.geometry(str(self.width) + "x" + str(self.width))
        #
        # self.canvas = Canvas(self.window, height=600, width=600, bg="white")
        # self.canvas.grid(row=0, column=0)
        #
        # self.update_period = 10
        # self.window.after(self.update_period, self.loop())
        # self.window.mainloop()
        while True:
            self.loop()

    def loop(self):
        # self.canvas.delete(self.canvas, ALL)
        arc = get_arc(0, 120, 1000, 100, 1)
        circles, picture = find_circle(*make_picture(arc))
        # self.draw_arc(self.normalize(arc))
        if circles is not None:
            circles = np.round(circles[0, :]).astype('int')
            for x, y, r in circles:
                cv2.circle(picture, (x, y), r, (255, 0, 0))
                # self.canvas.create_line(self.get_point_coords(x, y), fill="red")
                # print(x, y, r)
        else:
            print("no circles found")

        cv2.imshow("hough circles", picture)
        cv2.waitKey(1)

        # self.window.after(self.update_period, self.loop)

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

