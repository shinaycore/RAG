import json
import pymupdf
from pathlib import Path
from dataclasses import asdict

from src.models import Page
from config.logger import get_logger

log = get_logger(__name__)


def extract_text_from_pdf(pdf_path: str | Path) -> list[Page]:
    """
    Extracts text from a PDF, page by page.
    Returns a list of Page objects.
    """
    if not Path(pdf_path).exists():
        log.error(f"PDF Location Invalid: {pdf_path}")
        raise FileNotFoundError(f"No PDF found at: {pdf_path}")

    log.info(f"Extracting text from PDF: {pdf_path}")
    doc = pymupdf.open(pdf_path)
    pages = []

    for page_num, page in enumerate(doc):
        text = page.get_text()
        pages.append(
            Page(page_number=page_num + 1, text=text, source=str(pdf_path))
        )

    doc.close()
    return pages


def save_pages_to_json(pages: list[Page], output_path: str | Path) -> None:
    """
    Saves Page objects to a JSON file, creating parent dirs if needed.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    pages_as_dicts = [asdict(page) for page in pages]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(pages_as_dicts, f, indent=2, ensure_ascii=False)

    log.info(f"Saved {len(pages)} pages to {output_file}")