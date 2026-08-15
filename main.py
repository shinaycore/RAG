from uuid import uuid4
from pathlib import Path

from src.text_extractor import extract_text_from_pdf, save_pages_to_json
from src.text_preprocessing import TextPreprocessor
from src.chunker import TextChunker, save_chunks_to_json
from src.embedding import Embedder, save_embeddings_to_json
from src.vector_store import VectorStore

from config.logger import get_logger
log = get_logger(__name__)

# class objects
preprocessor = TextPreprocessor()
chunker = TextChunker(chunk_size=300, chunk_overlap=0)
embedder = Embedder()

# Extraction
pdf_path = Path("assets/claude_code.pdf")
pages = extract_text_from_pdf(pdf_path)

# Cleaning the text
log.info("Cleaning extracted text")
cleaned_pages = preprocessor.clean_pages(pages)

# Saving extracted and cleaned output to desired location
output_path = (
    Path("data/extracted")
    / f"{pdf_path.stem}_{uuid4().hex}.json"
)
save_pages_to_json(cleaned_pages, output_path)

# Chunking
chunks = chunker.chunk_pages(cleaned_pages)

chunk_output_path = (
    Path("data/chunked")
    / f"{pdf_path.stem}_chunks_{uuid4().hex}.json"
)
save_chunks_to_json(chunks, chunk_output_path)

# Embedding
embeddings = embedder.embed_chunks(chunks)

embedding_output_path = (
    Path("data/embedded")
    / f"{pdf_path.stem}_embeddings_{uuid4().hex}.json"
)
save_embeddings_to_json(chunks, embeddings, embedding_output_path)

# Vector Store
vector_store = VectorStore()
vector_store.add_chunks(chunks, embeddings)