from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from recommendation.data_handler import load_dataset, copy_default_dataset
from recommendation.hybrid import hybrid_recommendation

# Get the absolute path to the directory containing app.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Construct the absolute paths
CSV_PATH = os.path.join(BASE_DIR, "uploaded_data.csv")
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "default_data.csv")

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        csv_file = request.files.get("csvfile")

        # Check if a file was uploaded
        if csv_file:
            csv_file.save(CSV_PATH)  # Save the uploaded CSV
        else:
            copy_default_dataset(DEFAULT_CSV_PATH, CSV_PATH)

        return redirect(url_for('get_recommendation'))
    else:
        return render_template("upload.html")

@app.route("/use-default", methods=["GET"])
def use_default():
    # Copy the default CSV to the CSV_PATH
    copy_default_dataset(DEFAULT_CSV_PATH, CSV_PATH)
    return redirect(url_for('get_recommendation'))

@app.route("/recommend", methods=["GET", "POST"])
def get_recommendation():
    data = load_dataset(CSV_PATH)  # Read the saved CSV file

    recommended = None
    user_id = None
    item_name = None

    if request.method == "POST":
        user_id = int(request.form["user_id"])
        item_name = request.form["item_name"]
        recommended = hybrid_recommendation(user_id, item_name, data)

    return render_template("index.html", recommended=recommended, user_id=user_id, item_name=item_name)

if __name__ == "__main__":
    app.run(debug=True)
