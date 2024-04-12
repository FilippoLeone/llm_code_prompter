from src.structure_generator import list_directory_structure
from pathlib import Path
import pytest

def test_list_directory_structure(tmp_path):
    # Create a dummy structure
    d = tmp_path / "sub"
    d.mkdir()
    p = d / "hello.txt"
    p.write_text("file content")
    
    expected_structure = f"{tmp_path.name}/\n    sub/\n        hello.txt"
    assert list_directory_structure(tmp_path) == expected_structure
