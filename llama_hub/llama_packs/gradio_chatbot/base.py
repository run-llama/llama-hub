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
        self.chat_engine = index.as_chat_engine(chat_mode="context")

    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {}
    
    def _generate_response(self, query: str, chat_history: List[Tuple[str, str]]) -> Tuple[str, List[Tuple[str,str]]]:
        response = self.chat_engine.query(query)
        chat_history.append((query, response.response))
        return "", response.response

    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run the pipeline."""
        import gradio as gr


        demo = gr.Blocks() 
        with demo:
            gr.Markdown("Multi-Modal Retrieval")
            with gr.Row():
                images = gr.Gallery()
            with gr.Row():
                chat_window = gr.Chatbot(label="Message History")
                message = gr.Textbox(label="Write A Message")
                clear = gr.ClearButton([message, chat_window])
            
            message.submit(self._generate_response, [message, chat_window], [message, chat_window])
        demo.launch(server_name="0.0.0.0", server_port=8080)

if __name__ == "__main__":
    GradioChatPack(run_from_main=True).run()
