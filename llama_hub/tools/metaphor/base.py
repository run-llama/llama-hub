"""Metaphor tool spec."""

from llama_index.tools.tool_spec.base import BaseToolSpec


class MetaphorToolSpec(BaseToolSpec):
    """Metaphor tool spec."""

    spec_functions = []

    def __init__(self, api_key: str, verbose: bool = True) -> None:
        """Initialize with parameters."""
        raise NotImplementedError(
            "Metaphor is now Exa. Please use ExaToolSpec instead."
        )
