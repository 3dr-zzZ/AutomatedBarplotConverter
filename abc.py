"""AutomatedBarplotConverter (ABC)

Author: 3dr-zzZ

"""

import cv2
import numpy as np

# Read image
img = cv2.imread('chart.png')

# Convert to HSV
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

# Define lower and upper bounds for your bar color (e.g., blue)
# You must adjust these ranges for your specific chart color
lower_blue = np.array([100, 100, 50])  # Example range
upper_blue = np.array([140, 255, 255])

# Create a mask where pixels within the range are white (255) and others are black (0)
mask = cv2.inRange(hsv, lower_blue, upper_blue)

# Optional: morphological close to fill small gaps
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,3))
mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=2)

# Find contours on mask_closed
contours, _ = cv2.findContours(mask_closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Sort contours left to right
contours = sorted(contours, key=lambda c: cv2.boundingRect(c)[0])

# Collect bounding boxes (or heights)
bar_heights = []
out_img = img.copy()
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    bar_heights.append(h)
    cv2.rectangle(out_img, (x, y), (x+w, y+h), (0,255,0), 2)

cv2.imshow("Detected Bars", out_img)
cv2.waitKey(0)
cv2.destroyAllWindows()

print("Bar heights:", bar_heights)
