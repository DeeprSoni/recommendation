import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

def create_user_similarity_matrix(data):
    """Creates a user-to-user similarity matrix based on interactions."""
    sparse_matrix = csr_matrix(data.values)  # Convert to sparse format
    similarity_matrix = cosine_similarity(sparse_matrix)  # Compute similarity

    return pd.DataFrame(similarity_matrix, index=data.index, columns=data.index)
