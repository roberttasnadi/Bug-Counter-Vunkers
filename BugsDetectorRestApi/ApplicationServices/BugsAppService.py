import cv2
from matplotlib import pyplot as plt
import numpy as np

def imageProcessRequest(path):
    img = getImageFromFiles(path)
    return processImage(img)


def getImageFromFiles(path):
    img = cv2.imread("C:\\Users\\rober\\Documents\\imatges\\" + path)
    return img


def processImage(img):
    cropper = Crop(img)
    cropped_img = cropper.crop_image()
    counter = BugCounter(cropped_img)
    bugs = counter.count()
    return counter.classifyBugs(bugs)

MIN_FLY_SIZE = 4500
MIN_BIG_M_SIZE = 80
MIN_MEDIUM_M_SIZE = 50

class BugCounter(object):
    def __init__(self, src_img):
        # Contour validation criteria
        self.max_ratio = 3
        self.max_area = 10000
        self.min_area = 30
        self.src_img = src_img

    def count(self):
        """
        Begins the bug counting process
        :return: List of containing the number of each kind of bugs
        """
        processed_image = self.processImage()
        contours = self.getContours(processed_image)
        return self.filterContours(contours)

    def processImage(self):
        """
        Applies a filter to the image in order to enhance the contrast
        :return: The resulting image
        """
        gray_img = cv2.cvtColor(self.src_img, cv2.COLOR_BGR2GRAY)
        _, processed_img = cv2.threshold(gray_img, 127, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return processed_img

    def getContours(self, img):
        """
        Finds the contours (shapes) that represent bugs in the image
        :param img: The image where the shapes will be searched
        :return: A list containing all the contours
        """
        contours, _ = cv2.findContours(img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        return contours

    def filterContours(self, contours):
        """
        Removes shapes that are considered 'wrong' by the established criteria
        :param contours: List of contours
        :return: A list containing only the valid contours
        """
        valid_shapes = []
        for contour in contours[1:]:
            if self.validContour(contour):
                valid_shapes += [contour]

        return valid_shapes

    def validContour(self, contour):
        """
        Applies the criteria for telling which shapes are correct
        :param contour: A given shape
        :return: True if the shape is valid False otherwise
        """
        area = cv2.contourArea(contour)
        _, _, width, height = cv2.boundingRect(contour)
        vert_ratio = float(height) / width
        hor_ratio = float(width) / height
        if self.max_area > area > self.min_area and vert_ratio < self.max_ratio and hor_ratio < self.max_ratio:
            return True
        return False

    def classifyBugs(self, bugs, flies=0, big_m=0, medium_m=0, small_m=0):
        """
        Counts how many of each bug kind are there. It uses the size criteria
        :param bugs: List containing all the valid shapes
        :param flies: Number of flies
        :param big_m: Number of big mosquitoes
        :param medium_m: Number of medium mosquitoes
        :param small_m: Number of small mosquitoes
        :return: List containing all occurrences of each bug
        """
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
        """
        Prints all the valid contours over the original image
        :param contours: List of all valid contours
        """
        cv2.drawContours(self.src_img, contours, -1, (0, 0, 255), 1)
        plt.imshow(self.src_img)
        plt.show()

class Crop(object):
    def __init__(self, image):
        # Saves a copy of the original one and applies a color filter on a copy to crop it
        self.original_image = image
        self.image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        # Set the image height and width
        self._height = image.shape[0]
        self._width = image.shape[1]
        print("Height: ", self._height)
        print("Width: ", self._width)

        # Set yellow lower and upper ranges in BGr
        self._lower_yellow_range = np.array([22, 93, 0], dtype="uint8")
        self._upper_yellow_range = np.array([45, 255, 255], dtype="uint8")

        # Initialize bound to zero
        self._upper_bound = 0
        self._lower_bound = 0
        self._left_bound = 0
        self._right_bound = 0

        # Call method to get bounds
        self._find_bounds()

    def _find_bounds(self):
        """
        Finds the bounds to crop the image
        """
        self._find_upper_bound()
        self._find_lower_bound()
        self._find_left_bound()
        self._find_right_bound()

    def _find_upper_bound(self):
        """
        Sets the lower bound to the lower upper bound found
        """
        for i in range(self._height - 1, -1, -1):
            if self._vertical_bounds_conditions(i):
                self._upper_bound = i
                break

    def _find_lower_bound(self):
        """
        Sets the lower bound to the lower lower bound found
        """
        for i in range(self._height):
            if self._vertical_bounds_conditions(i):
                self._lower_bound = i
                break

    def _find_left_bound(self):
        """
        Sets the left bound to the lower left bound found
        """
        for i in range(self._width):
            if self._horizontal_bounds_conditions(i):
                self._left_bound = i
                break

    def _find_right_bound(self):
        """
        Sets the right bound to the lower right bound found
        """
        for i in range(self._width - 1, -1, -1):
            if self._horizontal_bounds_conditions(i):
                self._right_bound = i
                break

    def _vertical_bounds_conditions(self, position):
        """
        Checks whether the conditions to set the vertical bounds are satisfied
        :param position: Position to check the vertical conditions are satisfied
        :return: True if condition for the vertical bounds are true, false otherwise
        """
        return self._color_in_yellow_range(self.image[position, int(self._width / 4)]) or self._color_in_yellow_range(
            self.image[position, int(self._width * 2 / 4)]) or self._color_in_yellow_range(
            self.image[position, int(self._width * 3 / 4)])

    def _horizontal_bounds_conditions(self, position):
        """
        Checks whether the conditions to set the horizontal bounds are satisfied
        :param position: Position to check the horizontal conditions are satisfied
        :return: True if condition for the horizontal bounds are true, false otherwise
        """
        return self._color_in_yellow_range(self.image[int(self._height / 4), position]) or self._color_in_yellow_range(
            self.image[int(self._height * 2 / 4), position]) or self._color_in_yellow_range(
            self.image[int(self._height * 3 / 4), position])

    def _color_in_yellow_range(self, pixel):
        """
        Given a certain BGr numpy array, find if it's in the yellow range.
        :return: True if it's in the Yellow range, False otherwise
        """
        if self._lower_yellow_range[0] <= pixel[0] <= self._upper_yellow_range[0] and \
                self._lower_yellow_range[1] <= pixel[1] <= self._upper_yellow_range[1] and \
                self._lower_yellow_range[2] <= pixel[2] <= self._upper_yellow_range[2]:
            return True
        else:
            return False

    def crop_image(self):
        """
        Crops the image with the calculated bounds
        :return: Cropeed image
        """
        return self.original_image[self._lower_bound:self._upper_bound, self._left_bound:self._right_bound]
