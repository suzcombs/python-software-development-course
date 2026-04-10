"""
Author: Suzanne Combs
Course: CS 3270-X01
The main module for loading weather data, calculating statistics, and 
storing statistics in a text file.

AI Usage Disclosure:
This project used AI tools for assistance. GitHub Copilot was enabled in 
Visual Studio Code, and ChatGPT was used for guidance on design and Python syntax. 
All code was understood, reviewed, modified, and written by me.
"""

import my_package.data_fetching as d_fetch
import my_package.data_processing as d_process
import my_package.data_storage as d_store


def main() -> None:
    """
    Main function for loading data, calculating statistics, and storing statistics.
    """
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_data = d_fetch.DataFetching(csv_path)
    weather_df = weather_data.csv_to_df()

    # Calculate statistics for a specified column
    data_processor = d_process.DataProcessing(weather_df)
    stats = data_processor.get_statistics()

    # Store the statistics in a text file
    storage = d_store.DataStorage("weather_stats.txt", stats)
    storage.write_txt()


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
