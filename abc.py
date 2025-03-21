"""
AutomatedBarplotConverter (ABC)

Author: 3dr-zzZ

=== Module Description ===

"""

import cv2, os
import pandas as pd
import numpy as np
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk, ImageDraw
import tkinter as tk

from recognizer import Recognizer

class GUI:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Automated Barplot Converter")

        # Variables to store images and csv data
        self.image_path = ""
        self.original_image = None  # PIL Image
        self.processed_image = None  # PIL Image
        self.photo = None  # PhotoImage for display
        self.raw_data = []
        self.actual_val = []
        self.df = pd.DataFrame()

        # Button to select an image
        self.select_button = tk.Button(root, text="Select Image", command=self.load_image)
        self.select_button.pack(pady=5)

        # Label to preview image
        self.image_label = tk.Label(root, text="[No image selected]")
        self.image_label.pack(pady=5)

        # Label to preview data
        self.data_label = tk.Label(root, text="[No data preview]")
        self.data_label.pack(pady=5)

        # Button to process bar recognition
        self.process_button = tk.Button(root, text="Process Bar Recognition", command=self.process_image)
        self.process_button.pack(pady=5)

        # Frame for input boxes
        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=5)

        # Example input boxes with labels
        tk.Label(self.input_frame, text="Value of lowest bar:").grid(row=0, column=0, padx=5, pady=2, sticky='e')
        self.min_val = tk.Entry(self.input_frame)
        self.min_val.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.input_frame, text="Value of highest bar:").grid(row=1, column=0, padx=5, pady=2, sticky='e')
        self.max_val = tk.Entry(self.input_frame)
        self.max_val.grid(row=1, column=1, padx=5, pady=2)

        self.convert_button = tk.Button(root, text="Process Data Convertion", command=self.convert_data)
        self.convert_button.pack(pady=5)

        tk.Label(self.input_frame, text="Beginning date (YYYY-MM-DD):").grid(row=2, column=0, padx=5, pady=2, sticky='e')
        self.start_date = tk.Entry(self.input_frame)
        self.start_date.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.input_frame, text="End date (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=2, sticky='e')
        self.end_date = tk.Entry(self.input_frame)
        self.end_date.grid(row=3, column=1, padx=5, pady=2)

        # Button to export CSV
        self.export_button = tk.Button(root, text="Export CSV", command=self.export)
        self.export_button.pack(pady=5)

    def load_image(self) -> None:
        """Load the image."""
        self.image_path =  filedialog.askopenfilename()

        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.photo = ImageTk.PhotoImage(self.original_image)
                self.image_label.config(image=self.photo, text="")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
        else:
            messagebox.showinfo("Info", "No image selected")

    def process_image(self) -> None:
        recognizer = Recognizer(self.image_path)
        self.processed_image = recognizer.output_graph()
        self.raw_data = recognizer.output_data()
        self.photo = ImageTk.PhotoImage(Image.fromarray(self.processed_image))
        self.image_label.config(image=self.photo, text="")

    def convert_data(self) -> None:
        """Return a list of converted data from raw_data which values are actual."""
        # Reduce all data by height of min(raw_data)
        min_pixel = min(self.raw_data)
        secondary_data = []
        for data in self.raw_data:
            secondary_data.append(data - min_pixel)

        # Recognize the value of lowest bar and highest bar, calculate the
        # magnitude of each pixel.

        # For now, promote the user to recognize it.
        max_pixel = max(secondary_data)
        max_value = float(self.max_val.get())
        min_value = float(self.min_val.get())
        ratio = (max_value - min_value) / max_pixel

        # Convert secondary_data to data with actual value based on ratio.
        for data in secondary_data:
            self.actual_val.append(round(data * ratio + min_value, 2))

        self.data_label.config(text="Actual Values: " + ", ".join(map(str, self.actual_val)))


    def date_calculator(self) -> None:
        """Add a date feature to the DataFrame by creating a new 'Date' column.

        Prompts the user for the start and end date, and generates an evenly spaced date range
        corresponding to the number of rows in the DataFrame.
        """
        start_date = self.start_date.get()
        end_date = self.end_date.get()
        n = len(self.df)

        # Generate the date range with evenly spaced intervals
        date_range = pd.date_range(start=start_date, end=end_date, periods=n)

        # Add the date column to the DataFrame
        self.df['Date'] = date_range.strftime('%Y-%m-%d')

    def export(self) -> None:
        """
        Export the data into a CSV file using Pandas, including the date feature.

        The user is prompted to choose whether to create a new file or append to an existing file.
        If data is provided as a list, it will be converted to a DataFrame with a single column 'Value'.
        A date feature will be added to the DataFrame using date_calculator.
        """
        self.df = pd.DataFrame(self.actual_val, columns=["Value"])

        # Add the date feature to the DataFrame
        self.date_calculator()

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save DataFrame as CSV"
        )

        write_mode = 'w'
        write_header = True

        self.df.to_csv(file_path, mode=write_mode, header=write_header, index=False)

        print(f"Data exported to '{file_path}' (mode={write_mode}, header={write_header}).")

def main() -> None:
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
