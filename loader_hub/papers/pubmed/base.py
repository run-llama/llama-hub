"""Read Pubmed Papers."""
from typing import List, Optional

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class PubmedReader(BaseReader):
    """Pubmed Reader.

    Gets a search query, return a list of Documents of the top corresponding scientific papers on Pubmed.
    """

    def load_data(
        self,
        search_query: str,
        max_results: Optional[int] = 10,
    ) -> List[Document]:
        """Search for a topic on Pubmed, fetch the text of the most relevant full-length papers.

        Args:
            search_query (str): A topic to search for (e.g. "Alzheimers").
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects.
        """
        from datetime import datetime
        import xml.etree.ElementTree as xml
        
        import requests

        pubmed_search = []
        parameters = {"tool": "tool", "email": "email", "db": "pmc"}
        parameters["term"] = search_query
        parameters["retmax"] = max_results
        resp = requests.get(
            "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            params=parameters,
        )
        root = xml.fromstring(resp.content)

        for elem in root.iter():
            if elem.tag == "Id":
                _id = elem.text
                try:
                    resp = requests.get(
                        f"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC{_id}/ascii"
                    )
                    info = resp.json()
                    title = "Pubmed Paper"
                    try:
                        title = [
                            p["text"]
                            for p in info["documents"][0]["passages"]
                            if p["infons"]["section_type"] == "TITLE"
                        ][0]
                    except KeyError:
                        pass
                    pubmed_search.append(
                        {
                            "title": title,
                            "url": f"https://www.ncbi.nlm.nih.gov/pmc/articles/PMC{_id}/",
                            "date": info["date"],
                            "documents": info["documents"],
                        }
                    )
                except Exception:
                    print(f"Unable to parse PMC{_id} or it does not exist")
                    pass

        # Then get documents from Pubmed text, which includes abstracts
        pubmed_documents = []
        for paper in pubmed_search:
            for d in paper["documents"]:
                text = "\n".join([p["text"] for p in d["passages"]])
                pubmed_documents.append(
                    Document(
                        text,
                        extra_info={
                            "Title of this paper": paper["title"],
                            "URL": paper["url"],
                            "Date published": datetime.strptime(
                                paper["date"], "%Y%m%d"
                            ).strftime("%m/%d/%Y"),
                        },
                    )
                )

        return pubmed_documents
