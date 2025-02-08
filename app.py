from flask import Flask, render_template, request, redirect, url_for, jsonify
import pandas as pd
import os
from hybrid import hybrid_recommendation
from similarity import compute_item_score
from user_based import compute_user_score
from flask_cors import CORS  # Allows cross-origin requests

app = Flask(__name__)
CORS(app)

# Define dataset paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSV_PATH = os.path.join(BASE_DIR, "uploaded_data.csv")
DEFAULT_CSV_PATH = os.path.join(BASE_DIR, "default_data.csv")

def load_dataset():
    """Load dataset from CSV or return an empty DataFrame."""
    if os.path.exists(CSV_PATH):
        return pd.read_csv(CSV_PATH, index_col=0)
    return pd.DataFrame()

@app.route("/", methods=["GET", "POST"])
def index():
    """Handles dataset upload and redirects to recommendations."""
    if request.method == "POST":
        csv_file = request.files.get("csvfile")

        if csv_file:
            csv_file.save(CSV_PATH)  # Save uploaded CSV
        else:
            copy_default_dataset(DEFAULT_CSV_PATH, CSV_PATH)

        return redirect(url_for('recommend'))
    return render_template("upload.html")

@app.route("/use-default", methods=["GET"])
def use_default():
    """Loads the default dataset."""
    copy_default_dataset(DEFAULT_CSV_PATH, CSV_PATH)
    return redirect(url_for('recommend'))

@app.route("/recommend", methods=["GET", "POST"])
def recommend():
    """Handles recommendation requests from the HTML form."""
    data = load_dataset().drop(columns=["Order_ID"], errors="ignore")  # ✅ Drop Order_ID
    recommended = None
    user_id = None
    item_name = None

    if request.method == "POST":
        user_id = request.form.get("user_id")  # Allow empty input
        item_name = request.form.get("item_name")  # Allow empty input

        recommended = []

        if user_id:
            user_id = int(user_id)
            user_recommendations = compute_user_score(user_id, data)
            recommended += sorted(user_recommendations.items(), key=lambda x: x[1], reverse=True)[:5] if isinstance(user_recommendations, dict) else user_recommendations[:5]

        if item_name:
            item_recommendations = compute_item_score(item_name, data)
            recommended += sorted(item_recommendations.items(), key=lambda x: x[1], reverse=True)[:5] if isinstance(item_recommendations, dict) else item_recommendations[:5]

        recommended = list(set(recommended))[:5]  # Deduplicate and limit to 5 results

    return render_template("index.html", recommended=recommended, user_id=user_id, item_name=item_name)

@app.route("/api/recommend", methods=["GET"])
def api_recommend():
    """API endpoint for recommendations."""
    data = load_dataset().drop(columns=["Order_ID"], errors="ignore")

    user_id = request.args.get("user_id", type=int)
    item_name = request.args.get("item_name", type=str)

    if not user_id and not item_name:
        return jsonify({"error": "At least one parameter (user_id or item_name) is required"}), 400

    recommended = hybrid_recommendation(user_id, item_name, data)

    return jsonify({"recommendations": recommended})

@app.route("/api/debug", methods=["GET"])
def debug_data():
    """API endpoint to check dataset structure before making recommendations."""
    data = load_dataset().drop(columns=["Order_ID"], errors="ignore")
    return jsonify({
        "columns": list(data.columns),
        "sample_data": data.head(5).to_dict()
    })

if __name__ == "__main__":
    app.run(debug=True)
