# 💬🦙 Chat with Snowflake's Wikipedia page, powered by LlamaIndex

Build a chatbot powered by LlamaIndex that augments GPT 3.5 with the contents of Snowflake's Wikipedia page (or your own data).

## Overview of the App

<img src="app.png" width="75%">

- Takes user queries via Streamlit's `st.chat_input` and displays both user queries and model responses with `st.chat_message`
- Uses LlamaIndex to load and index data and create a chat engine that will retrieve context from that data to respond to each user query

## Demo App

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://llamapack.streamlit.app/))

## Get an OpenAI API key

You can get your own OpenAI API key by following the following instructions:
1. Go to https://platform.openai.com/account/api-keys.
2. Click on the `+ Create new secret key` button.
3. Next, enter an identifier name (optional) and click on the `Create secret key` button.
   
Use Streamlit's [secrets management feature](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management) to add your OpenAI API key to your Streamlit app.

## Try out the app

Once the app is loaded, enter your question about Snowflake (or choose from the example questions) and wait for a response.
