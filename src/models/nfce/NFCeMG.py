import re
from typing import Dict, List, Union, override

from bs4 import BeautifulSoup

from core.regex import RegexPatterns as regex
from nfce.NFCe import NFCe


class NFCeMG(NFCe):
    def __init__(self):
        super().__init__()

    @override
    def get_business_info(self, html_soup: BeautifulSoup) -> Dict[str, str]:
        sellers_info = super().get_business_info(html_soup=html_soup)

        business_name = html_soup.find("thead").find("h4").getText(strip=True)

        business_tax_id = regex.cnpj(
            html_soup.find("tbody")
            .find("td", string=re.compile(regex.CNPJ_PATTERN))
            .getText(strip=True)
        )

        business_address = (
            html_soup.find("tbody")
            .find("td", {"style": re.compile("font-style: italic;")})
            .getText(strip=True)
        )

        sellers_info["business_name"] = business_name
        sellers_info["business_tax_id"] = business_tax_id
        sellers_info["business_address"] = business_address

        return sellers_info

    @override
    def get_items_list(
        self, html_soup: BeautifulSoup
    ) -> List[Dict[str, Union[str, float]]]:
        items_list = [
            {
                "name": tr.find("h7").get_text(strip=True),
                "code": re.search(regex.MG_CODE_PATTERN, tr.get_text(strip=True)).group(
                    1
                ),
                "quantity": re.search(
                    regex.MG_ITEM_QUANTITY_PATTERN, tr.get_text(strip=True)
                ).group(1),
                "unit_type": re.search(
                    pattern=regex.MG_ITEM_UNITY_TYPE,
                    string=tr.find(
                        "td", string=re.compile(regex.MG_ITEM_UNITY_TYPE)
                    ).get_text(strip=True),
                ).group(1),
                "unit_value": regex.monetary_value(
                    re.search(
                        pattern=regex.MG_TOTAL_VALUE_PATTERN,
                        string=tr.find(
                            "td", string=re.compile(regex.MG_TOTAL_VALUE_PATTERN)
                        ).get_text(strip=True),
                    ).group(1)
                ),
                "total_value": regex.monetary_value(
                    re.search(
                        pattern=regex.MG_TOTAL_VALUE_PATTERN,
                        string=tr.find(
                            "td", string=re.compile(regex.MG_TOTAL_VALUE_PATTERN)
                        ).get_text(strip=True),
                    ).group(1)
                ),
            }
            for tr in html_soup.find("table", {"class": "table table-striped"})
            .find("tbody", {"id": "myTable"})
            .find_all("tr")
        ]

        items_list = self.merge_item_records(items_list)

        return items_list

    @override
    def get_receipt_details(
        self, html_soup: BeautifulSoup
    ) -> Dict[str, Union[str, int, float]]:
        receipt_details = super().get_receipt_details(html_soup=html_soup)

        items_count = int(
            (
                html_soup.find("strong", string="Qtde total de ítens")
                .find_next("strong")
                .get_text()
            )
        )

        total = float(
            html_soup.find("strong", string="Valor total R$")
            .find_next("strong")
            .get_text()
        )

        total_due = float(
            html_soup.find("strong", string="Valor pago R$")
            .find_next("strong")
            .get_text()
        )

        discounts = round(float(total - total_due), 2) if total and total_due else None

        taxes = "Na nota fiscal usada como referência não tinha impostos, não era possível saber como o imposto está descrito no site."

        payment_method = (
            html_soup.find("strong", string="Forma de Pagamento")
            .find_next("strong")
            .get_text()
        )

        additional_info = next(
            iter([
                td.text
                for td in html_soup.find("th", string="Descrição")
                .find_next("tbody")
                .find_all("td")
                if html_soup.find("th", string="Descrição").find_next("td").text
            ]),
            None,
        )

        receipt_details["items_count"] = items_count
        receipt_details["total"] = total
        receipt_details["total_due"] = total_due
        receipt_details["discounts"] = discounts
        receipt_details["taxes"] = taxes
        receipt_details["payment_method"] = payment_method
        receipt_details["additional_info"] = additional_info

        return receipt_details
