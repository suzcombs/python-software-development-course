"""
Author: Suzanne Combs
Course: CS 3270-X01
The main module for loading weather data, calculating statistics, data analysis,
and storing statistics in a text file.

AI Usage Disclosure:
This project used AI tools for assistance. GitHub Copilot was enabled in 
Visual Studio Code, and ChatGPT was used for guidance on design and Python syntax. 
All code was understood, reviewed, and modified by me.
"""

import my_package.data_fetching as d_fetch
import my_package.data_processing as d_process
import my_package.data_analysis as d_analyze
import my_package.data_storage as d_store
from app_logger import setup_logging


def main() -> None:
    """
    Main function for loading data, calculating statistics, and storing statistics.
    """
    setup_logging()  # Set up logging for the application
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    # Initialize the DataFetcher object
    load_data = d_fetch.DataFetcher(csv_path)

    stats = None  # Initialize stats variable

    # Load the data and process it
    try:
        weather_df = load_data.csv_to_df()  # Loads the CSV file into a dataframe

        # Data cleaning convert data to numeric values.
        # Initialize the DataCleaner object
        data_cleaner = d_fetch.DataCleaner(weather_df)
        cleaned_column = data_cleaner.data_to_numeric(
            "MaxTemp")  # Convert the column to numeric values

        # Process the data and get the statistics for the column
        data_processor = d_process.DataProcessor(
            # Make sure the column matches the column name used in data_to_numeric
            cleaned_column, "MaxTemp")  # Initialize the DataProcessor object
        stats = data_processor.get_statistics()  # Calculates statistics for the column
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")

    # Calculate and write statistics for the column to a text file
    if stats is not None:
        try:
            # Initialize the DataStorer object
            storage = d_store.DataStorer("weather_stats.txt", stats)
            storage.write_txt()  # Write the statistics to a text file
        except ValueError as e:  # If there was an error writing to the file, print this message
            print(f"Value error: {e}")

    # Create plots and write to a PDF file
    try:
        data_analyzer = d_analyze.DataAnalyzer(weather_df)
        # Write the plots to a PDF file
        storage.write_pdf(data_analyzer, "weather_plots.pdf")

    except ValueError as e:
        print(
            f"There is no numeric data for the specified column to plot: {e}")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
