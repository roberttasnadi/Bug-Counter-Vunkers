
import cv2
import numpy as np
from matplotlib import pyplot as plt
import crop

MIN_FLY_SIZE = 9000  # 9000
MIN_BIG_M_SIZE = 80
MIN_MEDIUM_M_SIZE = 50

class BugCounter(object):
    def __init__(self, src_img):
        self.max_ratio = 3
        self.max_area = 10000
        self.min_area = 30
        self.src_img = src_img

    def count(self):
        processed_image = self.processImage()
        contours = self.getContours(processed_image)
        return self.filterContours(contours)

    def processImage(self):
        gray_img = cv2.cvtColor(self.src_img, cv2.COLOR_BGR2GRAY)
        _, processed_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return processed_img

    def getContours(self, img):
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def filterContours(self, contours):
        valid_shapes = []

        for contour in contours[1:]:
            if self.validContour(contour):
                valid_shapes += [contour]

        return valid_shapes

    def validContour(self, contour):
        area = cv2.contourArea(contour)
        _, _, width, height = cv2.boundingRect(contour)
        vert_ratio = float(height) / width
        hor_ratio = float(width) / height
        if self.max_area > area > self.min_area and vert_ratio < self.max_ratio and hor_ratio < self.max_ratio:
            return True
        return False

    def classifyBugs(self, bugs, flies=0, big_m=0, medium_m=0, small_m=0):
        for bug in bugs:
            size = cv2.contourArea(bug)
            if size >= MIN_FLY_SIZE:
                flies += 1
            elif size >= MIN_BIG_M_SIZE:
                big_m += 1
            elif size >= MIN_MEDIUM_M_SIZE:
                medium_m += 1
            else:
                small_m += 1

        return [flies, big_m, medium_m, small_m]

    def printContours(self, contours):
        cv2.drawContours(self.src_img, contours, -1, (0, 0, 255), 1)
        plt.imshow(self.src_img)
        plt.show()

