"""Split extracted pages into overlapping chunks of roughly 500–800 words.

LangChain's recursive splitter supplies the separator hierarchy. Word count is
the length function so the chunk size matches the project specification.
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter

from app.services.nlp_service import clean_text, remove_duplicate_paragraphs

_splitter = RecursiveCharacterTextSplitter(
    chunk_size=700,
    chunk_overlap=100,
    length_function=lambda text: max(1, len(text.split())),
    separators=["\n\n", "\n", ". ", "? ", "! ", "; ", " ", ""],
)


def prepare_pages(pages: list[dict]) -> list[dict]:
    prepared = []
    for page in pages:
        text = remove_duplicate_paragraphs(clean_text(page.get("text", "")))
        if text:
            prepared.append({"page_number": page.get("page_number"), "text": text})
    return prepared


def chunk_pages(pages: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    seen: set[str] = set()
    for page in prepare_pages(pages):
        pieces = _splitter.split_text(page["text"])
        for piece in pieces:
            content = piece.strip()
            if len(content.split()) < 20 or content in seen:
                continue
            seen.add(content)
            chunks.append(
                {
                    "content": content,
                    "page_number": page["page_number"],
                    "token_count": len(content.split()),
                }
            )
    return chunks
