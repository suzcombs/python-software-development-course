"""
Author: Suzanne Combs
Course: CS 3270-X01
Module 2: Loads a csv file and converts to a dataframe using load_data.py.
Calculates and prints basic statistics using a specified column in the dataframe.
I have GitHub Copilot enabled in Visual Studio Code.
"""
from . import load_data as ld


def get_statistics(df, column="MaxTemp"):
    """
    Finds and prints basic statistics for the weather dataframe.

    Parameters: 
        df (dataframe): Dataframe with weather data.
        column (str): Column that the statistics are calculated from. Default is "MaxTemp".
    """
    # Finds the mean, median, mode, min, and max from the MaxTemp column
    df_mean = df[column].mean()
    df_median = df[column].median()
    df_mode = df[column].mode()
    df_max = df[column].max()
    df_min = df[column].min()
    # Print the statistics
    print(f"Mean:{round(df_mean, 2)}")
    print(f"Median:{round(df_median, 2)}")
    print(f"Mode: {round(df_mode[0], 2)}")
    print(f"Min: {round(df_min, 2)}")
    print(f"Max: {round(df_max, 2)}")


def main():
    """
    Imports the CSV and converts to a dataframe using load_data.py. Calls get_statistics
    to print basic statistics of a specified column of the dataframe.
    """
    # Import and save CSV weather data into a dataframe
    csv_path = "australia_weather_data/weather_training_data.csv"
    weather_df = ld.csv_to_df(csv_path)
    # Can add second argument to change the column from default "MaxTemp"
    get_statistics(weather_df)


if __name__ == '__main__':
    # Runs the main function when this file is executed
    main()
