import pandas as pd
import shutil

def load_dataset(filepath):
    """Loads a dataset from a CSV file and removes NaN values."""
    data = pd.read_csv(filepath)
    data.fillna(0, inplace=True)  # Replace NaN values with 0 for sparse representation
    return data

def copy_default_dataset(default_path, target_path):
    """Copies the default dataset to the target path."""
    shutil.copy(default_path, target_path)
