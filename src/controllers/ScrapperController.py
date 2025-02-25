import concurrent.futures
import re
from typing import List, Union

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import WebDriverException


class Scrapper:
    def __init__(
        self,
        docker_url: str = "http://localhost:4444/wd/hub",
        driver_method: str = "normal",
    ):
        self.docker_url = docker_url
        if driver_method not in ["docker", "normal"]:
            raise ValueError("driver_method must be either 'docker' or 'normal'")
        self.driver_method = driver_method

    def _load_html_page_docker(self, url: str) -> str:
        try:
            options = webdriver.ChromeOptions()
            driver = webdriver.Remote(self.docker_url, options=options)
            driver.get(url)
            html = driver.page_source
            driver.quit()
            return html
        except WebDriverException as e:
            print(f"Error loading page {url}: {e}")
            return ""

    def _load_html_page_normal(self, url: str) -> str:
        try:
            options = webdriver.ChromeOptions()
            options.add_argument("--headless")
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            html = driver.page_source
            driver.quit()
            return html
        except WebDriverException as e:
            print(f"Error loading page {url}: {e}")
            return ""

    def load_html_page(self, url: str) -> str:
        if self.driver_method == "docker":
            return self._load_html_page_docker(url)
        return self._load_html_page_normal(url)

    def get_html(self, url_list: List[str]) -> List[str]:
        if isinstance(url_list, str):
            url_list = [url_list]
        max_workers = 10 if self.driver_method == "docker" else 1
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            htmls = list(executor.map(self.load_html_page, url_list))
        return htmls

    def decompose_unnecessary_tags(self, html_soup: BeautifulSoup) -> BeautifulSoup:
        for script in html_soup.find_all("script"):
            script.decompose()

        for style in html_soup.find_all("style"):
            style.decompose()

        for link in html_soup.find_all("link"):
            link.decompose()

        for tag in html_soup.find_all(class_="hidden") or html_soup.find_all(
            type="hidden"
        ):
            tag.decompose()

        for script in html_soup.find_all("script"):
            script.decompose()

        for head in html_soup.find_all("head"):
            head.decompose()

        for tag in html_soup.find_all(True):
            if tag.string:
                tag.string = re.sub(r"\s+", " ", tag.string.strip())

        return html_soup

    def get_decomposed_html_soup(self, url_list: Union[str, List[str]]):
        html = self.get_html(url_list=url_list)
        html_soup = [BeautifulSoup(h, "html.parser") for h in html]
        decomposed_html_soup = [
            self.decompose_unnecessary_tags(html_soup=html) for html in html_soup
        ]

        return decomposed_html_soup
