"""
Author: Suzanne Combs
Course: CS 3270-X01
Data Processing Module
This module contains the DataProcessing class for calculating 
statistics from a specified column in a dataframe. It also contains a 
dataclass for storing the statistics summary.
See main.py for AI usage disclosure.
"""
import statistics
from dataclasses import dataclass
from my_package import data_fetching as d_fetch


@dataclass
class StatsSummary:
    """
    Dataclass for storing the statistics of a column in the dataframe.
    """
    column: str
    mean: float
    median: float
    min: float
    max: float

    def __str__(self) -> str:
        """
        Returns a string of the statistics summary for the specified column.

        Returns:
            str: String representation of the statistics summary.

        Example:
            >>> stats = StatsSummary(
            ...     column="TestColumn", mean=2.5, median=2.3, min=1.5, max=3.7)
            >>> print(stats)
            Statistics Summary for TestColumn Column
            Mean: 2.5
            Median: 2.3
            Min: 1.5
            Max: 3.7
        """
        return (f"Statistics Summary for {self.column} Column\n"
                f"Mean: {self.mean}\n"
                f"Median: {self.median}\n"
                f"Min: {self.min}\n"
                f"Max: {self.max}")


class DataProcessor:
    """
    Class for processing the data and calculating statistics.
    """

    def __init__(self, numeric_column_gen, column: str = "MaxTemp") -> None:
        """
        Initializes the DataProcessor object.

        Parameters:
            numeric_column_gen: Generator that yields numeric values form specified column
            column (str): Name of the column being processed. The default is "MaxTemp".
        """
        self.numeric_column_gen = numeric_column_gen
        self.column = column

    def get_statistics(self) -> StatsSummary:
        """
        Calculates the mean, median, max, and min for a specified column
        in the dataframe. Returns a dataclass with the statistics for the column.
        The default column is "MaxTemp".

        Returns:
            StatsSummary: A dataclass containing the statistics for the specified column.

        Example:
            >>> data = [1.5, 2.3, 3.7]
            >>> data_processor = DataProcessor(iter(data), "TestColumn")
            >>> stats = data_processor.get_statistics()
            >>> stats.mean
            2.5
            >>> stats.median
            2.3
            >>> stats.min
            1.5
            >>> stats.max
            3.7
        """
        # change the generator into a list to be used.
        # Use of iterator. Gets numeric values from the generator.
        cell_data = []
        for value in self.numeric_column_gen:
            cell_data.append(value)

        # Make sure there are items in the list before calculating statistics
        if not cell_data:
            raise ValueError(
                f"The column {self.column} contains no numeric data.")

        # Finds the mean, median, min, and max from the column
        return StatsSummary(
            column=self.column,
            mean=round(statistics.mean(cell_data), 2),
            median=round(statistics.median(cell_data), 2),
            min=round(min(cell_data), 2),
            max=round(max(cell_data), 2)
        )

    def __str__(self) -> str:
        """
        Returns a string of the DataProcessor object.

        Returns:
            str: String representation of the DataProcessor object.
        """
        return f"DataProcessing calculates the statistics for column {self.column} of the dataframe"

    def print_statistics(self, stats: StatsSummary) -> None:
        """
        Prints the calculated statistics for the specified column.

        Parameters:
            stats (StatsSummary): The statistics summary to print.
        """
        print(stats)


def main() -> None:
    """
    Imports the CSV and converts to a dataframe using load_data.py. Calls get_statistics
    to print basic statistics of a specified column of the dataframe.
    """
    # For testing purposes
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    load_data = d_fetch.DataFetcher(csv_path)

    try:
        weather_df = load_data.csv_to_df()
        # Make sure theconversion worked. Print basic info about the dataframe
        load_data.print_summary(weather_df)

        # Data cleaning test to ensure data converted to numeric values.
        data_cleaner = d_fetch.DataCleaner(weather_df)
        cleaned_column = data_cleaner.data_to_numeric("MaxTemp")

        # Process the data and print the statistics for the column
        data_processor = DataProcessor(cleaned_column, "MaxTemp")
        stats = data_processor.get_statistics()
        data_processor.print_statistics(stats)
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
