from typing import Any, Dict

from llama_index.agent import ReActAgent
from llama_index.llama_pack.base import BaseLlamaPack


class CogniswitchAgentPack(BaseLlamaPack):
    def __init__(self, cogniswitch_tool_kwargs: Dict[str, Any]) -> None:
        """Init params."""
        try:
            from llama_hub.tools.cogniswitch import CogniswitchToolSpec
        except ImportError:
            raise ImportError("llama_hub not installed.")

        self.tool_spec = CogniswitchToolSpec(**cogniswitch_tool_kwargs)
        self.agent = ReActAgent.from_tools(self.tool_spec.to_tool_list())

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {"cogniswitch_tool": self.tool_spec, "agent": self.agent}

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.agent.chat(*args, **kwargs)
