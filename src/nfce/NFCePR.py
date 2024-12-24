from typing import override

from bs4 import BeautifulSoup

from nfce.NFCe import NFCe


class NFCePR(NFCe):
    def __init__(self):
        super().__init__()

    @override
    def get_items_list(
        self,
        html_soup: BeautifulSoup,
        has_id: bool = True,
        normalize: bool = False,
    ):
        items_list = super().get_items_list(html_soup=html_soup, has_id=has_id, normalize=normalize)

        for item, tr in zip(items_list, html_soup.find_all("tr", id=has_id)):
            item["item_name"] = tr.find("span", {"class": "txtTit2"}).get_text(strip=True)

        items_list = self.merge_item_records(items_list)

        return items_list


pr_client = NFCePR()
