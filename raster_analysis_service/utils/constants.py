"""Some constants to utilize within the service
"""
import os
from pathlib import Path


PROJECT_PATH = Path(__file__).parents[2]
RELATIVE_DATASET_PATH = os.environ.get("DATASET_PATH", "dataset")
ABSOLUTE_DATASET_PATH = os.path.join(PROJECT_PATH, RELATIVE_DATASET_PATH)
