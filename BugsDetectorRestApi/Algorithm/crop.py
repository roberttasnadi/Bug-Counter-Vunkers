import cv2
import numpy as np
from matplotlib import pyplot as plt


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
