from typing import Any, Dict, List, Optional, Union

from bs4 import BeautifulSoup

from src.core.regex import RegexPatterns as regex


class NFCe:
    def __init__(self):
        pass

    def get_business_info(self, html_soup: BeautifulSoup) -> Dict[str, Optional[str]]:
        business_info = {
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

        return business_info

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
            key = (item["item_name"], item["code"])

            if key in combined_items:
                combined_items[key]["quantity"] += item["quantity"]
                combined_items[key]["total_price"] += item["total_price"]
            else:
                combined_items[key] = item.copy()

        return list(combined_items.values())

    def get_items_list(
        self,
        html_soup: BeautifulSoup,
        has_id: bool = True,
        normalize: bool = True,
    ) -> List[
        Union[Dict[str, Optional[Union[str, float]]], Any, Dict[str, Union[str, float]]]
    ]:
        items_list = [
            {
                "name": tr.find("span", class_="txtTit").get_text(strip=True)
                if tr.find("span", class_="txtTit")
                else None,
                "code": tr.find("span", class_="RCod").get_text(strip=True),
                # "code": regex.code(tr.find("span", class_="RCod").get_text(strip=True)),
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
            items_list = self.merge_item_records(items_list)

        return items_list

    def get_receipt_details(
        self,
        html_soup: BeautifulSoup,
        nfce_bpe_link: str,
    ) -> Dict[str, Optional[Union[str, int, float, List[str]]]]:
        purchased_date = regex.purchase_timestamp(html_soup.text)

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

        additional_info = "\n".join(
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

        receipt_details = {
            "nfce_bpe_link": nfce_bpe_link,
            "purchased_date": purchased_date,
            "items_count": items_count,
            "total": total,
            "total_due": total_due,
            "discounts": discounts,
            "taxes": taxes,
            "payment_method": payment_method,
            "additional_info": additional_info,
        }

        return receipt_details

    def build_receipt(
        self, html_soup: BeautifulSoup, nfce_bpe_link: str
    ) -> Dict[str, Any]:
        business_info = self.get_business_info(html_soup)
        receipt_details = self.get_receipt_details(html_soup, nfce_bpe_link)
        items_list = self.get_items_list(html_soup)

        return {
            "business_info": business_info,
            "receipt_details": receipt_details,
            "items": items_list,
        }
