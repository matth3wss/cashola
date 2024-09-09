import concurrent.futures
import re
from typing import Dict, List, Union, override

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from core.regex import RegexPatterns as regex


class Sefaz:
    def __init__(self):
        pass

    @staticmethod
    def load_html_page(url: str) -> str:
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote("http://localhost:4444/wd/hub", options=options)
        driver.get(url)
        html = driver.page_source
        driver.quit()
        return html

    def get_html(self, urls: List[str]) -> List[str]:
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            responses = list(executor.map(self.load_html_page, urls))

        return responses

    def rebuild_html(self, soup: BeautifulSoup) -> BeautifulSoup:
        for script in soup.find_all("script"):
            script.decompose()

        for style in soup.find_all("style"):
            style.decompose()

        for link in soup.find_all("link"):
            link.decompose()

        for tag in soup.find_all(class_="hidden") or soup.find_all(type="hidden"):
            tag.decompose()

        for tag in soup.find_all(True):
            if tag.string:
                tag.string = re.sub(r"\s+", " ", tag.string.strip())

        [sellers_info] = soup.find_all("div", class_="txtCenter", id=False)
        groceries_table = soup.find("table", id="tabResult")
        receipt_details = soup.find("div", class_="txtRight", id="totalNota")

        html_soup = BeautifulSoup(
            f"{sellers_info}{groceries_table}{receipt_details}",
            "html.parser",
        )

        return html_soup

    def get_sellers_info(self, soup: BeautifulSoup) -> List[Dict[str, str]]:
        sellers_info = []
        divs = soup.find_all("div", class_="txtCenter")
        for div in divs:
            name = (
                div.find("div", class_="txtTopo").get_text(strip=True)
                if div.find("div", class_="txtTopo")
                else None
            )
            cnpj = (
                regex._convert_brazilian_number(
                    div.find("div", class_="text").get_text(strip=True)
                )
                if div.find("div", class_="text")
                else None
            )
            address = (
                div.find_all("div", class_="text")[1].get_text(strip=True)
                if len(div.find_all("div", class_="text")) > 1
                else None
            )
            sellers_info.append({"name": name, "cnpj": cnpj, "address": address})

        return sellers_info

    def normalize_groceries(self, groceries: List[Dict[str, Union[str, int, float]]]):
        # Write a function that checks if the name, code, unit_type are the same and recreate the list of groceries summing the unit_value and total_value

        normalized_groceries = []
        for grocery in groceries:
            if grocery not in normalized_groceries:
                normalized_groceries.append(grocery)
            else:
                normalized_groceries[0]["unit_value"] += grocery["unit_value"]
                normalized_groceries[0]["total_value"] += grocery["total_value"]

        return normalized_groceries

    def get_groceries(
        self, soup: BeautifulSoup
    ) -> List[Dict[str, Union[str, int, float]]]:
        groceries = []
        for tr in soup.find_all("tr", id=True):
            grocery = {
                "name": tr.find("span", class_="txtTit").get_text(strip=True),
                "code": regex.code(tr.find("span", class_="RCod").get_text(strip=True)),
                "quantity": regex.quantity(
                    tr.find("span", class_="Rqtd").get_text(strip=True)
                ),
                "unit_type": regex.unit_type(
                    tr.find("span", class_="RUN").get_text(strip=True)
                ),
                "unit_value": regex.unit_value(
                    tr.find("span", class_="RvlUnit").get_text(strip=True)
                ),
                "total_value": regex.monetary_value(
                    tr.find("span", class_="valor").get_text(strip=True)
                ),
            }
            groceries.append(grocery)

        groceries = self.normalize_groceries(groceries)

        return groceries

    def get_receipt_details(self, soup: BeautifulSoup) -> dict:
        receipt_details = {
            "items_count": int(
                soup.find("span", class_="totalNumb").get_text(strip=True)
            )
            if soup.find("span", class_="totalNumb")
            else None,
            "total_amount": regex.monetary_value(
                soup.find("span", class_="totalNumb txtMax").get_text(strip=True)
            )
            if soup.find("span", class_="totalNumb txtMax")
            else None,
            "taxes": regex.monetary_value(
                soup.find("span", class_="totalNumb txtObs").get_text(strip=True)
            )
            if soup.find("span", class_="totalNumb txtObs")
            else None,
        }
        return receipt_details

    def get_receipt(self, soup: BeautifulSoup):
        sellers_info = self.get_sellers_info(soup)
        receipt_details = self.get_receipt_details(soup)
        groceries = self.get_groceries(soup)

        return {
            "sellers_info": sellers_info,
            "receipt_details": receipt_details,
            "groceries": groceries,
        }

    def get_receipts(self, urls: List[str]):
        results = self.get_html(urls)

        groceries_receipts = []
        for result in results:
            soup = BeautifulSoup(result, "html.parser")
            html = self.rebuild_html(soup)
            groceries_receipt = self.get_receipt(html)
            groceries_receipts.append(groceries_receipt)

        return groceries_receipts


class SefazMT(Sefaz):
    pass

    @override
    def get_receipt_details(self, soup: BeautifulSoup) -> Dict:
        receipt_details = {
            "items_count": int(
                soup.find("span", class_="totalNumb").get_text(strip=True)
            ),
            "total_amount": regex.monetary_value(
                soup.find("span", class_="totalNumb txtMax").get_text(strip=True)
            ),
            "taxes": regex.monetary_value(
                soup.find("span", class_="totalNumb txtObs").get_text(strip=True)
            ),
            "discount": regex.monetary_value(
                soup.find("span", class_="totalNumb txtDesc").get_text(strip=True)
            ),
        }
        return receipt_details

    # i need to override the method called inside get_receipt to the one that is specific to the SefazMT

    @override
    def get_receipt(self, soup: BeautifulSoup) -> list:
        sellers_info = self.get_sellers_info(soup)
        receipt_details = self.get_receipt_details(soup)
        groceries = self.get_groceries(soup)

        return {
            "sellers_info": sellers_info,
            "receipt_details": receipt_details,
            "groceries": groceries,
        }


class SefazRJ:
    def __init__(self):
        pass

    # override decorator is used to indicate that a method overrides a method in a superclass, override load_html_page method
    @override
    def load_html_page(self, url: str) -> str:
        options = webdriver.ChromeOptions()
        driver = webdriver.Remote("http://localhost:4444/wd/hub", options=options)
        driver.get(url)
        try:
            # Wait until the title contains the expected partial text
            WebDriverWait(driver, 20).until(
                EC.title_contains("DOCUMENTO AUXILIAR DA NOTA FISCAL")
            )

            # Get the page source or any other required information
            html = driver.page_source

        except TimeoutException:
            print("Timeout waiting for title to contain the expected text.")
            # Optionally print the page source for debugging
            print(driver.page_source)

        finally:
            driver.quit()


class SefazSC(Sefaz):
    def __init__(self):
        pass
