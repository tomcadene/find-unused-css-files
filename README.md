# 🕵️‍♂️ find-unused-css-files

A tiny command‑line helper that keeps your web projects tidy by spotting unused CSS files.

It crawls a folder (and every sub‑folder), compares every real *.css file on disk with every *.html file, and prints a clear summary:

✅ Used CSS files – referenced by at least one HTML file.

🗑️ Unused CSS files – never referenced (safe to delete or archive).

Matching is done by filename only so it still works when the <link href="..."> paths in your HTML don’t match your actual folder structure.

## Features

🗂️ Recursively scans any directory you point it at.

🔍 Uses a simple regular‑expression to find CSS references in HTML (works for <link>, @import, inline scripts, etc.).

🔄 Case‑insensitive filename matching.

💡 Zero third‑party dependencies – standard library only.

🖨️ Clear, colour‑free console logs (plays nicely with any terminal)

## Requirements

Python 3.8 or newer (tested on 3.8 → 3.12)

That’s it – no extra libraries to install

## Installation

```
# 1) Clone the repository (or download the single script)
 git clone https://github.com/your‑username/find_unused_css_files.git
 cd find_unused_css_files

# 2) (Optional) Create and activate a virtual‑env
 python -m venv .venv
 source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 3) No pip install needed – the script is self‑contained.
```

## Usage

Basic scan - Scans the current directory and everything inside it.  

```python find_unused_css_files.py```

Specifying a folder - Replace the path with the root folder of your website/project.  

```python find_unused_css_files.py /path/to/your/project/root```

Example Output
```
=== find_unused_css_files started for: /home/me/site ===

✅ CSS files referenced by at least one HTML file:
   • /home/me/site/css/main.css
   • /home/me/site/css/theme/dark.css

🗑️  CSS files NOT referenced anywhere (potentially removable):
   • /home/me/site/css/old/reset.css
   • /home/me/site/css/unused/print.css

Finished! 🚀
```


