import tiktoken
from langchain_text_splitters import RecursiveCharacterTextSplitter
from pathlib import Path
from dataclasses import asdict
import json

from src.models import Page, Chunk
from config.logger import get_logger
log = get_logger(__name__)


class TextChunker:
    def __init__(
        self,
        chunk_size: int = 300,
        chunk_overlap: int = 0,
    ):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap
        self._tokenizer = tiktoken.get_encoding("cl100k_base")

        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            length_function=self._token_length,
        )

        log.info(
            f"TextChunker initialized (chunk_size={chunk_size}, chunk_overlap={chunk_overlap})"
        )

    def _token_length(self, text: str) -> int:
        """Counts tokens instead of characters, matching our embedding model's real limit."""
        return len(self._tokenizer.encode(text))

    # def chunk_pages(self, pages: list[Page]) -> list[Chunk]:
    #     """
    #     Split pages into chunks while preserving metadata.
    #     """
    #     log.info(f"Chunking {len(pages)} pages")
    #     chunks: list[Chunk] = []

    #     for page in pages:
    #         split_texts = self._splitter.split_text(page.text)

    #         for split_text in split_texts:
    #             chunk = Chunk(
    #                 text=split_text,
    #                 page_number=page.page_number,
    #                 source=page.source,
    #             )
    #             chunks.append(chunk)

    #     log.info(f"Produced {len(chunks)} chunks from {len(pages)} pages")
    #     return chunks

    def chunk_pages(self, pages: list[Page], min_chunk_tokens: int = 15) -> list[Chunk]:
        log.info(f"Chunking {len(pages)} pages")
        chunks: list[Chunk] = []
        skipped = 0

        for page in pages:
            split_texts = self._splitter.split_text(page.text)

            for split_text in split_texts:
                if self._token_length(split_text) < min_chunk_tokens:
                    skipped += 1
                    continue

                chunk = Chunk(
                    text=split_text,
                    page_number=page.page_number,
                    source=page.source,
                )
                chunks.append(chunk)

        log.info(f"Produced {len(chunks)} chunks from {len(pages)} pages ({skipped} tiny fragments skipped)")
        return chunks

def save_chunks_to_json(chunks: list[Chunk], output_path: str | Path) -> None:
    """
    Saves Chunk objects to a JSON file, creating parent dirs if needed.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    chunks_as_dicts = [asdict(chunk) for chunk in chunks]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(chunks_as_dicts, f, indent=2, ensure_ascii=False)

    log.info(f"Saved {len(chunks)} chunks to {output_file}")