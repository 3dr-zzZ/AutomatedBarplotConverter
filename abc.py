"""
AutomatedBarplotConverter (ABC)

Author: 3dr-zzZ

=== Module Description ===

"""

import cv2, os
import pandas as pd
import numpy as np
from pandas.core.interchange.dataframe_protocol import DataFrame

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


def date_calculator(df: pd.DataFrame) -> pd.DataFrame:
    """Add a date feature to the DataFrame by creating a new 'Date' column.

    Prompts the user for the start and end date, and generates an evenly spaced date range
    corresponding to the number of rows in the DataFrame.
    """
    start_date = input("Start date of the data (YYYY-MM-DD): ").strip()
    end_date = input("End date of the data (YYYY-MM-DD): ").strip()
    n = len(df)

    # Generate the date range with evenly spaced intervals
    date_range = pd.date_range(start=start_date, end=end_date, periods=n)

    # Add the date column to the DataFrame
    df['Date'] = date_range.strftime('%Y-%m-%d')

    print("DataFrame with date feature added:")
    print(df.head())

    return df


def export(data) -> None:
    """
    Export the data into a CSV file using Pandas, including the date feature.

    The user is prompted to choose whether to create a new file or append to an existing file.
    If data is provided as a list, it will be converted to a DataFrame with a single column 'Value'.
    A date feature will be added to the DataFrame using date_calculator.
    """
    df = pd.DataFrame(data, columns=["Value"])

    # Add the date feature to the DataFrame
    df = date_calculator(df)

    csv_filename = "exported_data.csv"
    write_mode = 'w'
    write_header = True

    df.to_csv(csv_filename, mode=write_mode, header=write_header, index=False)

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
