import os
from pathlib import Path


def list_all():
    all_examples = []
    integrated_recognizers_directory = Path(__file__).parent
    for root, _, files in os.walk(integrated_recognizers_directory):
        for file in files:
            if file.endswith("_recognizer.py"):
                all_examples.append(os.path.join(root, file))
    return all_examples
