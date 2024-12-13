# Automação de Last Mile

Este projeto é uma API desenvolvida com Flask, que inclui autenticação, gerenciamento de atendimentos e integração com um banco de dados PostgreSQL. O objetivo principal é automatizar o cálculo dos indicadores operacionais para a operação de Last Mile, focando especificamente nos seguintes KPIs:

- Produtividade por Green Angel
- SLA de cada base logística
- SLA de cada Green Angel

## Requisitos

- Python 3.8+
- PostgreSQL
- pip

## Instalação

1. Clone o repositório:

    ```bash
    git clone https://github.com/yotta0/last-mile-automation.git
    cd last-mile-automation
    ```

2. Crie e ative um ambiente virtual:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. Instale as dependências:

    ```bash
    pip install -r requirements.txt
    ```

4. Configure as variáveis de ambiente no arquivo `.env`: 

    ```bash
    cp .env.example .env
    ```