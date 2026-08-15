from sentence_transformers import SentenceTransformer
from pathlib import Path
from dataclasses import asdict
import json

from src.models import Chunk
from config.logger import get_logger

log = get_logger(__name__)


class Embedder:
    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        batch_size: int = 32,
    ):
        self.model_name = model_name
        self.batch_size = batch_size
        self._model = SentenceTransformer(model_name)

        log.info(f"Embedder initialized (model={model_name}, batch_size={batch_size})")

    def embed_chunks(self, chunks: list[Chunk]) -> list[list[float]]:
        """
        Generates embeddings for a list of chunks, in batches.
        Returns a list of embedding vectors, in the same order as the input chunks.
        """
        log.info(f"Embedding {len(chunks)} chunks")
        texts = [chunk.text for chunk in chunks]

        embeddings = self._model.encode(
            texts,
            batch_size=self.batch_size,
            show_progress_bar=True,
        )

        log.info(f"Generated {len(embeddings)} embeddings")
        return embeddings.tolist()

def save_embeddings_to_json(
    chunks: list[Chunk],
    embeddings: list[list[float]],
    output_path: str | Path,
) -> None:
    """
    Saves embeddings to a JSON file, paired with their chunk_id for traceability.
    """
    output_file = Path(output_path)
    output_file.parent.mkdir(parents=True, exist_ok=True)

    records = [
        {"chunk_id": chunk.chunk_id, "embedding": embedding}
        for chunk, embedding in zip(chunks, embeddings)
    ]

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)

    log.info(f"Saved {len(records)} embeddings to {output_file}")