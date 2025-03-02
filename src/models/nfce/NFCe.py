from typing import Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup

from src.core.regex import RegexPatterns as regex
from src.models.finance_data_models import Business, Expense, PurchasedItem


class NFCe:
    def __init__(self):
        pass

    def get_business_info(self, html_soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        business = {
            "business_name": html_soup.find("div", class_="txtTopo").get_text(
                strip=True
            )
            if html_soup.find("div", class_="txtTopo")
            else None,
            "business_tax_id": regex._convert_brazilian_number(
                html_soup.find("div", class_="text").get_text(strip=True)
            )
            if html_soup.find("div", class_="text")
            else None,
            "business_address": regex.business_address(
                html_soup.find_all("div", class_="text")[1].get_text(strip=True)
            )
            if html_soup.find_all("div", class_="text")
            else None,
        }

        business = Business(
            **business,
            street_address=business["business_address"],
        )

        return business

    def merge_item_records(
        self,
        items_list: List[
            Union[
                Dict[str, Optional[Union[str, float]]],
                Any,
                Dict[str, Union[str, float]],
            ]
        ],
    ) -> List[
        Union[Dict[str, Optional[Union[str, float]]], Any, Dict[str, Union[str, float]]]
    ]:
        # Dictionary to store combined items
        combined_items = {}

        for item in items_list:
            key = (item["name"], item["code"])

            if key in combined_items:
                combined_items[key]["quantity"] += item["quantity"]
                combined_items[key]["total_price"] += item["total_price"]
            else:
                combined_items[key] = item.copy()

        return list(combined_items.values())

    def get_purchased_items(
        self,
        html_soup: BeautifulSoup,
        has_id: bool = True,
        normalize: bool = True,
    ):
        purchased_items = [
            {
                "name": tr.find("span", class_="txtTit").get_text(strip=True)
                if tr.find("span", class_="txtTit")
                else None,
                "code": tr.find("span", class_="RCod").get_text(strip=True),
                # "code": regex.code(tr.find("span", class_="RCod").get_text(strip=True)), needs to be implemented, some codes arent numbers so it returns None
                "quantity": regex.quantity(
                    tr.find("span", class_="Rqtd").get_text(strip=True)
                ),
                "unit_type": regex.unit_type(
                    tr.find("span", class_="RUN").get_text(strip=True)
                ),
                "unit_price": regex.unit_price(
                    tr.find("span", class_="RvlUnit").get_text(strip=True)
                ),
                "total_price": regex.monetary_value(
                    tr.find("span", class_="valor").get_text(strip=True)
                )
                if tr.find("span", class_="valor")
                else None,
            }
            for tr in html_soup.find_all("tr", id=has_id)
        ]

        if normalize:
            purchased_items = self.merge_item_records(purchased_items)

        purchased_items = [PurchasedItem(**item) for item in purchased_items]

        return purchased_items

    def get_nfce_details(
        self,
        html_soup: BeautifulSoup,
        nfce_bpe_link: str,
    ) -> Dict[str, Optional[Union[str, int, float, List[str]]]]:
        purchase_timestamp = regex.purchase_timestamp(html_soup.text)

        items_count = (
            int(
                html_soup.find("label", string="Qtd. total de itens:")
                .find_next("span")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Qtd. total de itens:")
            else None
        )

        total_due = (
            regex.monetary_value(
                html_soup.find("label", string="Valor a pagar R$:")
                .find_next("span")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Valor a pagar R$:")
            else None
        )

        total = (
            regex.monetary_value(
                html_soup.find("label", string="Valor total R$:")
                .find_next("span")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Valor total R$:")
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

        payment_method = (
            (
                html_soup.find("label", string="Forma de pagamento:")
                .find_next("label")
                .get_text(strip=True)
            )
            if html_soup.find("label", string="Forma de pagamento:")
            else None
        )

        additional_info_list = (
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

        additional_info = (
            "\n".join(additional_info_list) if additional_info_list else None
        )

        receipt_details = {
            "total": total,
            "total_due": total_due,
            "discounts": discounts,
            "taxes": taxes,
            "payment_method": payment_method,
            "additional_info": additional_info,
            "items_count": items_count,
            "nfce_bpe_link": nfce_bpe_link,
            "purchase_timestamp": purchase_timestamp,
        }

        expense = Expense(**receipt_details)

        return expense

    def build_nfce(
        self, html_soup: BeautifulSoup, nfce_bpe_link: str
    ) -> Dict[str, Any]:
        business_info = self.get_business_info(html_soup)
        nfce_details = self.get_nfce_details(html_soup, nfce_bpe_link)
        purchased_items = self.get_purchased_items(html_soup)

        return {
            "business_info": business_info,
            "nfce_details": nfce_details,
            "purchased_items": purchased_items,
        }
