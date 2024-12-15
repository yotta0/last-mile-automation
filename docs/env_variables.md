# Explicação das Variáveis de Ambiente

**Nota:** Os valores padrão recomendados são fornecidos para facilitar a configuração do ambiente local. Certifique-se de ajustar as variáveis conforme suas necessidades.

### POSTGRES_USER
**Função:** Define o nome do usuário utilizado para autenticação no banco de dados PostgreSQL.

- Valor padrão recomendado: `admin`
- Ambiente local: `admin`
- Ambiente Docker: `admin`

---

### POSTGRES_PASSWORD
**Função:** Define a senha do usuário configurado para o banco de dados PostgreSQL.

- Valor padrão recomendado: `admin`
- Ambiente local: `admin`
- Ambiente Docker: `admin`
---

### POSTGRES_HOST
**Função:** Define o host (endereço) do banco de dados PostgreSQL.

- Ambiente local: `localhost`
- Ambiente Docker: `operations-db`

---

### POSTGRES_DB
**Função:** Define o nome do banco de dados PostgreSQL utilizado pela aplicação.

- Valor padrão recomendado: `operations`
- Ambiente local: `operations`
- Ambiente Docker: `operations`

---

### POSTGRES_PORT
**Função:** Define a porta de conexão com o banco de dados PostgreSQL.

- Valor padrão recomendado: `5432`
- Ambiente local: `5432`
- Ambiente Docker: `5432`

---

### SECRET_KEY
**Função:** Define a chave secreta utilizada para gerar e validar tokens de autenticação JWT.

- Valor padrão recomendado: `secret-key-123`

**Nota:** Use uma chave longa e segura para produção.

---

### ALGORITHM
**Função:** Define o algoritmo utilizado para assinar os tokens JWT.

- Valor padrão recomendado: `HS256`

---

### SQLALCHEMY_DATABASE_URI
**Função:** Define a URI de conexão ao banco de dados utilizada pelo SQLAlchemy.

- Ambiente local:
  ```plaintext
  postgresql://admin:admin@localhost:5432/operations
  ```
- Ambiente Docker:
  ```plaintext
  postgresql://admin:admin@operations-db:5432/operations
  ```

**Nota:** Certifique-se de ajustar a URI conforme suas configurações de banco de dados.

---

### CSV_FILE_NAME
**Função:** Define o nome do arquivo CSV utilizado para popular o banco de dados.

**Nota:** Certifique-se de que o arquivo esteja localizado no diretório `src/infra/database/seeder`.
**Nota:** caso o seed não seja encontrado o banco de dados será populado com dados padrões.
