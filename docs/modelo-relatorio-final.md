# Relatório Final do Projeto

**Aplicação Full Stack - Servidores do Executivo Federal**

- Disciplina: Sistemas para Internet II - 3º Bimestre
- Prazo de entrega: 13/10/2026

## 1. Integrantes e Papel

| Nome | RA | Papel / Responsabilidades |
|---|---|---|
| Alessandro Goldas da Cruz | 166600 | Gerente / Líder Técnico: docker-compose, documentação, relatórios, burndown |
| Daniel Ubaldo | 166688 | Backend: Python, Flask, Gunicorn e endpoints da API |
| Jadson Henrique | 155483 | Frontend: HTML/CSS/JS, telas de busca, paginação, consumo da API |
| Matheus Siqueira | 129870 | Apoio na integração das buscas ao sistema e validação da integração |

## 2. Cronograma / Sprint (30 dias)

| Semana | Atividades |
|---|---|
| Semana 1 | Setup GitHub, análise dos dados do dados.gov.br, definição do schema do banco |
| Semana 2 | Desenvolvimento dos Dockerfiles e contêineres, preparação da base da API Flask |
| Semana 3 | Desenvolvimento dos endpoints de busca, desenvolvimento do frontend e integração dos contêineres |
| Semana 4 | Testes de sobrecarga, correções, integração final e elaboração do relatório |

## 3. Registro Diário de Commits

| Data | Autor (RA) | Hash | Descrição |
|---|---|---|---|
| 14/09/2026 | Ubaldo11 | 337d702 | Initial commit (README automático do GitHub) |
| 14/09/2026 | Alessandro (166600) | f3b44ee | feat: commit inicial (estrutura base + docker-compose) |
| 14/09/2026 | Alessandro (166600) | ef8726f | chore: integrar README do GitHub |
| 14/09/2026 | Alessandro (166600) | 5f58e82 | chore: hook de validação de commits |
| 15/09/2026 | Alessandro (166600) | bfa6bbe | docs: modelo do relatório final (PR #1) |
| 15/09/2026 | Alessandro (166600) | 1757929 | docs: atualizar histórico de commits no modelo do relatório |
| 15/09/2026 | Alessandro (166600) | 5827bd4 | docs: modelo do relatório final |
| 17/09/2026 | Jadson Henrique | 038d515 | feat(frontend): cria estrutura inicial do frontend |
| 18/09/2026 | Jadson Henrique | f31fddb | feat: aprimora interface do frontend |
| 19/09/2026 | Jadson Henrique | b6af9b1 | feat: aplica tema hacker ao frontend |

> Para atualizar este registro durante o desenvolvimento, pode ser utilizado:
>
> `git log --pretty=format:"%h|%an|%ad|%s" --date=format:"%d/%m/%Y %H:%M"`

## 4. Arquitetura dos Contêineres

O projeto utiliza uma arquitetura composta por três contêineres principais:

- `db-server`: PostgreSQL, responsável pelo armazenamento dos dados.
- `backend`: aplicação desenvolvida em Python utilizando Flask e Gunicorn, responsável pela API e comunicação com o banco de dados.
- `frontend`: aplicação web desenvolvida com HTML, CSS e JavaScript, responsável pela interface de consulta dos servidores.

A orquestração dos contêineres é realizada utilizando Docker Compose:

```bash
docker compose up --build
