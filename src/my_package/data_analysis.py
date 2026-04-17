"""
Author: Suzanne Combs
Course: CS 3270-X01
This module analyzes the weather data by using functional programming and visualizing the data.
See main.py for AI usage disclosure.
"""
import matplotlib.pyplot as plt
import pandas as pd
from my_package import data_fetching as d_fetch


class DataAnalyzer:
    """
    This module is responsible for analyzing the weather data.
    It includes functions for filtering and visualizing the data.
    """

    def __init__(self, df: pd.DataFrame) -> None:
        """
        Initializes the DataAnalyzer object.

        Parameters:
            df (pd.DataFrame): The dataframe containing the weather data.
        """
        self.df = df

    def group_by_location(self, column: str) -> pd.DataFrame:
        """
        Groups the data by location and calculates the mean of a numeric column for each locaiton.

        Parameters:
            column (str): The name of the numeric column to calculate the mean for.

        Returns:
            pd.DataFrame: A dataframe with the mean of the specified column for each location.
        """
        # numeric_column = self.cleaner.data_to_numeric(column)
        # self.df[column] = numeric_column
        if pd.to_numeric(self.df[column], errors='coerce').dropna().empty:
            raise ValueError(
                f"There is no numeric data to plot for column {column}")
        return self.df.groupby("Location")[
            column].mean().round(2).reset_index()

    def filter_rain_tomorrow(self) -> pd.DataFrame:
        """
        Filters the dataframe to include only rows where RainTomorrow is Yes. Could be used to 
        analyze the data for only rows where it is expected to rain tomorrow.

        Returns:
            pd.DataFrame: A dataframe containing only rows where RainTomorrow is Yes.
        """
        return self.df[self.df["RainTomorrow"] == 1]

    def rain_today_rain_likelihood(self) -> list:
        """
        Creates a list of tuples containing the values of RainToday and RainTomorrow for 
        each row of the dataframe.
        """
        rainfall_today_tomorrow_pairs = zip(
            self.df["RainToday"], self.df["RainTomorrow"])
        # Filter for only rows where RainTomorrow is Yes
        return list(
            filter(lambda x: x[1] == 1, rainfall_today_tomorrow_pairs))

    def hot_day_rain_likelihood(self) -> list:
        """
        Creates a list of tuples containing the values for MaxTemp as "Hot"
        or "Not Hot" and chance of RainTomorrow for each row of the dataframe.
        """
        temp_rain_tomorrow_pairs = zip(
            self.df["MaxTemp"], self.df["RainTomorrow"])
        # Map hot days from not hot days based on the MaxTemp value
        valid_pairs = filter(lambda x: pd.notna(
            x[0]) and pd.notna(x[1]), temp_rain_tomorrow_pairs)
        return list(
            map(lambda x: (x[0], "Hot" if x[0] > 30 else "Not Hot", x[1]), valid_pairs))

    def histogram_rainfall(self):
        """
        Creates a histogram of rainfall today for rows where RainTomorrow is Yes.
        """
        rainfall_pairs = self.rain_today_rain_likelihood()
        # Get the RainToday values for rows where RainTomorrow is Yes
        rainfall_values = [x[0] for x in rainfall_pairs if pd.notna(x[0])]

        fig, ax = plt.subplots()
        ax.hist(rainfall_values, bins=2, edgecolor='black', color='purple')
        ax.set_title(
            'Histogram of Rainfall Today for Rows Where Rain Tomorrow is Yes')
        ax.set_xlabel('Rainfall Today')
        ax.set_ylabel('Frequency')
        fig.tight_layout()
        return fig

    def create_histogram(self, column: str):
        """
        Creates a histogram for the specified column in the dataframe.

        Parameters:
            column (str): The name of the column to create a histogram for.
        """
        values = pd.to_numeric(
            self.df[column], errors='coerce').dropna().tolist()

        if not values:
            raise ValueError(
                f"There is no numeric data to plot for column {column}")

        fig, ax = plt.subplots()
        ax.hist(values, bins=20, edgecolor='black', color='teal')
        ax.set_title(f'Histogram of {column}')
        ax.set_xlabel(column)
        ax.set_ylabel('Frequency')
        fig.tight_layout()
        return fig

    def create_boxplot(self, column: str):
        """
        Creates a boxplot for the specified column in the dataframe.

        Parameters:
            column (str): The name of the column to create a boxplot for.
        """
        values = pd.to_numeric(
            self.df[column], errors='coerce').dropna().tolist()

        if not values:
            raise ValueError(
                f"There is no numeric data to plot for column {column}")

        fig, ax = plt.subplots()
        ax.boxplot(values, vert=False, patch_artist=True,
                   boxprops=dict(facecolor='steelblue'))
        ax.set_title(f'Boxplot of {column}')
        ax.set_xlabel(column)
        fig.tight_layout()
        return fig

    def create_barchart_by_location(self, column: str):
        """
        Creates a barchart by location for a specified column in the dataframe. 

        Parameters:
            column (str): The name of the column to create a bar chart for.
        """
        # Convert the specified column to numeric values and check if numeric data
        if pd.to_numeric(self.df[column], errors='coerce').dropna().empty:
            raise ValueError(
                f"There is no numeric data to plot for column {column}")

        group_data = self.group_by_location(column)
        # Sort the data by the column
        group_data = group_data.sort_values(by=column, ascending=False)

        fig, ax = plt.subplots()
        ax.bar(group_data["Location"], group_data[column],
               color='grey')
        ax.set_title(f"Bar Chart of {column} by Location")
        ax.set_xlabel("Location")
        ax.set_ylabel(column)
        ax.tick_params(axis="x", rotation=90, labelsize=8)
        fig.tight_layout()
        return fig

    def heat_rain_likelihood_barchart(self):
        """
        Creates a bar chart showing the likelihood of rain tomorrow based on 
        whether it is a hot day or not.
        """
        hot_day_data = self.hot_day_rain_likelihood()

        if not hot_day_data:
            raise ValueError(
                "There is no data to plot for the likelihood of rain tomorrow based on hot day.")

        # Find the total of hot days and not hot days
        hot_total = sum(1 for x in hot_day_data if x[1] == "Hot")
        not_hot_total = sum(1 for x in hot_day_data if x[1] == "Not Hot")

        # Find the total of rainy hot days and rainy not hot days
        hot_rain = sum(1 for x in hot_day_data if x[1] == "Hot" and x[2] == 1)
        not_hot_rain = sum(
            1 for x in hot_day_data if x[1] == "Not Hot" and x[2] == 1)

        # Find the percent of hot rainy days and not hot rainy days
        if hot_total > 0:
            hot_rain_percent = round((hot_rain / hot_total) * 100, 2)
        else:
            hot_rain_percent = 0
        if not_hot_total > 0:
            not_hot_rain_percent = round(
                (not_hot_rain / not_hot_total) * 100, 2)
        else:
            not_hot_rain_percent = 0

        categories = ['Hot Days', 'Not Hot Days']

        # Make the bar chart with the percent of rainy days for hot and not hot days
        fig, ax = plt.subplots()
        ax.bar(categories, [hot_rain_percent, not_hot_rain_percent], color=[
            "navy", "orange"])
        ax.set_title("Likelihood of Rain Tomorrow Based on Hot Day")
        ax.set_ylabel("Percentage of Rainy Days")
        ax.set_ylim(0, 100)
        fig.tight_layout()
        return fig


def main() -> None:
    """
    Imports the CSV and converts to a dataframe using load_data.py. Calls get_statistics
    to print basic statistics of a specified column of the dataframe.
    """
    # For testing purposes - Note: When I run this file, it prints any logs to the console.
    # The main.py file logs to a file.
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    load_data = d_fetch.DataFetcher(csv_path)

    try:
        weather_df = load_data.csv_to_df()
        # Make sure theconversion worked. Print basic info about the dataframe
        load_data.print_summary(weather_df)

        # Create a histogram for the specified column
        data_analyzer = DataAnalyzer(weather_df)
        data_analyzer.create_histogram("MaxTemp")
        data_analyzer.create_boxplot("MaxTemp")

        # group data together to see the mean for each location with a specified column
        group_data = data_analyzer.group_by_location("MaxTemp")
        print(group_data.to_string(index=False))
        data_analyzer.create_barchart_by_location("MaxTemp")

        # Make a histogram of rainfall today for rows where RainTomorrow is Yes
        data_analyzer.histogram_rainfall()

        # Make a bar chart showing the likelihood of rain tomorrow based on how hot the day is
        data_analyzer.heat_rain_likelihood_barchart()

    except FileNotFoundError:
        print("The file was not found. Please check the file path.")
    except ValueError as e:
        print(f"Value error: {e}")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
