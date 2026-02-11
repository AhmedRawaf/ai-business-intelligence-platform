from pathlib import Path
import pandas as pd
from docx import Document as DocxDocument
from pypdf import PdfReader


def parse_pdf(file_path: str) -> tuple[str, list[dict]]:
    reader = PdfReader(file_path)
    pages = []
    for page_number, page in enumerate(reader.pages, start=1):
        pages.append({"page": page_number, "text": page.extract_text() or ""})
    full_text = "\n\n".join(page["text"] for page in pages)
    return full_text, []


def parse_docx(file_path: str) -> tuple[str, list[dict]]:
    doc = DocxDocument(file_path)
    full_text = "\n".join(paragraph.text for paragraph in doc.paragraphs if paragraph.text.strip())
    return full_text, []


def parse_spreadsheet(file_path: str) -> tuple[str, list[dict]]:
    tables = []
    if file_path.endswith(".csv"):
        df = pd.read_csv(file_path)
        tables.append({"sheet": "csv", "columns": list(df.columns), "rows": df.head(200).fillna("").to_dict(orient="records")})
    else:
        xls = pd.ExcelFile(file_path)
        for sheet_name in xls.sheet_names:
            df = pd.read_excel(xls, sheet_name=sheet_name)
            tables.append(
                {"sheet": sheet_name, "columns": list(df.columns), "rows": df.head(200).fillna("").to_dict(orient="records")}
            )
    text = "\n".join(f"{table['sheet']}: {len(table['rows'])} rows" for table in tables)
    return text, tables


def parse_document_file(file_path: str) -> tuple[str, list[dict]]:
    suffix = Path(file_path).suffix.lower()
    if suffix == ".pdf":
        return parse_pdf(file_path)
    if suffix == ".docx":
        return parse_docx(file_path)
    if suffix in {".csv", ".xlsx"}:
        return parse_spreadsheet(file_path)
    raise ValueError("Unsupported file type.")
