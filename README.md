# LLM Code Prompter

## Overview
The LLM Code Prompter is a command-line utility designed to generate structured prompts for GPT-4 models, leveraging the maximum context limit. It efficiently handles project files to prepare them for GPT-4 interaction, ensuring that the content is within the 128k token limit imposed by OpenAI.

This utility is particularly useful for developers working with GPT-4 who need to manage and test large datasets or codebases. It streamlines the process of preparing data for the model, facilitating a more efficient workflow.

## Features
- **Automatic Prompt Generation**: Generates prompts by reading and structuring content from specified directories.
- **Token Count Management**: Ensures that the prompt does not exceed GPT-4's token limit by counting and adjusting the included content.
- **CLI Integration**: Easy-to-use command-line interface that makes it simple to integrate into any development workflow.
- **Optional Content Inclusion**: Automatically includes optional files like `OBJECTIVE.md` and `PROMPT.md` at the beginning of the prompt if they exist in the directory.
- **Clipboard Support**: Automatically copies the generated prompt to the clipboard for easy use.

## Installation

1. **Clone the repository:**

`git clone https://github.com/FilippoLeone/llm-code-prompter.git`

2. **Navigate to the project directory:**

`cd llm-code-prompter`

4. **Install the package in editable mode:**

`pip install -e .`

This allows you to modify the project and see changes without reinstalling the package.

## Usage

Run the script by navigating to the project directory and using the following command:

`llm_code_prompter [target_folder] [file_pattern] [exclude_pattern] [platform]`

Where:

    [target_folder] is the path to the directory containing the files you want to include in your prompt.
    [file_pattern] is the pattern to match the files you want to include (default is "*.py").
    [exclude_pattern] is a comma-separated list of file paths or patterns to exclude (default is empty).
    [platform] is the target platform for the clipboard operation (default is determined automatically).

Example usage:

    llm_code_prompter /path/to/directory
    llm_code_prompter /path/to/directory "*.py"
    llm_code_prompter /path/to/directory "*.py" "tests/,__pycache__/"
    llm_code_prompter /path/to/directory "*.py" "tests/,__pycache__/" win32

The script will read the contents of the specified directory, including any optional files (like OBJECTIVE.md and PROMPT.md), and then concatenate the contents of all the matching Python files. The resulting text will be copied to the system clipboard, so you can paste it into your LLM prompt.

## Development

This project is developed using Python 3.9+. It adheres to PEP standards and utilizes type hinting to ensure code quality and maintainability.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
