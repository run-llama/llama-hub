from llama_index.schema import Document
from llama_index.readers.base import BaseReader

try:
    from llama_hub.sec_filings.secData import sec_main
except:
    from secData import sec_main
from datetime import datetime
from typing import List


class SECFilingsLoader(BaseReader):
    def __init__(
        self, ticker: str, year: int, forms: List[str], include_amends: bool = True
    ):
        """SEC Filings loader for 10-K, 10-Q and S-1 filings

        Args:
            ticker (str): Symbol of the company
            year (str): Year of the data required
        """
        curr_year = datetime.now().year
        assert year <= curr_year, "The year should be less than current year"

        self.ticker = ticker
        self.year = str(year)
        self.forms = forms
        self.include_amends = include_amends

    def load_data(self) -> List[Document]:

        section_texts = sec_main(
            self.ticker, self.year, self.forms, self.include_amends
        )
        docs = []
        for filings in section_texts:
            texts_dict = filings[-1]

            for section_name, text in texts_dict.items():
                docs.append(
                    Document(
                        text=text,
                        extra_info={
                            "accessionNumber": filings[0],
                            "filing_type": filings[1],
                            "filingDate": filings[2],
                            "reportDate": filings[3],
                            "sectionName": section_name,
                        },
                    )
                )
        return docs
