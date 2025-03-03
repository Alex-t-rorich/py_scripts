#!/usr/bin/env python3
import os
import sys
from pathlib import Path

# Common files and directories to ignore (similar to .gitignore patterns)
IGNORE_PATTERNS = [
    "__pycache__",
    "*.pyc",
    "*.pyo",
    "*.pyd",
    ".Python",
    "env/",
    "venv/",
    "ENV/",
    ".env",
    ".venv",
    "build/",
    "develop-eggs/",
    "dist/",
    "downloads/",
    "eggs/",
    ".eggs/",
    "lib/",
    "lib64/",
    "parts/",
    "sdist/",
    "var/",
    "*.egg-info/",
    ".installed.cfg",
    "*.egg",
    ".git/",
    ".idea/",
    ".vscode/",
    "node_modules/",
    "*.so",
    ".DS_Store",
    "Thumbs.db",
]

def should_ignore(path, ignore_patterns):
    """Check if a path should be ignored based on patterns."""
    path_str = str(path)
    
    for pattern in ignore_patterns:
        # Handle directory patterns (ending with /)
        if pattern.endswith('/'):
            if pattern[:-1] in path_str.split(os.sep):
                return True
        # Handle wildcard patterns
        elif pattern.startswith('*'):
            if path_str.endswith(pattern[1:]):
                return True
        # Handle exact matches
        elif pattern in path_str.split(os.sep):
            return True
    
    return False

def print_tree(directory, prefix="", ignore_patterns=None):
    """Print the directory tree structure."""
    if ignore_patterns is None:
        ignore_patterns = []
    
    directory = Path(directory)
    
    # Get all items in the directory
    items = list(directory.iterdir())
    items = sorted(items, key=lambda x: (not x.is_dir(), x.name.lower()))
    
    # Count items (excluding ignored ones)
    count = len([item for item in items if not should_ignore(item, ignore_patterns)])
    
    # Process each item
    for i, item in enumerate(items):
        # Skip if item should be ignored
        if should_ignore(item, ignore_patterns):
            continue
        
        # Is this the last item?
        is_last = i == count - 1
        
        # Print the item
        if is_last:
            print(f"{prefix}└── {item.name}")
            next_prefix = prefix + "    "
        else:
            print(f"{prefix}├── {item.name}")
            next_prefix = prefix + "│   "
        
        # Recursively print subdirectories
        if item.is_dir():
            print_tree(item, next_prefix, ignore_patterns)

if __name__ == "__main__":
    # Get the target directory from command line argument or use the current directory
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    project_name = os.path.basename(os.path.abspath(target_dir))
    print(f"{project_name}/")
    print_tree(target_dir, ignore_patterns=IGNORE_PATTERNS)
