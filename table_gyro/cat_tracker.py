# Program to detect cat on the floor

import cv2
import numpy as np


def getWebcam(width=640, height=480, brightness=100):
    ''' Returns cap object of webcam stream'''
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # 0 uses default webcam
    cap.set(3, width)  # set width - first param here is a setting ID
    cap.set(4, height)  # set height
    cap.set(10, brightness)  # set brightness

    return cap


def preProcessing(img, debug=False):
    if debug:
        # parameters to tune
        p_1 = cv2.getTrackbarPos("P 1", "TrackBars")
        p_2 = cv2.getTrackbarPos("P 2", "TrackBars")
    else:
        # Values from tuning
        p_1 = 152
        p_2 = 193

    imgGray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    imgBlur = cv2.GaussianBlur(imgGray, (5, 5), 2)
    imgCanny = cv2.Canny(imgBlur, p_1, p_2)  # 1 and 2 are threshold params
    kernel = np.ones((5, 5), np.uint8)  # kernel required for dilation function
    imgDial = cv2.dilate(imgCanny, kernel, iterations=10)  # dilation makes edges thicker

    imgStack = stackImages(0.8, ([[imgGray, imgDial]]))

    if debug:
        cv2.imshow("Test", imgStack)

    return imgDial


def getContours(img, original_img, shape_rec=False):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    maxArea = 0
    biggest = np.array([])
    imgContour = original_img.copy()
    x, y, w, h = 0, 0, 0, 0

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 5000:  # Using a threshold to decide if it's worth drawing the contour
            peri = cv2.arcLength(cnt, True)  # Get perimeter of each contour
            approx = cv2.approxPolyDP(cnt, 0.02 * peri, True)  # Get corner points for each contour
            if area > maxArea:
                best_cnt = cnt
                biggest = approx
                maxArea = area
                x, y, w, h = cv2.boundingRect(approx)  # draw bounding box around contour
                cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
        else:
            best_cnt = cnt

    # Calculate center of biggest contour
    if len(contours) > 0:
        M = cv2.moments(best_cnt)
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])
        # draw the center of the shape on the image
        cv2.circle(imgContour, (cX, cY), 7, (255, 255, 255), -1)

    return imgContour, biggest


def perspectiveTransform(img, width, height):

    pts1 = np.float32([[173, 205], [536, 220], [67, 487], [621, 497]])  # the 4 corners of the shape - can be gotten from paint or ShareX (cursor locations at the corners)
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])  # the 4 points to map to
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    img_warped = cv2.warpPerspective(img, matrix, (width, height))

    return img_warped


def stackImages(scale, imgArray):  # function the guy wrote to stack images
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range(0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape[:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]),
                                                None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y] = cv2.cvtColor(imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank] * rows
        hor_con = [imageBlank] * rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None, scale,
                                         scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor = np.hstack(imgArray)
        ver = hor
    return ver


if __name__ == '__main__':
    debug = False

    # Frame size
    widthImg = 640
    heightImg = 640

    if debug:
        # Create trackbar for tuning
        def empty(a):
            pass

        cv2.namedWindow("TrackBars")
        cv2.resizeWindow("TrackBars", 640, 240)
        cv2.createTrackbar("P 1", "TrackBars", 0, 200, empty)
        cv2.createTrackbar("P 2", "TrackBars", 0, 200, empty)

        # parameters to tune
        p_1 = cv2.getTrackbarPos("P 1", "TrackBars")
        p_2 = cv2.getTrackbarPos("P 2", "TrackBars")

    cap = getWebcam(widthImg, heightImg)  # Get capture from webcam

    while True:
        success, img = cap.read()  # Read from the webcam
        img = cv2.resize(img, (widthImg, heightImg))
        imgWarped = perspectiveTransform(img, widthImg, heightImg)
        imgThresh = preProcessing(imgWarped, debug)
        imgContour, biggest = getContours(imgThresh, imgWarped)

        stackedImages = stackImages(0.6, [img, imgWarped, imgContour])

        cv2.imshow("Result", stackedImages)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break