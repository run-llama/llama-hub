# Paul Graham Essay Dataset

## CLI Usage

You can download `llamadatasets` directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamadataset PaulGrahamEssayDataset --download-dir ./data
```

You can then inspect the files at `./data`.

## Code Usage

You can download the dataset to a directory, say `./data`. Then download the
convenient `RagEvaluatorPack` llamapack to run your own LlamaIndex RAG pipeline
with the llamadataset.

```python
from llama_index.llama_dataset import download_llama_dataset
from llama_index.llama_pack import download_llama_pack
from llama_index import VectorStoreIndex

# download and install dependencies for rag evaluator pack
RagEvaluatorPack = download_llama_pack(
  "RagEvaluatorPack", "./rag_evaluator_pack"
)
rag_evaluator_pack = RagEvaluatorPack()

# download and install dependencies for benchmark dataset
rag_dataset, documents = download_llama_dataset(
  "PaulGrahamEssayDataset", "./data"
)

# build basic RAG system
index = VectorStoreIndex.from_documents(documents=documents)

# evaluate
query_engine = VectorStoreIndex.as_query_engine()  # previously defined, not shown here
rag_evaluate_pack.run(dataset=paul_graham_qa_data, query_engine=query_engine)
```

