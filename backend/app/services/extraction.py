"""Extract plain text from PDF, DOCX, and TXT knowledge documents."""

from pathlib import Path


class ExtractionError(ValueError):
    pass


def extract_document(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    try:
        if suffix == ".txt":
            text = path.read_text(encoding="utf-8", errors="replace")
            return paginate_plaintext(text)
        if suffix == ".pdf":
            return extract_pdf(path)
        if suffix == ".docx":
            return extract_docx(path)
    except ExtractionError:
        raise
    except Exception as exc:
        raise ExtractionError(f"Could not extract text: {exc}") from exc
    raise ExtractionError("Only PDF, DOCX, and TXT files can be processed.")


def paginate_plaintext(text: str, words_per_page: int = 450) -> list[dict]:
    words = text.split()
    if not words:
        raise ExtractionError("The file does not contain readable text.")
    pages = []
    for start in range(0, len(words), words_per_page):
        chunk = " ".join(words[start : start + words_per_page])
        pages.append({"page_number": len(pages) + 1, "text": chunk})
    return pages


def extract_pdf(path: Path) -> list[dict]:
    import fitz

    document = fitz.open(path)
    try:
        if document.is_encrypted:
            raise ExtractionError("Encrypted PDF files are not supported.")
        pages = []
        for index, page in enumerate(document, start=1):
            if index > 200:
                break
            text = page.get_text("text") or ""
            if text.strip():
                pages.append({"page_number": index, "text": text})
    finally:
        document.close()
    if not pages:
        raise ExtractionError("No extractable text was found in the PDF.")
    return pages


def extract_docx(path: Path) -> list[dict]:
    import docx

    document = docx.Document(str(path))
    paragraphs = [paragraph.text.strip() for paragraph in document.paragraphs if paragraph.text.strip()]
    for table in document.tables:
        for row in table.rows:
            cells = [cell.text.strip() for cell in row.cells if cell.text.strip()]
            if cells:
                paragraphs.append(" | ".join(cells))
    if not paragraphs:
        raise ExtractionError("No extractable text was found in the DOCX file.")
    return paginate_plaintext("\n\n".join(paragraphs))
