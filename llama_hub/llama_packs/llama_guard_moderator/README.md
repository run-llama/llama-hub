# Llama Guard Moderator Pack

This pack is to utilize Llama Guard 

## CLI Usage

You can download llamapacks directly using `llamaindex-cli`, which comes installed with the `llama-index` python package:

```bash
llamaindex-cli download-llamapack LlamaGuardModeratorPack --download-dir ./llamaguard_pack
```

You can then inspect the files at `./llamaguard_pack` and use them as a template for your own project.

## Code Usage

You can download the pack to a the `./llamaguard_pack` directory:

```python
from llama_index.llama_pack import download_llama_pack

# download and install dependencies
LlamaGuardModeratorPack = download_llama_pack(
  "LlamaGuardModeratorPack", "./llamaguard_pack"
)

# You have the option to pass in your custom taxonomy for unsafe categories during the pack construction. You can also leave it blank and the pack will use the default taxonomy from Llama Guard.
llamaguard_pack = LlamaGuardModeratorPack(custom_taxonomy)
```

From here, you can use the pack, or inspect and modify the pack in `./llamaguard_pack`.

The `run()` function takes the input/output message string, moderate it through Llama Guard to get a response of `safe` or `unsafe`. When it's `unsafe`, it also outputs the unsafe category from the taxonomy. 

```python
moderator_response = llamaguard_pack.run("I love Christmas season!")
```

Please refer to the notebook for a detailed sample RAG pipeline using LlamaGuardModeratorPack to safeguard both user input and LLM output messages.
