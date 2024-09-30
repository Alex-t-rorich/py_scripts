# Activate venv
# python format_image_names.py foldertolookat

import os
import sys
import re
from collections import defaultdict


def clean_filename(filename):
    name, ext = os.path.splitext(filename)
    name = name.lower()
    name = name.replace(" ", "-")
    name = re.sub(r"v?\d+", "", name)
    name = re.sub(r"[^a-z-]", "", name)
    name = name.strip("-")
    name = re.sub(r"-+", "-", name)

    return name, ext


def rename_files(root_dir):
    new_names = {}
    filename_count = defaultdict(int)
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            clean_name, ext = clean_filename(filename)
            new_names[os.path.join(dirpath, filename)] = f"{clean_name}{ext}"
            filename_count[clean_name] += 1

    for old_path, new_name in new_names.items():
        dirpath, filename = os.path.split(old_path)
        name, ext = os.path.splitext(new_name)

        if filename_count[name] > 1:
            filename_count[name] -= 1
            new_name = f"{name}_{filename_count[name]}{ext}"

        new_path = os.path.join(dirpath, new_name)

        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"Renamed file: {filename} -> {new_name}")


# Usage
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python rename_files.py <subfolder_name>")
        print("Example: python rename_files.py suiting")
        sys.exit(1)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    subfolder_name = sys.argv[1]
    root_directory = os.path.join(parent_dir, "swatches", subfolder_name)

    if not os.path.isdir(root_directory):
        print(f"Error: '{root_directory}' is not a valid directory.")
        sys.exit(1)

    print(f"Processing directory: {root_directory}")
    rename_files(root_directory)
