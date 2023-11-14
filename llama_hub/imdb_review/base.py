try:
    from llama_hub.imdb_review.scraper import main_scraper
except ImportError:
    from scraper import main_scraper
from typing import List
from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document


class IMDBReviews(BaseReader):
    def __init__(
        self,
        movie_name_year: str,
        webdriver_engine: str = "edge",
        generate_csv: bool = False,
    ):
        assert webdriver_engine in [
            "google",
            "edge",
            "firefox",
        ], "The webdriver should be in ['google','edge','firefox']"
        self.movie_name_year = movie_name_year
        self.webdriver_engine = webdriver_engine
        self.generate_csv = generate_csv

    def load_data(self) -> List[Document]:
        """scrapes the data from the IMDB website movie reviews

        Returns:
            List[Document]: document object in llama index with date and rating as extra information
        """
        (
            reviews_date,
            reviews_title,
            reviews_comment,
            reviews_rating,
            reviews_link,
        ) = main_scraper(self.movie_name_year, self.webdriver_engine, self.generate_csv)

        all_docs = []
        for i in range(len(reviews_date)):
            all_docs.append(
                Document(
                    text=reviews_title[i] + " " + reviews_comment[i],
                    extra_info={
                        "date": reviews_date[i],
                        "rating": reviews_rating[i],
                        "link": reviews_link[i],
                    },
                )
            )
        return all_docs


# if __name__ == '__main__':
#     loader = IMDBReviews(movie_name_year="The Social Network 2010",webdriver_engine='edge')
#     docs = loader.load_data()
#     print(docs)
