import pandas as pd
from recommendation.sparse_matrix import create_sparse_similarity_matrix

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
