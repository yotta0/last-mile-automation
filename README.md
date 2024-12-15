# Automação de Last Mile

Este projeto é uma API desenvolvida com Flask, que inclui autenticação, gerenciamento de atendimentos e integração com um banco de dados PostgreSQL. O objetivo principal é automatizar o cálculo dos indicadores operacionais para a operação de Last Mile, focando especificamente nos seguintes KPIs:

- **Produtividade por Green Angel**
- **SLA de cada base logística**
- **SLA de cada Green Angel**

---

## Requisitos

- Python 3.8+
- PostgreSQL
- pip
- (Opcional) Docker e Docker Compose

---

## Instalação Local

### Passo a passo

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/yotta0/last-mile-automation.git
    cd last-mile-automation
    ```

2. **Crie e ative um ambiente virtual**:

    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows use `venv\Scripts\activate`
    ```

3. **Instale as dependências**:

    ```bash
    pip install -r requirements.txt
    ```

4. **Configure as variáveis de ambiente**:

    - Copie o arquivo de exemplo:

        ```bash
        cp .env.example .env
        ```

    - Edite o arquivo `.env` e preencha os campos necessários, como as credenciais do banco de dados e a URL da aplicação.

5. **Configure o banco de dados**:

    - Crie as tabelas executando as migrações:

        ```bash
        flask db upgrade
        ```

6. **Opcional: Seed de usuários**:

    - Crie o usuário administrador com o comando:

        ```bash
        flask seed_users
        ```

7. **Inicie a aplicação**:

    ```bash
    flask run
    ```

    A API estará acessível em `http://127.0.0.1:5000` por padrão.

---

## Instalação com Docker

### Passo a passo

1. **Clone o repositório**:

    ```bash
    git clone https://github.com/yotta0/last-mile-automation.git
    cd last-mile-automation
    ```

2. **Configure as variáveis de ambiente**:

    - Copie o arquivo de exemplo:

        ```bash
        cp .env.example .env
        ```

    - Edite o arquivo `.env` e preencha os campos necessários.

3. **Inicie os containers**:

    - Construa e inicie os containers:

        ```bash
        docker-compose up --build
        ```

4. **Execute as migrações**:

    - Configure o banco de dados executando as migrações dentro do container:

        ```bash
        docker-compose exec app flask db upgrade
        ```

5. **Opcional: Seed de usuários**:

    - Crie o usuário administrador:

        ```bash
        docker-compose exec app flask seed_users
        ```

6. **Acesse a aplicação**:

    - A API estará disponível em `http://localhost:<PORTA>` (substitua `<PORTA>` pela porta definida no arquivo `docker-compose.yml` ou no `.env`).

---

## Sugestão de Melhorias Futura

- Adicionar testes automatizados para validação das funcionalidades principais.
- Criar uma pipeline CI/CD para automatizar testes e implantações.
- Incluir documentação interativa da API com Swagger ou Redoc.

---

Com essas instruções, você pode configurar e executar o projeto de forma local ou com Docker, dependendo das suas preferências e necessidades.

