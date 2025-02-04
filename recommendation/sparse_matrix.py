import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.metrics.pairwise import cosine_similarity

def convert_to_sparse(data):
    """Converts a Pandas DataFrame to a Compressed Sparse Row (CSR) matrix."""
    return csr_matrix(data.values)

def compute_sparse_similarity(sparse_matrix):
    """Computes cosine similarity for a sparse matrix."""
    return cosine_similarity(sparse_matrix, dense_output=False)

def create_sparse_similarity_matrix(data):
    """Creates a sparse cosine similarity matrix for items."""
    sparse_matrix = convert_to_sparse(data.T)  # Transpose to make items as rows
    similarity_matrix = compute_sparse_similarity(sparse_matrix)

    return pd.DataFrame(similarity_matrix.toarray(), index=data.columns, columns=data.columns)

