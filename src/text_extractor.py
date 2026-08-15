import pymupdf
from pathlib import Path
from dataclasses import dataclass, asdict
import json

from src.models import Page

from config.logger import get_logger
log = get_logger(__name__)

def extract_text_from_pdf(pdf_path: Path) -> list[Page]:
    """
    Extract text from a PDF and return a list of Page objects.
    """

    if not pdf_path.exists():
        log.error(f"PDF Location Invalid: {pdf_path}")
        raise FileNotFoundError(f"No PDF found at: {pdf_path}")

    log.info(f"Extracting text from PDF: {pdf_path}")

    pages: list[Page] = []

    with pymupdf.open(pdf_path) as doc:
        for page_num in range(doc.page_count):
            page = doc.load_page(page_num)

            text: str = page.get_text("text")

            pages.append(
                Page(
                    page_number=page_num + 1,
                    text=text,
                    source=pdf_path.name,
                )
            )

    return pages

def save_pages_to_json(
    pages: list[Page],
    output_path: Path,
) -> None:
    """
    Save extracted pages to a JSON file.
    """

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(
            [asdict(page) for page in pages],
            f,
            indent=2,
            ensure_ascii=False,
        )

    log.info(f"Saved {len(pages)} pages to {output_path}")

# import pymupdf
# from pathlib import Path
# import json

# from config.logger import get_logger
# log = get_logger(__name__)

# # function to extract text from a PDF file and return it as a list of dictionaries, 
# # where each dictionary contains the page number and the extracted text from that page.
# def extract_text_from_pdf(pdf_path: str) -> list[dict]:

#     if not Path(pdf_path).exists():
#         log.error(f"PDF Location Invalid: {pdf_path}")
#         raise FileNotFoundError(f"No PDF found at: {pdf_path}")

#     log.info(f"Extracting text from PDF: {pdf_path}")
#     doc = pymupdf.open(pdf_path)
#     pages = []

#     for page_num, page in enumerate(doc):
#         text = page.get_text()
#         pages.append({"page_number": page_num + 1, "text": text})

#     doc.close()
#     return pages

# # function to save the extracted text from the PDF pages to a JSON file.
# def save_pages_to_json(pages: list[dict], output_path: str) -> None:

#     output_file = Path(output_path)
#     output_file.parent.mkdir(parents=True, exist_ok=True)

#     with open(output_file, "w", encoding="utf-8") as f:
#         json.dump(pages, f, indent=2, ensure_ascii=False)

#     log.info(f"Saved {len(pages)} pages to {output_file}")     