# Program to move a laser around on the ground to entertain a cat.
# Written by Nic John 2021.

from Turret import *
from Vision import *
import time
import math


def convert_coords_for_laser(x_in, y_in, camera_obj):
    """ Converts x,y coordinates in the camera frame to base/tilt commands for the turret"""
    x_out_min = 60
    x_out_max = 124
    y_out_min = 10
    y_out_max = 40

    x_in_range = camera_obj.width
    y_in_range = camera_obj.height
    x_out_range = x_out_max - x_out_min
    y_out_range = y_out_max - y_out_min
    x_in_ratio = x_in / x_in_range
    y_in_ratio = y_in / y_in_range

    base = x_out_max - (x_out_range * x_in_ratio)
    tilt = y_out_max - (y_out_range * y_in_ratio)

    return base, tilt


def trace_circle(xc, yc, r, t):
    """ Draws a circle with radius r (not sure if I'm doing radius right tbh)
        around the given center points
    """
    x = xc + r * math.cos(4*t)
    y = yc + r * math.sin(4*t)

    return x, y


def pick_circle_offset(xc, yc, camera_obj, t):
    quad_1 = [camera_obj.width*3/4, camera_obj.height/4]
    quad_2 = [camera_obj.width/4, camera_obj.height/4]
    quad_3 = [camera_obj.width/4, camera_obj.height*3/4]
    quad_4 = [camera_obj.width*3/4, camera_obj.height*3/4]
    center = [camera_obj.width/2, camera_obj.height/2]

    if xc < (camera_obj.width/2) and yc < (camera_obj.height/2):
        print("quadrant: 2")
        quadrant = 2
    elif xc < (camera_obj.width/2) and yc >= (camera_obj.height/2):
        print("quadrant: 3")
        quadrant = 3
    elif xc >= (camera_obj.width/2) and yc < (camera_obj.height/2):
        print("quadrant: 1")
        quadrant = 1
    elif xc >= (camera_obj.width/2) and yc >= (camera_obj.height/2):
        print("quadrant: 4")
        quadrant = 4

    if camera_obj.width/4 < xc < camera_obj.width*3/4 and camera_obj.height/4 < yc < camera_obj.height*3/4:
        in_center = True
    else:
        in_center = False
    print(in_center)

    if in_center:
        return trace_circle(camera_obj.width/2, camera_obj.height/2, 300, t/8)
    else:
        return trace_circle(camera_obj.width/2, camera_obj.height/2, 50, t/2)


if __name__ == '__main__':
    camera = Vision()
    laser_turret = Turret()
    laser = "1"
    t = 0

    while True:
        cat = camera.get_center_of_object()
        #center = pick_circle_offset(cat[0], cat[1], camera, t)
        draw = pick_circle_offset(cat[0], cat[1], camera, t)
        #draw = trace_circle(center[0], center[1], 0, t)
        stacked_images = stack_images(0.8, [camera.img, camera.img_contour])

        base, tilt = convert_coords_for_laser(draw[0], draw[1], camera)

        laser_turret.command(base, tilt, laser)

        # Debugging visualization
        cv2.imshow("Result", stacked_images)
        print("Target: (%s, %s)" % (draw[0], draw[1]))
        #print("Base: %s, Tilt: %s" % (base, tilt))

        t += 0.1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    laser.command(90, 90, 0)  # Turn turret off
