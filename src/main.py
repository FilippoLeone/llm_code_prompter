import click
import logging
import platform
from pathlib import Path
from .file_reader import read_file
from .structure_generator import create_prompt, list_directory_structure

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def print_ascii_art():
    print("\033[93m")
    print(r"""
     ___      ___      __   __    _______  _______  __    _ 
    |   |    |   |    |  |_|  |  |       ||       ||  |  | |
    |   |    |   |    |       |  |    ___||    ___||   |_| |
    |   |    |   |    |       |  |   | __ |   |___ |       |
    |   |___ |   |___ |       |  |   ||  ||    ___||  _    |
    |       ||       || ||_|| |  |   |_| ||   |___ | | |   |
    |_______||_______||_|   |_|  |_______||_______||_|  |__|  
    """)
    print("\033[0m")

@click.command()
@click.argument('target_folder', type=click.Path(exists=True, file_okay=False, dir_okay=True))
@click.argument('file_pattern', type=str, default="*.py")
@click.argument('exclude_pattern', type=str, default="")
@click.argument('platform', type=str, default="")
def main(target_folder: str, file_pattern: str, exclude_pattern: str, platform: str):
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
    for file_path in folder_path.rglob(file_pattern):
        if exclude_pattern and any(exclude_path in str(file_path) for exclude_path in exclude_pattern.split(",")):
            continue
        file_content = read_file(file_path)
        full_prompt += f"# {file_path.name}\n{file_content}\n\n"

    prompt, token_count = create_prompt(full_prompt, folder_path)
    logging.info(f"Total number of tokens: {token_count}")

    if not platform:
        platform = platform_name()

    if platform.lower() == 'win32':
        copy_to_clipboard_win32(prompt)
    elif platform.lower() == 'linux':
        copy_to_clipboard_linux(prompt)
    elif platform.lower() == 'darwin':
        copy_to_clipboard_macos(prompt)
    else:
        logging.error(f"Unsupported platform: {platform}")

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

def platform_name():
    system = platform.system().lower()
    if system == 'windows':
        return 'win32'
    elif system == 'linux':
        return 'linux'
    elif system == 'darwin':
        return 'darwin'
    else:
        return ''

def copy_to_clipboard_win32(text):
    import win32clipboard
    try:
        win32clipboard.OpenClipboard()
        win32clipboard.EmptyClipboard()
        win32clipboard.SetClipboardText(text, win32clipboard.CF_TEXT)
        win32clipboard.CloseClipboard()
        print("\033[92mSuccessfully copied to clipboard.\033[0m")
    except Exception as e:
        logging.error(f"Failed to copy to clipboard: {e}")

def copy_to_clipboard_linux(text):
    try:
        import subprocess
        subprocess.run(['xclip', '-selection', 'clipboard'], input=text.encode(), check=True)
        print("\033[92mSuccessfully copied to clipboard.\033[0m")
    except (subprocess.CalledProcessError, ImportError) as e:
        logging.error(f"Failed to copy to clipboard: {e}")

def copy_to_clipboard_macos(text):
    try:
        import subprocess
        subprocess.run(['pbcopy'], input=text.encode(), check=True)
        print("\033[92mSuccessfully copied to clipboard.\033[0m")
    except subprocess.CalledProcessError as e:
        logging.error(f"Failed to copy to clipboard: {e}")

if __name__ == "__main__":
    main()