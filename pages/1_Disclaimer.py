import streamlit as st

st.title("Informações Importantes")

st.header("⚠️ Estados com Limitações de Acesso")

st.markdown("""
    Alguns estados possuem restrições que impedem o acesso automático aos dados das NFCe's:

    - **Rondônia (RO)**: Página possui CAPTCHA
    - **Paraíba (PB)**: 
        - Página possui CAPTCHA
        - Requer interação manual (clique em botão "Consultar")
        - Necessário navegar entre abas para coletar informações
    - **Piauí (PI)**: Requer alteração do link de acesso
    - **Maranhão (MA)**:
        - Página possui CAPTCHA
        - Requer navegação manual entre abas
        - Tempo de carregamento lento
    - **Pará (PA)**: Não exibe informações detalhadas dos itens
    - **Rio Grande do Norte (RN)**: Sistema frequentemente fora do ar
    - **Goiás (GO)**: Requer alteração do link de acesso
""")

st.header("❌ Estados sem Implementação")
st.markdown("""
    Os seguintes estados não possuem implementação por falta de exemplos de links/QR codes para teste:
    
    - Amazonas (AM)
    - Amapá (AP)
    - Ceará (CE)
    - Distrito Federal (DF)
    - Rio de Janeiro (RJ)
    - Roraima (RR)
    - Tocantins (TO)
""")
