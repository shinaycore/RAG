from dataclasses import replace
from uuid import uuid4
from pathlib import Path
from src.text_extractor import extract_text_from_pdf, save_pages_to_json
from src.text_preprocessing import TextPreprocessor

from config.logger import get_logger
log = get_logger(__name__)

# class objects
preprocessor = TextPreprocessor()

# Extraction text
pdf_path = Path("assets/claude_code.pdf")
pages = extract_text_from_pdf(pdf_path)

# Cleaning the text
log.info("Cleaning extracted text")
cleaned_pages = preprocessor.clean_pages(pages)

# Saving extracted and cleaned output to desired location
stem = Path(pdf_path).stem

output_path = (
    Path("data/extracted")
    / f"{pdf_path.stem}_{uuid4().hex}.json"
)
save_pages_to_json(cleaned_pages, output_path)

# Text Chunker