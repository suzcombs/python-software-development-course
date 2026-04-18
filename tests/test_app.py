"""
This module contains pytests for the project. 
It tests the functionality of data fetching, data processing, 
and data storage for the application.
"""
import asyncio
import pytest
import pandas as pd
import my_package.data_fetching as d_fetch
import my_package.data_processing as d_process
import my_package.data_storage as d_store
import my_package.data_analysis as d_analysis


# Test cases for csv_to_df method in DataFetcher class (data_fetching.py)
def test_csv_to_df_correctly_loads():
    """
    Test that the CSV file loads correctly and returns a DataFrame.
    """
    data_fetcher = d_fetch.DataFetcher(
        "australia_weather_data/weather_training_data.csv")
    df = data_fetcher.csv_to_df()
    assert df is not None
    assert not df.empty


def test_csv_to_df_empty_file():
    """
    Test an empty CSV file to make sure the DataFetcher class can catch without crashing.
    """
    data_fetcher = d_fetch.DataFetcher("")
    with pytest.raises(FileNotFoundError):
        data_fetcher.csv_to_df()


# Test cases for csv_to_df_async method in DataFetcher class (data_fetching.py)
def test_csv_to_df_async_correctly_loads():
    """
    Test that the CSV file loads correctly and returns a DataFrame asynchronously.
    """
    data_fetcher = d_fetch.DataFetcher(
        "australia_weather_data/weather_training_data.csv")
    df = asyncio.run(data_fetcher.csv_to_df_async())
    assert df is not None
    assert not df.empty


def test_csv_to_df_async_empty_file():
    """
    Test an empty CSV file to make sure the DataFetcher class can catch 
    without crashing asynchronously.
    """
    data_fetcher = d_fetch.DataFetcher("")
    with pytest.raises(FileNotFoundError):
        asyncio.run(data_fetcher.csv_to_df_async())


# Test cases for column_checker method in DataCleaner class (data_fetching.py)
def test_column_checker_existing_column():
    """
    Test the column_checker method with an existing column name to make sure it returns True
    """
    data_fetcher = d_fetch.DataFetcher(
        "australia_weather_data/weather_training_data.csv")
    df = data_fetcher.csv_to_df()
    data_cleaner = d_fetch.DataCleaner(df)
    assert data_cleaner.column_checker("Location") is True


def test_column_checker_nonexistent_column():
    """
    Test the column_checker method with a column that does not exists that it returns False
    """
    data_fetcher = d_fetch.DataFetcher(
        "australia_weather_data/weather_training_data.csv")
    df = data_fetcher.csv_to_df()
    data_cleaner = d_fetch.DataCleaner(df)
    assert data_cleaner.column_checker("ThisColumnDoesNotExist") is False


# Test cases for data_to_numeric method in DataCleaner class (data_fetching.py)
def test_data_to_numeric_valid_data():
    """
    Test the data_to_numeric method with valid numeric data to make sure it converts correctly.
    """
    df = pd.DataFrame({
        "NumberColumn": ["1.5", "2.3", "3.7"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    # Convert to list to see if the generator yielded correct numeric values
    values = list(data_cleaner.data_to_numeric("NumberColumn"))
    assert values == [1.5, 2.3, 3.7]


def test_data_to_numeric_some_invalid_data():
    """
    Test the data_to_numeric method with some invalid data. 
    Skips invalid data and only converts valid numeric data.
    """
    df = pd.DataFrame({
        "NumberColumn": ["Squirrel", "2.3", "Fox", "NaN", "5.6", "Burger"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    # Convert to list to see if the generator yielded correct numeric values
    values = list(data_cleaner.data_to_numeric("NumberColumn"))
    assert values == [2.3, 5.6]


def test_data_to_numeric_all_invalid_data():
    """
    Test the data_to_numeric method with all invalid data. 
    Skips all values and returns an empty list.
    """
    df = pd.DataFrame({
        "NumberColumn": ["Squirrel", "Fox", "NaN", "Burger"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    # Convert to list to see if the generator skipped all invalid data and returned an empty list
    values = list(data_cleaner.data_to_numeric("NumberColumn"))
    # Makes sure the list is empty. All values should be skipped.
    assert not values


# Test cases for get_statistics method in DataProcessor class (data_processing.py)
def test_get_statistics_valid_data():
    """
    Test the get_statistics method with valid numerical data 
    to make sure it calculates the statistics correctly.
    """
    df = pd.DataFrame({
        "NumberColumn": ["1.5", "2.3", "3.7"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    numeric_column_gen = data_cleaner.data_to_numeric("NumberColumn")
    data_processor = d_process.DataProcessor(
        numeric_column_gen, "NumberColumn")
    stats = data_processor.get_statistics()
    assert stats.mean == 2.5
    assert stats.median == 2.3
    assert stats.min == 1.5
    assert stats.max == 3.7


def test_get_statistics_invalid_data():
    """
    Test the get_statisics method with invalid data. 
    Make sure the value error is raised.
    """
    df = pd.DataFrame({
        # If I have any valid, it would not bring up the error
        "NumberColumn": ["Squirrel", "Fox", "NaN", "Burger"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    numeric_column_gen = data_cleaner.data_to_numeric("NumberColumn")
    data_processor = d_process.DataProcessor(
        numeric_column_gen, "NumberColumn")
    with pytest.raises(ValueError):
        data_processor.get_statistics()


def test_get_statistics_no_data():
    """
    Test the get_statistics method with an empty column. 
    Make sure the value error is raised.
    """
    df = pd.DataFrame({
        "NumberColumn": []
    })
    data_cleaner = d_fetch.DataCleaner(df)
    numeric_column_gen = data_cleaner.data_to_numeric("NumberColumn")
    data_processor = d_process.DataProcessor(
        numeric_column_gen, "NumberColumn")
    with pytest.raises(ValueError):
        data_processor.get_statistics()


# Test cases for get_statistics_multiprocessing method in DataProcessor class (data_processing.py)
def test_get_statistics_multiprocessing_valid_data():
    """
    Test the get_statistics_multiprocessing method with valid numerical data 
    to make sure it calculates the statistics correctly using multiprocessing.
    """
    df = pd.DataFrame({
        "NumberColumn": ["1.5", "2.3", "3.7"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    numeric_column_gen = data_cleaner.data_to_numeric("NumberColumn")
    data_processor = d_process.DataProcessor(
        numeric_column_gen, "NumberColumn")
    stats = data_processor.get_statistics_multiprocessing()
    assert stats.mean == 2.5
    assert stats.median == 2.3
    assert stats.min == 1.5
    assert stats.max == 3.7


def test_get_statistics_multiprocessing_invalid_data():
    """
    Test the get_statisics_multiprocessing method with invalid data. 
    Make sure the value error is raised.
    """
    df = pd.DataFrame({
        # If I have any valid, it would not bring up the error
        "NumberColumn": ["Squirrel", "Fox", "NaN", "Burger"]
    })
    data_cleaner = d_fetch.DataCleaner(df)
    numeric_column_gen = data_cleaner.data_to_numeric("NumberColumn")
    data_processor = d_process.DataProcessor(
        numeric_column_gen, "NumberColumn")
    with pytest.raises(ValueError):
        data_processor.get_statistics_multiprocessing()


def test_get_statistics_multiprocessing_no_data():
    """
    Test the get_statistics_multiprocessing method with an empty column. 
    Make sure the value error is raised.
    """
    df = pd.DataFrame({
        "NumberColumn": []
    })
    data_cleaner = d_fetch.DataCleaner(df)
    numeric_column_gen = data_cleaner.data_to_numeric("NumberColumn")
    data_processor = d_process.DataProcessor(
        numeric_column_gen, "NumberColumn")
    with pytest.raises(ValueError):
        data_processor.get_statistics_multiprocessing()


# Test case for write_txt method in DataStorer class (data_storage.py)
# Using a tmp_path instead of a real location
def test_write_txt_creates_file(tmp_path):
    """
    Test that the write_txt method creates a text file with the correct content.
    """
    stats = d_process.StatsSummary(
        column="TestColumn",
        mean=2.5,
        median=2.3,
        min=1.5,
        max=3.7
    )
    filepath = tmp_path / "test_stats.txt"
    data_storer = d_store.DataStorer(str(filepath), stats)
    data_storer.write_txt()
    assert filepath.exists()
    # If I want to see this fail, put asser not filepath.exists()


# Test cases for write_txt_async method in DataStorer class (data_storage.py)
def test_write_txt_async_creates_file(tmp_path):
    """
    Test that the write_txt_async method creates a text file with the 
    correct content asynchronously.
    """
    stats = d_process.StatsSummary(
        column="TestColumn",
        mean=2.5,
        median=2.3,
        min=1.5,
        max=3.7
    )
    filepath = tmp_path / "test_stats_async.txt"
    data_storer = d_store.DataStorer(str(filepath), stats)
    asyncio.run(data_storer.write_txt_async())
    assert filepath.exists()
    # If I want to see this fail, put asser not filepath.exists()


# Reusable dataframe for testing DataAnalyzer class (data_analysis.py)
@pytest.fixture
def sample_df():
    """
    Fixture that provides a sample dataframe for testing the DataAnalyzer class.
    """
    return pd.DataFrame({
        "Location": ["Location1", "Location2", "Location1", "Location2", "Location1"],
        "MaxTemp": [25, 32, 28, 27, 30],
        "MinTemp": [15, 20, 18, 16, 19],
        "RainToday": ["No", "Yes", "No", "Yes", "No"],
        "RainTomorrow": [0, 1, 0, 1, 0]
    })


# Test case for group_by_location method in DataAnalyzer class (data_analysis.py)
def test_group_by_location(sample_df):
    """
    Test the group_by_function method and make sure it correctly groups by location
    and calculates the mean of the specified column.
    """
    data_analyzer = d_analysis.DataAnalyzer(sample_df)
    result_df = data_analyzer.group_by_location("MaxTemp")
    assert result_df is not None
    assert list(result_df["Location"]) == ["Location1", "Location2"]
    assert list(result_df["MaxTemp"]) == [27.67, 29.5]


# Test case for filter_rain_tomorrow method in DataAnalyzer class (data_analysis.py)
def test_filter_rain_tomorrow(sample_df):
    """
    Test the filter_rain_tomorrow method and make sure it filters only rows where 
    rain tomorrow is Yes. 
    """
    data_analyzer = d_analysis.DataAnalyzer(sample_df)
    result_df = data_analyzer.filter_rain_tomorrow()
    assert result_df is not None
    assert len(result_df) == 2
    # checks to make sure all the values are a 1 (Yes)
    assert (result_df["RainTomorrow"] == 1).all()


# Test case for rain_today_rain_likelihood method in DataAnalyzer class (data_analysis.py)
def test_rain_today_rain_likelihood(sample_df):
    """
    Test the rain today_rain_likelihood method. It should make a list of tuples
    for the RainToday and RainTomorrow columns. Then it should filter
    only for rows where RainTomorrow is Yes.
    """
    data_analyzer = d_analysis.DataAnalyzer(sample_df)
    result_df = data_analyzer.rain_today_rain_likelihood()
    assert result_df == [("Yes", 1), ("Yes", 1)]


# Test case for hot_day_rain_likelihood method in DataAnalyzer class (data_analysis.py)
def test_hot_day_rain_likelihood(sample_df):
    """
    Test the hot_day_rain_likelihood method. It should make a list of tuples
    for the MaxTemp and RainTomorrow columns. Then it should check they are 
    valid pairs and map MaxTemp to "Hot" or "Not Hot". 
    """
    data_analyzer = d_analysis.DataAnalyzer(sample_df)
    result = data_analyzer.hot_day_rain_likelihood()
    assert result == [
        (25, "Not Hot", 0),
        (32, "Hot", 1),
        (28, "Not Hot", 0),
        (27, "Not Hot", 1),
        (30, "Not Hot", 0)
    ]
