import asyncio

from llama_index.llama_dataset import download_llama_dataset
from llama_index.llama_pack import download_llama_pack
from llama_index import VectorStoreIndex


async def main():
    # DOWNLOAD LLAMADATASET
    rag_dataset, documents = download_llama_dataset(
        "PatronusAIFinanceBenchDataset", "./patronus_financebench"
    )

    # BUILD BASIC RAG PIPELINE
    index = VectorStoreIndex.from_documents(documents=documents)
    query_engine = index.as_query_engine()

    # EVALUATE WITH PACK
    RagEvaluatorPack = download_llama_pack("RagEvaluatorPack", "./pack_stuff")
    rag_evaluator = RagEvaluatorPack(query_engine=query_engine, rag_dataset=rag_dataset)
    benchmark_df = await rag_evaluator.arun()
    print(benchmark_df)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main)
