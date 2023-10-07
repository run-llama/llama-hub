try:
    from llama_hub.imdb_review.scraper import main_scraper
except ImportError:
    from scraper import main_scraper

from llama_index.readers.base import BaseReader


class IMDBReviews(BaseReader):
    def __init__(self, movie_name_year: str, webdriver_engine: str = "edge"):
        self.movie_name_year = movie_name_year
        self.webdriver_engine = webdriver_engine

    def load_data(self):
        movie_reviews_df = main_scraper(self.movie_name_year, self.webdriver_engine)

        return movie_reviews_df


# if __name__ == '__main__':
#     df = IMDBMovieReviewsLoader('The Social Network 2010','edge').load_data()
#     print(df)
