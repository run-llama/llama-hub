"""Zapier tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from typing import Optional
import requests
import json

ACTION_URL_TMPL = "https://nla.zapier.com/api/v1/dynamic/exposed/{action_id}/execute/"

class ZapierToolSpec(BaseToolSpec):
    """Zapier tool spec."""

    spec_functions = ["list_actions", "natural_language_query"]

    def __init__(self, api_key: Optional[str] = None, oauth_access_token: Optional[str] = None) -> None:
        """Initialize with parameters."""
        if api_key:
            self._headers = {
                "x-api-key": api_key
                }
        elif oauth_access_token:
            self._headers = {
                "Authorization": f"Bearer {oauth_access_token}"
            }
        else:
            raise ValueError("Must provide either api_key or oauth_access_token")

    def list_actions(self):
        """
        List the actions that the Natual Language query can complete.

        All of the actions listed are accessible through the natural_language_query tool
        """

        response = requests.get(
            "https://nla.zapier.com/api/v1/dynamic/exposed/",
            headers=self._headers
        )
        return response.text


    def natural_language_query(self, id: str, instructions: str):
        """
        Make a natural language action to Zapier
        This endpoint accepts natural language instructions to integrate with other services

        Args:
            id (str): The id of the zapier action to call
            instructions (str): The natural language instruction to pass to Zapier

        """

        response = requests.post(
            ACTION_URL_TMPL.format(action_id=id),
            headers=self._headers,
            data=json.dumps({'instructions': instructions})
        )
        return response.text
