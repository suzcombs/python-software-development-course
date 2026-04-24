"""
Author: Suzanne Combs
Course: CS 3270-X01
Module for creating machine learning models and predictions
See main.py for AI usage disclosure.
"""
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

CSV_PATH = "australia_weather_data/weather_training_data.csv"

# Isolate columns
input_columns = ["MinTemp", "MaxTemp", "WindGustSpeed",
                 "Humidity9am", "Humidity3pm",
                 "Pressure9am", "Pressure3pm"]
OUTCOME_COLUMN = "RainTomorrow"


def train_model():
    """Train a decision tree model to predict whether it will rain tomorrow"""
    weather_df = pd.read_csv(CSV_PATH)

    # Create a df with only these columns for ML and remove NaN
    weather_df = weather_df[input_columns + [OUTCOME_COLUMN]].dropna()

    # Model training - split into 4 groups for training/testing
    X = weather_df[input_columns]
    y = weather_df[OUTCOME_COLUMN]
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = RandomForestClassifier(n_estimators=100, random_state=42)

    # Make the model
    model.fit(X_train, y_train)

    # Tell some to predict
    predictions = model.predict(X_test)

    # See how accurate it is
    score = accuracy_score(y_test, predictions)
    return model, score


def predict_rain_tomorrow(prediction_values):
    """
    Predict if it will rain tomorrow with prediction inputs
    """
    # Call the train_model function to get model, score
    model, score = train_model()

    input_data = pd.DataFrame([prediction_values], columns=input_columns)

    # Gets the first data for 0/1
    prediction = model.predict(input_data)[0]
    return prediction, score


if __name__ == "__main__":
    # Train the model
    model, score = train_model()
    print(f"Model accuracy: {score:.2%}")

    # Predict if it will rain
    # List of values to use for prediction
    prediction_values = [12.1, 36.4, 33.0, 55.0, 32.1, 1013.4, 1009.3]
    prediction, score = predict_rain_tomorrow(prediction_values)

    if prediction == 1:
        print("Prediction: It will rain tomorrow")
    else:
        print("Prediction: It will not rain tomorrow")
