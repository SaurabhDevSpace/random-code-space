# Directory Structure Generator

This Python script generates a directory structure in either JSON or text format, allowing you to document your project's file hierarchy in a dedicated Markdown file or display it in the console. It uses the `pathlib` library for cross-platform compatibility and supports recursive directory traversal with error handling for non-existent directories or permission issues.

## Features
- Generate directory structure in JSON or text format.
- Prompt user for directory path and output format.
- Save output to `DIR_STRUCTURE_OUTPUT(JSON).md` (for JSON) or `DIR_STRUCTURE_OUTPUT(TEXT).md` (for text) in a Markdown code block.
- Handle errors like non-existent directories or permission-denied access.
- Sort directory contents for consistent output.

## Requirements
- Python 3.10 or higher
- No external dependencies (uses standard library modules: `pathlib` and `json`)

## Usage
1. Save the script as `dir_structure.py`.
2. Run the script using:
   ```bash
   python dir_structure.py
   ```
3. Follow the prompts:
   - **Enter the directory path**: Provide the path to the directory (e.g., `.` for the current directory).
   - **Enter output format**: Choose `json` or `text` (defaults to `text` if invalid).
   - **Save to output file**: Choose `yes` to save to `DIR_STRUCTURE_OUTPUT(JSON).md` (for JSON) or `DIR_STRUCTURE_OUTPUT(TEXT).md` (for text), or `no` to skip.

### Example Run
```bash
$ python dir_structure.py
Enter the directory path (e.g., . for current directory): ./example_project
Enter output format (json or text): json
{
  "name": "example_project",
  "type": "directory",
  "contents": [
    {
      "name": "src",
      "type": "directory",
      "contents": [
        {
          "name": "main.py",
          "type": "file"
        },
        {
          "name": "utils",
          "type": "directory",
          "contents": [
            {
              "name": "helper.py",
              "type": "file"
            }
          ]
        }
      ]
    },
    {
      "name": "tests",
      "type": "directory",
      "contents": [
        {
          "name": "test_main.py",
          "type": "file"
        }
      ]
    },
    {
      "name": "README.md",
      "type": "file"
    }
  ]
}
Do you want to save the structure to DIR_STRUCTURE_OUTPUT(JSON).md? (yes/no): yes
Directory structure saved to DIR_STRUCTURE_OUTPUT(JSON).md in json format.
```

## Example Outputs

### JSON Format
When saved, the JSON output is written to `DIR_STRUCTURE_OUTPUT(JSON).md`:
```json
{
  "name": "example_project",
  "type": "directory",
  "contents": [
    {
      "name": "src",
      "type": "directory",
      "contents": [
        {
          "name": "main.py",
          "type": "file"
        },
        {
          "name": "utils",
          "type": "directory",
          "contents": [
            {
              "name": "helper.py",
              "type": "file"
            }
          ]
        }
      ]
    },
    {
      "name": "tests",
      "type": "directory",
      "contents": [
        {
          "name": "test_main.py",
          "type": "file"
        }
      ]
    },
    {
      "name": "README.md",
      "type": "file"
    }
  ]
}
```

### Text Format
When saved, the text output is written to `DIR_STRUCTURE_OUTPUT(TEXT).md`:
```text
example_project/
  ├── README.md
  ├── src/
  │   ├── main.py
  │   ├── utils/
  │   │   ├── helper.py
  ├── tests/
  │   ├── test_main.py
```

## Customization
You can modify the script to suit your needs:

### Exclude Specific Files or Directories
To skip directories like `.git` or `__pycache__`, add a filter in both `get_directory_structure_json` and `get_directory_structure_text` functions:
```python
for item in sorted(root_path.iterdir()):
    if item.name in {".git", "__pycache__"}:
        continue
```

### Add File Metadata
Enhance the JSON output with file details like size or modification time:
```python
if item.is_file():
    structure["contents"].append({
        "name": item.name,
        "type": "file",
        "size": item.stat().st_size,  # File size in bytes
        "last_modified": item.stat().st_mtime  # Last modified timestamp
    })
```

### Change Indentation or Symbols
Modify the `prefix` or `indent` in `get_directory_structure_text` to adjust the text output style (e.g., use `└──` or different indentation levels).

### Overwrite Instead of Append
To overwrite the output file instead of appending, change the file mode from `"a"` to `"w"` in `save_structure_to_readme`.

## Notes
- The script appends to the output file (`DIR_STRUCTURE_OUTPUT(JSON).md` or `DIR_STRUCTURE_OUTPUT(TEXT).md`) if it exists; otherwise, it creates a new file.
- Ensure you have write permissions for the directory where the output files are saved.
- The script handles errors gracefully, displaying `[Permission Denied]` or `"Directory does not exist"` as needed.
- The output filenames are fixed (`DIR_STRUCTURE_OUTPUT(JSON).md` for JSON, `DIR_STRUCTURE_OUTPUT(TEXT).md` for text) and cannot be customized in the current version.