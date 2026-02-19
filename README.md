# Automação de Fluxos Financeiros: Gestão e Estorno de PIX

Este projeto foi desenvolvido para solucionar um gargalo operacional crítico: o processo manual de estorno de transações PIX. Diante de uma alta demanda de solicitações, a execução manual via interface ou consultas isoladas tornou-se inviável, motivando a criação desta automação integrada diretamente às APIs bancárias e ao banco de dados PostgreSQL.

## O Problema (Cenário Real)
O processo de estorno era extremamente demorado e suscetível a erros, pois exigia:
1. Localização manual da transação no banco de dados.
2. Identificação do `enddId` ou `IDPX` correspondente.
3. Acesso à API da instituição para solicitar o estorno.
4. Validação posterior se o estorno foi concluído com sucesso.

## A Solução
Desenvolvi uma suíte de scripts em Python que automatiza o ciclo de vida do estorno:
- **Autenticação Segura (`Pix.py`):** Implementação de fluxo OAuth2 para obtenção de tokens de acesso às APIs financeiras.
- **Extração e Inteligência de Dados (`Txid.py`):** Lógica para fatiamento de identificadores (TXID) e consulta automatizada em banco de dados para validar se um cupom/pedido foi finalizado antes de decidir pelo estorno.
- **Execução de Estorno (`Estorno.py`):** Interface para realizar chamadas `PUT` e `GET` na API, processando a devolução de valores e monitorando o status final do evento.
