"""
Author: Suzanne Combs
Course: CS 3270-X01
Uses Flask to create a web application using python, html, and SQLite.
Includes machine learning model for raining tomorrow predictions
Requires a user to log in and upload a CSV file.

See main.py for AI usage disclosure.
"""
import base64
import io
import os
from datetime import datetime
from flask import Flask, render_template, request, \
    redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

import my_package.data_fetching as d_fetch
import my_package.data_processing as d_process
import my_package.data_analysis as d_analyze
import my_package.ml_model as ml_model


app = Flask(__name__)

# Set up the database
os.makedirs(app.instance_path, exist_ok=True)
db_path = os.path.join(app.instance_path, "weather.db")

# SQLite database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_path}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "secretkey"  # Secure session

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


# Flask handles login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# Setup folder for uploads
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@login_manager.user_loader
def load_user(user_id):
    """Reload user object from user id stored in user session"""
    return db.session.get(User, int(user_id))


class User(db.Model, UserMixin):
    """Creates a db with username and password"""
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


class RegistrationForm(FlaskForm):
    """Sets up the registration for user and password"""
    # Requirements for the username and password fields
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Register")

    # Validate that the username is unique
    def validate_username(self, username):
        """Checks the dabase to see if the username is already there. 
        If so, gives a ValidationError."""
        existing_user_username = User.query.filter_by(
            username=username.data).first()
        if existing_user_username:
            raise ValidationError(
                "That username already exists. Please choose another one.")


class LoginForm(FlaskForm):
    """Sets up the registration for user and password"""
    # Requirements for the username and password fields
    username = StringField(validators=[InputRequired(), Length(min=4, max=20)],
                           render_kw={"placeholder": "Username"})
    password = PasswordField(validators=[InputRequired(), Length(min=4, max=20)],
                             render_kw={"placeholder": "Password"})
    submit = SubmitField("Log In")


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


# Start page for logging in and verifying valid accounts
@app.route("/", methods=["POST", "GET"])
def login():
    """Login page to verify users before getting to other pages"""
    form = LoginForm()

    # Run this if the form is submitted
    if form.validate_on_submit():
        # Check if name is in the DB
        user = User.query.filter_by(username=form.username.data).first()

        if user:
            # Check the passwords match
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                return redirect("/upload")

    return render_template("login.html", form=form)


@app.route("/upload", methods=["POST", "GET"])
@login_required
def upload():
    """Enables a user to upload a CSV file"""
    if request.method == "POST":
        file = request.files.get("csv_file")

        # Make sure the file is a CSV
        if not file.filename.endswith(".csv"):
            return render_template("error.html", message="Please upload a CSV file")

        # Make the full filepath
        filepath = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(filepath)

        session["csv_path"] = filepath

        return redirect("/home")
    return render_template("upload.html")


@app.route("/home")
@login_required
def home():
    """Sets up the home page of the website"""
    # Get the csv from the user, CSV_PATH is the defaul
    csv_path = session.get("csv_path", CSV_PATH)
    load_data = d_fetch.DataFetcher(csv_path)
    weather_df = load_data.csv_to_df()
    locations = list(sorted(weather_df["Location"].dropna().unique()))
    return render_template("home.html", locations=locations, columns=column_list)


@app.route("/dashboard", methods=["POST"])
@login_required
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
@login_required
def history():
    """Sets up the query history page of the website"""
    queries = HistoryQuery.query.order_by(HistoryQuery.query_time.desc())
    return render_template("history.html", queries=queries)


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    """Sends the user back to the login page"""
    logout_user()
    return redirect("/")


# Page for registering for an account
@app.route("/register", methods=["POST", "GET"])
def register():
    """Allows people to register to become a valid user"""
    form = RegistrationForm()

    if form.validate_on_submit():
        # encrypt the password for secure registration
        hashed_password = bcrypt.generate_password_hash(
            form.password.data).decode("utf-8")
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/")

    return render_template("register.html", form=form)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)  # Starts the development server
