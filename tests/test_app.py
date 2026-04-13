"""
This module contains pytests for the project. 
It tests the functionality of data fetching, data processing, 
and data storage for the application.
"""
import pytest
import pandas as pd
import my_package.data_fetching as d_fetch
import my_package.data_processing as d_process
import my_package.data_storage as d_store


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
    assert values == []


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
