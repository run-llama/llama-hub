# Intro
Very often you have a large code base, with a rich docstrings and comments, that you would like to use to produce documentation. In fact, many open-source libraries like Scikit-learn or PyTorch have docstring so rich, that they contain LaTeX equations, or detailed examples. 

At the same time, sometimes LLMs are used to read the full code from a repository, which can cost you many tokens, time and computational power.

DocstringWalker tries to find a sweet spot between these two approaches. You can use it to:

1. Parse all docstrings from modules, classes, and functions in your local code directory.
2. Convert them do Llama Documents.
3. Feed into LLM of your choice to produce a code-buddy chatbot or generate documentation.
DocstringWalker utilizes only AST module, to process the code.

# Usage

Simply create a DocstringWalker and point it to the directory with the code. The class takes the following parameters:

1. Ignore __init__.py files - should __init__.py files be skipped? In some projects, they are not used at all, while in others they contain valuable info. 
2. Fail on error - AST will throw SyntaxError when parsing a malformed file. Should this raise an exception for the whole process, or be ignored?

# Examples

Below you can find examples of using DocstringWalker.

## Example 1

Let's start by using it.... on itself :) We will see what information gets extracted from the module.  
#TODO: add example


