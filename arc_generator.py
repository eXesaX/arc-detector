from random import randint
from math import sin, cos, radians
from numpy import linspace


def get_arc(start, finish, num, radius, r_rnd):
    points = []

    for i in linspace(start, finish, num):
        x = radius * cos(radians(i)) + randint(-r_rnd, r_rnd)
        y = radius * sin(radians(i)) + randint(-r_rnd, r_rnd)
        points.append((x, y))

    return points


if __name__ == '__main__':
    print(get_arc(0, 10, 500, 5, 0))