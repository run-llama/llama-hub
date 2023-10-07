## IMDB MOVIE REVIEWS LOADER

This loader fetches all the reviews of a movie or a TV-series from IMDB official site. This loader is working on Windows machine and it requires further debug on Linux. Fixes are on the way

Install the required dependencies

```
pip install -r requirements.txt
```

The IMDB downloader takes in two attributes
* movie_name_year: The name of the movie or series and year
* webdriver_engine: To use edge, google or gecko (mozilla) webdriver

## Usage
```python
from llama_index import download_loader

IMDBReviewsloader = download_loader('IMDBReviews')

loader = IMDBReviewsloader(movie_name_year="The Social Network 2010",webdriver_engine='edge')
df = loader.load_data()
```

It will download the files inside the folder `movie_reviews` with the filename as the movie name

## EXAMPLES

This loader can be used with both Langchain and LlamaIndex.

### LlamaIndex
```python
from llama_index import GPTVectorStoreIndex, download_loader
from llama_index.query_engine import PandasQueryEngine

SECFilingsLoader = download_loader('IMDBReviews')

loader = IMDBReviewsloader(movie_name_year="The Social Network 2010",webdriver_engine='edge')
df = loader.load_data()

query_engine = PandasQueryEngine(df=df, verbose=True)

response = query_engine.query(
    "What did the movie say about Mark Zuckerberg?",
)
print(response)

```

### Langchain

```python
from llama_index import download_loader
from langchain.llms import OpenAI
from langchain.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent

SECFilingsLoader = download_loader('IMDBReviews')

loader = IMDBReviewsloader(movie_name_year="The Social Network 2010",webdriver_engine='edge')
df = loader.load_data()

agent = create_pandas_dataframe_agent(OpenAI(temperature=0, model_name='gpt-3.5-turbo', deployment_id="chat"), df, verbose=True)
agent.run("What did the movie say about Mark Zuckerberg?")
```
