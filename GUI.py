import tkinter
from tkinter import *
from arc_generator import get_arc
from detector_recursive import find_intersection, get_perpendicular, find_segments, calc_radius, find_edges, \
    get_middle_norm, get_distance


class GUI:
    def __init__(self, width=600, height=600):
        self.window = tkinter.Tk()
        self.window.configure(background="white")
        self.width = width
        self.height = height
        self.window.geometry(str(self.width) + "x" + str(self.width))

        self.canvas = Canvas(self.window, height=600, width=600, bg="white")
        self.canvas.grid(row=0, column=0)

        self.update_period = 500
        self.counter = 0

        self.window.after(self.update_period, self.loop())
        self.window.mainloop()

        while True:
            self.loop()

    def loop(self):

        self.canvas.delete(self.canvas, ALL)
        r = 150
        arc = get_arc(20, 100, 1000, r, 1)

        sorted_arc = sorted(arc, key=lambda x: x[0])
        segments = find_segments(sorted_arc, 4)
        self.draw_arc(arc)
        for x, y in segments:
            self.canvas.create_oval(self.get_screen_coords(x - 2, y - 2, x + 2, y + 2), fill="yellow")


        radius_lines = []
        for i, (x, y) in enumerate(segments):
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

        radius_lines = radius_lines[1:]

        avg_points = []

        for line in radius_lines:
            for line2 in radius_lines:
                if line != line2:
                    avg_point = find_intersection(line[0], line[1], line2[0], line2[1])
                    avg_points.append(avg_point)

        sum = [0, 0]
        for x, y in avg_points:
            sum[0] += x
            sum[1] += y

        avg = sum[0] / len(avg_points), sum[1] / len(avg_points)

        raw_radius = calc_radius(arc, avg)

        new_avg_points = []
        for x, y in avg_points:
            if get_distance(x, y, avg[0], avg[1]) < raw_radius / 3:
                new_avg_points.append((x, y))

        new_avg = None
        try:
            sum = [0, 0]
            for x, y in new_avg_points:
                sum[0] += x
                sum[1] += y

            new_avg = sum[0] / len(new_avg_points), sum[1] / len(new_avg_points)

            radius = calc_radius(arc, new_avg)
        except ZeroDivisionError:
            print("no new avg points")




        # DRAWING

        for x,y in avg_points:
            self.canvas.create_oval(self.get_screen_coords(x - 1, y - 1, x + 1, y + 1), fill="black")
        self.canvas.create_oval(self.get_screen_coords(avg[0] - 5, avg[1] - 5, avg[0] + 5, avg[1] + 5), fill="red")
        if new_avg:
            self.canvas.create_oval(self.get_screen_coords(new_avg[0] - 5, new_avg[1] - 5, new_avg[0] + 5, new_avg[1] + 5), fill="blue")
            self.canvas.create_text([50, 50], text="R = {0:.2f}".format(radius), fill="black")
            self.canvas.create_text([50, 80], text="Ea = {0:.5f}".format(abs(r - radius)), fill="black")


        # for k, b in radius_lines:
        #     self.canvas.create_line(self.get_screen_coords(-self.width,
        #                                                    -k*self.width + b,
        #                                                    self.width,
        #                                                    k*self.width + b), fill="green")

            for x, y in new_avg_points:
                self.canvas.create_line(self.get_screen_coords(x, y, new_avg[0], new_avg[1]))

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

