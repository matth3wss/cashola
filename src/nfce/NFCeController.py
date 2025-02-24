import logging
import re
from typing import Any, Dict, List

from bs4 import BeautifulSoup

from nfce.NFCe import NFCe
from scrapper.Scrapper import Scrapper

from .NFCe import NFCe
from .NFCeMG import NFCeMG
from .NFCeMS import NFCeMS
from .NFCePE import NFCePE
from .NFCePR import NFCePR
from .NFCeSE import NFCeSE

scrapper = Scrapper()

# Configure logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class UrlPatterns:
    # create a pattern for SC, MS, MG and PE using pathlib to get the website withouth the protocol http(s)://www.

    # AL = re.compile(r"nfce\.sefaz\.al\.gov\.br/QRCode/consultarNFCe\.jsp\?p=\d{44}")
    MG = re.compile(
        r"portalsped\.fazenda\.mg\.gov\.br/portalnfce/sistema/qrcode\.xhtml\?p=\d{44}"
    )
    MS = re.compile(r"dfe\.ms\.gov\.br/nfce/qrcode\?p=\d{44}")
    PB_V1 = re.compile(r"receita\.pb\.gov\.br/nfce\?p=\d{44}")  # ANTIGO
    PB_V2 = re.compile(r"sefaz\.pb\.gov\.br/nfce\?p=\d{44}")  # NOVO
    PE = re.compile(r"nfce\.sefaz\.pe\.gov\.br/nfce/consulta\?p=\d{44}")
    PR = re.compile(r"fazenda\.pr\.gov\.br/nfce/qrcode\?p=\d{44}")
    # SC = re.compile(r"sat\.sef\.sc\.gov\.br/nfce/consulta\?p=\d{44}")
    SE = re.compile(r"nfce\.se\.gov\.br/portal/consultarNFCe\.jsp\?p=\d{44}")
    # MT = re.compile(r"sefaz\.mt\.gov\.br/nfce/consultanfce\?p=\d{44}")
    RS_V1 = re.compile(
        r"sefaz\.rs\.gov\.br/NFCE/NFCE-COM\.aspx\?p=\d{44}"
    )  # Antes do redirecionamento
    RS_V2 = re.compile(
        r"dfe-portal\.svrs\.rs\.gov\.br/Dfe/QrCodeNFce\?p=\d{44}"
    )  # Depois do redirecionamento

    @classmethod
    def get_nfce_state(cls, url: str) -> str:
        # if re.search(cls.AL, url):
        #     return "AL"

        if re.search(cls.MG, url):
            return "MG"

        elif re.search(cls.MS, url):
            return "MS"

        # elif re.search(cls.MT, url):
        #     return "MT"

        elif re.search(cls.PE, url):
            return "PE"

        elif re.search(cls.PR, url):
            return "PR"

        # elif re.search(cls.SC, url):
        #     return "SC"

        # elif re.search(cls.RS_V1, url) or re.search(cls.RS_V2, url):
        #     return "RS"

        elif re.search(cls.SE, url):
            return "SE"
        else:
            return None


class NFCeController:
    def get_nfce_client_by_state(self, url: str) -> NFCe:
        if re.search(UrlPatterns.PB_V1, url):
            url = re.sub(UrlPatterns.PB_V1, re.escape(UrlPatterns.PB_V2.pattern), url)
        if re.search(UrlPatterns.RS_V1, url):
            url = re.sub(UrlPatterns.RS_V1, re.escape(UrlPatterns.RS_V2.pattern), url)

        state = UrlPatterns.get_nfce_state(url)
        # if state == "AL":
        #     return NFCeAL()

        if state == "MG":
            return NFCeMG()

        elif state == "MS":
            return NFCeMS()

        # elif state == "MT":
        #     return NFCeMT()

        elif state == "PE":
            return NFCePE()

        elif state == "PR":
            return NFCePR()

        # elif state == "SC":
        #     return NFCeSC()

        # elif state == "RS":
        #     return NFCeRS()

        elif state == "SE":
            return NFCeSE()

        else:
            return NFCe()

    def get_receipts(self, urls: List[str]) -> List[Dict[str, Any]]:
        htmls = scrapper.get_html(url_list=urls)

        purchases_receipts = []
        for url, html_soup in zip(urls, htmls):
            if not html_soup:
                logger.error(f"Empty HTML for URL: {url}")
                continue
            try:
                html_soup = BeautifulSoup(html_soup, "html.parser")
                html_soup = scrapper.decompose_unnecessary_tags(html_soup=html_soup)

                nfce_instance = self.get_nfce_client_by_state(url)
                purchase_receipt = nfce_instance.build_receipt(
                    html_soup=html_soup, url=url
                )

                purchases_receipts.append(purchase_receipt)
            except Exception:
                logger.error(f"Error processing URL: {url}", exc_info=True)
                continue  # Continue processing the next URL even if an error occurs

        return purchases_receipts
