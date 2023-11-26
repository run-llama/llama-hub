"""Redis Ingestion Pipeline Completion pack."""


from typing import Any, Dict, List

from llama_index.ingestion.cache import RedisCache, IngestionCache
from llama_index.ingestion.pipeline import IngestionPipeline
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.vector_stores import RedisVectorStore
from llama_index.schema import BaseNode, TransformComponent


class RedisIngestionPipelinePack(BaseLlamaPack):
    """Redis Ingestion Pipeline Completion pack."""

    def __init__(
        self,
        transformations: List[TransformComponent],
        hostname: str = "localhost",
        port: int = 6379,
        cache_collection_name: str = "ingest_cache",
        vector_collection_name: str = "vector_store",
        **kwargs: Any,
    ) -> None:
        """Init params."""

        self.vector_store = RedisVectorStore(
            hostname=hostname,
            port=port,
            collection_name=vector_collection_name,
        )

        self.ingest_cache = IngestionCache(
            cache=RedisCache(
                hostname=hostname,
                port=port,
            ),
            collection_name=cache_collection_name,
        )

        self.pipeline = IngestionPipeline(
            transformations=transformations,
            cache=self.ingest_cache,
            vector_store=self.vector_store,
        )

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "pipeline": self.pipeline,
            "vector_store": self.vector_store,
            "ingest_cache": self.ingest_cache,
        }

    def run(self, inputs: List[BaseNode], **kwargs: Any) -> List[BaseNode]:
        """Run the pipeline."""
        return self.pipeline.run(nodes=inputs, **kwargs)
