"""LlamaPack class."""


from typing import Any, Dict

from llama_index.agent.openai_agent import OpenAIAgent
from llama_index.llama_pack.base import BaseLlamaPack


class GmailOpenAIAgentPack(BaseLlamaPack):
    def __init__(self, gmail_tool_kwargs: Dict[str, Any]) -> None:
        """Init params."""
        try:
            from llama_hub.tools.gmail.base import GmailToolSpec
        except ImportError:
            raise ImportError("llama_hub not installed.")

        self.tool_spec = GmailToolSpec(**gmail_tool_kwargs)
        self.agent = OpenAIAgent.from_tools(self.tool_spec.to_tool_list())

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {"gmail_tool": self.tool_spec, "agent": self.agent}

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.agent.chat(*args, **kwargs)
