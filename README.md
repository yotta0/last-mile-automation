# Automação de Last Mile
[![Python](https://img.shields.io/badge/Python-3.8-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.1.0-blue)](https://flask.palletsprojects.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-14.6-blue)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-Yes-blue)](https://www.docker.com/)
[![Docker Compose](https://img.shields.io/badge/Docker%20Compose-Yes-blue)](https://docs.docker.com/compose/)
[![Clean Architecture](https://img.shields.io/badge/Clean%20Architecture-Yes-blue)](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)

O Projeto é uma aplicação projetada para gerenciar e automatizar o cálculo de indicadores operacionais para operações de last mile. Ele oferece funcionalidades robustas para autenticação, gerenciamento de atendimentos, Green Angels, clientes e polos de atendimento, além de uma integração eficiente com bancos de dados e ferramentas de contêinerização.

## Desenvolvimento do Projeto

[Estrutura do Projeto e Clean Architecture](docs/project_structure.md)

[Modelagem do banco de dados](docs/database_model.md)


## Executando o Projeto

1. Clone o repositório:
```bash
git clone https://github.com/yotta0/last-mile-automation.git
cd last-mile-automation
```

### Configuração de Ambiente

#### **Configuração de Variáveis de Ambiente**
2. Copie o arquivo `.env_example` e renomeie a cópia para `.env`. em seguida Preencha as variáveis de ambiente necessárias para o ambiente de desenvolvimento.

```bash
  cp .env.example .env
```

[Informações sobre as variáveis de ambiente](docs/env_variables.md)

### Executando Localmente

Para executar o projeto localmente, siga os passos abaixo:

1. Crie um virtual env do python e ative-o:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
ou 
    ```bash
    python -m venv venv
    venv\Scripts\activate
    ```
(no Windows)
**Nota**: O uso de um ambiente virtual não é obrigatório, mas é altamente recomendado para evitar conflitos de dependências.

2.Instale as dependências necessárias:

   ```bash
   pip install -r requirements.txt
   ```

3.Defina a variavel do flask manualmente:
   ```bash
   export FLASK_APP=src/main.py
   ```
4.Rode os migrations para criar as tabelas no banco de dados:
   ```bash
   alembic upgrade head
   ```
5.rode o seeder de usuario, para criar o usuario padrão do sistema:
    ```bash
    python src/infra/database/seeder/seed_users.py
    ```
6.Inicie o servidor de desenvolvimento:

   ```bash
   flask run --host=0.0.0.0 --port=5000
   ```
Apos isso a aplicação estará disponível em `http://localhost:5000`.

### Utilizando Docker

Para executar o projeto com Docker, certifique-se de que Docker e Docker Compose estão instalados. Em seguida, use o seguinte comando:

```bash
docker compose up --build
```

ou 

```bash
docker compose up --build -d
```
para rodar em background

**Nota**: Isso pode levar algum tempo na primeira execução, pois o Docker precisa baixar as imagens necessárias e configurar o ambiente.
**Nota**: O Docker Compose irá configurar automaticamente o ambiente de desenvolvimento, incluindo a criação de um banco de dados PostgreSQL e a execução das migrações necessárias. A aplicação estará disponível em `http://localhost:5000`.

#### **Importação de planilha CSV para popular dados iniciais**

1. para importar dados do CSV para o banco de dados, é necessario colocar o arquivo CSV na pasta src/infra/database/seeder

```bash
mv ./planilha_exemplo.csv src/infra/database/seeder/planilha_exemplo.csv
```
2. Apos isso configurar a variavel de ambiente `CSV_FILE_PATH` no arquivo `.env` com o nome do arquivo CSV

**Nota**: Caso o arquivo não for encontrado, o sistema irá criar um banco de dados apenas com o seed basico de Usuario admin do sistema.

3.Apos isso rode localmente
```bash
    python src/infra/database/seeder/seed_from_csv.py
  ```
ou dentro do container do app no docker
```bash
docker compose exec app python src/infra/database/seeder/seed_from_csv.py
```
*Nota*: Talvez seja necessario rodar o build do container novamente para que o arquivo seja encontrado

**Nota**: O seeder irá popular o banco de dados com os dados do arquivo seed.csv isso irá demorar um pouco dependendo da quantidade de dados.
**Nota**: Importante rodar o seeder após a criação do banco de dados, e as migrações com o comando `alembic upgrade head`

## Testando o Projeto

**Nota**: O processo de testes ainda está em desenvolvimento e não cobre todas as funcionalidades do sistema.

1. para executar os testes, navegue até a pasta raiz do projeto, dentro do container do app ou localmente, execute o seguinte comando:
```bash
pytest
```

## Documentação da API
**Nota**: o usuario padrão para utilizar a API é:
```plaintext
email: admin@admin.com
senha: admin
```
[Fluxo de Autenticação](docs/authentication_flow.md)

###  Swagger
A documentação de todas as rotas pode ser acessada através do seguinte endereço:

```plaintext
localhost:5000/swagger
```
### Postman
se preferir utilizar o Postman
basta importar o arquivo `lastmile.postman_collection.json` que se encontra na pasta docs/postman

(Importar -> Upload Files -> Selecionar o arquivo `Last Mile automation.postman_collection`)

[Rotas Postman](docs/postman/Last Mile automation.postman_collection.json)