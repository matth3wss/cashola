import sys
import time

import streamlit as st

sys.path.append("./src/")

from src.controllers.NFCeController import NFCeController

st.header("Scrapper")

# Dictionary mapping states to their URLs
state_urls = {
    "AC": [
        "http://www.sefaznet.ac.gov.br/nfce/qrcode?p=12230333775462000130650010001995411061116333|2|1|1|D0C419A243BBF01C1DC06DCE50441A59DDE0FFD8"
    ],
    "AL": [
        "http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?p=27230206057223052058650110000134951110130423|2|1|1|DBBC3473E2D32F975F6561E2E0E6CDFDE71C67C9",
        "http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?p=27230222460487000128650010000556771783455510|2|1|1|2cfc9aa90d94e0384c6c5887c6df267a0bf28242",
        "http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?p=27230222460487000128650010000558661755774345|2|1|1|75a48e9b7016aec9454079b23d1ffadaad3e2649",
        "http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?p=27230228619052000160650010001143031944335660|2|1|1|B97EC1ECBB92907F3800A292A6AA504FC25141B4",
        "http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?p=27230239800071000104650010000548731786680678|2|1|1|DEBD1731EAD77D7B20F8721EE983675624F661C8",
        "http://nfce.sefaz.al.gov.br/QRCode/consultarNFCe.jsp?p=27230248222076000198650010000114711343974431|2|1|1|E55BFFE2F7BC64933C0558CA5EAC2ADC83196E05",
    ],
    "BA": [
        "http://nfe.sefaz.ba.gov.br/servicos/nfce/modulos/geral/NFCEC_consulta_chave_acesso.aspx?p=29210208739223000187650030000232451000396034|2|1|1|E69ABE87D06714A3B3267DEF6DE5F7FEA817BE1E"
    ],
    "ES": [
        "http://app.sefaz.es.gov.br/ConsultaNFCe/qrcode.aspx?p=32210108589031000131650010002463751002471932|2|1|1|AC536DE109D9284D743D7254FD799922E69837E0",
        "http://app.sefaz.es.gov.br/ConsultaNFCe/QRCode.aspx?chNFe=32170133014556014901652030000122301986636180&nVersao=100&tpAmb=1&dhEmi=323031372d30312d32305431353a34353a32362d30323a3030&vNF=65.34&vICMS=11.11&digVal=45695672632b6c79754a746c514d636f394e6d74526e304d7943513d&cIdToken=000001&cHashQRCode=eecfc7456aa218718d6dde149d761f8014388e60",
    ],
    "MG": [
        "https://portalsped.fazenda.mg.gov.br/portalnfce/sistema/qrcode.xhtml?p=31220703986136000100650010003145091103798610|2|1|1|C55282631A8A3A9B81D0795C09383247FFAEAC5F"
    ],
    "MS": [
        "http://www.dfe.ms.gov.br/nfce/qrcode?p=50200207751593000509651080001463271064101307|2|1|1|04385CA49D41356E3F40D809FA45174AE46B0692",
        "https://www.dfe.ms.gov.br/nfce/qrcode?p=50210407638491000492651160000292711000519350|2|1|1|AF5C8648A7052F374DB3505B10D8B16FD456B64B",
    ],
    "MT": [
        "https://www.sefaz.mt.gov.br/nfce/consultanfce?p=51240810693312000505650020001655501200071901|2|1|1|E6BC9D2608B0D3602CA9C17692DB6406518D072F"
    ],
    "PE": [
        "http://nfce.sefaz.pe.gov.br/nfce/consulta?p=26181212263187000103650020000343871054717914|2|1|1|956A093A06F18EB455DB7075DF72583E0217D324"
    ],
    "PR": [
        "http://www.fazenda.pr.gov.br/nfce/qrcode?p=41210279052460000113651060006921791106231222|2|1|1|51428D909ED8D4F247E4FF753353FDC78CDB292C",
        "https://www.fazenda.pr.gov.br/nfce/qrcode?p=41230989237911021148650310000174051623905300|2|1|2|3df2ed084a625a36846a25e3da8aaa3607187903",
    ],
    "RS": [
        "https://dfe-portal.svrs.rs.gov.br/Dfe/QrCodeNFce?p=43210204583300000100650010016037771292151264|2|1|1|92E231ECA5BD4CE2D345FE70CF811C3C1D6AB717",
        "https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx?p=43210208407768000609651010004631581904538012|2|1|1|DD7F77804502265D77615FCC294A25AC7865B05A",
        "https://www.sefaz.rs.gov.br/NFCE/NFCE-COM.aspx?p=43231212340107000168650010001942331011942334|2|1|1|35AC6E329FC6D30C5B920835DF0C3D78B0F66468",
    ],
    "SP": [
        "https://www.nfce.fazenda.sp.gov.br/NFCeConsultaPublica/Paginas/ConsultaQRCode.aspx?p=35241013574594020030650010014277331679230370|2|1|1|809D91F3DED9AE2E85765DB7F421BABB505B9530"
    ],
}

# Add state selection dropdown
selected_state = st.selectbox(
    "Selecione o estado", options=list(state_urls.keys()), key="state_selector"
)

# Add URL selector for the selected state
selected_url = st.selectbox(
    "Selecione a URL", options=state_urls[selected_state], key="url_selector"
)

# Text area for URL display/edit
url = st.text_area(
    label="URL da NFCE",
    key="url_nfce",
    value=selected_url,
    help="Você pode alterar a URL para testar com outras notas fiscais.",
)

start_time = 0
end_time = 0
receipts = None

if st.button("Extrair dados"):
    start_time = time.time()
    receipts = NFCeController().get_receipts(urls=url)
    end_time = time.time()
    st.write(f"Tempo de execução: {end_time - start_time} segundos")

    if receipts and len(receipts) > 0:
        st.write("Informações vendedor")
        st.dataframe(receipts[0]["sellers_info"], use_container_width=True)

        st.write("Detalhes da nota")
        st.dataframe(receipts[0]["receipt_details"], use_container_width=True)

        st.write("Produtos")
        st.dataframe(receipts[0]["items"], use_container_width=True)
    else:
        st.warning("Nenhum dado foi encontrado para exibir.")
