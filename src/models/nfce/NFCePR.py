from typing import Dict, List, Union, override

from bs4 import BeautifulSoup

from src.core.regex import RegexPatterns as regex
from src.models.finance_data_models import PurchasedItem
from src.models.nfce.NFCe import NFCe


class NFCePR(NFCe):
    def __init__(self):
        super().__init__()

    @override
    def get_purchased_items(
        self,
        html_soup: BeautifulSoup,
        has_id: bool = True,
        normalize: bool = False,
    ) -> List[Dict[str, Union[str, float]]]:
        purchased_items = [
            {
                "name": tr.find("span", class_="txtTit2").get_text(strip=True)
                if tr.find("span", class_="txtTit2")
                else None,
                "code": regex.code(tr.find("span", class_="RCod").get_text(strip=True)),
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

        # this is gonna break the code
        purchased_items = [PurchasedItem(**item) for item in purchased_items]

        return purchased_items


pr_client = NFCePR()
