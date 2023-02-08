from typing import List
from gpt_index.readers.base import BaseReader
from gpt_index.readers.schema.base import Document

class KnowledgeBaseWebReader(BaseReader):
    """Knowledge base reader.
    
    Crawls and reads articles from a knowledge base/help center with Playwright.
    Tested on Zendesk and Intercom CMS, may work on others. 
    Can be run in headless mode but it may be blocked by Cloudflare. Run it headed to be safe.
    Times out occasionally, just increase the default time out if it does.
    Requires the `playwright` package.
    
    Args:
        root_url (string): the base url of the knowledge base, with no trailing slash
            e.g. 'https://support.intercom.com'
        link_selectors (list): list of css selectors to find links to articles while crawling
            e.g. ['.article-list a', '.article-list a']
        article_path (string): the url path of articles on this domain so the crawler knows when to stop
            e.g. '/articles'
        title_selector (string): css selector to find the title of the article
            e.g. '.article-title'
        subtitle_selector (string): css selector to find the subtitle/description of the article
            e.g. '.article-subtitle'
        body_selector (string): css selector to find the body of the article
            e.g. '.article-body'
    """

    def __init__(self, root_url, link_selectors, article_path, title_selector, subtitle_selector, body_selector) -> None:
        """Initialize with parameters."""
        self.root_url = root_url
        self.link_selectors = link_selectors
        self.article_path = article_path
        self.title_selector = title_selector
        self.subtitle_selector = subtitle_selector
        self.body_selector = body_selector

    def load_data(self) -> List[Document]:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)

            # Crawl
            article_urls = self.get_article_urls(browser, self.root_url, self.root_url, self.link_selectors, self.article_path)

            # Scrape
            documents = []
            for url in article_urls:
                article = self.scrape_article(browser, url, self.title_selector, self.subtitle_selector, self.body_selector)
                extra_info = {'title': article['title'], 'subtitle': article['subtitle'], 'url': article['url']}
                documents.append(Document(article['body'], extra_info=extra_info))

            browser.close()

            return documents

    def scrape_article(self, browser, url, title_selector, subtitle_selector, body_selector):
        page = browser.new_page(ignore_https_errors=True)
        page.set_default_timeout(60000)
        page.goto(url, wait_until='domcontentloaded')

        title = (page.query_selector(title_selector).evaluate("node => node.innerText")) if title_selector else ''
        subtitle = (page.query_selector(subtitle_selector).evaluate("node => node.innerText")) if subtitle_selector else ''
        body = (page.query_selector(body_selector).evaluate("node => node.innerText")) if body_selector else ''

        page.close()
        print('scraped:', url)
        return {
            'title': title,
            'subtitle': subtitle,
            'body': body,
            'url': url
        }
    
    def get_article_urls(self, browser, root_url, current_url, link_selectors, article_path):
        page = browser.new_page(ignore_https_errors=True)
        page.set_default_timeout(60000)
        page.goto(current_url, wait_until="domcontentloaded")

        # If this is a leaf node aka article page, return itself
        if article_path in current_url:
            print('Found an article: ', current_url)
            page.close()
            return [current_url]

        # Otherwise crawl this page and find all the articles linked from it
        article_urls = []
        links = []

        for link_selector in link_selectors:
            ahrefs = page.query_selector_all(link_selector)
            links.extend(ahrefs)

        for link in links:
            url = root_url + page.evaluate("(node) => node.getAttribute('href')", link)
            article_urls.extend(self.get_article_urls(browser, root_url, url, link_selectors, article_path))

        page.close()

        return article_urls
