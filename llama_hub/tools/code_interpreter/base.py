"""Code Interpreter tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec
from llama_index.llms.openai import OpenAI
from llama_index.llms.base import LLM, ChatMessage, MessageRole
from typing import Optional, List
import requests
import urllib.parse
import sys
import subprocess

INITIAL_PROMPT = """
    You are an AI assistant that is used to generate code.
    When receiving natural language commands you will generate code to complete the required tasks.
    The code that you generate should always be complete and runnable, as it will be executed immediately

    You will ALWAYS write the function in python. You must import any libraries you use.

    By default, the only response returned by the code is through stdout. Use print statements heavily.

    Any code that is passed in as a prompt is NOT executed.

    If you are requested to generate a graph, and want to use something like plt.show(), DONT. Instead save the output to a file.
"""


class CodeInterpreterToolSpec(BaseToolSpec):
    """Code Interpreter tool spec."""

    spec_functions = ["generate_and_execute"]

    def __init__(
        self,
        llm_cls: Optional[LLM] = OpenAI,
        llm_args: Optional[dict] = {}
    ) -> None:
        self._llm = llm_cls(*llm_args)
        self._initial_prompt = ChatMessage(role=MessageRole.SYSTEM, content=INITIAL_PROMPT)
        self._prompts = []
        self._responses = []

    def _history(self) -> List[ChatMessage]:
        return [msg for pair in zip(self._prompts, self._responses) for msg in pair]

    def format_chat(self, prompt: ChatMessage) -> List[ChatMessage]:
        return [self._initial_prompt, *self._history(), prompt]

    def generate_code(self, prompt: str) -> str:
        formatted_prompt = ChatMessage(role=MessageRole.USER, content=prompt)
        response = self._llm.chat(self.format_chat(formatted_prompt))
        self._prompts.append(formatted_prompt)
        self._responses.append(ChatMessage(role=MessageRole.ASSISTANT, content=response.message.content))
        return response.message.content

    def code_interpreter(self, code: str):
        """
        A function to execute python code, and return the stdout and stderr
        """
        result = subprocess.run([sys.executable, '-c', code], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return f'StdOut:\n{result.stdout}\nStdErr:\n{result.stderr}'

    def generate_and_execute(self, prompt: str) -> str:
        """
        This tool generates python code and immediately executes the code.
        Treat this tool as another Large Language Model Agent that will create the code for you, and execute it
        This tool will also keep track of the previous calls you make for conveinence

        An example input to this tool would be 'Calculate the quadratic formula at (0,1,2)'
        or 'Analyze the csv at my_data.csv and tell me the average of a column'

        Args:
            prompt (str): the natural langauge prompt to generate code from

        This function will return the code generated as well as the output
        If the response contains stderr output, update the prompt to include the error and try again
        """
        code = self.generate_code(prompt)
        result = self.code_interpreter(code)
        return f'Code:\n{code}\n\n{result}'


