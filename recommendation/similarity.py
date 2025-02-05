import pandas as pd
from recommendation.hybrid import create_sparse_similarity_matrix

def get_recommendation_for_item(item_name, data):
    """Gets the most similar item for the given item name using sparse matrices."""
    similarity_matrix = create_sparse_similarity_matrix(data)
    item_similarities = similarity_matrix[item_name]

    # Sort items by similarity score
    recommended_items = item_similarities.sort_values(ascending=False)

    # Remove the input item and irrelevant columns like 'Order_ID'
    recommended_items = recommended_items.drop(labels=[item_name, 'Order_ID'], errors='ignore')

    # Return the top recommendation
    return recommended_items.head(1).index.tolist()[0]
    
def create_sparse_similarity_matrix(data):
    """Creates a sparse cosine similarity matrix for items."""
    sparse_matrix = csr_matrix(data.T)  # Transpose to make items as rows
    similarity_matrix = cosine_similarity(sparse_matrix)

    return pd.DataFrame(similarity_matrix, index=data.columns, columns=data.columns)

def compute_item_score(item_name, data):
    """Computes item-based similarity scores."""
    similarity_matrix = create_sparse_similarity_matrix(data)

    if item_name not in similarity_matrix.columns:
        return {}

    item_similarities = similarity_matrix[item_name]

    # ✅ Exclude the input item from the recommendations
    recommended_items = item_similarities.drop(labels=[item_name, "Order_ID"], errors="ignore").sort_values(ascending=False)

    # Return top 5 recommended items
    return recommended_items.head(5).to_dict()

