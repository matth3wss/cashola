from typing import Dict, List, Union

from bs4 import BeautifulSoup

from core.regex import RegexPatterns as regex


class NFCe:
    def __init__(self):
        pass

    def get_sellers_info(self, html_soup: BeautifulSoup) -> List[Dict[str, str]]:
        sellers_info = {
            "sellers_name": html_soup.find("div", class_="txtTopo").get_text(strip=True)
            if html_soup.find("div", class_="txtTopo")
            else None,
            "sellers_cnpj": regex._convert_brazilian_number(
                html_soup.find("div", class_="text").get_text(strip=True)
            )
            if html_soup.find("div", class_="text")
            else None,
            "sellers_address": regex.sellers_address(
                html_soup.find_all("div", class_="text")[1].get_text(strip=True)
            )
            if html_soup.find_all("div", class_="text")
            else None,
        }

        return sellers_info

    def merge_item_records(self, items_list):
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
        has_id: bool = False,
        normalize: bool = True,
    ) -> List[Dict[str, Union[str, int, float]]]:
        items_list = [
            {
                "item_name": tr.find("span", class_="txtTit").get_text(strip=True)
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

    def get_receipt_details(self, html_soup: BeautifulSoup):
        timestamp = regex.purchase_timestamp(html_soup.text)

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

        discounts = float(total - total_due) if total and total_due else None

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

        receipt_details = {
            "timestamp": timestamp,
            "items_count": items_count,
            "total": total,
            "total_due": total_due,
            "discounts": discounts,
            "taxes": taxes,
            "payment_method": payment_method,
            "additional_info": additional_info,
        }

        return receipt_details

    def build_receipt(self, html_soup: BeautifulSoup, url):
        sellers_info = self.get_sellers_info(html_soup)
        receipt_details = self.get_receipt_details(html_soup)
        items_list = self.get_items_list(html_soup)

        return {
            "url": url,
            "sellers_info": sellers_info,
            "receipt_details": receipt_details,
            "items": items_list,
        }
