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

## Author

Suzanne Combs
