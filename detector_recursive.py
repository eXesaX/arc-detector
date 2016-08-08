import numpy as np
from math import sqrt

def detect_arc(arc):
    pass


def find_edges(arc):
    left_point = min(arc, key=lambda x: x[0])
    right_point = max(arc, key=lambda x: x[0])

    return left_point, right_point


def get_middle_norm(l, r):
    # get line equation
    A = r[0] - l[0]
    B = l[1] - r[1]
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


def find_intersection(k1, b1, k2, b2):
    x = (b2 - b1) / (k1 - k2)
    y = k1 * x + b1

    return x, y


def get_distance(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def find_segments(arc, depth, segments_acc=None):
    if depth == 0:
        return segments_acc
    elif len(arc) < 2:
        return segments_acc
    else:
        left_edge, right_edge = find_edges(arc)
        try:
            arc_line, norm, midpoint = get_middle_norm(*(left_edge, right_edge))

            sorted_arc = sorted(arc, key=lambda x: x[0])

            distances = []

            for i, (x, y) in enumerate(sorted_arc):
                perp = get_perpendicular(norm[0], norm[1], x, y)
                intersection = find_intersection(perp[0], perp[1], norm[0], norm[1])
                distance = get_distance(intersection[0], intersection[1], x, y)
                distances.append((x, y, distance, i))

            arc_midpoint = min(distances, key=lambda x: x[2])
            am_index = arc_midpoint[3]
            if not segments_acc:
                sa_new = [left_edge]
            else:
                sa_new = [left_edge] + segments_acc

            return find_segments(sorted_arc[:am_index], depth - 1, sa_new) + find_segments(sorted_arc[am_index:], depth - 1, sa_new)
        except ZeroDivisionError:
            return [left_edge] + segments_acc
