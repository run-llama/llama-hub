from llama_index.tools.tool_spec.base import BaseToolSpec
from simple_salesforce import Salesforce, SalesforceError

class SalesforceToolSpec(BaseToolSpec):
    """Salesforce tool spec.

    Gives the agent the ability to interact with Salesforce using simple_salesforce

    """

    sf: Salesforce = None
    spec_functions = ["execute_SOSL", "execute_SOQL", "lookUpsObjectFields"]

    def __init__(self, **kargs) -> None:
        """Initialize with parameters for Salesforce connection."""
        self.sf = Salesforce(**kargs)

    def execute_SOSL(self, search: str) -> str:
        """Returns the result of a Salesforce search as a dict decoded from
        the Salesforce response JSON payload.
        Arguments:
        * search -- the fully formatted SOSL search string, e.g.
                    `FIND {Waldo}`
        """
        try:
            res = self.sf.search(search)
        except SalesforceError as err:
            return f"Error running SOSL query: {err}"
        return res

    def execute_SOQL(self, query: str) -> str:
        """Returns the full set of results for the `query`. This is a
        convenience wrapper around `query(...)` and `query_more(...)`.
        The returned dict is the decoded JSON payload from the final call to
        Salesforce, but with the `totalSize` field representing the full
        number of results retrieved and the `records` list representing the
        full list of records retrieved.
        Arguments:
        * query -- the SOQL query to send to Salesforce, e.g.
                   SELECT Id FROM Lead WHERE Email = "waldo@somewhere.com"
        """
        try:
            res = self.sf.query_all(query)
        except SalesforceError as err:
            return f"Error running SOQL query: {err}"
        return res