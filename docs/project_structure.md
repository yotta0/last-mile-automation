## Estrutura do Projeto

O projeto é baseado no padrão **Clean Architecture**, adaptado para as necessidades específicas deste sistema. Ele é organizado em camadas para garantir flexibilidade, separação de responsabilidades e facilidade de manutenção. As principais camadas implementadas são:

1. **Serviços de Aplicação (Application)**: Esta camada implementa a lógica de aplicação, incluindo os casos de uso. Aqui estão os serviços para autenticação, gerenciamento de atendimentos, clientes, Green Angels e polos de atendimento, além das definições de rotas da API.
2. **Domínio (Domain)**: Focada nas regras de negócio, esta camada contém as entidades do domínio, exceções específicas e contratos (interfaces) que definem como as interações entre os componentes devem ocorrer.
3. **Infraestrutura (Infra)**: Lida com a integração com bancos de dados, repositórios concretos e serviços externos. Também inclui configurações de infraestrutura e scripts de inicialização.
4. **Interface**: Gerencia a comunicação com o mundo externo, incluindo controladores da API, middleware para autenticação e validações de entrada por meio de schemas.

Embora siga os princípios do padrão Clean Architecture, algumas adaptações foram feitas para atender melhor aos requisitos do projeto, como a inclusão de uma camada dedicada para middleware e validação de dados na **Interface**.

### Comparação com o Clean Architecture

No Clean Architecture, as camadas possuem responsabilidades bem definidas, e as dependências sempre apontam para o núcleo da aplicação (a camada de domínio). Este projeto mantém os princípios básicos, mas com algumas adaptações práticas:

- **Interface e Infra**: Foram organizadas para facilitar a separação entre lógica de controle (controladores e middleware) e lógica de infraestrutura (repositórios e banco de dados).
- **Foco nos Casos de Uso**: A lógica principal de negócios foi centralizada na camada de **Application**, refletindo os princípios do Clean Architecture.]
- **Injeção de Dependências**: O uso do **Dependency Injector** assegura que as dependências sejam configuradas de forma flexível e injetadas apenas onde necessário, promovendo alta testabilidade e modularidade.
- **Adaptabilidade**: A estrutura permite que partes individuais sejam modificadas ou substituídas sem impactar o restante do sistema, seguindo o objetivo principal do Clean Architecture de facilitar a manutenção e escalabilidade.
