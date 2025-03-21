# AutomatedBarplotConverter
A converter that takes an image of a bar plot and output the values of each bar.

<img width="1105" alt="image" src="https://github.com/user-attachments/assets/987440fd-9103-4e85-a7e5-2b59c9d18ee6" />

# How to use:
**Step 1: Select Image** 
<br>
After running, use "Select Image" button to choose the graph(.png, .jpg, .jpeg, .bmp, .tif, .tiff) to process.
<br>
Crop the image to leave just the bar plot (without title, legend, etc.) to avoid disrupting the bar plot recognition.
<br>
<br>
**Step 2: Bar Recognition**
<br>
Press the "Process Bar Recognition" button to activate bar recognition.
<br>
The resulting graph will be displayed as well as the bar heights (in pixel).
 - the blue line indicates the top of the shortest bar, while
 - the red line indicates the top of the highest bar.

**Step 3: Convert Data**
<br>
Type in the value for the shortest/highest bar, and the start/end date of the bars, then
<br>
Press the "Process Data Conversion" button to convert the data. Results will be displayed in the "Data Preview" section.

# Mechanism:
1. The Recognizer class in 'recognizer.py' uses *OpenCV* package to recognize each bar in the graph, noting down the height of each bar (in pixel).
2. Value Estimate: The program then automatically calculates the ratio of pixels to actual values, therefore getting the values of each bar.
3. Date Estimate: Since the time gap b/w each bar is fixed, the gap could be calculated using the start/end date and number of bars.
4. Using the *tkinter* package to open/save file, as well as constructing the GUI of the app.
5. Using the *Pandas* package to help with storing data, as well as date calculating and .csv exporting.
