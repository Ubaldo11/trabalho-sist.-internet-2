# Relatorio de Mudanca 001 - Contenerizacao do banco

- Data: 24/09/2026
- Responsavel: Alessandro Goldas da Cruz (166600), gerente
- Branch: `gerente`
- Commit previsto: `feat(db): conteinerizar banco e importar dados`
- Status: planejada

## Motivo

A auditoria confirmou que o `docker-compose.yml` referencia `db/Dockerfile`, mas esse arquivo ainda nao existe. Tambem nao existe schema PostgreSQL, rotina de importacao ou indice de busca. Sem essa etapa, o servico `db-server` nao pode ser construido nem atender ao backend.

## Escopo desta mudanca

1. Criar o `db/Dockerfile` baseado em PostgreSQL.
2. Criar a inicializacao SQL com as tabelas de aposentados e carreiras.
3. Importar os CSVs preparados durante a inicializacao do banco.
4. Criar extensao e indices para buscas por nome, cargo, UF e orgao.
5. Validar build, inicializacao e contagens dos registros.

## Fora do escopo

- Backend Flask/Gunicorn.
- Frontend.
- Alteracoes no `docker-compose.yml`, salvo necessidade descoberta no teste.
- Versionamento dos CSVs grandes no Git.

## Criterio de aceite

O servico `db-server` deve construir e iniciar com os dados preparados, sem erro de importacao, e as tabelas devem responder a consultas de contagem e busca indexada.

## Resultado

A preencher apos a implementacao e os testes. Nenhum arquivo de codigo foi alterado nesta etapa do relatorio.
