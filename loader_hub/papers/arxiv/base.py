"""Read Arxiv Papers."""
import os
import hashlib
from typing import List, Optional

from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document
from gpt_index import download_loader


class ArxivReader(BaseReader):
    """Arxiv Reader.

    Gets a search query, return a list of Documents of the top corresponding scientific papers on Arxiv.
    """

    def __init__(
        self,
        verbose: bool = False,
    ):
        """Initialize with parameters."""
        super().__init__(verbose)

    def _hacky_hash(self, some_string):
        _hash = hashlib.md5(some_string.encode("utf-8")).hexdigest()
        return _hash

    def load_data(
        self,
        search_query: str,
        papers_dir: Optional[str] = ".papers",
        max_results: Optional[int] = 10,
    ) -> List[Document]:
        """Search for a topic on Arxiv, download the PDFs of the top results locally, then read them.

        Args:
            search_query (str): A topic to search for (e.g. "Artificial Intelligence").
            papers_dir (Optional[str]): Locally directory to store the papers
            max_results (Optional[int]): Maximum number of papers to fetch.

        Returns:
            List[Document]: A list of Document objects.
        """
        import arxiv

        arxiv_search = arxiv.Search(
            query=search_query,
            id_list=[],
            max_results=max_results,
            sort_by=arxiv.SortCriterion.Relevance,
        )
        search_results = list(arxiv_search.results())
        if self.verbose:
            print(f"> Successfully fetched {len(search_results)} paperes")

        if not os.path.exists(papers_dir):
            os.makedirs(papers_dir)

        paper_lookup = {}
        for paper in search_results:
            # Hash filename to avoid bad charaters in file path
            filename = f"{self._hacky_hash(paper.title)}.pdf"
            paper_lookup[os.path.join(papers_dir, filename)] = {
                "Title of this paper": paper.title,
                "Authors": (", ").join([a.name for a in paper.authors]),
                "Date published": paper.published.strftime("%m/%d/%Y"),
                "URL": paper.entry_id,
                # "summary": paper.summary
            }
            paper.download_pdf(dirpath=papers_dir, filename=filename)
            if self.verbose:
                print(f"> Downloading {filename}...")

        def get_paper_metadata(filename):
            return paper_lookup[filename]

        SimpleDirectoryReader = download_loader("SimpleDirectoryReader")
        arxiv_documents = SimpleDirectoryReader(
            papers_dir, file_metadata=get_paper_metadata
        ).load_data()
        # Include extra documents containing the abstracts
        abstract_documents = []
        for paper in search_results:
            d = f"The following is a summary of the paper: {paper.title}\n\nSummary: {paper.summary}"
            abstract_documents.append(Document(d))

        # Delete downloaded papers
        try:
            for f in os.listdir(papers_dir):
                os.remove(os.path.join(papers_dir, f))
                if self.verbose:
                    print(f"> Deleted file: {f}")
            os.rmdir(papers_dir)
            if self.verbose:
                print(f"> Deleted directory: {papers_dir}")
        except OSError:
            print("Unable to delete files or directory")

        return arxiv_documents + abstract_documents
