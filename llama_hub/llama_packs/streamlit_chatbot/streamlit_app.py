import streamlit as st
import llama_index
from llama_index.llms import OpenAI
import openai
from streamlit_pills import pills
from llama_index.tools.query_engine import QueryEngineTool
from llama_index import (
    VectorStoreIndex,
    ServiceContext,
    download_loader,
)

st.set_page_config(page_title="Chat with Snowflake's Wikipedia page, powered by LlamaIndex", page_icon="🦙", layout="centered", initial_sidebar_state="auto", menu_items=None)

if "messages" not in st.session_state.keys(): # Initialize the chat messages history
    st.session_state.messages = [
        {"role": "assistant", "content": "Ask me a question about Snowflake!"}
    ]

st.title("Chat with Snowflake's Wikipedia page, powered by LlamaIndex 💬🦙")
st.info("This example is powered by the **[Llama Hub Wikipedia Loader](https://llamahub.ai/l/wikipedia)**. Use any of [Llama Hub's many loaders](https://llamahub.ai/) to retrieve and chat with your data via a Streamlit app.", icon="ℹ️")
openai.api_key = st.secrets.openai_key

def add_to_message_history(role, content):
    message = {"role": role, "content": str(content)}
    st.session_state.messages.append(message) # Add response to message history

@st.cache_resource
def load_index_data():
    WikipediaReader = download_loader("WikipediaReader",custom_path="local_dir")
    loader = WikipediaReader()
    docs = loader.load_data(pages=['Snowflake Inc.'])
    service_context = ServiceContext.from_defaults(llm=OpenAI(model="gpt-3.5-turbo", temperature=0.5))
    index = VectorStoreIndex.from_documents(docs, service_context=service_context)
    return index

index = load_index_data()

selected = pills("Choose a question to get started or write your own below.", ["What is Snowflake?", "What company did Snowflake announce they would acquire in October 2023?", "What company did Snowflake acquire in March 2022?", "When did Snowflake IPO?"], clearable=True, index=None)

if "chat_engine" not in st.session_state.keys(): # Initialize the query engine
    st.session_state.chat_engine = index.as_chat_engine(chat_mode="condense_question", verbose=True)

for message in st.session_state.messages: # Display the prior chat messages
    with st.chat_message(message["role"]):
        st.write(message["content"])

if selected:
    with st.chat_message("user"):
        st.write(selected)
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(selected)
            st.write(str(response))
            add_to_message_history("user",selected)
            add_to_message_history("assistant",response)

if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
    add_to_message_history("user",prompt)

# If last message is not from assistant, generate a new response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = st.session_state.chat_engine.chat(prompt)
            st.write(response.response)
            add_to_message_history("assistant",response.response)
