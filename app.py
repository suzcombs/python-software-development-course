"""
Author: Suzanne Combs
Course: CS 3270-X01
Uses Flask to create a web application using python, html, and SQLite.
Includes machine learning model for raining tomorrow predictions

See main.py for AI usage disclosure.
"""
import base64
import io
import os
from datetime import datetime
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

import my_package.data_fetching as d_fetch
import my_package.data_processing as d_process
import my_package.data_analysis as d_analyze
import my_package.ml_model as ml_model


app = Flask(__name__)

# Set up the database
os.makedirs(app.instance_path, exist_ok=True)  # Yes?
db_path = os.path.join(app.instance_path, "weather.db")

# SQLite database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


class HistoryQuery(db.Model):
    """Creates a db of customer query and time"""
    id = db.Column(db.Integer, primary_key=True)
    location = db.Column(db.String(100), nullable=False)
    column_name = db.Column(db.String(100), nullable=False)
    query_time = db.Column(db.DateTime, nullable=False,
                           default=lambda: datetime.now().replace(microsecond=0))


CSV_PATH = "australia_weather_data/weather_training_data.csv"
column_list = [
    "MaxTemp", "MinTemp", "WindGustSpeed",
    "Humidity9am", "Humidity3pm", "Pressure9am"
]


@app.route("/")
def index():
    """Sets up the index page of the website"""
    load_data = d_fetch.DataFetcher(CSV_PATH)
    weather_df = load_data.csv_to_df()
    locations = list(sorted(weather_df["Location"].dropna().unique()))
    return render_template("index.html", locations=locations, columns=column_list)


@app.route("/dashboard", methods=["POST"])
def dashboard():
    """Sets up the dashboard page of the website"""
    selected_location = request.form.get("location")
    selected_column = request.form.get("column")

    if not selected_location:
        return render_template("error.html", message="Missing location")

    if not selected_column:
        return render_template("error.html", message="Missing column")

    if selected_column not in column_list:
        return render_template("error.html", message="That column is invalid")

    load_data = d_fetch.DataFetcher(CSV_PATH)
    weather_df = load_data.csv_to_df()

    # filter for the selected location
    filtered_df = weather_df[weather_df["Location"] == selected_location]

    # Save the query to SQLite database
    new_query = HistoryQuery(location=selected_location,
                             column_name=selected_column)
    db.session.add(new_query)
    db.session.commit()

    # Compute the stats for the column
    data_cleaner = d_fetch.DataCleaner(filtered_df)
    cleaned_column = data_cleaner.data_to_numeric(selected_column)

    data_processor = d_process.DataProcessor(cleaned_column, selected_column)
    stats = data_processor.get_statistics()

    # Add a histogram of the information - Can't do the matplotlib directly
    # Need to save as an image
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    data_analyzer = d_analyze.DataAnalyzer(filtered_df)
    hist_fig = data_analyzer.create_histogram(selected_column)

    # Save the plot
    hist_img = io.BytesIO()  # Change into bytes
    hist_fig.savefig(hist_img, format="png")  # Save as a png
    hist_img.seek(0)

    # Encode the image to use for HTML
    plot_web = base64.b64encode(hist_img.getvalue()).decode()

    # ML prediction - clean the columns
    prediction_data = filtered_df[ml_model.input_columns].dropna()

    # Empty values to be filled with results predict_rain_tomorrow
    prediction = None
    model_score = None

    has_data = not prediction_data.empty

    if has_data:
        # Get the mean for all the columns that have data
        mean_data = prediction_data.mean()
        # Get the mean values for the specified columns
        prediction_values = [
            mean_data["MinTemp"],
            mean_data["MaxTemp"],
            mean_data["WindGustSpeed"],
            mean_data["Humidity9am"],
            mean_data["Humidity3pm"],
            mean_data["Pressure9am"],
            mean_data["Pressure3pm"]
        ]

        prediction, model_score = ml_model.predict_rain_tomorrow(
            prediction_values)

    # Need to close
    plt.close(hist_fig)

    return render_template("dashboard.html", location=selected_location,
                           column=selected_column, stats=stats, plot_web=plot_web,
                           prediction=prediction, model_score=model_score)


# Display the query history
@app.route("/history")
def history():
    """Sets up the query history page of the website"""
    queries = HistoryQuery.query.order_by(HistoryQuery.query_time.desc())
    return render_template("history.html", queries=queries)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # Starts the development server
