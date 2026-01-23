"""
Author: Suzanne Combs
Course: CS 3270-X01
Main module for loading the weather data and calculating statistics.
"""
import my_package.load_data as ld
import my_package.weather_statistics as ws


def main():
    """
    Main function for loading data and calculating statistics.
    """
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_df = ld.csv_to_df(csv_path)
    # Calculate and print statistics for the MaxTemp column
    ws.get_statistics(weather_df, column="MaxTemp")


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
