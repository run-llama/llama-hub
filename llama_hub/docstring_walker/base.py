import ast
import os
import networkx as nx
import networkx as nx
import logging

from llama_index import Document
from llama_index.readers.base import BaseReader
from typing import Any, Tuple, List

TYPES_TO_PROCESS = {ast.FunctionDef, ast.ClassDef}


from typing import List, Tuple

log = logging.getLogger(__name__)


class DocstringWalker(BaseReader):
    """A loader for docstring extraction and building structured documents from them.
    Recursively walks a directory and extracts docstrings from each Python module - starting from the module
    itself, then classes, then functions. Builds a graph of dependencies between the extracted docstrings.
    """
    
    def __init__(
        self, 
        code_dir: str,
        skip_initpy: bool = True,
        fail_on_malformed_files: bool = False):
        """
        Initialize the DocstringWalker object.

        Parameters
        ----------
            code_dir : str 
                The directory path to the code files.
            skip_initpy : bool
                Whether to skip the __init__.py files. Defaults to True.
            fail_on_malformed_files : bool
                Whether to fail on malformed files. Defaults to False - in this case, the malformed files are skipped
                and a warning is logged.
        """
        if not os.path.exists(code_dir):
            raise ValueError(f"Directory {code_dir} does not exist.")
        self.code_dir = code_dir
        self.skip_initpy = skip_initpy
        self.fail_on_malformed_files = fail_on_malformed_files
        self.code_graph_ = None
        
    @property
    def code_graph(self) -> nx.Graph:
        """The dependency graph between the loaded documents.
        The graph is built after loading the data from the specified directory, 
        so first you have to call the load_data method.
        """
        return self.code_graph_
    
    def load_data(self, *args, **kwargs) -> List[Document]:
        """
        Load data from the specified code directory.
        Additionally, after loading the data, build a dependency graph between the loaded documents.
        The graph is stored as an attribute of the class.
        

        Parameters
        ----------
        *args : Any
            Additional positional arguments.
        **load_kwargs : Any
            Additional keyword arguments.

        Returns
        -------
        List[Document]
            A list of loaded documents.
        """

        llama_docs, code_graph = self.process_directory()
        self.code_graph_ = code_graph
        return llama_docs
    
   
    def process_directory(self) -> Tuple[List[Document], nx.Graph]:
        """
        Process a directory and extract information from Python files.

        Returns
        -------
        Tuple[List[Document], nx.Graph]
            A tuple containing a list of Document objects and a networkx Graph object.
            The Document objects represent the extracted information from Python files in the directory.
            The Graph object represents the dependency graph between the extracted documents.
        """    
        G = nx.Graph()
        llama_docs = []
        for root, _, files in os.walk(self.code_dir):
            for file in files:
                if file.endswith(".py"):
                    if self.skip_initpy and file == "__init__.py":
                        continue
                    module_name = file.replace(".py", "")
                    module_path = os.path.join(root, file)
                    try:
                        doc = self.parse_module(module_name, module_path, G)
                        llama_docs.append(doc)
                    except Exception as e:
                        if self.fail_on_malformed_files:
                            raise e
                        else:
                            log.warning(f"Failed to parse file {module_path}. Skipping. Error: {e}")
                            continue
        return llama_docs, G


    def read_module_text(self, path: str) -> str:
        """Read the text of a Python module. For tests this function can be mocked.

        Parameters
        ----------
        path : str
            Path to the module.

        Returns
        -------
        str
            The text of the module.
        """
        with open(path) as f:
            text = f.read()
        return text


    def parse_module(self, module_name: str, path: str, G: nx.Graph) -> Document:
        """Function for parsing a single Python module.

        Parameters
        ----------
        module_name : str
            A module name.
        path : str
            Path to the module.
        G : nx.Graph
            A networkx Graph object.

        Returns
        -------
        Document
            A LLama Index Document object with extracted information from the module.
        """
        module_text = self.read_module_text(path)
        module = ast.parse(module_text)
        module_docstring = ast.get_docstring(module)
        G.add_node(module_name, docstring=module_docstring, kind="module")
        module_text = f"Module name: {module_name} \n Docstring: {module_docstring}"
        sub_texts = []
        for elem in module.body:
            if type(elem) in TYPES_TO_PROCESS:
                sub_text = self.process_elem(elem, module_name, G)
                sub_texts.append(sub_text)
        module_text += "\n".join(sub_texts)
        document = Document(text=module_text)
        return document


    def process_class(self, class_node: ast.ClassDef, parent_node: str, graph: nx.Graph):
        """
        Process a class node in the AST and add relevant information to the graph.

        Parameters:
        ----------
        class_node : ast.ClassDef
            The class node to process. It represents a class definition in the abstract syntax tree (AST).
        parent_node : str 
            The name of the parent node. It specifies the name of the parent node in the graph.
        graph : nx.Graph
            The graph to add the information to. It is a NetworkX graph object used to store the processed information.

        Returns:
        ----------
        str 
            A string representation of the processed class node and its sub-elements. 
            It provides a textual representation of the processed class node and its sub-elements.
        """
        cls_name = class_node.name
        cls_docstring = ast.get_docstring(class_node)
        graph.add_node(cls_name, docstring=cls_docstring, kind="module")
        graph.add_edge(parent_node, cls_name, kind='in_module')

        text = f"\n Class name: {cls_name} \n Docstring: {cls_docstring}"
        sub_texts = []
        for elem in class_node.body:
            sub_text = self.process_elem(elem, cls_name, graph)
            sub_texts.append(sub_text)
        return text + "\n".join(sub_texts)

    def process_function(self, func_node: ast.FunctionDef, parent_node: str, graph: nx.Graph) -> str:
        """
        Process a function node in the AST and add it to the graph. Build node text.

        Parameters
        ----------
        func_node : ast.FunctionDef
            The function node to process.
        parent_node : str
            The name of the parent node.
        graph : nx.Graph
            The graph to add the function node to.

        Returns
        -------
        str
            A string representation of the processed function node with its sub-elements.
        """
        func_name = func_node.name
        func_docstring = ast.get_docstring(func_node)
        graph.add_node(func_name, docstring=func_docstring, kind="function")
        graph.add_edge(parent_node, func_name, kind='contains')

        text = f"\n Function name: {func_name}, In: {parent_node} \n Docstring: {func_docstring}"
        sub_texts = []
        for elem in func_node.body:
            sub_text = self.process_elem(elem, func_name, graph)
            sub_texts.append(sub_text)
        return text+ "\n".join(sub_texts)


    def process_elem(self, elem, parent_node: str, graph: nx.Graph) -> str:
        """
        Process an element in the abstract syntax tree (AST).

        This is a generic function that delegates the execution to more specific functions based on the type of the element.

        Args:
            elem (ast.AST): The element to process.
            parent_node (str): The parent node in the graph.
            graph (nx.Graph): The graph to update.

        Returns:
            str: The result of processing the element.
        """
        if type(elem) == ast.FunctionDef:
            return self.process_function(elem, parent_node, graph)
        elif type(elem) == ast.ClassDef:
            return self.process_class(elem, parent_node, graph)
        else:
            return ""
