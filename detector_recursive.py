import numpy as np

def detect_arc(arc):
    pass


def find_edges(arc):
    left_point = min(arc, key=lambda x: x[0])
    right_point = max(arc, key=lambda x: x[0])

    return left_point, right_point


def get_middle_norm(l, r):
    # get line equation
    A = r[1] - l[1]
    B = r[0] - l[0]
    C = l[0]*r[1] - r[0]*l[1]

    k = B / -A
    b = C / -A

    arc_line = k, b
    midpoint = (l[0] + r[0]) / 2, (l[1] + r[1]) / 2

    # get perpendicular line
    perp_line = get_perpendicular(k, b, midpoint[0], midpoint[1])

    return arc_line, perp_line, midpoint


def get_perpendicular(k, b, x, y):
    perp_k = -1/k
    perp_b = -perp_k*x + y

    return perp_k, perp_b

