"""Code Interpreter tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.llms.base import LLM, ChatMessage, MessageRole
from typing import Optional, List
import requests
import urllib.parse
import sys
import subprocess

class CodeInterpreterToolSpec(BaseToolSpec):
    """Code Interpreter tool spec."""

    spec_functions = ["code_interpreter"]

    def code_interpreter(self, code: str):
        """
        A function to execute python code, and return the stdout and stderr

        You should import any libraries that you wish to use. You have access to any libraries the user has installed.

        The code passed to this functuon is executed in isolation. It should be complete at the time it is passed to this function.

        You should interpret the output and errors returned from this function, and attempt to fix any problems.
        If you cannot fix the error, show the code to the user and ask for help

        It is not possible to return graphics or other complicated data from this function. If the user cannot see the output, save it to a file and tell the user.
        """
        result = subprocess.run([sys.executable, '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f'StdOut:\n{result.stdout}\nStdErr:\n{result.stderr}'
