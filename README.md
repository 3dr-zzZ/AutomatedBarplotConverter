# AutomatedBarplotConverter
A converter that takes an image of a bar plot and outputs the values of each bar.

<img width="1105" alt="image" src="https://github.com/user-attachments/assets/987440fd-9103-4e85-a7e5-2b59c9d18ee6" />

 - *See `example_chart.png` for example input, and `example_export.csv` for the output.*

---
## Download
Download the latest version from [Github Releases](https://github.com/3dr-zzZ/AutomatedBarplotConverter/releases)
 - If you don't have Python on your PC, download the `abc.exe` file and double-click to run it (Windows).
 - If you are familiar with Python, the `abc.py` is the main file you are looking for; All required packages can be found in requirements.txt

---

## Usage Guide

### **Step 1: Select Image**
1. Click the **"Select Image"** button to upload an image file. Supported formats:  
   - `.png`, `.jpg`, `.jpeg`, `.bmp`, `.tif`, `.tiff`
*Note: use cropped images containing only the bar plot (excluding titles, legends, etc.) to improve accuracy.*

### **Step 2: Process Bar Recognition**
1. Click the **"Process Bar Recognition"** button to analyze the bar plot.
2. The recognized bars will be highlighted in **green**.
3. The system will mark:
   - The **shortest bar's top** with a **blue line**.
   - The **tallest bar's top** with a **red line**.
4. Bar heights (in pixels) will be displayed.

### **Step 3: Convert Data**
1. Enter the **real-world values** for:
   - The shortest bar
   - The tallest bar
   - The beginning date (YYYY-MM-DD)
   - The end date (YYYY-MM-DD)
2. Click **"Process Data Conversion"** to calculate and display the extracted values.

### **Step 4: Export CSV**
Click the **"Export CSV"** button to save the extracted data for further analysis.

---
## How It Works:
1. **Bar Detection**  
   - The `Recognizer` class in `recognizer.py` uses **OpenCV** to detect and measure bar heights (in pixels).
   
2. **Value Estimation**  
   - The program computes the pixel-to-value ratio based on the tallest and shortest bars to determine each bar’s real-world value.

3. **Date Estimation**  
   - Since the bars represent evenly spaced time intervals, the program distributes the provided start and end dates across all detected bars.

4. **Graphical Interface**  
   - The application uses **tkinter** for an interactive user interface.

---
## License
This project is licensed under the MIT License.
