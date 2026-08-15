import re

from src.models import Page
from dataclasses import replace

from config.logger import get_logger
log = get_logger(__name__)

class TextPreprocessor:
    """
    Handles text preprocessing for extracted documents.
    """

    def clean_text(self, text: str) -> str:
        """
        Apply minimal cleanup while preserving document structure.
        """

        text = re.sub(r"\n{3,}", "\n\n", text)
        text = re.sub(r"[ \t]+", " ", text)
        text = "\n".join(line.rstrip() for line in text.split("\n"))

        return text.strip()

    def clean_pages(self, pages: list[Page]) -> list[Page]:
        return [
            replace(
                page,
                text=self.clean_text(page.text),
            )
            for page in pages
        ]