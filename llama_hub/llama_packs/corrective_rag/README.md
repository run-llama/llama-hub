# Corrective-RAG Pack

Create a query engine using completely local and private models -- `HuggingFaceH4/zephyr-7b-beta` for the LLM and `BAAI/bge-base-en-v1.5` for embeddings.

## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack CorrectiveRAGPack --download-dir ./corrective_rag_pack
```

You can then inspect the files at `./corrective_rag_pack` and use them as a template for your own project.

## Code Usage

You can download the pack to a the `./corrective_rag_pack` directory:

```python
from llama_index.llama_pack import download_llama_pack

# download and install dependencies
CorrectiveRAGPack = download_llama_pack(
  "CorrectiveRAGPack", "./corrective_rag_pack"
)

# You can use any llama-hub loader to get documents!
corrective_rag_pack = CorrectiveRAGPack(documents)
```

From here, you can use the pack, or inspect and modify the pack in `./corrective_rag_pack`.

The `run()` function contains around logic behind Corrective RAG - [CRAG](https://arxiv.org/pdf/2401.15884.pdf) PAPER.

```python
response = corrective_rag_pack.run("What did the author do growing up?", similarity_top_k=2)
```
