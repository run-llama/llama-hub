from base import IMDBReviews

loader = IMDBReviews(
    "The Social Network 2010",
    webdriver_engine="google"
)

ad = loader.load_data()
# print(ad)