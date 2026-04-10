"""
Author: Suzanne Combs
Course: CS 3270-X01
This module contains the DataStorage class for storing weather statistics in a text file.
See main.py for AI usage disclosure.
"""
from . import data_fetching as d_fetch
from . import data_processing as d_process


class DataStorage:
    """Class for storing data in a text file.

    Parameters: 
        filename (str): Name of the txt file being written to. 
        stats (dict): Dictionary containing the statistics being written to the text file.
    """

    def __init__(self, filename: str, stats: d_process.StatsSummary) -> None:
        self.filename = filename
        self.stats = stats

    def write_txt(self) -> None:
        """Create a txt file and write to it."""
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(str(self.stats))

    def __str__(self) -> str:
        return f"DataStorage writing to {self.filename} with stats {self.stats}"


def main() -> None:
    """
    Calls write_txt to write to a txt file.   
    """
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_data = d_fetch.DataFetching(csv_path)
    weather_df = weather_data.csv_to_df()

    # Calculate and write statistics for the column to a text file
    data_processor = d_process.DataProcessing(weather_df)
    stats = data_processor.get_statistics()
    storage = DataStorage("weather_stats.txt", stats)
    storage.write_txt()


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
