"""
AutomatedBarplotConverter (ABC)

Author: 3dr-zzZ

=== Module Description ===
This module provides a class for processing bar plot images.
It extracts bar heights and generates a preview image with detected bars highlighted.
"""

import cv2
import numpy as np

class Recognizer:
    def __init__(self, image_path):
        """
        Initializes the converter with the specified image path.

        :param image_path: Path to the bar plot image.
        """
        self.image_path = image_path
        self.original_image = cv2.imread(self.image_path)
        if self.original_image is None:
            raise ValueError(f"Image not found or unable to load: {self.image_path}")

        self.processed_image = None
        self.bar_heights = None
        self._process_image()

    def _process_image(self):
        """
        Processes the image to detect bars and computes their heights.
        """
        # Convert image to HSV for color segmentation
        hsv = cv2.cvtColor(self.original_image, cv2.COLOR_BGR2HSV)

        # Define lower and upper bounds for the bar color (e.g., blue)
        # Adjust these values for your specific chart color if needed
        lower_blue = np.array([100, 100, 50])
        upper_blue = np.array([140, 255, 255])

        # Create a mask where the bar color is white and the rest is black
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # Morphological close to fill small gaps in the mask
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

        # Find contours on the processed mask
        contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # Sort contours left-to-right
        contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

        # Initialize results
        self.bar_heights = []
        self.processed_image = self.original_image.copy()

        # Loop over contours, compute bounding boxes, and extract bar heights
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            self.bar_heights.append(h)
            cv2.rectangle(self.processed_image, (x, y), (x + w, y + h), (0, 255, 0), 2)

    def output_graph(self):
        """
        Returns the processed image with detected bars highlighted.

        :return: Processed image (numpy array).
        """
        return self.processed_image

    def output_data(self):
        """
        Returns the list of bar heights in pixels.

        :return: List of integers representing bar heights.
        """
        return self.bar_heights

if __name__ == "__main__":
    # Example usage
    recognizer = Recognizer('chart.png')
    graph_preview = recognizer.output_graph()
    data_preview = recognizer.output_data()

    # Display the processed image
    cv2.imshow("Graph Preview", graph_preview)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Print bar heights
    print("Bar heights:", data_preview)
