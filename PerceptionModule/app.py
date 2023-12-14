import numpy as np
from flask import Flask
from flask_restful import Api
import flask
import os
import cv2

app = Flask(__name__)
API = Api(app)
port = int(os.getenv("PORT", 1090))


@app.route('/', methods=['POST'])
def decide():
    (tmp_x, tmp_y), tmp_r = find_blob()
    ovni = {
        'tmp_x': tmp_x,
        'tmp_y': tmp_y,
        'tmp_r': tmp_r
    }
    ovni = flask.jsonify(ovni)
    ovni.status_code = 200
    return ovni


def find_blob():
    radius = 0
    center = 0
    kernel = np.ones((5,5),np.uint8)
    img = cv2.VideoCapture(-1)
    screen_width = 160
    screen_hight = 120
    img.set(3, screen_width)
    img.set(4, screen_hight)

    # Load input image
    _, bgr_image = img.read()

    bgr_image = cv2.medianBlur(bgr_image, 3)

    # Convert input image to HSV
    hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)

    # Threshold the HSV image, keep only the red pixels
    lower_red_hue_range = cv2.inRange(hsv_image, (0, 100, 100), (10, 255, 255))
    upper_red_hue_range = cv2.inRange(hsv_image, (160, 100, 100), (179, 255, 255))
    # Combine the above two images
    red_hue_image = cv2.addWeighted(lower_red_hue_range, 1.0, upper_red_hue_range, 1.0, 0.0)

    red_hue_image = cv2.GaussianBlur(red_hue_image, (9, 9), 2, 2)

    # Use the Hough transform to detect circles in the combined threshold image
    circles = cv2.HoughCircles(red_hue_image, cv2.HOUGH_GRADIENT, 1, 120, 100, 20, 10, 0)
    circles = np.uint16(np.around(circles))
    # Loop over all detected circles and outline them on the original image
    all_r = np.array([])
    # print("circles: %s"%circles)
    if circles is not None:
        try:
            for i in circles[0, :]:
                # print("i: %s"%i)
                all_r = np.append(all_r, int(round(i[2])))
            closest_ball = all_r.argmax()
            center = (int(round(circles[0][closest_ball][0])), int(round(circles[0][closest_ball][1])))
            radius = int(round(circles[0][closest_ball][2]))

        except IndexError:
            pass
            # print("circles: %s"%circles)

    k = cv2.waitKey(5) & 0xFF
    if k == 27:
        return (0, 0), 0
    if radius > 3:
        return center, radius
    else:
        return (0, 0), 0


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=port)
