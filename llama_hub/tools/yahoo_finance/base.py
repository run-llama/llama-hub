from llama_index.tools.tool_spec.base import BaseToolSpec
import yfinance as yf


class YahooFinanceToolSpec(BaseToolSpec):
    """Yahoo Finance tool spec."""
    spec_functions = ["balance_sheet", "income_statement", "cash_flow", "stock_basic_info",
                      "stock_analyst_recommendations", "stock_news"]

    def __init__(self):
        """Initialize the Yahoo Finance tool spec."""

    def balance_sheet(self, ticker: str) -> str:
        """
        Return the balance sheet of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        return "Balance Sheet: \n" + str(stock.balance_sheet)

    def income_statement(self, ticker: str) -> str:
        """
        Return the income statement of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        return "Income Statement: \n" + str(stock.income_stmt)

    def cash_flow(self, ticker: str) -> str:
        """
        Return the cash flow of the stock.

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """

        stock = yf.Ticker(ticker)
        return "Cash Flow: \n" + str(stock.cashflow)

    def stock_basic_info(self, ticker: str) -> str:
        """
        Return the basic info of the stock. Ex: price, description, name

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        return "Info: \n" + str(stock.info)

    def stock_analyst_recommendations(self, ticker: str) -> str:
        """
        Get the analyst recommendations for a stock
        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        return "Recommendations: \n" + str(stock.recommendations)

    def stock_news(self, ticker: str) -> str:
        """
        Get the most recent news titles of a stock

        Args:
          ticker (str): the stock ticker to be given to yfinance

        """
        stock = yf.Ticker(ticker)
        news = stock.news
        out = "News: \n"
        for i in news:
            out += i['title'] + "\n"
        return out