"""
Author: Suzanne Combs
Course: CS 3270-X01
This module contains the DataFetching class for converting a file into another format. It
currently converts a CSV file to a pandas dataframe. It prints a summary of the number of
columns and rows in the dataframe and the column names.
See main.py for AI usage disclosure.
"""
import logging
import math
import pandas as pd


logger = logging.getLogger(__name__)


class DataFetcher:
    """
    Class for converting a file to another format.
    Currently can convert a CSV file to a dataframe.
    """

    def __init__(self, file_path: str) -> None:
        """
        Initializes the DataFetcher object

        Parameters:
            file_path (str): Path to the file being converted.
        """
        self.file_path = file_path

    def csv_to_df(self) -> pd.DataFrame:
        """
        Reads in a CSV file and returns a dataframe.

        Returns:
            pd.DataFrame: Dataframe containing the CSV data
        """
        try:
            df = pd.read_csv(self.file_path)
            logger.info("The CSV file (%s) loaded successfully",
                        self.file_path)
            return df
        except FileNotFoundError:
            logger.error("The CSV file (%s) was not found.", self.file_path)
            raise

    def print_summary(self, df: pd.DataFrame) -> None:
        """
        Prints a summary of the columns and row count of the dataframe.

        Parameters:
            pd.DataFrame: Dataframe containing the CSV data
        """
        print(
            f"Dataframe Summary\n"
            f"Columns: {df.shape[1]}\n"
            f"Rows: {df.shape[0]}\n\n"
            f"Column Names:\n{df.columns.tolist()}"
        )

    def __str__(self) -> str:
        """
        Returns a string representation of the DataFetcher object.

        Returns:
            str: String representation of the DataFetcher object.
        """
        return f"DataFetching converts CSV file: {self.file_path} to a dataframe"


class DataCleaner:
    """
    Class for cleaning data in a dataframe.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initializes the DataCleaner object.

        Parameters:
            df (dataframe): Dataframe containing the CSV data
        """
        self.df = df

    def column_checker(self, column_name: str) -> bool:
        """
        Makes sure the column exists in the dataframe.

        Parameters:
            column_name (str): Name of the column being checked.

        Returns:
            bool: True if the column exists in the dataframe, False otherwise.
        """
        if column_name in self.df.columns:
            return True
        logger.warning(
            "The column %s does not exist in the dataframe.", column_name)
        return False

    def data_to_numeric(self, column_name: str):
        """
        Converts data from a column to a numeric value.
        Checks to ensure data can be converted to a numeric value. If not, skips
        and logs a warning.

        Parameters:
            column_name (str): Name of the column being converted.
        """
        if not self.column_checker(column_name):
            return  # Skip if the column does not exist

        for value in self.df[column_name]:
            try:
                num = float(value)  # Convert a value to a float

                if math.isnan(num):  # Check if the value is NaN
                    logger.warning(
                        "The data value %s in column %s is NaN. Skipping the value.",
                        value, column_name)
                    continue  # Skip NaN values
                yield num  # Generator yields the numeric value
            except ValueError:
                logger.warning(
                    "The data value %s in column %s cannot be converted. "
                    "Skipping the value.", value, column_name)


def main() -> None:
    """
    Imports CVS, calls csv_to_df to change to a dataframe.
    Changes the data in a column to numberic values and prints the values. 
    If the file is not found, prints an error message.
    """
    # For testing purposes
    # Import and convert CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    load_data = DataFetcher(csv_path)

    try:
        weather_df = load_data.csv_to_df()
        # Make sure theconversion worked. Print basic info about the dataframe
        load_data.print_summary(weather_df)

        # Data cleaning test to ensure data converted to numeric values.
        data_cleaner = DataCleaner(weather_df)
        values = data_cleaner.data_to_numeric("MaxTemp")
        # print(values) - this prints the generator object location, for the
        # values, need to iterate through
        print(values)
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
