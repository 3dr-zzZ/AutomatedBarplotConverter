"""
AutomatedBarplotConverter (ABC)

Author: 3dr-zzZ

=== Module Description ===

"""

import cv2, os
import pandas as pd
import numpy as np
from recognizer import Recognizer


def load_image() -> str:
    """Return the path of image."""
    return "example_chart.png"


def convert_data(raw_data: list) -> list:
    """Return a list of converted data from raw_data which values are actual."""
    # Reduce all data by height of min(raw_data)
    min_pixel = min(raw_data)
    secondary_data = []
    for data in raw_data:
        secondary_data.append(data - min_pixel)

    # Recognize the value of lowest bar and highest bar, calculate the
    # magnitude of each pixel.

    # For now, promote the user to recognize it.
    min_value = float(input("What is the value of the lowest bar:").strip())
    max_value = float(input("What is the value of the highest bar:").strip())
    max_pixel = max(secondary_data)
    ratio = (max_value - min_value) / max_pixel

    # Convert secondary_data to data with actual value based on ratio.
    output = []
    for data in secondary_data:
        output.append(round(data * ratio + min_value, 2))
    return output


def export(data: list) -> None:
    """
    Export the data into .csv using Pandas.

    The user is prompted to choose:
      - Whether to export as a row or a column.
      - Whether to create a new file or append to an existing file.
    """
    # Prompt user for how to arrange the data
    export_type = input("Export data as row or column? (r/c): ").strip().lower()
    if export_type not in ('r', 'c'):
        print("Invalid choice; defaulting to column export.")
        export_type = 'c'

    # Prompt user for how to write the file
    mode_choice = input("Create new file or append to existing? (n/a): ").strip().lower()
    if mode_choice not in ('n', 'a'):
        print("Invalid choice; defaulting to creating a new file.")
        mode_choice = 'n'

    # Decide whether to write a header row
    # If appending, we typically skip the header
    write_header = (mode_choice == 'n')

    # Convert the data into a pandas DataFrame
    if export_type == 'r':
        # data as a single row
        df = pd.DataFrame([data])
    else:
        # data as a single column
        df = pd.DataFrame(data, columns=["Value"])

    # Decide the write mode
    if mode_choice == 'n':
        write_mode = 'w'
        csv_filename = "exported_data.csv"
    else:
        write_mode = 'a'
        csv_filename = input("Intended filename to extend:").strip()

    # Write the DataFrame to CSV
    df.to_csv(
        csv_filename,
        mode=write_mode,
        header=write_header,
        index=False
    )

    print(f"Data exported to '{csv_filename}' (mode={write_mode}, header={write_header}).")

if __name__ == "__main__":
    # Load the image
    image_path = load_image()

    # Send the image to Recognizer to process
    recognizer = Recognizer(image_path)
    graph = recognizer.output_graph()
    raw_data = recognizer.output_data()

    print("Bar heights (in pixels):", raw_data)
    cv2.imshow("Graph Preview", graph)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Convert raw_data to actual values
    converted = convert_data(raw_data)
    print("Bar heights (actual):", converted)

    # Export the results
    export(converted)
