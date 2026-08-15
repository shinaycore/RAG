import logging
from rich.logging import RichHandler

def get_logger(name: str = "rag_system") -> logging.Logger:
    """
    Returns a configured logger with Rich formatting:
    colored levels, timestamps, and clickable file/line links in supported terminals.
    """
    logging.basicConfig(
        level=logging.INFO,
        format="%(message)s",
        datefmt="[%X]",
        handlers=[RichHandler(rich_tracebacks=True, markup=True)]
    )
    return logging.getLogger(name)