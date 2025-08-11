from pathlib import Path
import json

def get_directory_structure_json(root_dir):
    """
    Generate a JSON representation of the directory structure starting from root_dir.
    Args:
        root_dir (str): Path to the root directory.
    Returns:
        dict: Dictionary representing the directory structure.
    """
    root_path = Path(root_dir)
    if not root_path.exists():
        return {"error": "Directory does not exist"}

    structure = {
        "name": root_path.name,
        "type": "directory",
        "contents": []
    }

    try:
        # Iterate over directory contents, sorted for consistent output
        for item in sorted(root_path.iterdir()):
            if item.is_dir():
                # Recursively get structure for subdirectories
                structure["contents"].append(get_directory_structure_json(item))
            else:
                # Add file
                structure["contents"].append({
                    "name": item.name,
                    "type": "file"
                })
    except PermissionError:
        structure["contents"].append({
            "name": "[Permission Denied]",
            "type": "error"
        })

    return structure

def get_directory_structure_text(root_dir, prefix="", level=0):
    """
    Generate a text-based directory structure starting from root_dir.
    Args:
        root_dir (str): Path to the root directory.
        prefix (str): Prefix for the current line (used for indentation).
        level (int): Current depth level for indentation.
    Returns:
        str: Text representation of the directory structure.
    """
    root_path = Path(root_dir)
    if not root_path.exists():
        return "Directory does not exist."

    structure = []
    indent = "  " * level  # Two spaces per level for indentation

    # Add the current directory
    structure.append(f"{prefix}{root_path.name}/")

    try:
        # Iterate over directory contents, sorted to ensure consistent output
        for item in sorted(root_path.iterdir()):
            if item.is_dir():
                # Recursively get structure for subdirectories
                structure.append(get_directory_structure_text(item, prefix=indent + "├── ", level=level + 1))
            else:
                # Add file with appropriate indentation
                structure.append(f"{indent}├── {item.name}")
    except PermissionError:
        structure.append(f"{indent}├── [Permission Denied]")

    return "\n".join(structure)

def save_structure_to_readme(root_dir, output_format):
    """
    Save the directory structure to a file in the specified format.
    Args:
        root_dir (str): Path to the root directory.
        output_format (str): Output format ('json' or 'text').
    """
    if output_format.lower() == "json":
        structure = get_directory_structure_json(root_dir)
        output = json.dumps(structure, indent=2)
        code_block = "json"
        output_path = "DIR_STRUCTURE_OUTPUT(JSON).md"
    else:
        structure = get_directory_structure_text(root_dir)
        output = structure
        code_block = "text"
        output_path = "DIR_STRUCTURE_OUTPUT(TEXT).md"

    with open(output_path, "a") as f:
        f.write("\n## Codebase Directory Structure\n\n")
        f.write(f"```{code_block}\n")
        f.write(output + "\n")
        f.write("```\n")

if __name__ == "__main__":
    # Prompt user for directory path
    root_directory = input("Enter the directory path (e.g., . for current directory): ").strip()
    if not root_directory:
        root_directory = "."  # Default to current directory if empty

    # Prompt user for output format
    output_format = input("Enter output format (json or text): ").strip().lower()
    if output_format not in ["json", "text"]:
        print("Invalid format. Using 'text' as default.")
        output_format = "text"

    # Generate and print the directory structure
    if output_format == "json":
        structure = get_directory_structure_json(root_directory)
        print(json.dumps(structure, indent=2))
    else:
        structure = get_directory_structure_text(root_directory)
        print(structure)

    # Optionally save to output file
    save_to_readme = input(f"Do you want to save the structure to DIR_STRUCTURE_OUTPUT({'JSON' if output_format == 'json' else 'TEXT'}).md? (yes/no): ").strip().lower()
    if save_to_readme == "yes":
        save_structure_to_readme(root_directory, output_format)
        print(f"Codebase directory structure saved to DIR_STRUCTURE_OUTPUT({'JSON' if output_format == 'json' else 'TEXT'}).md in {output_format} format.")