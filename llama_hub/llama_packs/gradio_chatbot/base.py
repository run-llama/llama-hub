from typing import Dict, Any, List, Tuple

from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
)
from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.llms import OpenAI
from llama_index import ServiceContext
from llama_index.readers import WikipediaReader
from llama_index.agent import ReActAgent
from llama_index.tools import QueryEngineTool, ToolMetadata
from ansi2html import Ansi2HTMLConverter

from contextlib import redirect_stdout
from io import StringIO 
import sys

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout


class GradioChatPack(BaseLlamaPack):
    """Gradio chatbot pack."""

    def __init__(
        self,
        wikipedia_page: str = "Snowflake Inc.",
        **kwargs: Any,
    ) -> None:
        """Init params."""        
        self.wikipedia_page = wikipedia_page
        self.llm = OpenAI(model="gpt-4")
        self.reader = WikipediaReader()
        self.chat_history = []
        service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5))
        docs = self.reader.load_data(pages=[wikipedia_page])
        index = VectorStoreIndex.from_documents(docs, service_context=service_context)
        query_engine = index.as_query_engine(chat_mode="context")
        tools = [QueryEngineTool(
            query_engine=query_engine,
            metadata=ToolMetadata(
                name="Wikipedia Page",
                description=(
                    "Provides information about this wikipedia page."
                )
            )
        )]
        self.agent = ReActAgent.from_tools(tools, llm=self.llm, verbose=True)
        self.thoughts = ""
        self.conv = Ansi2HTMLConverter()


    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}
    
    def _user(self, user_message, history):
        return "", history + [(user_message, "")]
    
    def _generate_response(self, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str,str]]]:
        with Capturing() as output:
            response = self.agent.stream_chat(chat_history[-1][0])
        ansi = "\n========\n".join(output)
        html_output = self.conv.convert(ansi)
        print(html_output)
        for token in response.response_gen:
            chat_history[-1][1] += token
            yield chat_history, str(html_output)

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        import gradio as gr


        demo = gr.Blocks(css="#box { height: 420px; overflow-y: scroll !important}") 
        with demo:
            gr.Markdown("ReAct Agent")
            with gr.Row():
                chat_window = gr.Chatbot(label="Message History", scale=3)
                console = gr.HTML(label="Thoughts", elem_id="box")
            with gr.Row():
                message = gr.Textbox(label="Write A Message", scale=4)
                clear = gr.ClearButton([message, chat_window])
            
            message.submit(self._user, [message, chat_window], [message, chat_window], queue=False).then(
                self._generate_response, chat_window, [chat_window, console], queue=True
            )
        demo.launch(server_name="0.0.0.0", server_port=8080)

if __name__ == "__main__":
    GradioChatPack(run_from_main=True).run()
