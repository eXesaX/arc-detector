import numpy as np
from math import sqrt, cos, radians, sin
from sklearn.cluster import DBSCAN

dbscan = DBSCAN(eps=200, min_samples=5)


def detect_arc(arc):
    pass


def find_edges(arc):
    sorted_arc = sorted(arc, key=lambda x: x[0])
    left_point = calc_avg(sorted_arc[:10])
    right_point = calc_avg(sorted_arc[-10:])
    # left_point = min(arc, key=lambda x: x[0])
    # right_point = max(arc, key=lambda x: x[0])

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
        if segments_acc is None:
            return []
        else:
            return segments_acc
    elif len(arc) < 2:
        print("len arc exit")
        if segments_acc is None:
            return []
        else:
            return segments_acc
    else:
        left_edge, right_edge = find_edges(arc)
        try:
            arc_line, norm, midpoint = get_middle_norm(left_edge, right_edge)

            sorted_arc = sorted(arc, key=lambda x: x[0])

            distances = []

            for i, (x, y) in enumerate(sorted_arc):
                perp = get_perpendicular(norm[0], norm[1], x, y)
                intersection = find_intersection(perp[0], perp[1], norm[0], norm[1])
                distance = get_distance(intersection[0], intersection[1], x, y)
                distances.append((x, y, distance, i))

            arc_midpoint = min(distances, key=lambda x: x[2])
            am_index = arc_midpoint[3]
            if depth == 1:
                if not segments_acc:
                    sa_new = [left_edge]
                else:
                    sa_new = [left_edge] + segments_acc
            else:
                sa_new = segments_acc
            a = find_segments(sorted_arc[:am_index], depth - 1, sa_new)
            b = find_segments(sorted_arc[am_index:], depth - 1, sa_new)
            if a is None: a = []
            if b is None: b = []
            return a + b
        except ZeroDivisionError:
            if segments_acc is not None:
                return [left_edge] + segments_acc
            else:
                return [left_edge]


def calc_radius(arc, midpoint):
    distances = []
    for x, y in arc:
        dist = sqrt(pow(x - midpoint[0], 2) + pow(y - midpoint[1], 2))
        distances.append(dist)
    avg = np.average(distances)
    return avg

def get_radius_lines(segments):
    radius_lines = []
    for i, (x, y) in enumerate(segments):
        x1, y1, x2, y2 = segments[i - 1][0], segments[i - 1][1], x, y
        midpoint = (x2 + x1) / 2, (y2 + y1) / 2
        try:
            A = x2 - x1
            B = y1 - y2
            C = x1 * y2 - y1 * x2
            k = B / -A
            b = C / -A
            r_line = get_perpendicular(k, b, midpoint[0], midpoint[1])
            radius_lines.append(r_line)
        except ZeroDivisionError:
            pass
    radius_lines = radius_lines[1:]
    return radius_lines

def get_avg_points(radius_lines):
    avg_points = []
    for line in radius_lines:
        for line2 in radius_lines:
            if line != line2:
                avg_point = find_intersection(line[0], line[1], line2[0], line2[1])
                avg_points.append(avg_point)

    return avg_points


def filter_far_points(avg_points):
    clusters = dbscan.fit_predict(avg_points)
    clusters = list(zip(clusters, avg_points))
    grouped_clusters = dict()
    for id, points in clusters:
        if id in grouped_clusters:
            grouped_clusters[id].append(points)
        else:
            grouped_clusters[id] = [points]
    sorted_clusters = sorted(grouped_clusters.items(), key=lambda x: len(x[1]), reverse=True)
    largest_cluster = max(sorted_clusters, key=lambda x: len(x[1]))[1]
    return largest_cluster

def calc_avg(largest_cluster):
    sum = [0, 0]
    for x, y in largest_cluster:
        sum[0] += x
        sum[1] += y
    avg = sum[0] / len(largest_cluster), sum[1] / len(largest_cluster)
    return avg


def rotate(arc, angle):
    rotated_arc = []
    rad_angle = radians(angle)
    for x, y in arc:
        x_r = x * cos(rad_angle) - y * sin(rad_angle)
        y_r = x * sin(rad_angle) + y * cos(rad_angle)
        rotated_arc.append((x_r, y_r))

    return rotated_arc


def filter_noise_points(arc):
    filtered = []
    for x, y in arc:
        if x >= 10:
            filtered.append((x + 200, y))

    return filtered