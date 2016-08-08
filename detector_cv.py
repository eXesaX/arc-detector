import cv2
import numpy as np


def make_picture(arc):
    w_arc = abs(max(arc, key=lambda x: x[0])[0]) + abs(min(arc, key=lambda x: x[0])[0])
    h_arc = abs(max(arc, key=lambda x: x[1])[1]) + abs(min(arc, key=lambda x: x[1])[1])
    width = w_arc + 600
    height = h_arc + 600

    picture = np.zeros((height, width), np.uint8)

    for x, y in arc:
        picture[int(y + height / 2), int(x + width / 2)] = 255

    return picture, w_arc, h_arc


def find_circle(picture, w_arc, h_arc):
    # picture = cv2.blur(src=picture, ksize=(3, 3))
    return cv2.HoughCircles(picture, cv2.HOUGH_GRADIENT, 1, picture.shape[0],
                            param1=1,
                            param2=1,
                            maxRadius=int(max((w_arc, h_arc))),
                            minRadius=int(min((w_arc, h_arc))),
                            ), picture
