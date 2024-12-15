# Fluxo de autenticação

O fluxo de autenticação do projeto usa um bearer token JWT (JSON Web Token) para autenticar usuários e proteger rotas sensíveis. O token é gerado após a autenticação do usuário e é enviado no cabeçalho de todas as requisições subsequentes.

## Autenticação

Para fazer login, basta apenas enviar uma requisição `POST` para a rota `/api/v1/auth` com o seguinte corpo:

```json
{
  "email": "admin@admin.com",
  "password": "admin"
}

```

O servidor irá responder com um token JWT, que deve ser armazenado pelo cliente e enviado no cabeçalho `Authorization` de todas as requisições subsequentes.

```json
{
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzQwNzQwNzEsImlhdCI6MTYzNDA3MzY3MSwic3ViIjoxfQ.7",
  "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE2MzQwNzQwNzEsImlhdCI6MTYzNDA3MzY3MSwic3ViIjoxfQ.7"
}
```
**Nota**: O token de acesso por padrão dura 8 minutos. após o token de acesso expirar, é necessario fazer uma requisição para a rota `/api/v1/auth/refresh` com o token de refresh para obter um novo token de acesso.
**Nota**: O token de refresh é valido por 8 horas, após isso é necessario fazer login novamente.

#### Exemplo de requisição com token de acesso:

```http
GET /api/v1/users HTTP/1.1
Host: localhost
Header: Authorization Bearer <access_token>
```
