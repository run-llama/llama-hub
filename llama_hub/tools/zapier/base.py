"""Zapier tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from typing import Optional, Dict
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

        The actions will be listed in the following format:

        List[{
                id: str,
                description: str,
                params: Dict[str, str]
            }]

        The params dictionary always accepts the value 'instructions'.
        All other values in params are optional. If you provide a value for the parameter, it will override the 'instructions'.
        Therefore, if you are not sure of the value for a param, leave it blank and prefer instead to provide more details in the 'instructions'.

        However, NEVER leave instructions blank, as it is required. No other fields are required.
        """

        response = requests.get(
            "https://nla.zapier.com/api/v1/dynamic/exposed/",
            headers=self._headers
        )
        return response.text


    def natural_language_query(self, id: str, params: Dict[str, str]):
        """
        Make a natural language action to Zapier
        This endpoint accepts natural language instructions to integrate with other services
        You should always provide a natural language string in the params dict descrbing the overall action to be taken

        The action being called must have an id obtained from list_actions. If the action is not exposed it can be here: 
        Args:
            id (str): The id of the zapier action to call
            params (Optional[dict]): The instructions and other values instructing the action to be taken

        If the error field is not null, interpret the error and try to fix it. Otherwise, inform the user of how they might fix it.
        """

        response = requests.post(
            ACTION_URL_TMPL.format(action_id=id),
            headers=self._headers,
            data=json.dumps(params)
        )
        return response.text
