from pathlib import Path
import os
from tiktoken import get_encoding
from .file_reader import read_file
import logging

def list_directory_structure(startpath: Path) -> str:
    """
    Generates a textual representation of the directory structure.
    
    Args:
        startpath (Path): The path to the directory to list.
    
    Returns:
        str: A structured string representing the directory layout.
    """
    structure = []
    for root, dirs, files in os.walk(startpath):
        level = root.replace(str(startpath), '').count(os.sep)
        indent = ' ' * 4 * level
        structure.append(f"{indent}{os.path.basename(root)}/")
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            structure.append(f"{subindent}{f}")
    return '\n'.join(structure)

def create_prompt(full_prompt: str, folder_path: Path, max_tokens: int = 128000) -> tuple:
    """
    Returns the assembled prompt within token limits and the token count.
    """
    encoder = get_encoding("cl100k_base")
    prompt_tokens = encoder.encode(full_prompt)
    
    if len(prompt_tokens) > max_tokens:
        logging.warning("Initial token count exceeds the limit. Adjusting to fit within the allowed token limit.")
        prompt_tokens = prompt_tokens[:max_tokens]

    return encoder.decode(prompt_tokens), len(prompt_tokens)
