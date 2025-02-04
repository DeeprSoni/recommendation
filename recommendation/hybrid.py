import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from recommendation.user_based import create_user_similarity_matrix  # Keep this import

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
    return similarity_matrix[item_name].to_dict()

def compute_user_score(user_id, data):
    """Computes user-based similarity scores."""
    similarity_matrix = create_user_similarity_matrix(data)
    if user_id not in similarity_matrix.index:
        return {}
    return similarity_matrix[user_id].to_dict()

def hybrid_recommendation(user_id, item_name, data, threshold=5):
    """
    Dynamically decides between user-based and item-based recommendations.

    - If user has interacted with **less than threshold items**, use item-based filtering.
    - If user has interacted with **more than threshold items**, use user-based filtering.
    - Otherwise, use a mix based on confidence probability.
    """

    # Get number of interactions for this user
    user_interactions = (data.loc[user_id] > 0).sum() if user_id in data.index else 0

    # Compute probability weight (0 = full item-based, 1 = full user-based)
    probability_weight = min(user_interactions / threshold, 1)

    # Compute item-based recommendation scores
    item_scores = compute_item_score(item_name, data)

    # Compute user-based recommendation scores
    user_scores = compute_user_score(user_id, data)

    # Normalize scores
    if item_scores and user_scores:
        max_item_score = max(item_scores.values()) if item_scores else 1
        max_user_score = max(user_scores.values()) if user_scores else 1
        for k in item_scores:
            item_scores[k] /= max_item_score
        for k in user_scores:
            user_scores[k] /= max_user_score

    # Merge scores dynamically based on probability
    final_scores = {}
    for key in set(item_scores.keys()).union(user_scores.keys()):
        item_score = item_scores.get(key, 0)
        user_score = user_scores.get(key, 0)
        final_scores[key] = ((1 - probability_weight) * item_score) + (probability_weight * user_score)

    # Sort recommendations by final score
    sorted_recommendations = sorted(final_scores.items(), key=lambda x: x[1], reverse=True)

    # Return top 5 recommendations
    return [rec[0] for rec in sorted_recommendations[:5]]
