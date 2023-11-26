"""Vectara RAG Pack."""


from typing import Any, Dict, List, Optional

from llama_index.indices import VectaraIndex
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.schema import TextNode


class VectaraRagPack(BaseLlamaPack):
    """Vectara RAG pack."""

    def __init__(
        self,
        verbose: bool = True,
        nodes: Optional[List[TextNode]] = None,
        **kwargs: Any,
    ):
        self._index = VectaraIndex(nodes, verbose=verbose, **kwargs)

        similarity_top_k = kwargs.get("similarity_top_k", 5)
        n_sentences_before = kwargs.get("n_sentences_before", 2)
        n_sentences_after = kwargs.get("n_sentences_after", 2)
        vectara_query_mode = kwargs.get("vectara_query_mode", "default")
        vectara_kwargs = kwargs.get("vectara_kwargs", {})
        if "summary_enabled" not in vectara_kwargs:
            vectara_kwargs["summary_enabled"] = True
        self._query_engine = self._index.as_query_engine(
            similarity_top_k=similarity_top_k,
            n_sentences_before=n_sentences_before,
            n_sentences_after=n_sentences_after,
            vectara_query_mode=vectara_query_mode,
            vectara_kwargs=vectara_kwargs,
        )

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "index": self._index,
            "query_engine": self._query_engine,
        }

    def retrieve(self, query_str: str) -> Any:
        """Retrieve."""
        return self._query_engine.retrieve(query_str)

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self._query_engine.query(*args, **kwargs)
