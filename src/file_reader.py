from pathlib import Path

def read_file(file_path: Path) -> str:
    """
    Reads the content of a file and returns it as a string.
    
    Args:
        file_path (Path): The path to the file to be read.
    
    Returns:
        str: The content of the file.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()
