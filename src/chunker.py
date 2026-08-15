from src.models import Page, Chunk

class TextChunker:
    def __init__(
        self,
        chunk_size: int = 300,
        chunk_overlap: int = 0,
    ):

        def chunk_pages(self, pages: list[Page]) -> list[Chunk]:
            """
            Split pages into chunks while preserving metadata.
            """

            chunks: list[Chunk] = []

            for page in pages:
                ...
                # Split the page's text
                text = page.text
                # Convert each split into a Chunk
                ...

            return chunks

    # def _token_length(self):
    # def splitter(self):