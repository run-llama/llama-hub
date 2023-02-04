"""Base schema for Documents."""
from abc import abstractmethod
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from dataclasses_json import DataClassJsonMixin


@dataclass
class BaseDocument(DataClassJsonMixin):
    """Base document.
    Generic abstract interfaces that captures both index structs
    as well as documents.
    """

    # TODO: consolidate fields from Document/IndexStruct into base class
    text: Optional[str] = None
    doc_id: Optional[str] = None
    embedding: Optional[List[float]] = None

    # extra fields
    extra_info: Optional[Dict[str, Any]] = None

    @classmethod
    @abstractmethod
    def get_type(cls) -> str:
        """Get Document type."""

    def get_text(self) -> str:
        """Get text."""
        if self.text is None:
            raise ValueError("text field not set.")
        return self.text

    def get_doc_id(self) -> str:
        """Get doc_id."""
        if self.doc_id is None:
            raise ValueError("doc_id not set.")
        return self.doc_id

    @property
    def is_doc_id_none(self) -> bool:
        """Check if doc_id is None."""
        return self.doc_id is None

    def get_embedding(self) -> List[float]:
        """Get embedding.
        Errors if embedding is None.
        """
        if self.embedding is None:
            raise ValueError("embedding not set.")
        return self.embedding

    @property
    def extra_info_str(self) -> Optional[str]:
        """Extra info string."""
        if self.extra_info is None:
            return None

        return "\n".join([f"{k}: {str(v)}" for k, v in self.extra_info.items()])


@dataclass
class Document(BaseDocument):
    """Generic interface for a data document.
    This document connects to data sources.
    """

    def __post_init__(self) -> None:
        """Post init."""
        if self.text is None:
            raise ValueError("text field not set.")

    @classmethod
    def get_type(cls) -> str:
        """Get Document type."""
        return "Document"

    # def to_langchain_format(self) -> LCDocument:
    #     """Convert struct to LangChain document format."""
    #     metadata = self.extra_info or {}
    #     return LCDocument(page_content=self.text, metadata=metadata)

    # @classmethod
    # def from_langchain_format(cls, doc: LCDocument) -> "Document":
    #     """Convert struct from LangChain document format."""
    #     return cls(text=doc.page_content, extra_info=doc.metadata)
