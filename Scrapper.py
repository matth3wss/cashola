import time

import streamlit as st

from nfce.NFCeController import NFCeController

st.header("Scrapper")

url = st.text_area(
    label="URL da NFCE",
    key="url_nfce",
    value="https://sat.sef.sc.gov.br/nfce/consulta?p=42241181332439000113650020002315731951045146|2|1|1|F7BF241ACD370C3F581C26740B1C08A59BB10357",
)

start_time = 0
end_time = 0
receipts = None

if st.button("Extrair dados"):
    start_time = time.time()
    receipts = NFCeController().get_receipts(urls=url)
    end_time = time.time()
    st.write(f"Tempo de execução: {end_time - start_time} segundos")


st.write("Informações vendedor")
st.dataframe(receipts[0]["sellers_info"], use_container_width=True)

st.write("Detalhes da nota")
st.dataframe(receipts[0]["receipt_details"], use_container_width=True)

st.write("Produtos")
st.dataframe(receipts[0]["items"], use_container_width=True)
