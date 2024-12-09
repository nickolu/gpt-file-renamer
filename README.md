# gpt-file-renamer
Use GPT API to intelligently rename a set of files

## Description
This Python script uses OpenAI's GPT API to intelligently rename files by removing numeric prefixes, correcting formatting issues, and ensuring consistent naming conventions.

## Prerequisites
- Python 3.6 or higher
- OpenAI API key
- `openai` Python package

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/yourusername/gpt-file-renamer.git
   cd gpt-file-renamer
   ```

2. Install the required package:
   ```bash
   pip install openai
   ```

3. Set up your OpenAI API key as an environment variable:
   ```bash
   # On macOS/Linux
   export OPENAI_API_KEY='your-api-key-here'
   
   # On Windows (Command Prompt)
   set OPENAI_API_KEY=your-api-key-here
   
   # On Windows (PowerShell)
   $env:OPENAI_API_KEY='your-api-key-here'
   ```

## Customizing for Your Files

The script's behavior can be customized by modifying the `config.py` file. This file contains:
- The system prompt that guides how files should be renamed
- Example conversations that help the model understand the desired formatting

By default, the script is configured to rename video game files, but you can easily modify it for other use cases by editing `config.py`. The file includes commented examples for different use cases such as:
- Music files (artist names and song titles)
- Photo files (date-based naming)
- Document files (proper case formatting)

Simply uncomment and modify the appropriate `SYSTEM_PROMPT` in `config.py` to match your needs.

## Usage

Run the script by providing the directory path containing the files you want to rename:

```bash
python rename_file.py /path/to/your/directory
```

The script will:
1. Process all files in the specified directory
2. Generate new filenames using the OpenAI API
3. Handle any duplicate filenames automatically
4. Show progress as it processes the files

## Example

```bash
python rename_file.py ~/Documents/game_files
```

## Notes
- The script will maintain file extensions while renaming
- If a suggested filename already exists, the script will append a number to prevent overwriting
- Progress updates will be displayed in the console during processing
- Customize the renaming behavior by modifying `config.py`
- **Strongly recommend running the script on a test folder first to ensure it works as expected**
