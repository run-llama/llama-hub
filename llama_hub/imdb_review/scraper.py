try:
    from selenium import webdriver
    from selenium.webdriver.common.by import By
    from selenium.common.exceptions import NoSuchElementException
    import pandas as pd
    import os
    import time
    import re
    import concurrent.futures
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.microsoft import EdgeChromiumDriverManager
    from webdriver_manager.chrome import ChromeDriverManager
    from webdriver_manager.firefox import GeckoDriverManager

    import imdb
except ImportError:
    print("There is an import error")


def clean_text(text: str) -> str:
    """Clean raw text string.

    Args:
        text (str): Raw text to clean.

    Returns:
        str: cleaned text.
    """
    # Spacing and filters
    text = re.sub(
        r"([!\"'#$%&()*\+,-./:;<=>?@\\\[\]^_`{|}~])", r" \1 ", text
    )  # add spacing
    text = re.sub("[^A-Za-z0-9]+", " ", text)  # remove non alphanumeric chars
    text = re.sub(" +", " ", text)  # remove multiple spaces
    text = re.sub(r"http\S+", "", text)  # remove links
    text = re.sub("Was this review helpful? Sign in to vote.", "", text)
    text = re.sub("Permalink", "", text)
    text = re.sub(r"\.\.\.", "", text)
    text = re.sub(r"\.\.", "", text)
    text = re.sub('""', "", text)
    text = re.sub(r"\d+ out of \d+ found this helpful", "", text)
    text = text.strip()  # strip white space at the ends

    return text


def scrape_data(revs):
    """Multiprocessing function to get the data from the IMDB reviews page

    Args:
        revs (selenium element): element for all the reviews

    Returns:
        date (str): The date of the review
        contents (str): the review of the movie
        rating (str): The ratinng given by the user
        title (str): the title of the review
        link(str): the link of the review
    """

    try:
        # if_spoiler = revs.find_element(By.CLASS_NAME, "spoiler-warning")
        spolier_btn = revs.find_element(By.CLASS_NAME, "ipl-expander")
        spolier_btn.click()
        contents = revs.find_element(
            By.XPATH, "//div[contains(@class, 'text show-more__control')]"
        ).text
    except NoSuchElementException:
        contents = revs.find_element(By.CLASS_NAME, "content").text
        if contents == "":
            contents = revs.find_element(
                By.CLASS_NAME, "text show-more__control clickable"
            ).text

    try:
        title = revs.find_element(By.CLASS_NAME, "title").text.strip()
    except NoSuchElementException:
        title = ""
    try:
        link = revs.find_element(By.CLASS_NAME, "title").get_attribute("href")
    except NoSuchElementException:
        link = ""
    try:
        rating = revs.find_element(
            By.CLASS_NAME, "rating-other-user-rating"
        ).text.split("/")[0]
    except NoSuchElementException:
        rating = ""
    re.sub("\n", " ", contents)
    re.sub("\t", " ", contents)
    contents.replace("//", "")
    date = revs.find_element(By.CLASS_NAME, "review-date").text
    contents = clean_text(contents)
    return date, contents, rating, title, link


def main_scraper(
    movie_name: str, webdriver_engine: str = "edge", generate_csv: bool = False
):
    """The main helper function to scrape data in multiprocessing way

    Args:
        movie_name (str): The name of the movie along with the year
        webdriver_engine (str, optional): The webdriver engine to use. Defaults to "edge".
        generate_csv (bool, optional): whether to save the dataframe files. Defaults to False.

    Returns:
        reviews_date (List): list of dates of each review
        reviews_title (List): list of title of each review
        reviews_comment (List): list of comment of each review
        reviews_rating (List):  list of ratings of each review
        reviews_link (List):  list of links of each review
    """
    ia = imdb.Cinemagoer()
    movies = ia.search_movie(movie_name)
    movie_name = movies[0].data["title"] + " " + str(movies[0].data["year"])

    assert movie_name != "", "Please check the movie name that you passed"
    print(
        f"Scraping movie reviews for {movie_name}. If you think it is not the right one, the best practice is to pass the movie name and year"
    )
    movie_id = movies[0].movieID
    movie_link = f"https://www.imdb.com/title/tt{movie_id}/reviews/?ref_=tt_ql_2"
    if webdriver_engine == "edge":
        driver = webdriver.Edge(service=Service(EdgeChromiumDriverManager().install()))
    elif webdriver_engine == "google":
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    elif webdriver_engine == "firefox":
        driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()))

    driver.get(movie_link)
    driver.maximize_window()

    driver.execute_script("return document.body.scrollHeight")

    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight-250);")
        try:
            load_button = driver.find_element(By.CLASS_NAME, "ipl-load-more__button")
            load_button.click()
            time.sleep(1)
        except Exception:
            print("Load more operation complete")
            break

    driver.execute_script("window.scrollTo(0, 100);")

    rev_containers = driver.find_elements(By.CLASS_NAME, "review-container")

    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        results = executor.map(scrape_data, rev_containers)
    reviews_date = []
    reviews_comment = []
    reviews_rating = []
    reviews_title = []
    reviews_link = []
    for result in results:
        date, contents, rating, title, link = result
        reviews_date.append(date)

        reviews_comment.append(contents)
        reviews_rating.append(rating)
        reviews_title.append(title)
        reviews_link.append(link)

        # driver.quit()
    if generate_csv:
        os.makedirs("movie_reviews", exist_ok=True)
        df = pd.DataFrame(
            columns=["review_date", "review_title", "review_comment", "review_rating"]
        )

        df["review_date"] = reviews_date
        df["review_title"] = reviews_title
        df["review_comment"] = reviews_comment
        df["review_rating"] = reviews_rating
        df["review_link"] = reviews_link

        # print(df)
        df.to_csv(f"movie_reviews/{movie_name}.csv", index=False)

    return reviews_date, reviews_title, reviews_comment, reviews_rating, reviews_link
