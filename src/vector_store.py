import chromadb

from src.models import Chunk
from config.logger import get_logger

log = get_logger(__name__)


class VectorStore:
    def __init__(
        self,
        persist_directory: str = "data/chroma_db",
        collection_name: str = "rag_collection",
    ):
        self._client = chromadb.PersistentClient(path=persist_directory)
        self._collection = self._client.get_or_create_collection(name=collection_name)

        log.info(
            f"VectorStore initialized (collection={collection_name}, path={persist_directory})"
        )

    def add_chunks(self, chunks: list[Chunk], embeddings: list[list[float]]) -> None:
        """
        Adds chunks and their embeddings to the vector store.
        """
        log.info(f"Adding {len(chunks)} chunks to vector store")

        ids = [chunk.chunk_id for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [
            {"page_number": chunk.page_number, "source": chunk.source}
            for chunk in chunks
        ]

        self._collection.add(
            ids=ids,
            embeddings=embeddings,
            documents=documents,
            metadatas=metadatas,
        )

        log.info(f"Vector store now contains {self._collection.count()} total entries")

    def query(self, query_embedding: list[float], n_results: int = 5) -> dict:
        """
        Retrieves the top-k most similar chunks to a query embedding.
        """
        results = self._collection.query(
            query_embeddings=[query_embedding],
            n_results=n_results,
        )
        return results