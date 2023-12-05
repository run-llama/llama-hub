"""Waii Tool."""
import json
from typing import List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document
from llama_index.response_synthesizers import TreeSummarize
from llama_index.tools.tool_spec.base import BaseToolSpec


class WaiiToolSpec(BaseToolSpec, BaseReader):
    spec_functions = [
        "get_answer",
        "describe_query",
        "performance_analyze",
        "diff_query",
        "describe_dataset",
        "transcode",
        "get_semantic_contexts",
        "generate_query_only",
        "run_query",
    ]

    def __init__(
        self,
        url: Optional[str] = None,
        api_key: Optional[str] = None,
        database_key: Optional[str] = None,
        verbose: Optional[bool] = False,
    ) -> None:
        from waii_sdk_py import WAII

        WAII.initialize(url=url, api_key=api_key)
        WAII.Database.activate_connection(key=database_key)
        self.verbose = verbose

    def load_data(self, ask: str) -> List[Document]:
        """Query using natural language and load data from the Database, returning a list of Documents.

        Args:
            ask: a natural language question.

        Returns:
            List[Document]: A list of Document objects.
        """
        from waii_sdk_py import WAII
        from waii_sdk_py.query import QueryGenerationRequest, RunQueryRequest

        query = WAII.Query.generate(
            QueryGenerationRequest(ask=ask), verbose=self.verbose
        ).query
        documents = WAII.Query.run(
            RunQueryRequest(query=query), verbose=self.verbose
        ).rows
        return [Document(text=str(doc)) for doc in documents]

    def _get_summarization(self, original_ask: str, documents):
        texts = []

        n_chars = 0
        for i in range(len(documents)):
            t = str(documents[i].text)
            if len(t) + n_chars > 8192:
                texts.append(f"... {len(documents) - i} more results")
                break
            texts.append(t)
            n_chars += len(t)

        summarizer = TreeSummarize(verbose=self.verbose)
        response = summarizer.get_response(original_ask, texts)
        return response

    def get_answer(self, ask: str):
        """
        Generate a SQL query and run it against the database, returning the summarization of the answer
        Args:
            ask: a natural language question.

        Returns:
            str: A string containing the summarization of the answer.
        """
        docs = self.load_data(ask)
        return self._get_summarization(ask, docs)

    def generate_query_only(self, ask: str):
        """
        Generate a SQL query and NOT run it, returning the query. If you need to get answer, you should use get_answer instead.

        Args:
            ask: a natural language question.

        Returns:
            str: A string containing the query.
        """
        from waii_sdk_py import WAII
        from waii_sdk_py.query import QueryGenerationRequest

        query = WAII.Query.generate(
            QueryGenerationRequest(ask=ask), verbose=self.verbose
        ).query
        return query

    def run_query(self, sql: str):
        """
        This function run a SQL query against the database, returning the summarization of the answer. You use choose the function when you need to run a SQL query

        Args:
            sql: a SQL query.

        Returns:
            str: A string containing the summarization of the answer.
        """
        from waii_sdk_py import WAII
        from waii_sdk_py.query import RunQueryRequest

        documents = WAII.Query.run(
            RunQueryRequest(query=sql), verbose=self.verbose
        ).rows
        return self._get_summarization(
            "run query", [Document(text=str(doc)) for doc in documents]
        )

    def describe_query(self, question: str, query: str):
        """
        Describe a sql query, returning the summarization of the answer

        Args:
            question: a natural language question which the people want to ask.
            query: a sql query.

        Returns:
            str: A string containing the summarization of the answer.
        """
        from waii_sdk_py import WAII
        from waii_sdk_py.query import DescribeQueryRequest

        result = WAII.Query.describe(DescribeQueryRequest(query=query))
        result = json.dumps(result.dict(), indent=2)
        response = self._get_summarization(question, [Document(text=result)])
        return response

    def performance_analyze(self, query_uuid: str):
        """
        Analyze the performance of a query, returning the summarization of the answer

        Args:
            query_uuid: a query uuid, e.g. xxxxxxxxxxxxx...

        Returns:
            str: A string containing the summarization of the answer.
        """
        from waii_sdk_py import WAII
        from waii_sdk_py.query import QueryPerformanceRequest

        result = WAII.Query.analyze_performance(
            QueryPerformanceRequest(query_id=query_uuid)
        )
        result = json.dumps(result.dict(), indent=2)
        return result

    def diff_query(self, previous_query: str, current_query: str):
        """
        Diff two sql queries, returning the summarization of the answer

        Args:
            previous_query: previous sql query.
            current_query: current sql query.

        Returns:
            str: A string containing the summarization of the answer.
        """
        from waii_sdk_py import WAII
        from waii_sdk_py.query import DiffQueryRequest

        result = WAII.Query.diff(
            DiffQueryRequest(query=current_query, previous_query=previous_query)
        )
        result = json.dumps(result.dict(), indent=2)
        return self._get_summarization("get diff summary", [Document(text=result)])

    def describe_dataset(
        self,
        ask: str,
        schema_name: Optional[str] = None,
        table_name: Optional[str] = None,
    ):
        """
        Describe a dataset (no matter if it is a table or schema), returning the summarization of the answer.
        Example questions like: "describe the dataset", "what the schema is about", "example question for the table xxx", etc.
        When both schema and table are None, describe the whole database.

        Args:
            ask: a natural language question (how you want to describe the dataset).
            schema_name: a schema name (shouldn't include the database name or the table name).
            table_name: a table name. (shouldn't include the database name or the schema name).

        Returns:
            str: A string containing the summarization of the answer.
        """
        from waii_sdk_py import WAII

        catalog = WAII.Database.get_catalogs()

        # filter by schema / table
        schemas = {}
        tables = {}

        for c in catalog.catalogs:
            for s in c.schemas:
                for t in s.tables:
                    if (
                        schema_name is not None
                        and schema_name.lower() != t.name.schema_name.lower()
                    ):
                        continue
                    if table_name is not None:
                        if table_name.lower() != t.name.table_name.lower():
                            continue
                        tables[str(t.name)] = t
                    schemas[str(s.name)] = s

        # remove tables ref from schemas
        for schema in schemas:
            schemas[schema].tables = None

        # generate response
        response = self._get_summarization(
            ask + ", use the provided information to get comprehensive summarization",
            [Document(text=str(schemas[schema])) for schema in schemas]
            + [Document(text=str(tables[table])) for table in tables],
        )
        return response

    def transcode(
        self,
        instruction: Optional[str] = "",
        source_dialect: Optional[str] = None,
        source_query: Optional[str] = None,
        target_dialect: Optional[str] = None,
    ):
        """
        Transcode a sql query from one dialect to another, returning generated query

        Args:
            instruction: instruction in natural language.
            source_dialect: the source dialect of the query.
            source_query: the source query.
            target_dialect: the target dialect of the query.

        Returns:
            str: A string containing the generated query.
        """

        from waii_sdk_py import WAII
        from waii_sdk_py.query import TranscodeQueryRequest

        result = WAII.Query.transcode(
            TranscodeQueryRequest(
                ask=instruction,
                source_dialect=source_dialect,
                source_query=source_query,
                target_dialect=target_dialect,
            )
        )
        return result.query

    def get_semantic_contexts(self):
        """
        Get all pre-defined semantic contexts
        :return:
        """
        from waii_sdk_py import WAII

        return WAII.SemanticContext.get_semantic_context().semantic_context
