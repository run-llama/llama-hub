import os

# from llama_index import download_loader
from llama_hub.preprocess.base import PreprocessReader
from llama_index.readers.schema.base import Document
from llama_index.schema import TextNode

API_KEY = (
    ""  # you've to contact support@preprocess.co for generating an api key for you...
)


def test_preprocess_load_document_and_get_text():
    filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "preprocess_test.pdf"
    )
    loader = PreprocessReader(api_key=API_KEY, filepath=filepath)
    documents = loader.load_data()

    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)
    assert all(doc.text is not None for doc in documents)


def test_preprocess_load_document_and_get_nodes():
    filepath = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "preprocess_test.pdf"
    )
    loader = PreprocessReader(api_key=API_KEY, filepath=filepath)
    nodes = loader.get_nodes()

    assert isinstance(nodes, list)
    assert all(isinstance(node, TextNode) for node in nodes)
    assert all(node.text is not None and node.node_id is not None for node in nodes)
