import click
import win32clipboard
import logging
from pathlib import Path

from .file_reader import read_file
from .structure_generator import create_prompt, list_directory_structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_ascii_art():
    print("\033[93m")
    print(r"""
     ____  _              _____                _             
    |  _ \| |            / ____|              | |            
    | |_) | | _____  __ | |     _ __ ___  __ _| |_ ___  _ __ 
    |  _ <| |/ _ \ \/ / | |    | '__/ _ \/ _` | __/ _ \| '__|
    | |_) | |  __/>  <  | |____| | |  __/ (_| | || (_) | |   
    |____/|_|\___/_/\_\  \_____|_|  \___|\__,_|\__\___/|_|   
    """)
    print("\033[0m")

@click.command()
@click.argument('target_folder', type=click.Path(exists=True, file_okay=False, dir_okay=True))
def main(target_folder: str):
    print_ascii_art()
    folder_path = Path(target_folder)
    
    # Start with optional files if they exist
    full_prompt = ''
    full_prompt = append_optional_contents(folder_path, full_prompt)
    
    # Append README.md and project structure
    readme_content = read_file(folder_path / 'README.md')
    structure_snapshot = list_directory_structure(folder_path)
    full_prompt += f"# README.md\n{readme_content}\n\n# Project structure\n{structure_snapshot}\n"

    # Append content of each Python file in the directory
    for file_path in folder_path.rglob('*.py'):
        file_content = read_file(file_path)
        full_prompt += f"# {file_path.name}\n{file_content}\n\n"

    prompt, token_count = create_prompt(full_prompt, folder_path)
    logging.info(f"Total number of tokens: {token_count}")

    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(prompt, win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
        print("\033[92mSuccessfully copied to clipboard.\033[0m")
    except Exception as e:
        logging.error(f"Failed to copy to clipboard: {e}")
        
    print("\nFinal Prompt for GPT-4 has been copied to the clipboard. You can paste it anywhere using Ctrl+V.\n")
    print(prompt)

def append_optional_contents(folder_path, full_prompt):
    # Check for OBJECTIVE.md and PROMPT.md and prepend if they exist
    for filename in ['OBJECTIVE.md', 'PROMPT.md']:
        file_path = folder_path / filename
        if file_path.exists():
            content = read_file(file_path)
            # Prepend to ensure they are at the top
            full_prompt = f"# {filename}\n{content}\n\n" + full_prompt
    return full_prompt

if __name__ == "__main__":
    main()
