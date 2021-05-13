# Program to move a laser around on the ground to entertain a cat.
# Written by Nic John 2021.

from Turret import *
from Vision import *
import time
import math


x_in_min = 44
x_in_max = 579
y_in_min = 55
y_in_max = 512
x_out_min = 50
x_out_max = 130
y_out_min = 51
y_out_max = 70

def convert_coords_for_laser(x_in, y_in):
    x_in_range = x_in_max - x_in_min
    y_in_range = y_in_max - y_in_min
    x_out_range = x_out_max - x_out_min
    y_out_range = y_out_max - y_out_min
    x_in_ratio = x_in / x_in_range
    y_in_ratio = y_in / y_in_range

    base = x_out_max - (x_out_range * x_in_ratio)
    tilt = y_out_max - (y_out_range * y_in_ratio)

    return base, tilt


def trace_circle(xc, yc, r, t):
    x = xc + r * math.cos(4*t)
    y = yc + r * math.sin(4*t)

    return x, y


def pick_circle_offset(xc, yc):
    if xc < ((x_in_max-x_in_min)/2) and yc < ((y_in_max-y_in_min)/2):  # 1st quadrant
        print("1")
        return (x_in_max-x_in_min) * 3 /4, (y_in_max-y_in_min) * 3 / 4
    elif xc < ((x_in_max-x_in_min)/2) and yc >= ((y_in_max-y_in_min)/2):  # 2nd quadrant
        print("2")
        return (x_in_max - x_in_min) * 3 / 4, (y_in_max - y_in_min) / 4
    elif xc >= ((x_in_max-x_in_min)/2) and yc < ((y_in_max-y_in_min)/2):  # 2nd quadrant
        print("3")
        return (x_in_max - x_in_min) / 4, (y_in_max - y_in_min) * 3 / 4
    elif xc >= ((x_in_max-x_in_min)/2) and yc >= ((y_in_max-y_in_min)/2):  # 2nd quadrant
        print("4")
        return (x_in_max - x_in_min) / 4, (y_in_max - y_in_min) / 4
    return (x_in_max - x_in_min) / 2, (y_in_max - y_in_min) / 2


if __name__ == '__main__':
    camera = Vision()
    laser_turret = Turret()
    laser = "1"
    t = 0

    while True:
        cat = camera.get_center_of_object()
        center = pick_circle_offset(cat[0], cat[1])
        draw = trace_circle(center[0], center[1], 50, t)
        stacked_images = stack_images(0.8, [camera.img, camera.img_contour])

        base, tilt = convert_coords_for_laser(draw[0], draw[1])

        laser_turret.command(base, tilt, laser)

        # Debugging visualization
        cv2.imshow("Result", stacked_images)
        print("Target: (%s, %s)" % (center[0], center[1]))
        #print("Base: %s, Tilt: %s" % (base, tilt))

        t += 0.1
        time.sleep(0.1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    laser.command(90, 90, 0)  # Turn turret off
