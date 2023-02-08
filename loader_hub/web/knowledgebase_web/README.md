# Knowledge Base Website Loader

This loader is a web crawler and scraper that fetches text content from websites structed as knowledge bases. Typically these sites have a directory structure with several sections and many articles in each section. This loader crawls and finds all links that match the article path provided, and scrapes the content of each page.

It uses [Playwright](https://playwright.dev/python/) to drive a browser to do the scraping, this reduces the chance of getting blocked by Cloudflare or other CDNs.

## Usage

To use this loader, you need to pass in the root URL and the string to search for in the URL to tell if the crawler has reached an article. You also need to pass in several CSS selectors so the cralwer knows which links to follow and which elements to extract content from. use 

```python
from gpt_index import download_loader

KnowledgeBaseWebReader = download_loader("KnowledgeBaseWebReader")

loader = KnowledgeBaseWebReader()
documents = loader.load_data(
  root_url='https://support.intercom.com', 
  link_selectors=['.article-list a', '.article-list a']
  article_path='/articles'
  body_selector='.article-body'
  title_selector='.article-title'
  subtitle_selector='.article-subtitle'
  )
```

## Examples

This loader is designed to be used as a way to load data into [GPT Index](https://github.com/jerryjliu/gpt_index/tree/main/gpt_index) and/or subsequently used as a Tool in a [LangChain](https://github.com/hwchase17/langchain) Agent.

### GPT Index

```python
from gpt_index import GPTSimpleVectorIndex, download_loader

KnowledgeBaseWebReader = download_loader("KnowledgeBaseWebReader")

loader = KnowledgeBaseWebReader()
documents = loader.load_data(
  root_url='https://support.intercom.com', 
  link_selectors=['.article-list a', '.article-list a']
  article_path='/articles'
  body_selector='.article-body'
  title_selector='.article-title'
  subtitle_selector='.article-subtitle'
  )
index = GPTSimpleVectorIndex(documents)
index.query('What languages does Intercom support?')
```

### LangChain

Note: Make sure you change the description of the `Tool` to match your use-case.

```python
from gpt_index import GPTSimpleVectorIndex, download_loader
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
from langchain.chains.conversation.memory import ConversationBufferMemory

KnowledgeBaseWebReader = download_loader("KnowledgeBaseWebReader")

loader = KnowledgeBaseWebReader()
documents = loader.load_data(
  root_url='https://support.intercom.com', 
  link_selectors=['.article-list a', '.article-list a']
  article_path='/articles'
  body_selector='.article-body'
  title_selector='.article-title'
  subtitle_selector='.article-subtitle'
  )
index = GPTSimpleVectorIndex(documents)

tools = [
    Tool(
        name="Website Index",
        func=lambda q: index.query(q),
        description=f"Useful when you want answer questions about a product that has a public knowledge base.",
    ),
]
llm = OpenAI(temperature=0)
memory = ConversationBufferMemory(memory_key="chat_history")
agent_chain = initialize_agent(
    tools, llm, agent="zero-shot-react-description", memory=memory
)

output = agent_chain.run(input="What languages does Intercom support?")
```
