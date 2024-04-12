from click.testing import CliRunner
from src.main import main
import pytest
from pathlib import Path

def setup_test_files(test_folder):
    # Assuming the script expects a README.md at least
    readme_file = test_folder / "README.md"
    readme_file.write_text("Project Name: Example Project")

    # Add more setup here if your main function expects more files or specific content

def test_main_cli(tmp_path):
    runner = CliRunner()
    test_folder = tmp_path / "test_folder"
    test_folder.mkdir()
    setup_test_files(test_folder)  # Set up necessary test files

    result = runner.invoke(main, [str(test_folder)])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}. Output: {result.output}"

    # Additional assertions can be made here based on expected output
