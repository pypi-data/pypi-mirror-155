import pickle
from pathlib import Path


def pickle_to_file(obj, filepath: str or Path):
    file_path = Path(filepath)
    file_path.parent.mkdir(exist_ok=True, parents=True)
    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def unpickle_from_file(filepath: str or Path):
    file_path = Path(filepath)

    if not file_path.exists():
        return None

    with open(filepath, 'rb') as f:
        return pickle.load(f)
