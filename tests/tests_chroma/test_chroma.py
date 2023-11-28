import shutil
from typing import Any, Generator
import pytest
import tempfile
from llama_hub.chroma import ChromaReader


@pytest.fixture
def chroma_persist_dir() -> Generator[str, None, None]:
    temp_dir = tempfile.mkdtemp()
    yield temp_dir
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def chroma_client(chroma_persist_dir: str) -> Generator[Any, None, None]:
    import chromadb
    from chromadb.config import Settings

    # The client settings must align with ChromaReader's settings otherwise
    # an exception will be raised.
    client = chromadb.Client(
        Settings(
            is_persistent=True,
            persist_directory=chroma_persist_dir,
        )
    )
    yield client


def test_chroma_with_client(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(ids=["1"], documents=["test"], embeddings=[[1, 2, 3]])
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3]], limit=5)
    assert len(docs) == 1


def test_chroma_with_persist_dir(chroma_client: Any, chroma_persist_dir: str) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(ids=["1"], documents=["test"], embeddings=[[1, 2, 3]])
    chroma = ChromaReader(
        collection_name="test_collection", persist_directory=chroma_persist_dir
    )

    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3]], limit=5)
    assert len(docs) == 1


def test_chroma_with_where_filter(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1"],
        documents=["test"],
        embeddings=[[1, 2, 3]],
        metadatas=[{"test": "test"}],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3]], limit=5, where={"test": "test"})
    assert len(docs) == 1


def test_chroma_with_where_filter_no_match(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1"],
        documents=["test"],
        embeddings=[[1, 2, 3]],
        metadatas=[{"test": "test"}],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3]], where={"test": "test1"})
    assert len(docs) == 0


def test_chroma_with_where_document_filter(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1"],
        documents=["this is my test document"],
        embeddings=[[1, 2, 3]],
        metadatas=[{"test": "test"}],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(
        query_vector=[[1, 2, 3]], limit=5, where_document={"$contains": "test"}
    )
    assert len(docs) == 1


def test_chroma_with_where_document_filter_no_match(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1"],
        documents=["this is my test document"],
        embeddings=[[1, 2, 3]],
        metadatas=[{"test": "test"}],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(
        query_vector=[[1, 2, 3]], limit=5, where_document={"$contains": "test1"}
    )
    assert len(docs) == 0


def test_chroma_with_multiple_docs(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1", "2"],
        documents=["test", "another test doc"],
        embeddings=[[1, 2, 3], [1, 2, 3]],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3]], limit=5)
    assert len(docs) == 2


def test_chroma_with_multiple_docs_multiple_queries(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1", "2"],
        documents=["test", "another test doc"],
        embeddings=[[1, 2, 3], [3, 2, 1]],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3], [3, 2, 1]], limit=5)
    assert len(docs) == 4  # there are duplicates in this result


def test_chroma_with_multiple_docs_with_limit(chroma_client: Any) -> None:
    test_collection = chroma_client.get_or_create_collection("test_collection")
    test_collection.add(
        ids=["1", "2"],
        documents=["test", "another test doc"],
        embeddings=[[1, 2, 3], [3, 2, 1]],
    )
    chroma = ChromaReader(
        collection_name="test_collection",
        client=chroma_client,
    )
    assert chroma is not None
    docs = chroma.load_data(query_vector=[[1, 2, 3]], limit=1)
    assert len(docs) == 1
