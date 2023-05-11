"""MangoppsGuides reader."""
import json
from typing import List

from llama_index.readers.base import BaseReader
from llama_index.readers.schema.base import Document

from bs4 import BeautifulSoup
from concurrent.futures import ThreadPoolExecutor
import requests
from urllib.parse import urlparse


class MangoppsGuidesReader(BaseReader):
    """MangoppsGuides reader. Reads data from a MangoppsGuides workspace.

    Args:
        domain_url (str): MangoppsGuides domain url
        limir (int): depth to crawl
    """

    def __init__(self, domain_url: str, limit: int) -> None:
        """Initialize MangoppsGuides reader."""
        self.domain_url = domain_url
        self.limit = limit
        self.start_url = f"{self.domain_url}/home/"

    def load_data(self) -> List[Document]:
        """Load data from the workspace.
        Returns:
            List[Document]: List of documents.
        """

        results = []

        self.fetched_urls = self.crawl_urls()

        self.guides_pages = {}
        self.failed_urls = []

        for url in self.fetched_urls:
            scraper = GuidesScraper(url)
            print(f"Url scraping: {url}")
            try:
                page_text = scraper.scrape()
                guides_page = {}
                guides_page["text"] = page_text
                self.guides_pages[url] = guides_page
                print(f"Url scraping done: {url}")
            except Exception as e:
                self.failed_urls.append(url)
                print(f"Url scraping failed: {url}")

        for k, v in self.guides_pages.items():
            extra_info = {
                "url": k,
            }
            results.append(
                Document(
                    v["text"],
                    extra_info=extra_info,
                )
            )

        return results

    def crawl_urls(self) -> List[str]:
        """Crawls all the urls from given domain"""

        self.visited = []
        fetched_urls = self.fetch_url(self.start_url)

        print(f"All urls {fetched_urls}")
        print(f"All visited urls {self.visited}")

        return fetched_urls

    def fetch_url(self, url):
        """Fetch the urls from given domain"""

        newurls = []
        self.visited.append(url)

        print(f"Checking URL: {url}")
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")

        for link in soup.find_all("a")[:self.limit]:
            href: str = link.get("href")
            if href and urlparse(href).netloc == self.domain_url:
                newurls.append(href)
            elif href and href.startswith("/"):
                newurls.append(f"{self.domain_url}{href}")

        for newurl in newurls[:self.limit]:
            if (
                newurl not in self.visited
                and not newurl.startswith("#")
                and f"https://{urlparse(newurl).netloc}" == self.domain_url
            ):
                newurls = newurls + self.fetch_url(newurl)
        return newurls


class GuidesScraper:
    def __init__(self, url) -> None:
        self.url = url

    def scrape(self):
        self.extracted_text = self.page_text(self.url)
        self.formatted_text = self.reformat_text(self.extracted_text)
        return self.formatted_text

    def extract_text(self, element: BeautifulSoup):
        result = ""
        for ele in reversed(element.find_all("div", {"class": "css-175oi2r"})):
            indent = "  " * len(ele.find_parents(["ol", "ul"]))
            text = ele.get_text().strip()
            if text:
                if len(ele.get_attribute_list("class")) > 1:
                    result = f"{indent}- {text}\n{result}"
                else:
                    ind = result.find("-")
                    result = f"{indent}- {text} {result[ind+2:]}"

            if ele.find_all("a"):
                anch = ele.find("a")
                if anch["href"].startswith("#"):
                    result = f"{anch['href']}\n{result}"

            ele.decompose()

        return result

    def reformat_text(self, text: str):
        new_text = []
        for line in text.split("\n"):
            line = line.replace("\u200b", "")
            l_tex = line.strip()
            if not len(l_tex) < 3:
                if l_tex.startswith("#"):
                    new_text.append("")

                new_text.append(line)

        return "\n".join(new_text)

    def page_text(self, url):
        page_class = "r-1oszu61 r-1xc7w19 r-1phboty r-1yadl64 r-deolkf r-6koalj r-crgep1 r-ifefl9 r-bcqeeo r-t60dpp r-bnwqim r-417010 r-1ro0kt6 r-16y2uox r-1wbh5a2 r-eqz5dr"

        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        page_content: List[BeautifulSoup] = soup.find_all(
            "main", {"class": page_class})

        soup_page: BeautifulSoup = page_content[0]

        blocks: List[BeautifulSoup] = soup_page.find_all(
            "div", {"class": "css-175oi2r r-1ro0kt6 r-16y2uox r-1wbh5a2 r-ecifi"}
        )

        text = ""
        for i, block in enumerate(blocks):
            if i == 0:
                first = block.get_text(separator="\n")
                text += first
                block.decompose()
                continue

            text += "\n" + self.extract_text(block)
            block.decompose()

        return text


if __name__ == "__main__":
    reader = MangoppsGuidesReader(
        domain_url="https://guides.mangoapps.com", limit=5)
    print("Initialized MangoppsGuidesReader")
    output = reader.load_data()
    print(output)
