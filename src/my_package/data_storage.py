"""
Author: Suzanne Combs
Course: CS 3270-X01
This module contains the DataStorage class for storing weather statistics in a text file.
See main.py for AI usage disclosure.
"""
import logging
from my_package import data_fetching as d_fetch
from my_package import data_processing as d_process

logger = logging.getLogger(__name__)


class DataStorer:
    """
    Class for storing data in a text file.
    """

    def __init__(self, filename: str, stats: d_process.StatsSummary) -> None:
        """
        Initializes the DataStorer object.

        Parameters:
            filename (str): Name of the text file to store the statistics in.
            stats (StatsSummary): Dataclass containing the statistics to be stored.
        """
        self.filename = filename
        self.stats = stats

    def write_txt(self) -> None:
        """
        Create a txt file and write to it.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(str(self.stats))
        logger.info("Statistics written to %s successfully.", self.filename)

    def __str__(self) -> str:
        """
        Returns a string of the DataStorer object.

        Returns:
            str: A string representation of the DataStorer object.
        """
        return f"DataStorage writing to {self.filename} with stats {self.stats}"


def main() -> None:
    """
    Calls write_txt to write to a txt file.   
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
        data_processor = d_process.DataProcessor(cleaned_column, "MaxTemp")
        stats = data_processor.get_statistics()
        data_processor.print_statistics(stats)
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")

    # Calculate and write statistics for the column to a text file
    storage = DataStorer("weather_stats.txt", stats)
    storage.write_txt()


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
