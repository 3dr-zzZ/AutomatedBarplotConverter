import cv2
import numpy as np

#-----------------------------------------------------------
# 1. LOAD THE IMAGE
#    Update this path to your actual chart image:
#-----------------------------------------------------------
image_path = "chart.png"
img = cv2.imread(image_path)
if img is None:
    raise SystemExit("Could not load image at: " + image_path)

#-----------------------------------------------------------
# 2. CONVERT TO HSV FOR COLOR MASKING
#-----------------------------------------------------------
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

#-----------------------------------------------------------
# 3. DEFINE COLOR RANGES & CREATE MASKS
#    You may need to adjust these ranges to match your colors:
#-----------------------------------------------------------

# Example ranges for blue bars (roughly around HSV hue ~110–130):
lower_blue = np.array([100, 100, 50])   # H=100, S=100, V=50
upper_blue = np.array([130, 255, 255]) # H=130
mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

# Example ranges for red bars (two ranges, because red wraps around hue=0/180):
#   Range 1: 0 to ~10
#   Range 2: ~160 to 179
lower_red1 = np.array([0,   80,  50])   
upper_red1 = np.array([10, 255, 255])
mask_red1 = cv2.inRange(hsv, lower_red1, upper_red1)

lower_red2 = np.array([160, 80,  50])
upper_red2 = np.array([179, 255, 255])
mask_red2 = cv2.inRange(hsv, lower_red2, upper_red2)

# Combine red masks
mask_red = cv2.bitwise_or(mask_red1, mask_red2)

# FINAL MASK: includes both red + blue bars
mask_all_bars = cv2.bitwise_or(mask_blue, mask_red)

# (Optional) You could also just do mask = mask_blue if you only want blue bars,
# or mask = mask_red if you only want red bars. 
# For demonstration, we'll detect both at once.
mask = mask_all_bars

#-----------------------------------------------------------
# 4. CLEAN UP THE MASK (OPTIONAL)
#    Sometimes applying morphological ops helps separate bars
#-----------------------------------------------------------
kernel = np.ones((3,3), np.uint8)
# e.g., close small gaps inside the bars:
mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
# e.g., open small noises:
mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel, iterations=1)

# Save intermediate mask for debugging
cv2.imwrite("mask_debug.png", mask)

#-----------------------------------------------------------
# 5. FIND CONTOURS IN THE MASK
#-----------------------------------------------------------
contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#-----------------------------------------------------------
# 6. FILTER CONTOURS THAT LOOK LIKE BARS
#    We expect a bar to be tall & relatively narrow.
#    Adjust these thresholds to match your chart size.
#-----------------------------------------------------------
bar_contours = []
for c in contours:
    x, y, w, h = cv2.boundingRect(c)
    aspect_ratio = (h + 1e-5) / (w + 1e-5)

    # Example filter: 
    #   Minimum width = 2, maximum width = 50 (just guess),
    #   Minimum height = 20,
    #   aspect ratio at least 1.5
    if (2 <= w <= 50) and (h >= 20) and (aspect_ratio >= 1.5):
        bar_contours.append((x, y, w, h))

#-----------------------------------------------------------
# 7. SORT BARS LEFT-TO-RIGHT
#-----------------------------------------------------------
bar_contours.sort(key=lambda b: b[0])  # sort by x-coordinate

#-----------------------------------------------------------
# 8. DETERMINE YOUR BASELINE & TOP PIXEL COORDINATES
#    This part *must* be tuned for your image.
#    Manually inspect the image (e.g., in Paint) to find:
#      Y_base = pixel row of the x-axis (where bars start)
#      Y_top  = pixel row that corresponds to the top scale (e.g. 4000 units)
#-----------------------------------------------------------
# Example guess:
Y_base = 400
Y_top  = 50
max_units = 4000.0  # If top of chart is ~4000 units

pixel_range = float(Y_base - Y_top)  # e.g., 400 - 50 = 350
units_per_pixel = max_units / pixel_range if pixel_range else 0

#-----------------------------------------------------------
# 9. COMPUTE APPROX VALUES FOR EACH BAR
#-----------------------------------------------------------
approx_values = []
for (x, y, w, h) in bar_contours:
    bar_top = y
    bar_bottom = y + h

    # If the baseline is Y_base, the bar height in pixels is
    bar_height_px = Y_base - bar_bottom  # how far above the baseline
    if bar_height_px < 0: 
        # The bar might extend below the baseline or the baseline is set incorrectly
        bar_height_px = 0

    # Convert to data units
    estimated_units = bar_height_px * units_per_pixel

    approx_values.append((x, estimated_units))

#-----------------------------------------------------------
# 10. PRINT RESULTS & DEBUG
#-----------------------------------------------------------
for i, (x_coord, val) in enumerate(approx_values, start=1):
    print(f"Bar {i:2d} at x={x_coord:4d} => approx. {val:.1f} units sold")

#-----------------------------------------------------------
# 11. (OPTIONAL) DRAW BOUNDING BOXES FOR VISUAL INSPECTION
#-----------------------------------------------------------
debug_img = img.copy()
for (x, y, w, h) in bar_contours:
    cv2.rectangle(debug_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

cv2.imwrite("bars_detected.png", debug_img)
print("Detection with bounding boxes saved to bars_detected.png")