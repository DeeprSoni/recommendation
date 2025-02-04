from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import os
from recommendation.data_handler import load_dataset, copy_default_dataset
from recommendation.hybrid import hybrid_recommendation
from recommendation.similarity import compute_item_score
from recommendation.user_based import compute_user_score

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
        user_id = request.form.get("user_id")  # Allow empty input
        item_name = request.form.get("item_name")  # Allow empty input

        if user_id:  # If user ID is provided, get user-based recommendations
            user_id = int(user_id)
            recommended = compute_user_score(user_id, data)

            # Fix: Ensure recommended is a dictionary before calling .items()
            if isinstance(recommended, dict):
                recommended = sorted(recommended.items(), key=lambda x: x[1], reverse=True)[:5]
            else:
                recommended = recommended[:5]  # If it's a list, just slice the top 5

        if item_name:  # If item name is provided, get item-based recommendations
            item_recommendations = compute_item_score(item_name, data)

            if isinstance(item_recommendations, dict):
                item_recommendations = sorted(item_recommendations.items(), key=lambda x: x[1], reverse=True)[:5]
            else:
                item_recommendations = item_recommendations[:5]  

            if recommended:
                recommended.extend(item_recommendations)  # Merge results if both user_id & item exist
                recommended = list(set(recommended))[:5]  # Deduplicate and limit to 5 results
            else:
                recommended = item_recommendations  # If only item is entered, use item recommendations

    return render_template("index.html", recommended=recommended, user_id=user_id, item_name=item_name)


if __name__ == "__main__":
    app.run(debug=True)
