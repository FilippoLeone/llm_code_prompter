from click.testing import CliRunner
from src.main import main
import pytest
from pathlib import Path

def setup_test_files(test_folder):
    # Assuming the script expects a README.md at least
    readme_file = test_folder / "README.md"
    readme_file.write_text("Project Name: Example Project")

    # Add some Python files
    python_file1 = test_folder / "example1.py"
    python_file1.write_text("print('Hello, World!')")

    python_file2 = test_folder / "example2.py"
    python_file2.write_text("x = 42\nprint(x)")

def test_main_cli(tmp_path):
    runner = CliRunner()
    test_folder = tmp_path / "test_folder"
    test_folder.mkdir()
    setup_test_files(test_folder)

    # Test with default arguments
    result = runner.invoke(main, [str(test_folder)])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}. Output: {result.output}"
    assert "Successfully copied to clipboard" in result.output

    # Test with file_pattern argument
    result = runner.invoke(main, [str(test_folder), "*.py"])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}. Output: {result.output}"
    assert "Successfully copied to clipboard" in result.output

    # Test with exclude_pattern argument
    result = runner.invoke(main, [str(test_folder), "*.py", "example2.py"])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}. Output: {result.output}"
    assert "Successfully copied to clipboard" in result.output

    # Test with platform argument
    result = runner.invoke(main, [str(test_folder), "*.py", "", "win32"])
    assert result.exit_code == 0, f"Unexpected exit code: {result.exit_code}. Output: {result.output}"
    assert "Successfully copied to clipboard" in result.output

if __name__ == "__main__":
    pytest.main()