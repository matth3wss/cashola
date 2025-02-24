from typing import override

from bs4 import BeautifulSoup

from core.regex import RegexPatterns as regex
from nfce.NFCe import NFCe


class NFCeSE(NFCe):
    def __init__(self):
        super().__init__()

    @override
    def get_receipt_details(self, html_soup: BeautifulSoup):
        receipt_details = super().get_receipt_details(html_soup=html_soup)

        items_count = (
            int(
                html_soup.find("label", string="Qtd. total de Itens:")
                .find_next("span")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Qtd. total de Itens:")
            else None
        )

        total_due = (
            regex.monetary_value(
                html_soup.find("label", string="Valor a Pagar R$:")
                .find_next("span")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Valor a pagar R$:")
            else None
        )

        total = (
            regex.monetary_value(
                html_soup.find("label", string="Valor Total R$:")
                .find_next("span")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Valor Total R$:")
            else total_due
        )

        discounts = round(float(total - total_due), 2) if total and total_due else None

        taxes = (
            regex.monetary_value(
                html_soup.find("span", class_="totalNumb txtObs").get_text(strip=True)
            )
            if html_soup.find("span", class_="totalNumb txtObs")
            else None
        )

        additional_info = (
            next(
                (
                    [li.text.strip() for li in t.find("ul").find_all("li")]
                    for t in html_soup.find("div", {"id": "infos"}).find_all(
                        "div", {"data-role": "collapsible"}
                    )
                    if t.find("h4")
                    and "Informações de interesse do contribuinte"
                    in " ".join(t.find("h4").text.split())
                    and t.find("ul") is not None
                ),
                None,
            )
            if html_soup.find("div", {"id": "infos"})
            else None
        )

        receipt_details["items_count"] = items_count
        receipt_details["total"] = total
        receipt_details["total_due"] = total_due
        receipt_details["discounts"] = discounts
        receipt_details["taxes"] = taxes
        receipt_details["additional_info"] = additional_info

        return receipt_details
