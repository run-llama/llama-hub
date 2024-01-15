# Mix-Self-Consistency Pack

This LlamaPack implements the the mix self-consistency method proposed in ["Rethinking Tabular Data Understanding with Large Language Models"](https://arxiv.org/pdf/2312.16702v1.pdf) paper by Liu et al.

LLMs can reason over tabular data in 2 main ways:
1. textual reasoning via direct prompting
2. symbolic reasoning via program synthesis (e.g. python, SQL, etc)

The key insight of the paper is that different reasoning pathways work well in different tasks. By aggregating results from both with a self-consistency mechanism (i.e. majority voting), it achieves SoTA performance.

We implemented the paper based on the prompts described in the paper, and adapted it to get it working. That said, this is marked as beta, so there may still be kinks to work through. Do you have suggestions / contributions on how to improve the robustness? Let us know! 

A full notebook guide can be found [here](https://github.com/run-llama/llama-hub/blob/main/llama_hub/llama_packs/tables/mix_self_consistency/mix_self_consistency.ipynb).


## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack MixSelfConsistencyPack --download-dir ./mix_self_consistency_pack
```

You can then inspect the files at `./mix_self_consistency_pack` and use them as a template for your own project!

## Code Usage

We will show you how to import the module from these files!

```python
from llama_index.llama_pack import download_llama_pack

# download and install dependencies
MixSelfConsistencyPack = download_llama_pack(
  "MixSelfConsistencyPack", "./mix_self_consistency_pack"
)

```

From here, you can use the pack. You can import the relevant modules from the download folder (in the example below we assume it's a relative import or the directory 
has been added to your system path).

```python
from mix_self_consistency_pack.base import MixSelfConsistencyQueryEngine

query_engine = MixSelfConsistencyQueryEngine(
    df=df, 
    llm=llm, 
    verbose=True
)
response = query_engine.query("Who won best Director in the 1972 Academy Awards?")
```

You can also use/initialize the pack directly.

```python
from mix_self_consistency_pack.base import MixSelfConsistencyPack

pack = MixSelfConsistencyPack(df=df, llm=llm, verbose=True)
```

The `run()` function is a light wrapper around `query_engine.query()`.

```python
response = pack.run("Who won best Director in the 1972 Academy Awards?")
```
