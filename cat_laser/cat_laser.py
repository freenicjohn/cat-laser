# Program to move a laser around on the ground to entertain a cat.
# Written by Nic John 2021.

from Turret import *
from Vision import *
import time


def convert_coords_for_laser(x, y):
    max = 640
    min_x_out = 49
    min_y_out = 45
    max_x_out = 125
    max_y_out = 75

    x_range_out = max_x_out - min_x_out
    y_range_out = max_y_out - min_y_out

    percent_x = x/max
    percent_y = y/max

    base = min_x_out + (percent_x * x_range_out)
    tilt = min_y_out + (percent_y * y_range_out)

    return base, tilt


if __name__ == '__main__':
    camera = Vision()
    laser_turret = Turret()
    laser = "1"

    while True:
        center = camera.get_center_of_object()
        stacked_images = stack_images(0.8, [camera.img, camera.img_contour])

        base, tilt = convert_coords_for_laser(center[0], center[1])

        laser_turret.command(base, tilt, laser)

        # Debugging visualization
        cv2.imshow("Result", stacked_images)
        print("Target: (%s, %s)" % (center[0], center[1]))
        print("Base: %s, Tilt: %s" % (base, tilt))

        time.sleep(0.1)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    laser.command(90, 90, 0)  # Turn turret off
