import os
# from llama_index import download_loader
from llama_hub.preprocess.base import PreprocessReader
from llama_index.readers.schema.base import Document

API_KEY = "" # you've to contact support@preprocess.co for generating an api key for you...
def test_preprocess():
    filepath = os.path.join(os.path.abspath("./"), "preprocess_test.pdf")
    loader = PreprocessReader(api_key=API_KEY, filepath=filepath)
    documents = loader.load_data()
    
    assert isinstance(documents, list)
    assert all(isinstance(doc, Document) for doc in documents)
    assert all(doc.text is not None for doc in documents)
