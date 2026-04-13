# Project: Weather Data Analysis and Visualization Tool

## Overview

This is a course long project that analyzes and visualizes weather data. It is broken up into different modules.

## Installation

Use pandas to transform a csv file into a dataframe

```python
import pandas as pd
```

To install the load_data and weather_statistics package

```python
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps weather-load-stats-suzannecombs
```

## Usage

- Load weather data from a CVS file
- Convert to a dataframe using pandas.
- Compute and print statistics for a column of the dataframe

## Module 1 - Optimal Python Development Lifecycle

In this module, a professional-style development environment was set up using Visual Studio Code and GitHub. A public domain csv file containing a dataset of Australia weather was downloaded from kaggle.com. Pandas was used to create a dataframe from this file and basic information about this data was printed in the terminal. Docstrings and comments were added for documentation.

## Module 2 - Modularization

A statistics module was created for performing mean, median, mode, min, and max on different columns of the dataframe. A package was created containing load_data.py and weather_statistics.py. main.py was also created to import the package modules.

## Module 3 - Object Oriented Programming

This module refactored the previous application using object oriented programming. The code was split into four modules: main.py, data_fetching.py, data_processing.py, and data_storage.py. Each module has a specific task. main.py orchestrates the application, data_fetching.py has a DataFetching class that currently converts a CSV to a dataframe, data_processing.py has a class DataProcessing which calculates the statistics of the dataframe, and DataStorage currently saves the statistics to a text file. These modules and classes can be expanded on to include different data or storage types for the future. A dataclass was created for the calculated statistics for a cleaner way to store the data. Finally, type hints were added to the code for better readability and clearer expectations.

## Module 4 - Libraries for Advanced Programming

This module introduced generators and iterators to the project. A new class DataCleaning was created in the data_fetching.py module. A generator was made which converts values in a column to a numeric if it is a valid type. This generator can be used for calculating the statistics for the column in the data_processing.py module with the method get_statistics. In the get_statistics method, there is an iterator which creates a list of the generator to be used for calculating statistics.

There was also file/error handling and logging added to the project in this module. There is a check to make sure a file can be loaded. If it can be loaded, an info log saying it was successful is sent to app.log, otherwise an error log is sent. There is also a check that a column exists in a dataframe and that it is a numerical value before any statistics are performed on it. If there are any values that cannot be changes to a numeric, then it is skipped and there is a warning sent to app.log.

## Module 5 - Automated Testing

This module introduced automated testing using both pytest and doctest. A new module test_app.py was created which contains the pytests. There were tests created for the methods csv_to_df, column_checker, data_to_numeric, get_statistics, and write_txt.
Doctests were created for the csv_to_df, data_to_numeric, and get_statistics methods.
The pytests for csv_to_df tested for a correct file path and an incorrect file path. The pytests for column_checker tested an existing column and a nonexistent column. The pytests for data_to_numeric tested a data frame with valid data, a data frame with some valid data, and a data frame with no valid data. The pytests for get_statistics tested for valid data and invalid data.
Finally the pytest for write_txt tested that the method would create a file with the correct content.

## Author

Suzanne Combs
