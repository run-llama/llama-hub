"""Snowflake Query Engine Pack."""

import os
import json
from typing import Any, Dict, List

def snowflake_sqlalchemy_20_monkey_patches():
    import sqlalchemy.util.compat

    # make strings always return unicode strings
    sqlalchemy.util.compat.string_types = (str,)
    sqlalchemy.types.String.RETURNS_UNICODE = True

    import snowflake.sqlalchemy.snowdialect

    snowflake.sqlalchemy.snowdialect.SnowflakeDialect.returns_unicode_strings = True

    # make has_table() support the `info_cache` kwarg
    import snowflake.sqlalchemy.snowdialect

    def has_table(self, connection, table_name, schema=None, info_cache=None):
        """
        Checks if the table exists
        """
        return self._has_object(connection, "TABLE", table_name, schema)

    snowflake.sqlalchemy.snowdialect.SnowflakeDialect.has_table = has_table

# workaround for https://github.com/snowflakedb/snowflake-sqlalchemy/issues/380.
try:
    snowflake_sqlalchemy_20_monkey_patches()
except Exception:
    raise ImportError("Please run `pip install snowflake-sqlalchemy`")

from sqlalchemy import create_engine
from llama_index import SQLDatabase, ServiceContext
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.indices.struct_store.sql_query import NLSQLTableQueryEngine

class SnowflakeQueryEnginePack(BaseLlamaPack):
    """Snowflake query engine pack. 
    
    It uses snowflake-sqlalchemy to connect to Snowflake, then calls 
    NLSQLTableQueryEngine to query data.
    
    """

    def __init__(
        self,
        tables: List[str],
        **kwargs: Any,
    ) -> None:
        """Init params."""

        if not os.environ.get("OPENAI_API_KEY", None):
            raise ValueError("OpenAI API Token is missing or blank.")

        # Check if credentials file exists
        if not os.path.exists('credentials.json'):
            raise FileNotFoundError("The 'credentials.json' file is mandatory for connecting to Snowflake.")

        # connect to Snowflake
        with open('credentials.json') as f:
            connection_parameters = json.load(f)

        snowflake_uri = f"snowflake://{connection_parameters['user']}:{connection_parameters['password']}@{connection_parameters['account']}/{connection_parameters['database']}/{connection_parameters['schema']}?warehouse={connection_parameters['warehouse']}&role={connection_parameters['role']}"
        
        engine = create_engine(snowflake_uri)

        self._sql_database = SQLDatabase(engine)
        self.tables = tables

        self._service_context = ServiceContext.from_defaults()

        self.query_engine = NLSQLTableQueryEngine(
            sql_database=self._sql_database,
            tables=self.tables,
            service_context=self._service_context
        )    

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "service_context": self._service_context,
            "sql_database": self._sql_database,
            "query_engine": self.query_engine,
        }

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.query_engine.query(*args, **kwargs)
