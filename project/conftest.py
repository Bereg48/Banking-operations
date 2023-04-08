import json
import pytest

from pathlib import Path


@pytest.fixture
def load_json_file():
    current_dirpath = Path(__file__).parent

    def load_file(relative_filepath):
        filepath = (current_dirpath / relative_filepath).resolve()
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data

    return load_file