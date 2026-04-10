"""
Author: Suzanne Combs
Course: CS 3270-X01
Data Processing Module
This module contains the DataProcessing class for calculating 
statistics from a specified column in a dataframe.
See main.py for AI usage disclosure.
"""
from dataclasses import dataclass
import pandas as pd
from . import data_fetching as d_fetch


@dataclass
class StatsSummary:
    """Dataclass for storing the statistics of a column in the dataframe."""
    column: str
    mean: float
    median: float
    mode: float
    min: float
    max: float

    def __str__(self) -> str:
        return (f"Statistics Summary for {self.column} Column\n"
                f"Mean: {self.mean}\n"
                f"Median: {self.median}\n"
                f"Mode: {self.mode}\n"
                f"Min: {self.min}\n"
                f"Max: {self.max}")


class DataProcessing:
    """
    Class for processing the data and calculating statistics.

    Parameters: 
        df (dataframe): Dataframe with weather data.
        column (str): Column that the statistics are calculated from. Default is "MaxTemp".

    Returns:
        StatsSummary: A dataclass with the calculated statistics for the specified column.
    """

    def __init__(self, df: pd.DataFrame, column: str = "MaxTemp") -> None:
        self.df = df
        self.column = column

    def get_statistics(self) -> StatsSummary:
        """ Finds and prints basic statistics for the weather dataframe."""
        # Finds the mean, median, mode, min, and max from the MaxTemp column
        df_mean = self.df[self.column].mean()
        df_median = self.df[self.column].median()
        df_mode = self.df[self.column].mode()
        df_max = self.df[self.column].max()
        df_min = self.df[self.column].min()
        # Print the statistics
        return StatsSummary(
            column=self.column,
            mean=round(df_mean, 2),
            median=round(df_median, 2),
            mode=round(df_mode[0], 2),
            min=round(df_min, 2),
            max=round(df_max, 2)
        )

    def __str__(self) -> str:
        return f"DataProcessing calculates the statistics for column {self.column} of the dataframe"

    def print_statistics(self, stats: StatsSummary) -> None:
        """Prints the calculated statistics for the specified column."""
        print(stats)


def main() -> None:
    """
    Imports the CSV and converts to a dataframe using load_data.py. Calls get_statistics
    to print basic statistics of a specified column of the dataframe.
    """
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_data = d_fetch.DataFetching(csv_path)
    weather_df = weather_data.csv_to_df()
    # Can add second argument to change the column from default "MaxTemp"
    data_processor = DataProcessing(weather_df)
    stats = data_processor.get_statistics()
    data_processor.print_statistics(stats)


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
