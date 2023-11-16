# LLaVA Completion Pack

This LlamaPack creates the LLaVA multimodal model, and runs its `complete` endpoint to execute queries.

## Usage

You can download the pack to a `./llava_pack` directory:

```python
from llama_index.llama_packs import download_llama_pack

# download and install dependencies
LlavaCompletionPack = download_llama_pack(
  "LlavaCompletionPack", "./llava_pack"
)
```

From here, you can use the pack, or inspect and modify the pack in `./llava_pack`.

Then, you can set up the pack like so:

```python
# create the pack
llava_pack = LlavaCompletionPack(
  image_url="./images/image1.jpg" 
)
```

The `run()` function is a light wrapper around `llm.complete()`.

```python
response = llava_pack.run("What dinner can I cook based on the picture of the food in the fridge?")
```

You can also use modules individually.

```python
# call the llm.complete()
llm = llava_pack.llm
response = llm.complete("query_str")
```