"""LLM Compiler agent pack."""

from typing import Dict, Any, List, Optional
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.agent import AgentRunner
from llama_index.llms.llm import LLM
from llama_index.llms.openai import OpenAI
from llama_index.tools.types import BaseTool
from llama_index import set_global_handler

from .step import LLMCompilerAgentWorker



class LLMCompilerAgentPack(BaseLlamaPack):
    """LLMCompilerAgent pack.

    Includes using Arize Phoenix for tracing.

    Args:
        tools (List[BaseTool]): List of tools to use.
        llm (Optional[LLM]): LLM to use.

    """

    def __init__(
        self,
        tools: List[BaseTool],
        llm: Optional[LLM] = None,
    ) -> None:
        """Init params."""
        try:
            import phoenix as px
        except ImportError:
            raise ImportError(
                "The arize-phoenix package could not be found. "
                "Please install with `pip install arize-phoenix`."
            )
        self._session: "PhoenixSession" = px.launch_app()

        set_global_handler("arize_phoenix")

        self.llm = llm or OpenAI(model="gpt-4")
        self.callback_manager = llm.callback_manager
        self.agent_worker = LLMCompilerAgentWorker.from_tools(
            tools,
            llm=llm,
            verbose=True,
            callback_manager=self.callback_manager
        )
        self.agent = AgentRunner(
            self.agent_worker, callback_manager=self.callback_manager
        )

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            "session": self._session,
            "llm": self.llm,
            "callback_manager": self.callback_manager,
            "agent_worker": self.agent_worker,
            "agent": self.agent,
        }

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        return self.agent.chat(*args, **kwargs)
