import yfinance as yf
from typing import List, Dict, Any

from llama_index.llama_pack.base import BaseLlamaPack
from llama_index.schema import IndexNode
from llama_index import VectorStoreIndex
from llama_index.query_engine import PandasQueryEngine
from llama_index.retrievers import RecursiveRetriever
from llama_index.query_engine import RetrieverQueryEngine
from llama_index.response_synthesizers import get_response_synthesizer


def get_stock_market_data(ticker, **kwargs):
    """
    Retrieve historical market data for a given stock ticker using yfinance.

    Args:
        ticker (str): Stock ticker symbol.
        kwargs: Additional keyword arguments to pass to the yfinance.

    Returns:
        pandas.DataFrame: Historical market data for the specified stock.
    """
    stock = yf.Ticker(ticker)
    hist = stock.history(**kwargs)

    year = [i.year for i in hist.index]
    hist.insert(0, 'year', year)
    month = [i.month for i in hist.index]
    hist.insert(1, 'month', month)
    day = [i.day for i in hist.index]
    hist.insert(2, 'day', day)
    hist.reset_index(drop=True, inplace=True)

    return hist


class StockMarketDataQueryEnginePack(BaseLlamaPack):
    """Historical stock market data query engine pack."""

    def __init__(
        self, 
        tickers: List[str],
        **kwargs: Any,
    ):
        self.tickers = tickers
        self.stocks_market_data = [get_stock_market_data(ticker, **kwargs) for ticker in tickers]
    
    def set_query_engines(self):
        """
        Set up pandas query engines and recursive retriever for historical stock market data.
        """
        
        df_price_query_engines = [PandasQueryEngine(stock) for stock in self.stocks_market_data]

        summaries = [
            f'{ticker} historical market data'
            for ticker in self.tickers
        ]

        df_price_nodes = [
            IndexNode(text=summary, index_id=f'pandas{idx}') 
            for idx, summary in enumerate(summaries)
        ]

        df_price_id_query_engine_mapping = {
            f'pandas{idx}': df_engine
            for idx, df_engine in enumerate(df_price_query_engines)
        }

        stock_price_vector_index = VectorStoreIndex(df_price_nodes)
        stock_price_vector_retriever = stock_price_vector_index.as_retriever(similarity_top_k=1)

        stock_price_recursive_retriever = RecursiveRetriever(
            "vector",
            retriever_dict={"vector": stock_price_vector_retriever},
            query_engine_dict=df_price_id_query_engine_mapping,
            verbose=True,
        )

        stock_price_response_synthesizer = get_response_synthesizer(
            # service_context=service_context,
            response_mode="compact"
        )

        stock_price_query_engine = RetrieverQueryEngine.from_args(
        stock_price_recursive_retriever, response_synthesizer=stock_price_response_synthesizer
        )

        return stock_price_query_engine
    
    def get_modules(self) -> Dict[str, Any]:
        """Get modules."""
        return {
            'tickers': self.tickers,
            'stocks market data': self.stocks_market_data,
            'query engine': self.set_query_engines,
        }
    
    def run(self, *args: Any, **kwargs: Any) -> Any:
        """Run."""
        engine = self.set_query_engines()
        return engine.query(*args, **kwargs)