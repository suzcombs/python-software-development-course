"""
Author: Suzanne Combs
Course: CS 3270-X01
This module contains the DataStorage class for storing weather statistics in a text file.
See main.py for AI usage disclosure.
"""
import asyncio
import logging
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib import pyplot as plt
from my_package import data_fetching as d_fetch
from my_package import data_processing as d_process
from my_package import data_analysis as d_analyze

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

    def write_txt_file(self) -> None:
        """
        Helper function that creates and writes to a text file.
        """
        with open(self.filename, 'w', encoding='utf-8') as file:
            file.write(str(self.stats))
        logger.info("Statistics written to %s successfully.", self.filename)

    def write_txt(self) -> None:
        """
        Sequentially create txt file and write to it.
        """
        self.write_txt_file()

    async def write_txt_async(self) -> None:
        """
        Asynchronously create txt file and write to it.
        """
        loop = asyncio.get_event_loop()

        await loop.run_in_executor(None, self.write_txt_file)
        logger.info("Statistics written to %s successfully.",
                    self.filename)

    def write_pdf(self, analyzer, pdf_filename: str, column_name: str) -> None:
        """
        Create a PDF file and write the plots to it.

        Parameters:
            plots (list): A list of matplotlib plot objects to be written to the PDF file.
        """
        with PdfPages(pdf_filename) as pdf:
            figures = [
                analyzer.create_histogram(column_name),
                analyzer.create_boxplot(column_name),
                analyzer.create_barchart_by_location("Rainfall"),
                analyzer.histogram_rainfall(),
                analyzer.heat_rain_likelihood_barchart()
            ]
            for fig in figures:
                pdf.savefig(fig)
                plt.close(fig)
        logger.info("Plots written to weather_plots.pdf successfully.")

    def __str__(self) -> str:
        """
        Returns a string of the DataStorer object.

        Returns:
            str: A string representation of the DataStorer object.
        """
        return f"DataStorage writing to {self.filename} with stats {self.stats}"


async def main() -> None:
    """
    Calls write_txt to write to a txt file.   
    """
    # For testing purposes - Note: When I run this file, it prints any logs to the console.
    # The main.py file logs to a file.
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
        # Calculates statistics for the column
        stats = data_processor.get_statistics_multiprocessing()
    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")

    # Calculate and write statistics for the column to a text file
    if stats is not None:
        try:
            # Initialize the DataStorer object
            storage = DataStorer("output/weather_stats.txt", stats)
            # Write the statistics to a text file asynchronously
            await storage.write_txt_async()
        except ValueError as e:  # If there was an error writing to the file, print this message
            print(f"Value error: {e}")

    # Create plots and write to a PDF file
    try:
        data_analyzer = d_analyze.DataAnalyzer(weather_df)
        # Write the plots to a PDF file
        storage.write_pdf(data_analyzer, "output/weather_plots.pdf", "MaxTemp")

    except ValueError as e:
        print(
            f"There is no numeric data for the specified column to plot: {e}")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    asyncio.run(main())
