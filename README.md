# Cashola - Gerenciador de Finanças Pessoais

Cashola é um projeto de gerenciamento de finanças pessoais que utiliza dados de Notas Fiscais do Consumidor Eletrônicas (NFC-e) para rastrear gastos, com planos futuros para suporte a Bilhetes de Passagem Eletrônicos (BP-e). O projeto está em desenvolvimento e atualmente possui um módulo de extração de dados de NFC-e implementado com uma interface Streamlit.

## 🚀 Status do Projeto

- ✅ Módulo de extração de NFC-e
- ✅ Interface Streamlit básica
- 🔄 Suporte a BP-e (planejado)
- 🔄 API FastAPI (em desenvolvimento)
- 🔄 Backend Django (em desenvolvimento)
- 🔄 Frontend (planejado)

## 🛠️ Tecnologias Utilizadas

- Python
- Streamlit
- Selenium
- BeautifulSoup4
- Docker
- Django (em desenvolvimento)
- FastAPI (em desenvolvimento)

## 📋 Funcionalidades Atuais

- Extração de dados de NFC-e dos estados:
  - Minas Gerais (MG)
  - Mato Grosso do Sul (MS)
  - Pernambuco (PE)
  - Paraná (PR)
  - Sergipe (SE)
  - Santa Catarina (SC)
- Interface web simples para consulta individual de NFC-e
- Processamento via Selenium Grid

## ⚠️ Limitações Atuais

- Alguns estados possuem restrições de acesso:
  - Rondônia (RO): Possui CAPTCHA na página de consulta
  - Paraíba (PB): Requer interação manual para consulta
  - Piauí (PI): Necessita de redirecionamento específico
  - Maranhão (MA): Possui CAPTCHA e carregamento lento
  - Pará (PA): Não exibe informações detalhadas dos itens
  - Rio Grande do Norte (RN): Problemas de acesso ao portal
- Processamento limitado a uma NFC-e por vez no Streamlit
- Estados não suportados:
  - Amazonas (AM)
  - Amapá (AP)
  - Ceará (CE)
  - Distrito Federal (DF)
  - Rio de Janeiro (RJ)
  - Roraima (RR)
  - Tocantins (TO)
- BP-e ainda não implementado

## 🔧 Configuração do Ambiente

1. Clone o repositório:

```bash
git clone https://github.com/seu-usuario/cashola.git
cd cashola
```

2. Crie e ative um ambiente virtual:

```bash
python -m venv venv
# No Windows
.\venv\Scripts\activate
# No Linux/MacOS
source venv/bin/activate
```

3. Instale as dependências:

```bash
pip install -r requirements.txt
```

4. Inicie o Selenium Hub:

```bash
docker-compose -f docker-compose-selenium-hub.yml up -d
```

5. Execute a aplicação Streamlit:

```bash
streamlit run Scrapper.py
```

## 🗺️ Roadmap

- [ ] Implementação da API FastAPI para processamento em lote
- [ ] Desenvolvimento do backend Django
- [ ] Criação de interface web completa
- [ ] Suporte a mais estados
- [ ] Implementação inicial do suporte a BP-e
- [ ] Desenvolvimento da estrutura de dados para BP-e
- [ ] Dashboard de análise de gastos
- [ ] Categorização automática de despesas
- [ ] Tratamento de CAPTCHAs

## 👥 Contribuições

Contribuições são bem-vindas! Se você tiver interesse em colaborar com o projeto, sinta-se à vontade para:

1. Fazer um fork do projeto
2. Criar uma branch para sua feature
3. Commitar suas mudanças
4. Fazer push para a branch
5. Abrir um Pull Request

## 📝 Nota

Este projeto está em desenvolvimento ativo e foi criado com o objetivo de demonstrar habilidades em desenvolvimento backend, webscraping e integração de sistemas.
