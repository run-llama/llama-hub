# SEC DATA DOWNLOADER

Please checkout this repo that I am building on SEC Question Answering Agent [SEC-QA](https://github.com/Athe-kunal/SEC-QA-Agent)

This repository downloads all the texts from SEC documents (10-K and 10-Q). Currently, it is not supporting documents that are amended, but that will be added in the near futures.

Install the required dependencies

```
python install -r requirements.txt
```

The SEC Downloader expects 4 attributes

* tickers: It is a list of valid tickers
* filing_types (List): 10-K or 10-Q or S-1 filing type 
* include_amends: To include amendments or not.
* year: The year for which you need the data

## Usage
```python
from llama_index import download_loader

SECFilingsLoader = download_loader('SECFilingsLoader')

loader = SECFilingsLoader(tickers='TSLA',year=2023,forms=["10-K","10-Q"],include_amends=True)
docs = loader.load_data()
```

It also returns the following metadata

* Filing Date of the filing
* Reporting date of the filing
* Accession number of the filing (unique identifier of the filing)
* form type: "10-K" or "10-Q1", "10-Q2", "10-Q3" and for amended documents, it will end with /A
* Section name of the text

There are also section names in different document types. You can check it by running

```python
from llama_hub.sec_filings.section_names import SECTIONS_10K, SECTION_10Q

print(SECTIONS_10K)
```

## EXAMPLES

This loader is can be used with both Langchain and LlamaIndex.

### LlamaIndex
```python
from llama_index import VectorStoreIndex, download_loader
from llama_index import SimpleDirectoryReader

SECFilingsLoader = download_loader('SECFilingsLoader')

loader = SECFilingsLoader(tickers='TSLA',year=2023,forms=["10-K","10-Q"],include_amends=True)
documents = loader.load_data()

index = VectorStoreIndex.from_documents(documents)
index.query('What are the risk factors of Tesla for the year 2022?')

```

### Langchain

```python
from llama_index import download_loader
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA
from langchain.document_loaders import DirectoryLoader
from langchain.indexes import VectorstoreIndexCreator

SECFilingsLoader = download_loader('SECFilingsLoader')

loader = SECFilingsLoader(tickers='TSLA',year=2023,forms=["10-K","10-Q"],include_amends=True)
documents = loader.load_data()

index = VectorstoreIndexCreator().from_documents(documents)
retriever = index.vectorstore.as_retriever()
qa = RetrievalQA.from_chain_type(llm=OpenAI(), chain_type="stuff", retriever=retriever)

query = "What are the risk factors of Tesla for the year 2022?"
qa.run(query)
```
## REFERENCES
1. Unstructured SEC Filings API: [repo link](https://github.com/Unstructured-IO/pipeline-sec-filings/tree/main)


