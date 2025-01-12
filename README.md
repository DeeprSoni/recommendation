# AI Recommendation System

The **AI Recommendation System** is a powerful platform for generating personalized recommendations using vector-based cosine similarity. Originally designed for restaurant menu recommendations, the system is adaptable for various domains, such as e-commerce, movies, music, and more.

---

## 🚀 Features

- **Vector-Based Recommendations**: Employs cosine similarity to identify relationships between items and users.
- **User-Friendly Web Interface**: Provides an intuitive Flask-based web interface for interaction.
- **Customizable Datasets**: Accepts uploaded datasets in CSV format for tailored recommendations.
- **Default Dataset Support**: Includes preloaded data to get started quickly.
- **Dynamic Order Management**: Allows users to add new orders dynamically.

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/your_username/ai-recommendation.git
cd ai-recommendation
```

### 2. Install Dependencies
Ensure Python 3.7+ is installed. Install the required libraries:
```bash
pip install -r requirements.txt
```

### 3. Run the Application
Start the Flask server:
```bash
python app.py
```

The application will be accessible at `http://127.0.0.1:5000`.

---

## 🎮 Usage

### Uploading a Dataset
1. Prepare a CSV file with the following structure:
   - **Column 1**: `User_ID` (unique identifier for each user).
   - **Columns 2+**: Items or products with binary values:
     - `1`: The item was purchased/liked by the user.
     - `0`: The item was not purchased/liked.

   Example Dataset:
   ```csv
   User_ID,Pizza,Burger,Pasta,Salad
   1,1,0,1,0
   2,0,1,0,1
   3,1,1,0,0
   ```

2. Visit the app's homepage and upload your dataset.

### Using Default Data
- Click the **Use Default Data** button to load the preloaded dataset.

### Getting Recommendations
1. Navigate to the **Recommendations** page.
2. Enter a **User ID** to get personalized item recommendations or an **Item Name** to find similar items.
3. Submit your query to view the results.

### Example Queries
#### Example 1: Recommendations by User ID
- **Input**: User ID = `1`
- **Output**: Recommended Items: `Burger, Salad`

#### Example 2: Recommendations by Item Name
- **Input**: Item Name = `Pizza`
- **Output**: Most Similar Item: `Pasta`

---

## 🧠 Algorithm Explanation

The AI Recommendation System is powered by **cosine similarity**, a widely used method in recommendation systems. Cosine similarity measures how similar two vectors are, based on the angle between them in a multi-dimensional space.

### Formula
\[
\text{Cosine Similarity} = \frac{\mathbf{A} \cdot \mathbf{B}}{\|\mathbf{A}\| \|\mathbf{B}\|}
\]

### How It Works

1. **Data Preparation**:
   - The dataset is transformed into a matrix where rows represent users and columns represent items.
   - Binary values (`1` or `0`) indicate whether a user has interacted with an item.

2. **Similarity Matrix**:
   - Cosine similarity is computed for all pairs of items.
   - The result is a square matrix where the value at `(i, j)` indicates the similarity between Item `i` and Item `j`.

3. **Generating Recommendations**:
   - **Item-Based**: For a given item, the algorithm identifies the most similar items using the similarity matrix.
   - **User-Based**: For a given user, the system aggregates their preferences and recommends items they are likely to enjoy based on past interactions.

### Example Walkthrough

#### Dataset Example:
```csv
User_ID,Pizza,Burger,Pasta,Salad
1,1,0,1,0
2,0,1,0,1
3,1,1,0,0
```

#### Step 1: Compute Cosine Similarity
- The similarity between `Pizza` and `Pasta` is high because both are purchased by User 1.
- The similarity between `Pizza` and `Burger` is moderate due to overlap in Users 1 and 3.

#### Step 2: Recommendations
- For `Pizza`, the most similar item is `Pasta`.
- For User 1, recommend `Burger` and `Salad` based on overall similarity.

---

## 📂 Project Structure

```
.
├── app.py               # Flask web application
├── recommendation.py    # Core recommendation logic
├── templates/           # HTML templates for Flask
│   ├── upload.html      # File upload interface
│   ├── index.html       # Recommendation display
│   ├── new_order.html   # Add new order interface
├── static/              # Static assets (CSS, JS, images)
├── uploaded_data.csv    # Uploaded dataset (dynamic)
├── default_data_file.csv# Preloaded sample dataset
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
├── LICENSE              # MIT License
```

---

## 🧪 Testing

### Unit Testing
Run unit tests for the recommendation algorithm using `pytest`:
```bash
pytest tests/
```

### Example Test Case
- **Input**: Dataset with items `Pizza` and `Burger`.
- **Expected Output**: Recommendations correctly identify `Burger` as similar to `Pizza`.

---

## 🌟 How to Contribute

We welcome contributions! Here’s how you can help:

1. **Fork the Repository**: Click the **Fork** button on GitHub.
2. **Create a Branch**: Create a new branch for your changes:
   ```bash
   git checkout -b feature-name
   ```
3. **Make Changes**: Add features, fix bugs, or improve documentation.
4. **Submit a Pull Request**: Open a pull request with a description of your changes.

See the [CONTRIBUTING.md](CONTRIBUTING.md) file for more details.

---

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## 📫 Contact

For questions, feedback, or feature requests:
- Email: **your_email@example.com**
- GitHub: [Your Username](https://github.com/your_username)

---

Happy coding! 🚀

