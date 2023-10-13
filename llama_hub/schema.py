from typing import TYPE_CHECKING
from llama_index.schema import Document as LI_Document

if TYPE_CHECKING:
    from langchain.docstore.document import Document as LC_Document


class Document(LI_Document):

    def to_langchain_format(self) -> LC_Document:
        """Convert struct to LangChain document format."""
        from langchain.docstore.document import Document as LC_Document

        metadata = self.metadata or {}
        return LC_Document(page_content=self.text, metadata=metadata)
    