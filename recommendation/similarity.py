import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity


def create_similarity_matrix(data):
    """Creates a cosine similarity matrix for items in the dataset."""
    similarity_matrix = cosine_similarity(data.T)  # Note the transpose here
    return pd.DataFrame(similarity_matrix, index=data.columns, columns=data.columns)

def get_recommendation_for_item(item_name, data):
    """Gets the most similar item for the given item name."""
    similarity_matrix = create_similarity_matrix(data)
    item_similarities = similarity_matrix[item_name]

    # Sort items by similarity score
    recommended_items = item_similarities.sort_values(ascending=False)

    # Remove the input item and irrelevant columns like 'Order_ID'
    recommended_items = recommended_items.drop(labels=[item_name, 'Order_ID'], errors='ignore')

    # Return the top recommendation
    return recommended_items.head(1).index.tolist()[0]
