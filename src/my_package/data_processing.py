"""
Author: Suzanne Combs
Course: CS 3270-X01
This module contains the DataProcessing class for calculating 
statistics from a specified column in a dataframe. It also contains a 
dataclass for storing the statistics summary.
See main.py for AI usage disclosure.
"""
import statistics
import concurrent.futures
import asyncio
from dataclasses import dataclass
from my_package import data_fetching as d_fetch


def calc_mean(data: list) -> float:
    """
    Calculates the mean of a list of numeric values.

    Parameters:
        data (list): A list of numeric values.

    Returns:
        float: The mean of the list of numeric values.

    Example:
        >>> calc_mean([1.5, 2.3, 3.7])
        2.5
    """
    return round(statistics.mean(data), 2)


def calc_median(data: list) -> float:
    """
    Calculates the median of a list of numeric values.

    Parameters:
        data (list): A list of numeric values.

    Returns:
        float: The median of the list of numeric values.

    Example:
        >>> calc_median([1.5, 2.3, 3.7])
        2.3
    """
    return round(statistics.median(data), 2)


def calc_min(data: list) -> float:
    """
    Calculates the minimum value of a list of numeric values.

    Parameters:
        data (list): A list of numeric values.

    Returns:
        float: The minimum value of the list of numeric values.

    Example:
        >>> calc_min([1.5, 2.3, 3.7])
        1.5
    """
    return round(min(data), 2)


def calc_max(data: list) -> float:
    """
    Calculates the maximum value of a list of numeric values.

    Parameters:
        data (list): A list of numeric values.

    Returns:
        float: The maximum value of the list of numeric values.

    Example:
        >>> calc_max([1.5, 2.3, 3.7])
        3.7
    """
    return round(max(data), 2)


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

    def gen_to_list(self) -> list:
        """
        Converts the generator of numeric values into a list.

        Returns:
            list: A list of numeric values from the generator.
        """
        return list(self.numeric_column_gen)

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
        cell_data = self.gen_to_list()

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

    def get_statistics_multiprocessing(self) -> StatsSummary:
        """
        Calculates the mean, median, max, and min for a specified column
        in the dataframe using multiprocessing. Returns a dataclass with the 
        statistics for the column. The default column is "MaxTemp".

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
        cell_data = self.gen_to_list()

        # Make sure there are items in the list before calculating statistics
        if not cell_data:
            raise ValueError(
                f"The column {self.column} contains no numeric data.")

        with concurrent.futures.ThreadPoolExecutor() as executor:
            mean_future = executor.submit(calc_mean, cell_data)
            median_future = executor.submit(calc_median, cell_data)
            min_future = executor.submit(calc_min, cell_data)
            max_future = executor.submit(calc_max, cell_data)

            # Get the results from the futures
            return StatsSummary(
                column=self.column,
                mean=round(mean_future.result(), 2),
                median=round(median_future.result(), 2),
                min=round(min_future.result(), 2),
                max=round(max_future.result(), 2)
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


async def main() -> None:
    """
    Imports the CSV and converts to a dataframe using load_data.py. Calls get_statistics
    to print basic statistics of a specified column of the dataframe.
    """
    # For testing purposes - Note: When I run this file, it prints any logs
    # to the console. The main.py file logs to a file.
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    load_data = d_fetch.DataFetcher(csv_path)

    try:
        weather_df = await load_data.csv_to_df_async()
        # Make sure theconversion worked. Print basic info about the dataframe
        load_data.print_summary(weather_df)

        # Data cleaning test to ensure data converted to numeric values.
        data_cleaner = d_fetch.DataCleaner(weather_df)
        cleaned_column = data_cleaner.data_to_numeric("MaxTemp")

        # Process the data and print the statistics for the column sequentially
        data_processor = DataProcessor(cleaned_column, "MaxTemp")
        data_processor.get_statistics_multiprocessing()
        # data_processor.print_statistics(stats)

    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    asyncio.run(main())
