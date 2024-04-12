import pytest
from pathlib import Path
from src.file_reader import read_file

def test_read_file(tmp_path):
    test_file_path = tmp_path / "test_file.txt"
    expected_content = "Hello, world!"
    test_file_path.write_text(expected_content)

    # Test read_file function
    assert read_file(test_file_path) == expected_content
