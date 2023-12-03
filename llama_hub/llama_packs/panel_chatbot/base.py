from typing import Dict, Any
import os
from llama_index.llama_pack.base import BaseLlamaPack

ENVIRONMENT_VARIABLES = [
    "GITHUB_TOKEN",
    "OPENAI_API_KEY",
]


class PanelChatPack(BaseLlamaPack):
    """Panel chatbot pack."""

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        for variable in ENVIRONMENT_VARIABLES:
            if not variable in os.environ:
                raise ValueError(f"{variable} is not set")

        import panel as pn
        from app import create_app

        if __name__ == "__main__":
            pn.serve(create_app)
        elif __name__.startswith("bokeh"):
            create_app().servable()
        else:
            print("Please run this file with 'python' or serve it with 'panel serve'")


PanelChatPack().run()
