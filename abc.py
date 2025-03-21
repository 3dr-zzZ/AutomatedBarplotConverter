"""
AutomatedBarplotConverter (ABC)

Author: 3dr-zzZ

=== Module Description ===

"""

import pandas as pd
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from PIL import Image, ImageTk, ImageDraw
from recognizer import Recognizer
import cv2, os
import numpy as np

class GUI:
    def __init__(self, root) -> None:
        self.root = root
        self.root.title("Automated Barplot Converter")

        # -----------------------------
        # Main frames: Left and Right
        # -----------------------------
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Left frame (for graph + data preview)
        self.left_frame = tk.Frame(self.main_frame)
        self.left_frame.pack(side="left", fill="both", expand=True)

        # Right frame (for controls/buttons/entries)
        self.right_frame = tk.Frame(self.main_frame)
        self.right_frame.pack(side="right", fill="y", padx=10, pady=10)

        # -----------------------------
        # Left side: Graph display
        # -----------------------------
        # LabelFrame around the graph area
        self.graph_frame = tk.LabelFrame(self.left_frame, text="Graph Preview")
        self.graph_frame.pack(side="top", fill="both", expand=True, padx=5, pady=(5, 0))

        # Canvas for the bar chart
        self.graph_canvas = tk.Canvas(self.graph_frame, width=600, height=400)
        self.graph_canvas.pack(side="left", fill="both", expand=True)

        # Vertical scrollbar (inside the LabelFrame)
        self.canvas_vscrollbar = tk.Scrollbar(
            self.graph_frame, orient="vertical", command=self.graph_canvas.yview
        )
        self.canvas_vscrollbar.pack(side="right", fill="y")

        # Horizontal scrollbar (in left_frame, below the graph_frame)
        self.canvas_hscrollbar = tk.Scrollbar(
            self.left_frame, orient="horizontal", command=self.graph_canvas.xview
        )
        # Pack it below the graph preview
        self.canvas_hscrollbar.pack(side="top", fill="x")

        # Configure the Canvas to use both scrollbars
        self.graph_canvas.configure(
            yscrollcommand=self.canvas_vscrollbar.set,
            xscrollcommand=self.canvas_hscrollbar.set
        )

        # -----------------------------
        # Left side: Data preview area
        # -----------------------------
        self.data_frame = tk.LabelFrame(self.left_frame, text="Data Preview")
        self.data_frame.pack(side="top", fill="both", expand=False, padx=5, pady=5)

        self.data_text = scrolledtext.ScrolledText(self.data_frame, wrap="word", width=70, height=6)
        self.data_text.pack(fill="both", expand=True)

        # -----------------------------
        # Right side: Buttons & inputs
        # -----------------------------
        self.select_button = tk.Button(self.right_frame, text="Select Image", command=self.load_image)
        self.select_button.pack(pady=5, fill="x")

        self.process_button = tk.Button(self.right_frame, text="Process Bar Recognition", command=self.process_image)
        self.process_button.pack(pady=5, fill="x")

        self.input_frame = tk.Frame(self.right_frame)
        self.input_frame.pack(pady=5, fill="x")

        tk.Label(self.input_frame, text="Value of lowest bar:").grid(
            row=0, column=0, padx=5, pady=2, sticky="e"
        )
        self.min_val = tk.Entry(self.input_frame)
        self.min_val.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(self.input_frame, text="Value of highest bar:").grid(
            row=1, column=0, padx=5, pady=2, sticky="e"
        )
        self.max_val = tk.Entry(self.input_frame)
        self.max_val.grid(row=1, column=1, padx=5, pady=2)

        self.convert_button = tk.Button(self.right_frame, text="Process Data Conversion", command=self.convert_data)
        self.convert_button.pack(pady=5, fill="x")

        tk.Label(self.input_frame, text="Beginning date (YYYY-MM-DD):").grid(
            row=2, column=0, padx=5, pady=2, sticky="e"
        )
        self.start_date = tk.Entry(self.input_frame)
        self.start_date.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(self.input_frame, text="End date (YYYY-MM-DD):").grid(
            row=3, column=0, padx=5, pady=2, sticky="e"
        )
        self.end_date = tk.Entry(self.input_frame)
        self.end_date.grid(row=3, column=1, padx=5, pady=2)

        self.export_button = tk.Button(self.right_frame, text="Export CSV", command=self.export)
        self.export_button.pack(pady=5, fill="x")

        # -----------------------------
        # Initialize variables
        # -----------------------------
        self.image_path = ""
        self.original_image = None
        self.processed_image = None
        self.photo = None
        self.raw_data = []
        self.actual_val = []
        self.df = pd.DataFrame()

    def load_image(self) -> None:
        """Load the image."""
        self.image_path =  filedialog.askopenfilename()

        if self.image_path:
            try:
                self.original_image = Image.open(self.image_path)
                self.photo = ImageTk.PhotoImage(self.original_image)
                self.graph_canvas.delete("all")
                self.graph_canvas.create_image(0, 0, anchor="nw", image=self.photo)
                # Update scrollregion so we can scroll if image is larger than 600x400
                w, h = self.original_image.size
                self.graph_canvas.config(scrollregion=(0, 0, w, h))
            except Exception as e:
                messagebox.showerror("Error", f"Failed to open image: {e}")
        else:
            messagebox.showinfo("Info", "No image selected")

    def process_image(self) -> None:
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return
        try:
            recognizer = Recognizer(self.image_path)
            self.processed_image = recognizer.output_graph()
            self.raw_data = recognizer.output_data()

            pil_image = Image.fromarray(self.processed_image)
            self.photo = ImageTk.PhotoImage(pil_image)
            self.graph_canvas.delete("all")
            self.graph_canvas.create_image(0, 0, anchor="nw", image=self.photo)
            # Update scrollregion
            w, h = pil_image.size
            self.graph_canvas.config(scrollregion=(0, 0, w, h))

            # Optionally, show raw data in the ScrolledText
            self.data_text.delete("1.0", tk.END)
            self.data_text.insert(tk.END, "Raw data:\n" + str(self.raw_data))
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process image: {e}")


    def convert_data(self) -> None:
        """Return a list of converted data from raw_data which values are actual."""
        if not self.raw_data:
            messagebox.showwarning("Warning", "No raw data to convert. Please process an image first.")
            return
        try:
            max_value = float(self.max_val.get())
            min_value = float(self.min_val.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter numeric values for min/max.")
            return

        # Reduce all data by height of min(raw_data)
        min_pixel = min(self.raw_data)
        shifted_data = []
        for data in self.raw_data:
            shifted_data.append(data - min_pixel)

        # Recognize the value of lowest bar and highest bar, calculate the
        # magnitude of each pixel.

        # For now, promote the user to recognize it.
        max_pixel = max(shifted_data)
        max_value = float(self.max_val.get())
        min_value = float(self.min_val.get())
        ratio = (max_value - min_value) / max_pixel

        # Convert shifted_data to data with actual value based on ratio.
        for data in shifted_data:
            self.actual_val.append(round(data * ratio + min_value, 2))

        self.data_text.delete("1.0", tk.END)
        self.data_text.insert(tk.END, "Converted values:\n" + ", ".join(map(str, self.actual_val)))

    def date_calculator(self) -> None:
        """Add a date feature to the DataFrame by creating a new 'Date' column.

        Since the time gap b/w each bar is the same, calculate the date of each
        bar by using user's input of start date and end date.
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

        The CSV file will have headers "Value" and "Date" on the first row, each
        following row represents the value and date of a bar.
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

def main() -> None:
    root = tk.Tk()
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
