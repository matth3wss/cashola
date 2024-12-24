from typing import override

from bs4 import BeautifulSoup

from nfce.NFCe import NFCe


class NFCeMS(NFCe):
    def __init__(self):
        super().__init__()

    @override
    def get_receipt_details(self, soup: BeautifulSoup) -> dict:
        receipt_details = super().get_receipt_details(soup)

        additional_info = (
            next(
                (
                    t.find(
                        "div", {"class": "ui-collapsible-content ui-body-inherit"}
                    ).text.strip()
                    for t in soup.find("div", {"id": "infos"}).find_all(
                        "div", {"data-role": "collapsible"}
                    )
                    if t.find("h4")
                    and "Informações de interesse do contribuinte"
                    in " ".join(t.find("h4").text.split())
                ),
                None,
            )
            if soup.find("div", {"id": "infos"})
            else None
        )

        receipt_details["additional_info"] = additional_info

        return receipt_details
