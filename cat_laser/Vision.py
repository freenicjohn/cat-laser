# Program to get the center points of a cat on the floor

import cv2
import numpy as np


class Vision:
    def __init__(self, p1=0, p2=109):
        """ Initialize the Vision object """
        self.width = 640
        self.height = 640
        self.p1 = p1
        self.p2 = p2
        self.img = np.zeros(1)
        self.img_warped = np.zeros(1)
        self.img_dilated = np.zeros(1)
        self.img_contour = np.zeros(1)
        self.brightness = 100
        self.contour_threshold = 5000
        self.cX = 0
        self.cY = 0

        # Initialize webcam capture
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 uses default webcam
        self.cap.set(3, self.width)  # set width - first param here is a setting ID
        self.cap.set(4, self.height)  # set height
        self.cap.set(10, self.brightness)  # set brightness

    def pre_processing(self):
        """ Creates dilated image ready for contouring """
        if __name__ == '__main__':
            # parameters to tune
            p_1 = cv2.getTrackbarPos("P 1", "TrackBars")
            p_2 = cv2.getTrackbarPos("P 2", "TrackBars")
        else:
            # Values from tuning
            p_1 = self.p1
            p_2 = self.p2

        img_gray = cv2.cvtColor(self.img_warped, cv2.COLOR_BGR2GRAY)
        img_blur = cv2.GaussianBlur(img_gray, (5, 5), 2)
        img_canny = cv2.Canny(img_blur, p_1, p_2)  # 1 and 2 are threshold params
        kernel = np.ones((5, 5), np.uint8)  # kernel required for dilation function
        self.img_dilated = cv2.dilate(img_canny, kernel, iterations=10)  # dilation makes edges thicker

    def get_contours(self):
        contours, hierarchy = cv2.findContours(self.img_dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        max_area = 0
        best_cnt = []
        self.img_contour = self.img_warped.copy()

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if area > self.contour_threshold:  # Using a threshold to decide if it's worth drawing the contour
                if area > max_area:
                    # Found new largest contour
                    best_cnt = cnt
                    max_area = area
                    cv2.drawContours(self.img_contour, cnt, -1, (255, 0, 0), 2)

        if len(contours) > 0 and best_cnt != []:
            # Calculate center of biggest contour
            M = cv2.moments(best_cnt)
            self.cX = int(M["m10"] / M["m00"])
            self.cY = int(M["m01"] / M["m00"])
            # draw the center of the shape on the image
            cv2.circle(self.img_contour, (self.cX, self.cY), 7, (255, 255, 255), -1)

    def get_center_of_object(self):
        """ Draws a blue line around every object larger than the threshold area and a white dot at the center
            of the largest object
            Returns the center point coordinates of the largest object in an image
        """
        success, self.img = self.cap.read()  # Read from the webcam
        self.img = cv2.resize(self.img, (self.width, self.height))
        self.img_warped = perspective_transform(self.img, self.width, self.height)
        self.pre_processing()
        self.get_contours()

        return self.cX, self.cY


def perspective_transform(img, width, height):
    """ Warps an angled image to create flat 2d image"""
    pts1 = np.float32([[173, 205], [536, 220], [67, 487], [621, 497]])  #  the 4 corners of the shape - can be gotten
                                                                        #  from paint or ShareX (cursor locations at
                                                                        #  the corners)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])  # the 4 points to map to
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warped = cv2.warpPerspective(img, matrix, (width, height))

    return img_warped


def stack_images(scale, img_array):
    """ Helper function to stack images together for display
        Written by murtaza (YouTube) (I only re-factored variable names)
    """
    rows = len(img_array)
    cols = len(img_array[0])
    rows_available = isinstance(img_array[0], list)
    width = img_array[0][0].shape[1]
    height = img_array[0][0].shape[0]
    if rows_available:
        for x in range(0, rows):
            for y in range(0, cols):
                if img_array[x][y].shape[:2] == img_array[0][0].shape[:2]:
                    img_array[x][y] = cv2.resize(img_array[x][y], (0, 0), None, scale, scale)
                else:
                    img_array[x][y] = cv2.resize(img_array[x][y], (img_array[0][0].shape[1], img_array[0][0].shape[0]),
                                                None, scale, scale)
                if len(img_array[x][y].shape) == 2: img_array[x][y] = cv2.cvtColor(img_array[x][y], cv2.COLOR_GRAY2BGR)
        img_blank = np.zeros((height, width, 3), np.uint8)
        hor = [img_blank] * rows
        hor_con = [img_blank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(img_array[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if img_array[x].shape[:2] == img_array[0].shape[:2]:
                img_array[x] = cv2.resize(img_array[x], (0, 0), None, scale, scale)
            else:
                img_array[x] = cv2.resize(img_array[x], (img_array[0].shape[1], img_array[0].shape[0]), None, scale,
                                         scale)
            if len(img_array[x].shape) == 2: img_array[x] = cv2.cvtColor(img_array[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(img_array)
        ver = hor
    return ver


if __name__ == '__main__':
    camera = Vision()

    # Create trackbars for contour recognition tuning
    def empty(a):
        pass
    cv2.namedWindow("TrackBars")
    cv2.resizeWindow("TrackBars", 640, 240)
    cv2.createTrackbar("P 1", "TrackBars", camera.p1, 200, empty)
    cv2.createTrackbar("P 2", "TrackBars", camera.p2, 200, empty)

    while True:
        x, y = camera.get_center_of_object()
        stackedImages = stack_images(0.6, [camera.img, camera.img_dilated, camera.img_warped, camera.img_contour])
        cv2.imshow("Result", stackedImages)

        print(x, y)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
