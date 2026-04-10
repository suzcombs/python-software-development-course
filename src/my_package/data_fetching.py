"""
Author: Suzanne Combs
Course: CS 3270-X01
This module contains the DataFetching class for converting a file into another format. It 
currently converts a CSV file to a pandas dataframe. It prints a summary of the number of 
columns and rows in the dataframe and the column names.
See main.py for AI usage disclosure.
"""
import pandas as pd


class DataFetching:
    """
    Class for converting a file to another format.
    Currently can convert a CSV file to a dataframe.

    Parameters:
        file_path (str): Path to the file being converted.

    Returns:
        df (dataframe): Dataframe containing the CSV data
        Dataframe summary (str): Dataframe summary with the number of columns and row
    """

    def __init__(self, file_path: str) -> None:
        self.file_path = file_path

    def csv_to_df(self) -> pd.DataFrame:
        """
        Reads in a CSV file and returns a dataframe.

        Parameters:
            file_path (str): Path to the CSV file.

        Returns:
            df (dataframe): Dataframe containing the CSV data
        """
        df = pd.read_csv(self.file_path)
        return df

    def __str__(self) -> str:
        return f"DataFetching converts CSV file: {self.file_path} to a dataframe"

    def print_summary(self) -> None:
        """ Prints a summary of the columns and row count of the dataframe."""
        print(
            f"Dataframe Summary\n"
            f"Columns: {self.csv_to_df().shape[1]}\n"
            f"Rows: {self.csv_to_df().shape[0]}\n\n"
            f"Column Names\n{self.csv_to_df().columns.tolist()}"
        )


def main() -> None:
    """
    Imports the CSV and calls csv_to_df to change to a dataframe. Calls print_weather_info
    to display info about the dataframe.
    """
    # Import and convert CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_data = DataFetching(csv_path)
    # Test to when main to ensure conversion worked. Print basic info about the dataframe
    print(weather_data)
    weather_data.print_summary()


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
