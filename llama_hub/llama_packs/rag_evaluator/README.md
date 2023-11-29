# Retrieval-Augmented Generation (RAG) Evaluation Pack

Get benchmark scores on your own RAG pipeline (i.e. `BaseQueryEngine`) on a RAG 
dataset (i.e., `BaseLlamaDataset`). Specifically this pack takes in as input a
query engine and a `LabelledRagDataset`, which can also be downloaded from
[llama-hub](https://llamahub.ai).

## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack RagEvaluatorPack --download-dir ./rag_evaluator_pack
```

You can then inspect the files at `./rag_evaluator_pack` and use them as a template for your own project!

## Code Usage

You can download the pack to a the `./rag_evaluator_pack` directory:

```python
from llama_index.llama_dataset import download_llama_dataset
from llama_index.llama_pack import download_llama_pack
from llama_index import VectorStoreIndex

# download a rag_dataset from llama-hub
rag_dataset, documents = download_llama_dataset(
    "PaulGrahamEssayDataset", "./paul_graham"
)

# default will use OpenAI GPT-4
index = VectorStoreIndex.from_documents(documents=documents)
query_engine = index.as_query_engine()

# download and install dependencies
RagEvaluatorPack = download_llama_pack(
  "RagEvaluatorPack", "./rag_evaluator_pack"
)

# construction requires a query_engine, a rag_dataset, and optionally a judge_llm
rag_evaluator_pack = RagEvaluatorPack(
    query_engine=query_engine
    rag_dataset=rag_dataset
)

# PERFORM EVALUATION
benchmark_df = rag_evaluator_pack.run()
print(benchmark_df)
```

**Sample Output**
```
rag                            base_rag
metrics                                
mean_correctness_score         4.511364
mean_relevancy_score           0.931818
mean_faithfulness_score        1.000000
mean_context_similarity_score  0.945952
```

Note that `rag_evaluator_pack.run()` will also save two files in the same directory
in which the pack was invoked:

1. `benchmark.csv` - CSV format of the benchmark scores.
2. `_evaluations.json` - A JSON filed containing the evaluation results for all predictions (made by the `query_engine`) on each example (of the `rag_dataset`).