#!/usr/bin/env python3
"""
find_unused_css_files.py
------------------------
A tiny utility that scans a folder (and all its sub-folders) for:

1. Every *.html file – it reads each one and notes every CSS filename it refers to.
2. Every *.css file actually present on disk.

It then prints:
• The CSS files that **are** referenced by some HTML file.
• The CSS files that **are NOT** referenced by any HTML file.

Matching is done **by filename only** (ignores paths) to cope with mismatched
relative/absolute paths in the HTML.
"""

# ========== Imports ========== #
import os                          # Standard library: directory walking
import re                          # Regular expressions to spot “something.css”
import sys                         # For optional command-line argument
from pathlib import Path           # Path objects are more convenient than strings
from collections import defaultdict # For grouping duplicate filenames

# ========== Global-scope “constants” ========== #
# Default directory to scan – current working directory.  
# Override by running:  python find_unused_css_files.py /path/to/site
TARGET_DIR = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()

# Regex that finds any substring ending in “.css” (case-insensitive)
CSS_FILENAME_REGEX = re.compile(r'([\w\-.]+\.css)', re.IGNORECASE)

# ========== Helper Functions ========== #
def collect_files(root_dir: Path, extension: str):
    """
    Walk through every file under *root_dir* and return a list of Paths
    that end with the given *extension* (e.g. '.html' or '.css').

    Args:
        root_dir (Path): Folder to scan.
        extension (str): File-name suffix to filter by.

    Returns:
        list[Path]: All matching files.
    """
    print(f"[collect_files] 🔍 Looking for *{extension} files inside {root_dir}")
    matches = []                                   # Empty list to fill up
    for folder, _subfolders, filenames in os.walk(root_dir):
        for name in filenames:
            if name.lower().endswith(extension.lower()):
                file_path = Path(folder) / name
                matches.append(file_path)
                print(f"  ↳ Found {file_path}")
    return matches


def extract_css_filenames_from_html(html_file: Path):
    """
    Read one HTML file and pull out every `something.css` token.

    Args:
        html_file (Path): The .html file to inspect.

    Returns:
        set[str]: All distinct CSS filenames (lower-case, no path) mentioned.
    """
    print(f"[extract] 📝 Scanning HTML for CSS references: {html_file}")
    try:
        content = html_file.read_text(encoding="utf-8", errors="ignore")
    except Exception as err:
        print(f"    ⚠️  Could not read {html_file}: {err}")
        return set()

    # Find all occurrences of *.css (href, @import, inline, etc.)
    found = CSS_FILENAME_REGEX.findall(content)
    # Lower-case the names so matching is case-insensitive
    cleaned = {Path(name).name.lower() for name in found}
    if cleaned:
        print(f"    → Found references: {', '.join(sorted(cleaned))}")
    return cleaned


def group_css_by_filename(css_paths):
    """
    Build a dict mapping *filename* → [all Path objects with that filename].

    Helps handle projects where the same file name exists in multiple folders.

    Args:
        css_paths (list[Path]): Every CSS file found on disk.

    Returns:
        dict[str, list[Path]]
    """
    grouped = defaultdict(list)
    for path in css_paths:
        grouped[path.name.lower()].append(path)
    return grouped

# ========== Main Procedure ========== #
def main():
    """Run the full scan and print summary tables."""
    print(f"\n=== find_unused_css_files started for: {TARGET_DIR} ===\n")

    # 1. Gather every *.html and *.css file on disk.
    html_files = collect_files(TARGET_DIR, ".html")
    css_files  = collect_files(TARGET_DIR, ".css")

    # 2. Build a set of every CSS filename referenced somewhere in HTML.
    referenced_css_names = set()
    for html in html_files:
        referenced_css_names.update(extract_css_filenames_from_html(html))

    # 3. Build lookup: filename -> [full paths] for every CSS file on disk.
    css_on_disk = group_css_by_filename(css_files)

    # 4. Work out which are used and which are unused.
    used_css_files    = []
    unused_css_files  = []

    for filename, paths in css_on_disk.items():
        if filename in referenced_css_names:
            used_css_files.extend(paths)   # These paths are considered “used”
        else:
            unused_css_files.extend(paths) # No HTML referenced this filename

    # 5. Pretty-print results.
    print("\n================= SUMMARY =================\n")

    print("✅ CSS files referenced by at least one HTML file:")
    if used_css_files:
        for path in used_css_files:
            print(f"   • {path}")
    else:
        print("   (none)")

    print("\n🗑️  CSS files NOT referenced anywhere (potentially removable):")
    if unused_css_files:
        for path in unused_css_files:
            print(f"   • {path}")
    else:
        print("   (none)")

    print("\n===========================================\n")
    print("Finished! 🚀")

# ========== Script Entry-Point ========== #
if __name__ == "__main__":
    main()
