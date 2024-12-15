#  Modelagem do Banco de Dados

## Arquivos CSV Recebidos
Os arquivos CSV recebidos serviram como base para a modelagem do banco de dados que foi feita pensando em uma forma de abstrair o problem, mas ao mesmo tempo facilite a expansão, facilidade de manutenção e escalabilidade,
mesmo com a falta de algumas informações no arquivo (Como dados do cliente por exemplo).
---

## Modelagem no Banco de Dados
A modelagem foi definida com base nos princípios de normalização, garantindo a integridade dos dados e facilitando consultas eficientes. Abaixo, descrevo as entidades do banco de dados:

### 1. **Tabela: `attendances`**
- **Descrição:** Armazena informações sobre atendimentos.
- **Campos:**
  - `id`: Chave primária.
  - `client_id`: Chave estrangeira referenciando `clients(id)`.
  - `green_angel_id`: Chave estrangeira referenciando `green_angels(id)`.
  - `hub_id`: Chave estrangeira referenciando `hubs(id)`.
  - `attendance_date`: Data do atendimento.
  - `limit_date`: Data limite para resolução do atendimento.
  - `is_active`: Status do atendimento.

### 2. **Tabela: `clients`**
- **Descrição:** Armazena informações sobre os clientes.
- **Campos:**
  - `id`: Chave primária.
  - `is_active`: Status do cliente.

### 3. **Tabela: `green_angels`**
- **Descrição:** Armazena informações sobre os colaboradores.
- **Campos:**
  - `id`: Chave primária.
  - `name`: Nome do colaborador.
  - `is_active`: Status do colaborador.

### 4. **Tabela: `hubs`**
- **Descrição:** Armazena informações sobre os Polos.
- **Campos:**
  - `id`: Chave primária.
  - `name`: Nome do Polo.
  - `is_active`: Status do hub.

---

## Decisões de Modelagem
1. **Chaves Estrangeiras:**
   - Relacionei as tabelas `attendances` com `clients`, `green_angels` e `hubs` através de chaves estrangeiras para garantir a integridade referencial.

2. **Status (`is_active`):**
   - Todos os registros possuem um campo `is_active` para indicar se o recurso está ativo ou inativo, facilitando filtros e garantindo que dados históricos não sejam apagados.

3. **Datas (`attendance_date` e `limit_date`):**
   - As datas são armazenadas no formato `YYYY-MM-DD HH:MM:SS` para padronização e compatibilidade com sistemas de análise de dados.

4. **Normalização:**
   - A modelagem evita redundâncias e promove escalabilidade ao separar as entidades relacionadas (ex.: clientes, colaboradores, hubs).

---

   
