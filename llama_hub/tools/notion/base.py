"""Notion tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from typing import Optional, List, Dict, Any
from llama_index.readers.schema.base import Document
import re
import requests
import os

SEARCH_URL = "https://api.notion.com/v1/search"
INTEGRATION_TOKEN_NAME = "NOTION_INTEGRATION_TOKEN"
BLOCK_CHILD_URL_TMPL = "https://api.notion.com/v1/blocks/{block_id}/children"
DATABASE_URL_TMPL = "https://api.notion.com/v1/databases/{database_id}/query"
UUID_REGEX = re.compile(
    "^[a-f0-9]{8}-?[a-f0-9]{4}-?4[a-f0-9]{3}-?[89ab][a-f0-9]{3}-?[a-f0-9]{12}", re.I
)


class NotionToolSpec(BaseToolSpec):
    """Notion tool spec.

    Currently a simple wrapper around the data loader.
    TODO: add more methods to the Notion spec.

    """

    spec_functions = ["load_data", "search_data", "append_data"]

    def __init__(self, integration_token: Optional[str] = None) -> None:
        """Initialize with parameters."""
        if integration_token is None:
            integration_token = os.getenv(INTEGRATION_TOKEN_NAME)
            if integration_token is None:
                raise ValueError(
                    "Must specify `integration_token` or set environment "
                    "variable `NOTION_INTEGRATION_TOKEN`."
                )
        self.token = integration_token
        self.headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28",
        }

    def append_data(
        self, block_id: Optional[str], content: str, text_type: str = "paragraph"
    ) -> bool:
        """Accepts the id of a page or block as block_id and text content as input, and appends the text content to the end of the specfied block.

        You can change the formatting of the text with text_type. Possible options include paragraph, heading_1, quote

        Don't use this endpoint if you don't know the page id or content to append

        """
        if not UUID_REGEX.match(block_id):
            return "This endpoint only supports block ids in the form of a uuid as input. Please use the search_data endpoint to find the id of the page you are looking for and then call this endpoint again"

        block_url = BLOCK_CHILD_URL_TMPL.format(block_id=block_id)
        block = {
            "children": [
                dict(
                    [
                        ("object", "block"),
                        ("type", text_type),
                        (
                            text_type,
                            {
                                "rich_text": [
                                    {"type": "text", "text": {"content": content}}
                                ]
                            },
                        ),
                    ]
                )
            ]
        }
        res = requests.request("PATCH", block_url, headers=self.headers, json=block)
        res.json()
        return "success"

    def _read_block(self, block_id: str, num_tabs: int = 0) -> str:
        """Read a block."""
        done = False
        result_lines_arr = []
        cur_block_id = block_id
        while not done:
            block_url = BLOCK_CHILD_URL_TMPL.format(block_id=cur_block_id)
            query_dict: Dict[str, Any] = {}

            res = requests.request(
                "GET", block_url, headers=self.headers, json=query_dict
            )
            data = res.json()

            for result in data["results"]:
                result_type = result["type"]
                result_obj = result[result_type]

                cur_result_text_arr = []
                if "rich_text" in result_obj:
                    for rich_text in result_obj["rich_text"]:
                        # skip if doesn't have text object
                        if "text" in rich_text:
                            text = rich_text["text"]["content"]
                            prefix = "\t" * num_tabs
                            cur_result_text_arr.append(prefix + text)

                result_block_id = result["id"]
                has_children = result["has_children"]
                if has_children:
                    children_text = self._read_block(
                        result_block_id, num_tabs=num_tabs + 1
                    )
                    cur_result_text_arr.append(children_text)

                cur_result_text = "\n".join(cur_result_text_arr)
                result_lines_arr.append(cur_result_text)

            if data["next_cursor"] is None:
                done = True
                break
            else:
                cur_block_id = data["next_cursor"]

        result_lines = "\n".join(result_lines_arr)
        return result_lines

    def read_page(self, page_id: str) -> str:
        """Read a page."""
        return self._read_block(page_id)

    def query_database(
        self, database_id: str, query_dict: Dict[str, Any] = {"page_size": 100}
    ) -> List[str]:
        """Get all the pages from a Notion database."""
        pages = []

        res = requests.post(
            DATABASE_URL_TMPL.format(database_id=database_id),
            headers=self.headers,
            json=query_dict,
        )
        res.raise_for_status()
        data = res.json()

        pages.extend(data.get("results"))

        while data.get("has_more"):
            query_dict["start_cursor"] = data.get("next_cursor")
            res = requests.post(
                DATABASE_URL_TMPL.format(database_id=database_id),
                headers=self.headers,
                json=query_dict,
            )
            res.raise_for_status()
            data = res.json()
            pages.extend(data.get("results"))

        page_ids = [page["id"] for page in pages]
        return page_ids

    def search_data(self, query: str) -> List[str]:
        """Search Notion page given a text query."""
        done = False
        next_cursor: Optional[str] = None
        page_ids = []
        while not done:
            query_dict = {
                "query": query,
            }
            if next_cursor is not None:
                query_dict["start_cursor"] = next_cursor
            res = requests.post(SEARCH_URL, headers=self.headers, json=query_dict)
            data = res.json()
            for result in data["results"]:
                page_id = result["id"]
                page_ids.append(page_id)

            if data["next_cursor"] is None:
                done = True
                break
            else:
                next_cursor = data["next_cursor"]
        return page_ids

    def load_data(
        self, page_ids: List[str] = [], database_id: Optional[str] = None
    ) -> List[Document]:
        """Load data from the input directory.

        Args:
            page_ids (List[str]): List of page ids to load.
            database_id (str): Database_id from which to load page ids.

        Returns:
            List[Document]: List of documents.

        """
        if not page_ids and not database_id:
            raise ValueError("Must specify either `page_ids` or `database_id`.")
        docs = []
        if database_id is not None:
            # get all the pages in the database
            page_ids = self.query_database(database_id)
            for page_id in page_ids:
                page_text = self.read_page(page_id)
                docs.append(Document(text=page_text, extra_info={"page_id": page_id}))
        else:
            for page_id in page_ids:
                page_text = self.read_page(page_id)
                docs.append(Document(text=page_text, extra_info={"page_id": page_id}))

        return docs
