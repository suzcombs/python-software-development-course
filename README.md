# Project: Weather Data Analysis and Visualization Tool

## Overview

This is a course long project that analyzes and visualizes weather data. It is broken up into different modules.

## Installation

- pandas to transform a csv file into a dataframe
- matplotlib for data visualization
- Flask and Flask SQL alchemy for the web application
- scikit-learn for machine learning modeling

For all installation essentials, see requirements.txt

To install my_package through by typing in the terminal

```python
python3 -m pip install --index-url https://test.pypi.org/simple/ --no-deps weather-load-stats-suzannecombs
```

Note: this package has been changed through the different modules. At the final module, I will add the changes to test.pypi.org

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

## Module 6 - Functional Programming Paradigm

This module added data analysis through functional programming and visualization. A new module data_analysis.py was added to the project and contains the DataAnalyzer class. This class has methods which use functional features such as zip, map, groupby, lambda, and filter. They were used to see patterns and trends in the data. There are also methods that create graphs of the data.

Functional Features:

- The group_by_location method uses groupby to group the data by location and calculate the mean of a numeric column for each location
- The filter_rain_tomorrow method filters for only the rows that were prected to rain tomorrow
- The rain_today_rain_likelihood method uses zip to bring together the columns "RainToday" "RainTomorrow" for comparison into a tuple. Filter and lambda were used to return a list of the rows where the prediction was it would rain tomorrow
- The hot_day_rain_likelihood method uses zip to bring together the columns "MaxTemp" and "RainTomorrow" for comparision into a tuple. It uses the map function with a lambda to categorize the data into hot days or not hot days depending on the temperature. From this we can see the likeliness of rain tomorrow based on the temperature.

Charts Created:

- Charts for a basic histogram or a boxplot to quickly visualize the numeric data in a column. This can be useful for seeing the distribution of data for the column.
- Barchart that has each location grouped together for the x axis and the y axis is a specified numerical column. This graph can show the correlation between data such as temperature or wind speed mean by each location for comparison.
- Histogram of the likelihood of rain tomorrow based on whether it is raining today.
- Barchart of the likelihood of rain tomorrow based on whether it was a hot or not as hot day today.

Test Cases Automated:

- A pytest.fixture was created for sample data for these tests. There were 4 pytests added
- test_group_by_location: Created to test that the data frame was grouped by location and calculated the mean for each group for the specified column
- test_filter_rain_tomorrow: Tests that the method filters only rows where it is predicted to rain tomorrow and creates a data frame
- test_rain_today_rain_likelihood: Tests the method to make sure a list of tuples containing RainToday and RainTomorrow columns are created and that it filters only for the days that RainTomorrow is Yes.
- test_hot_day_rain_likelihood: Tests the method to make sure a list of tuples containing MaxTemp and RainTomorrow columns are created and checks that the MaxTemp column is mapped to "Hot" or "Not Hot"
- The visualizations were checked by visual inspection.

## Module 7 - Multiprocessing and Aysnchronous Programming

This module introduces asynchronous programming and multiprocessing to the project.

Asynchronous programming was implemented for data fetching in csv_to_df_async() and was also implemented in write_txt_async(). This makes these methods non-blocking and allows other tasks to process instead of waiting. Both of these are I/O-bound tasks and async using the asyncio built-in module was utilized.

Parallelism was implemented using multiprocessing in get_statistics_multiprocessing() using ProcessPoolExecutor to parallelize the CPU-bound statistical calculations. This allows computations such as mean, median, min, and max to be executed concurrently across different cores and allow for more efficiency.

The non-asynchronous and multiprocessing methods were kept in the code for comparison. A timer was used to compare the different tasks and was removed. The results were included in the screenshots for this module. The speed of the processes were slightly quicker with asynchronous and multiprocessing, but not by much. This is likely because of the scale of the project and with more files being converted to a dataframe, write txt files, and statistics calculations the difference in speed would increase.

Testing Cases:
There were Pytests created for each of these methods. these Pytests included the same input and the same results were expected:

- csv_to_df_async: a test to ensure it correctly loads, and another test to make sure empty files are handled correclty
- write_txt_async: a test to ensure the txt file was created
- get_statistics_multiprocessing: tests were created for when there is valid data, invalid data, and no data.

Doctests for csv_to_df_async() and get_statistics_multiprocessing() were also created.

## Module 9 - Web Development

To run this web application, Flask and Flask SQLalchemy need to be installed. See requirements.txt for all necessary installations. To establish the connection type python app.py into the terminal.

In this module, a 3-tier web application was created using Flask with jinja, HTML, and Python. The 3 tiers were: user interface where the user can interact with the weather data, Flask was used for the application server/business logic, and SQL alchemy was used to create a SQLite database. The web application utilized some of the code written in previous modules.

The website allows a user to select a location and a column from the Australia weather dataset. If the user does not select a location or column, then they are redirected to the error page stating that there was an error and whether it was due to a missing location or column. Once the user has selected a valid location and column, they are directed to the dashboard. The dashboard includes information about the location and column selected, statistics for that column, and a histogram of the column and location. On this dashboard are options to go back to the home page or to view query history. The application stores the query history in a weather database using SQLite. The history page shows a list of all the queries including the location selected, column selected, and time it occurred. This history page also includes an option to go back to the home page.

Testing cases:

- Manual test selecting no location. This lead to the error page stating missing location
- Manual test selecting no column. This lead to the error page stating missing column
- Visual inspection that the dashboard and history pages loaded with correct information
- Pytests were created to make sure the index, dashboard, and history pages loaded get a status code 200. For the dashboard an additional test was created to make sure the status code was 405.
- For the Pytests to work correctly to import app.py, a pytest.ini was created and put in the root folder.

## Module 10 - Machine Learning

This model introduced machine learning into the project. A new module ml_model.py was created to keep the machine learning code together. In it are 2 functions: train_model() and predict_rain_tomorrow(). In train_model(), it reads in a csv file and selects columns for input and a column for the outcome. I selected the columns MinTemp, MaxTemp, WindGustSpeed, Humidity9am, Humidity3pm, Pressure9am, Pressure3pm for input. For the outcome column, I selected RainTomorrow. These columns were put together into a dataframe and then split into 4 groups. X train, X test, y train, y test. The percent that was put into the test groups was 20% and the percent in the training group was 80%. The higher percent for the training group is so there are more data points the model can learn from.

Using scikit-learn, I tried a couple different models and made some modifications to the arguments. The models I tried were:

- DecisionTreeClassifier
- LogisticRegression
- RandomForestClassifier

The model that had the highest accuracy was RandomForestClassifier. This model along with the 7 columns stated above had an accuracy of about 84.50%. The train_model function returns the model and the accuracy score. The predict_rain_tomorrow function calls train_model() and gives a prediction based on the model on whether it is likely to rain tomorrow or not.

The model was integrated into the web application. On the dashboard, it states the prediction of whether it is likely to rain tomorrow or not and give the model accuracy percentage.

Test cases:

- test_train_model_return: tests a model is made and a score is returned with a value between 0 and 1 (for a percentage)
- test_predict_rain_tomorrow: tests a prediction is made and a score between 0 and 1 is returned (for a percentage)

## Author

Suzanne Combs
