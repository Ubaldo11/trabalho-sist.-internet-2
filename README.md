# Servidores Executivo Federal - Aplicação Full Stack

Aplicação full stack que consulta uma base de dados de servidores ativos e aposentados do Poder Executivo Federal (dados.gov.br), rodando com Docker Compose.

## Stack

- **db-server**: PostgreSQL (contêiner)
- **backend**: Python + Flask + WSGI Gunicorn (API REST, contêiner)
- **frontend**: HTML/CSS/JS (consumo da API, contêiner)

## Execução

```bash
docker compose up --build
```

Serviços:

| Serviço | URL |
|---|---|
| Frontend | http://localhost:8080 |
| Backend (API) | http://localhost:5000 |
| PostgreSQL | localhost:5432 |

## Equipe

- Alessh, Alessandro Goldas da Cruz (166600) - Gerente
- Daniel Ubaldo (166688)
- Jadson Henrique (155483)
- Matheus Siqueira (129870)