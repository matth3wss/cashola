from typing import Dict, List, Union, override

from bs4 import BeautifulSoup

from core.regex import RegexPatterns as regex
from nfce.NFCe import NFCe


class NFCePE(NFCe):
    def __init__(self):
        super().__init__()

    @override
    def get_items_list(
        self,
        soup: BeautifulSoup,
        has_id: bool = False,
    ) -> List[Dict[str, Union[str, int, float]]]:
        items_list = super().get_items_list(html_soup=soup, has_id=has_id)

        for item, tr in zip(items_list, soup.find_all("tr", id=has_id)):
            item["total_price"] = regex.total_value(
                tr.find("td", {"class": "txtTit noWrap"}).text
            )

        items_list = self.merge_item_records(items_list)

        return items_list
