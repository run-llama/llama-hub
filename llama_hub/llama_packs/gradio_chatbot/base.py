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

from contextlib import redirect_stdout
import io


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


    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}
    
    def _user(self, user_message, history):
        return "", history + [(user_message, "")]
    
    def _generate_response(self, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str,str]]]:
        f = io.StringIO()
        with redirect_stdout(f):
            response = self.agent.stream_chat(chat_history[-1][0])
        for token in response.response_gen:
            print(token)
            chat_history[-1][1] += token
            yield chat_history

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        import gradio as gr


        demo = gr.Blocks() 
        with demo:
            gr.Markdown("ReAct Agent")
            with gr.Row():
                chat_window = gr.Chatbot(label="Message History", scale=3)
                console = gr.Textbox(label="Thoughts", lines=18, interactive=False)
            with gr.Row():
                message = gr.Textbox(label="Write A Message", scale=4)
                clear = gr.ClearButton([message, chat_window])
            
            message.submit(self._user, [message, chat_window], [message, chat_window], queue=False).then(
                self._generate_response, chat_window, chat_window
            )
        demo.launch(server_name="0.0.0.0", server_port=8080)

if __name__ == "__main__":
    GradioChatPack(run_from_main=True).run()
