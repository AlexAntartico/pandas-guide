#!/usr/bin/env python3
"""Generate pandas-guide.html from all markdown module files."""

import re
from pathlib import Path
import markdown

GUIDE_DIR = Path(__file__).parent

MD_FILES = [
    "README.md",
    "MODULE-00-GETTING-STARTED.md",
    "MODULE-01a-DATA-INGESTION-CSV-JSON.md",
    "MODULE-01b-DATA-INGESTION-EXCEL-SQL-API.md",
    "MODULE-02a-DATA-EXPLORATION-BASIC.md",
    "MODULE-02b-DATA-EXPLORATION-ADVANCED.md",
    "MODULE-03a-DATA-CLEANING-MISSING.md",
    "MODULE-03b-DATA-CLEANING-PATTERNS.md",
    "MODULE-04a-DATA-MANIPULATION-INDEXING.md",
    "MODULE-04b-DATA-MANIPULATION-GROUPBY-MERGE.md",
    "MODULE-05a-DATA-TRANSFORMATION-PIVOT-RESHAPE.md",
    "MODULE-05b-DATA-TRANSFORMATION-STRINGS-TIMESERIES.md",
    "MODULE-06a-VISUALIZATION-BASIC.md",
    "MODULE-06b-VISUALIZATION-ADVANCED.md",
    "MODULE-07a-DATA-EXPORT-CSV-EXCEL.md",
    "MODULE-07b-DATA-EXPORT-JSON-SQL-PARQUET.md",
    "MODULE-08a-PRODUCTION-PERFORMANCE.md",
    "MODULE-08b-PRODUCTION-PATTERNS.md",
]

CSS = """
body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    line-height: 1.6;
    color: #1f2937;
    max-width: 900px;
    margin: 0 auto;
    padding: 20px;
    background: #fff;
}
h1 { color: #1e40af; border-bottom: 2px solid #e5e7eb; padding-bottom: 8px; margin-top: 40px; }
h2 { color: #1e3a8a; border-bottom: 1px solid #e5e7eb; padding-bottom: 6px; margin-top: 32px; }
h3 { color: #374151; margin-top: 24px; }
h4 { color: #4b5563; margin-top: 20px; }
code {
    background: #f3f4f6;
    padding: 2px 6px;
    border-radius: 4px;
    font-family: "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
    font-size: 0.9em;
    color: #dc2626;
}
pre {
    background: #1e293b;
    color: #e2e8f0;
    padding: 16px;
    border-radius: 8px;
    overflow-x: auto;
    font-size: 0.85em;
    line-height: 1.4;
    margin: 16px 0;
}
pre code {
    background: none;
    color: inherit;
    padding: 0;
    border-radius: 0;
    font-size: inherit;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin: 20px 0;
    font-size: 0.9em;
}
th, td {
    border: 1px solid #d1d5db;
    padding: 8px 12px;
    text-align: left;
}
th { background: #f9fafb; font-weight: 600; }
tr:nth-child(even) { background: #f9fafb; }
img {
    max-width: 100%;
    height: auto;
    border: 1px solid #e5e7eb;
    border-radius: 8px;
    margin: 16px 0;
    display: block;
}
blockquote {
    border-left: 4px solid #3b82f6;
    margin: 16px 0;
    padding: 8px 16px;
    background: #eff6ff;
    color: #1e40af;
}
blockquote.jupyter-note {
    border-left: 4px solid #f59e0b;
    background: #fffbeb;
    color: #78350f;
}
blockquote.jupyter-note code {
    background: #fef3c7;
    color: #92400e;
}
blockquote.jupyter-note pre {
    background: #1c1917;
}
ul, ol { padding-left: 24px; }
li { margin-bottom: 4px; }
hr { border: none; border-top: 1px solid #e5e7eb; margin: 32px 0; }
a { color: #2563eb; text-decoration: none; }
a:hover { text-decoration: underline; }
.page-break { page-break-after: always; }
@media print {
    body { padding: 0; }
    pre { page-break-inside: avoid; }
    img { page-break-inside: avoid; max-width: 100%; }
    h1, h2, h3 { page-break-after: avoid; }
    blockquote { page-break-inside: avoid; }
}
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Pandas Master Guide</title>
    <style>
{css}
    </style>
</head>
<body>
{body}
</body>
</html>"""


def convert_md(text: str) -> str:
    md = markdown.Markdown(extensions=["extra"])
    html = md.convert(text)
    # Give JupyterLab callout blockquotes a distinct class
    html = re.sub(
        r"<blockquote>\s*\n\s*<p><strong>JupyterLab:",
        '<blockquote class="jupyter-note">\n<p><strong>JupyterLab:',
        html,
    )
    return html


def main():
    sections = []
    for fname in MD_FILES:
        fpath = GUIDE_DIR / fname
        if not fpath.exists():
            print(f"  WARNING: {fname} not found, skipping")
            continue
        content = fpath.read_text(encoding="utf-8")
        sections.append(convert_md(content))
        print(f"  converted {fname}")

    body = "\n<hr>\n".join(sections)
    output = HTML_TEMPLATE.format(css=CSS, body=body)

    out_path = GUIDE_DIR / "pandas-guide.html"
    out_path.write_text(output, encoding="utf-8")
    print(f"\nHTML generated: {out_path}  ({out_path.stat().st_size / 1024:.1f} KB)")


if __name__ == "__main__":
    main()
