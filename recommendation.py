import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

def create_similarity_matrix(data):
    # Assuming each row is an order and columns (excluding the first) are items
    # Calculate the cosine similarity between items
    similarity_matrix = cosine_similarity(data.T)  # Note the transpose here
    
    return pd.DataFrame(similarity_matrix, index=data.columns, columns=data.columns)

def get_recommendation_for_item(item_name, data):
    # Create the similarity matrix
    similarity_matrix = create_similarity_matrix(data)

    # Get similarities for the specific item
    item_similarities = similarity_matrix[item_name]

    # Sort the items based on the cosine similarity scores
    recommended_items = item_similarities.sort_values(ascending=False)

    # Remove the input item itself and the 'Order_ID' from the recommendation list
    recommended_items = recommended_items.drop(labels=[item_name, 'Order_ID'])

    # Return only the top most similar item
    return recommended_items.head(1).index.tolist()[0]

def generate_recommendations(data):
    # Return a list of all item names (excluding Order_ID)
    return data.columns[1:].tolist()
