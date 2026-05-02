#!/usr/bin/env python3
"""Generate a professional PDF from the pandas guide MD files using fpdf2."""

import re
import os
from pathlib import Path
from fpdf import FPDF

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

FONT_DIR = "/usr/share/fonts/TTF"

class GuidePDF(FPDF):
    def __init__(self):
        super().__init__()
        self.add_font("DejaVu", "", f"{FONT_DIR}/DejaVuSans.ttf")
        self.add_font("DejaVu", "B", f"{FONT_DIR}/DejaVuSans-Bold.ttf")
        self.add_font("DejaVu", "I", f"{FONT_DIR}/DejaVuSans-Oblique.ttf")
        self.add_font("DejaVu", "BI", f"{FONT_DIR}/DejaVuSans-BoldOblique.ttf")
        self.set_auto_page_break(auto=True, margin=15)

    def add_md_content(self, text):
        lines = text.split('\n')
        in_code = False
        code_lines = []
        in_table = False
        table_rows = []

        for line in lines:
            # Code blocks
            if line.strip().startswith('```'):
                if in_code:
                    self._flush_code(code_lines)
                    code_lines = []
                    in_code = False
                else:
                    in_code = True
                continue
            if in_code:
                code_lines.append(line)
                continue

            # Tables
            if line.strip().startswith('|') and line.strip().endswith('|'):
                cells = [c.strip() for c in line.split('|')[1:-1]]
                if all(re.match(r'^[-:]+$', c) for c in cells):
                    continue
                if not in_table:
                    in_table = True
                    table_rows = []
                table_rows.append(cells)
                continue
            else:
                if in_table and table_rows:
                    self._flush_table(table_rows)
                    table_rows = []
                    in_table = False

            # Empty line
            if not line.strip():
                self.ln(4)
                continue

            # Headers
            if line.startswith('#### '):
                self.set_font("DejaVu", "I", 10)
                self.multi_cell(0, 6, line[5:])
                self.ln(2)
            elif line.startswith('### '):
                self.set_font("DejaVu", "B", 12)
                self.multi_cell(0, 7, line[4:])
                self.ln(3)
            elif line.startswith('## '):
                self.set_font("DejaVu", "B", 14)
                self.multi_cell(0, 8, line[3:])
                self.ln(4)
            elif line.startswith('# '):
                self.add_page()
                self.set_font("DejaVu", "B", 18)
                self.multi_cell(0, 10, line[2:])
                self.ln(6)
            # Images
            elif line.startswith('!['):
                match = re.search(r'!\[([^\]]*)\]\(([^)]+)\)', line)
                if match:
                    img_path = GUIDE_DIR / match.group(2)
                    if img_path.exists():
                        self.image(str(img_path), x=10, w=190)
                        self.ln(4)
            # Horizontal rule
            elif line.strip() == '---':
                self.set_draw_color(200, 200, 200)
                self.line(10, self.get_y(), 200, self.get_y())
                self.ln(4)
            # Lists
            elif line.startswith('- ') or line.startswith('* '):
                self.set_font("DejaVu", "", 10)
                self.set_x(15)
                self.cell(5, 5, "•")
                self.multi_cell(0, 5, line[2:])
                self.ln(1)
            elif re.match(r'^\d+\. ', line):
                self.set_font("DejaVu", "", 10)
                self.set_x(15)
                self.multi_cell(0, 5, line)
                self.ln(1)
            # Blockquotes
            elif line.startswith('> '):
                self.set_font("DejaVu", "I", 10)
                self.set_text_color(59, 130, 246)
                self.set_x(15)
                self.multi_cell(0, 5, line[2:])
                self.set_text_color(0, 0, 0)
                self.ln(2)
            # Regular text
            else:
                self.set_font("DejaVu", "", 10)
                # Handle inline formatting
                clean_line = re.sub(r'\*\*\*(.+?)\*\*\*', r'<b><i>\1</i></b>', line)
                clean_line = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', clean_line)
                clean_line = re.sub(r'\*(.+?)\*', r'<i>\1</i>', clean_line)
                clean_line = re.sub(r'`([^`]+)`', r'<code>\1</code>', clean_line)
                clean_line = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'\1', clean_line)  # Strip links for PDF
                # Replace em-dash and other chars
                clean_line = clean_line.replace('—', '--').replace('–', '-')
                self.multi_cell(0, 5, clean_line)
                self.ln(2)

        if in_code:
            self._flush_code(code_lines)
        if in_table and table_rows:
            self._flush_table(table_rows)

    def _flush_code(self, lines):
        self.set_font("DejaVu", "", 8)
        self.set_fill_color(30, 41, 59)
        self.set_text_color(226, 232, 240)
        self.ln(2)
        y_start = self.get_y()
        for line in lines:
            if self.get_y() > 270:
                self.add_page()
                y_start = self.get_y()
            self.set_x(10)
            self.cell(0, 4, line, fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_text_color(0, 0, 0)
        self.ln(4)

    def _flush_table(self, rows):
        if not rows:
            return
        self.ln(4)
        col_width = 190 / len(rows[0])
        for i, row in enumerate(rows):
            if self.get_y() > 260:
                self.add_page()
            self.set_font("DejaVu", "B" if i == 0 else "", 9)
            self.set_fill_color(249, 250, 251)
            for j, cell in enumerate(row):
                cell = cell.replace('—', '-').replace('–', '-')
                self.cell(col_width, 6, cell, border=1, fill=True)
            self.ln()
        self.ln(4)

def main():
    pdf = GuidePDF()
    for fname in MD_FILES:
        fpath = GUIDE_DIR / fname
        if fpath.exists():
            content = fpath.read_text(encoding='utf-8')
            # Clean problematic chars
            content = content.replace('—', '--').replace('–', '-')
            content = re.sub(r'[\U00010000-\U0010ffff]', '', content)
            pdf.add_md_content(content)

    out_path = GUIDE_DIR / "Pandas-Master-Guide.pdf"
    pdf.output(str(out_path))
    print(f"PDF generated: {out_path}")
    print(f"Size: {out_path.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    main()
