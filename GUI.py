import tkinter
from tkinter import *
from arc_generator import get_arc
from detector_recursive import find_segments, calc_radius, get_radius_lines, get_avg_points, filter_far_points, calc_avg, \
    rotate, filter_noise_points
from LS2D import LS2D


class GUI:
    def __init__(self, width=600, height=600):
        self.window = tkinter.Tk()
        self.window.configure(background="white")
        self.width = width
        self.height = height
        self.window.geometry(str(self.width) + "x" + str(self.width))

        self.sensor = LS2D("192.168.1.56", 11681, 123)
        print("Sensor init done")

        self.canvas = Canvas(self.window, height=600, width=600, bg="white")
        self.canvas.grid(row=0, column=0)

        self.update_period = 10

        self.window.after(self.update_period, self.loop)
        self.window.mainloop()

    def loop(self):

        self.canvas.delete(self.canvas, ALL)
        r = 150
        arc = get_arc(20, 100, 1000, r, 1)
        # self.sensor.read_single_packet()
        # arc = self.sensor.packets[0][0]
        # arc = filter_noise_points(arc)
        # rotate arc to fit algorithm's requirements.

        # arc = rotate(arc, -90)
        # radius calc

        sorted_arc = sorted(arc, key=lambda x: x[0])

        segments = find_segments(sorted_arc, 4)

        radius_lines = get_radius_lines(segments)

        avg_points = get_avg_points(radius_lines)

        largest_cluster = filter_far_points(avg_points)

        avg = calc_avg(largest_cluster)

        radius = calc_radius(arc, avg)

        # DRAWING

        self.draw_arc(arc)
        for x, y in segments:
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill="yellow")


        for x, y in largest_cluster:
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill="red")
            self.canvas.create_line(self.get_screen_coords(x, y, avg[0], avg[1]), fill="red")
        self.canvas.create_oval(self.get_screen_coords(avg[0] - 5, avg[1] - 5, avg[0] + 5, avg[1] + 5), fill="red")
        self.canvas.create_text([50, 50], text="R = {0:.2f}".format(radius), fill="black")

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

