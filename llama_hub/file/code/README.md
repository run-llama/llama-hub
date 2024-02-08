
# CodeHierarchyNodeParser

The `CodeHierarchyNodeParser` is useful to split long code files into more reasonable chunks. What this will do is create a "Hierarchy" of sorts, where sections of the code are made more reasonable by replacing the scope body with short comments telling the LLM to search for a referenced node if it wants to read that context body. This is called skeletonization, and is toggled by setting `skeleton` to `True` which it is by default.

Nodes in this hierarchy will be split based on scope, like function, class, or method scope, and will have links to their children and parents so the LLM can traverse the tree.

```python
from llama_index.node_parser.code_hierarchy import CodeHierarchyNodeParser
from llama_index.text_splitter.code_splitter import CodeSplitter

split_nodes = CodeHierarchyNodeParser(
    language="python",
    # You can further parameterize the CodeSplitter to split the code
    # into "chunks" that match your context window size using
    # chunck_lines and max_chars parameters, here we just use the defaults
    code_splitter=CodeSplitter(language="python"),
)
```

A full example can be found [here in combination with `CodeSplitter`](./CodeHierarchyNodeParserUsage.ipynb).

# Repo Maps

TODO

# Indexing

TODO

# Adding new languages

## SignatureCaptureType

TODO

## SignatureCaptureOptions

TODO

## DEFAULT_SIGNATURE_IDENTIFIERS

TODO

## Future

I'm considering adding all the languages from [aider](https://github.com/paul-gauthier/aider/tree/main/aider/queries)
by incorporating `.scm` files instead of `_SignatureCaptureType`, `_SignatureCaptureOptions`, and `_DEFAULT_SIGNATURE_IDENTIFIERS`