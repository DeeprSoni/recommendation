import pandas as pd
import shutil

def load_dataset(filepath):
    """Loads a dataset from a CSV file."""
    return pd.read_csv(filepath)

def copy_default_dataset(default_path, target_path):
    """Copies the default dataset to the target path."""
    shutil.copy(default_path, target_path)
