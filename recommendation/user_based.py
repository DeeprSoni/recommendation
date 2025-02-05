import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def create_user_similarity_matrix(data):
    """Creates a user-to-user similarity matrix based on interactions."""
    sparse_matrix = csr_matrix(data.values)  # Convert to sparse format
    similarity_matrix = cosine_similarity(sparse_matrix)  # Compute similarity

    return pd.DataFrame(similarity_matrix, index=data.index, columns=data.index)
def compute_user_score(user_id, data):
    """Returns item recommendations based on similar users."""
    similarity_matrix = create_user_similarity_matrix(data)

    if user_id not in similarity_matrix.index:
        return {}

    # Get the most similar users (excluding the user itself)
    similar_users = similarity_matrix[user_id].sort_values(ascending=False).index.tolist()
    similar_users.remove(user_id)  # ✅ Remove the input user

    recommended_items = {}

    # Find items liked by similar users
    for similar_user in similar_users:
        for item, rating in data.loc[similar_user].items():
            if rating > 0 and item != "Order_ID":  # ✅ Exclude Order_ID
                recommended_items[item] = recommended_items.get(item, 0) + rating

    # Sort and return top 5 recommended items
    return sorted(recommended_items.items(), key=lambda x: x[1], reverse=True)[:5]


