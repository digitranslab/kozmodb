from typing import Optional

from langchain.text_splitter import RecursiveCharacterTextSplitter

from kozmochain.chunkers.base_chunker import BaseChunker
from kozmochain.config.add_config import ChunkerConfig
from kozmochain.helpers.json_serializable import register_deserializable


@register_deserializable
class DocxFileChunker(BaseChunker):
    """Chunker for .docx file."""

    def __init__(self, config: Optional[ChunkerConfig] = None):
        if config is None:
            config = ChunkerConfig(chunk_size=1000, chunk_overlap=0, length_function=len)
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=config.chunk_size,
            chunk_overlap=config.chunk_overlap,
            length_function=config.length_function,
        )
        super().__init__(text_splitter)
