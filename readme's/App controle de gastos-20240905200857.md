# App controle de gastos

## Dashboards

*   Interfaces web com dashboard que mostra os ganhos e gastos

## Entradas e Saídas

*   Adicionar valores de entrada
*   Renda é depositada no N dia útil do mês então calcular de acordo com isso e não com a data (deposita sempre depois do fim se semana)
*   Se é depositada no dia 29 mas é em um sábado então é depositado na sexta (nem sempre)
*   Gimmick, adicionar gastos a partir das notificações
*   Conta vence no dia tal, mas é feriado (nacional) ou fim de semana, o vencimento muda automaticamente pro próximo dia útil

## Conexões

*   OFX, CSV, XML, PDF: importar dados que estiverem nesse formato
*   Recuperar boletos no cpf do cliente a partir do dda eletronico (febrabam
*   Precisa conectar o cartão de crédito
*   Open finance para poder conectar com todos os bancos
    *   Integração nubank e c6
*   Importar gastos em planilhas feitas pelo usuário, criar programa que vc vai dizer quais colunas significam quais dados para poder servir de input para
*   Importar gasto a partir do qr code de uma nota fiscal, mas tem que fazer Cross reference para não adicionar o valor duas vezes caso a integração com o banco já tenha funcionado, útil talvez se vc gastou no dinheiro, mas nem sempre a nota tem qr code. Enfim até onde sei entrar na NF-E precisa passar pelo CAPTCHA. Talvez inteligência artificial pra burlar ele?
*   Score do Serasa

## Rastreamento de fluxo financeiro contínuo

*   Função que diz que dinheiro foi transferido entre contas de mesma titularidade

## Investimentos

*   Integração com a b3

## Serviços trabalhistas

*   Not urgent: Calculadora de FGTS, e recisão, multa, seguro desemprego.