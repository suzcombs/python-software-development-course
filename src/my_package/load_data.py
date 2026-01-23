"""
Author: Suzanne Combs
Course: CS 3270-X01
Module 1: Loads a weather dataset and creates a dataframe using pandas. 
Performs funtions on the dataframe to display basic information about the dataset.
I have GitHub Copilot enabled in Visual Studio Code.
"""
import pandas as pd


def csv_to_df(file_path):
    """
    Reads in a CSV file and returns a dataframe.

    Parameters:
        file_path (str): Path to the CSV file.
    Returns:
        df (dataframe): Dataframe containing the CSV data 
    """
    df = pd.read_csv(file_path)
    return df


def print_weather_info(df):
    """
    Prints basic information about the weather dataframe.

    Parameters:
        df (dataframe): Dataframe containing weather data.
    """
    print(df.head())  # First 5 rows
    print(df.describe())  # Summarizes statistics of the weather data
    print(df.columns)  # Lists all column names


def main():
    """
    Imports the CSV and calls csv_to_df to change to a dataframe. Calls print_weather_info
    to display info about the dataframe.
    """
    # Import and convert CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_df = csv_to_df(csv_path)
    # Test to make sure the conversion worked by printing basic info about the dataframe
    print_weather_info(weather_df)


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
