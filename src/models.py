from dataclasses import dataclass, field
from uuid import uuid4


@dataclass(slots=True)
class Page:
    page_number: int
    text: str
    source: str

@dataclass(slots=True)
class Chunk:
    text: str
    page_number: int
    source: str

    chunk_id: str = field(default_factory=lambda: str(uuid4()))