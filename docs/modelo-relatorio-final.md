# Relatorio Final do Projeto

**Aplicacao Full Stack - Servidores do Executivo Federal**

- Disciplina: Sistemas para Internet II - 3o Bimestre
- Prazo de entrega: 13/10/2026

## 1. Integrantes e Papel

| Nome | RA | Papel / Responsabilidades |
|---|---|---|
| Alessandro Goldas da Cruz | 166600 | Gerente / Lider Tecnico: docker-compose, documentacao, relatorios, burndown |
| Daniel Ubaldo | 166688 | Banco de Dados: schema PostgreSQL, contêiner db-server, importacao e indices |
| Jadson Henrique | 155483 | Frontend: HTML/CSS/JS, telas de busca, paginacao, consumo da API |
| Matheus Siqueira | 129870 | Backend API: Flask + Gunicorn, endpoints, buscas, seguranca |

## 2. Cronograma / Sprint (30 dias)

| Semana | Atividades |
|---|---|
| Semana 1 | Setup GitHub, analise dos dados do dados.gov.br, schema do banco |
| Semana 2 | Dockerfiles e contêineres, base da API Flask |
| Semana 3 | Endpoints de busca, frontend, integracao dos 3 contêineres |
| Semana 4 | Testes de sobrecarga, correcoes, relatorio final |

## 3. Registro Diario de Commits

| Data | Autor (RA) | Commit | Descricao |
|---|---|---|---|
| 14/09/2026 | Alessandro (166600) | f3b44ee | feat: commit inicial (estrutura base + docker-compose) |
| 14/09/2026 | Alessandro (166600) | ef8726f | chore: integrar README do GitHub |
| 14/09/2026 | Alessandro (166600) | 5f58e82 | chore: hook de validacao de commits |
| ... | ... | ... | ... |

## 4. Arquitetura dos Contêineres

- `db-server`: PostgreSQL (porta 5432)
- `backend`: Python + Flask + Gunicorn (porta 5000)
- `frontend`: HTML/CSS/JS (porta 8080 -> 80)

Orquestracao: `docker compose up --build`

## 5. Burndown da Sprint

_(preencher ao final, com pontos concluidos por dia pela equipe)_

## 6. Pontos Fortes e Fracos da Equipe

_(preencher ao final)_

## 7. Dificuldades e Impedimentos

_(preencher ao final)_