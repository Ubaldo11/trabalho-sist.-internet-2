CREATE EXTENSION IF NOT EXISTS pg_trgm;

CREATE TABLE aposentados (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    matricula TEXT NOT NULL,
    orgao TEXT NOT NULL,
    sigla_orgao TEXT NOT NULL,
    orgao_vinculacao TEXT NOT NULL,
    cargo_emprego TEXT NOT NULL,
    classe TEXT NOT NULL,
    padrao TEXT NOT NULL,
    referencia TEXT NOT NULL,
    nivel TEXT NOT NULL,
    tipo_aposentadoria TEXT NOT NULL,
    fundamento_legal TEXT NOT NULL,
    portaria_aposentadoria TEXT NOT NULL,
    data_inatividade DATE,
    nome_ocorrencia TEXT NOT NULL,
    data_ingresso_servico_publico DATE,
    valor_aposentadoria NUMERIC(12, 2)
);

CREATE TABLE carreiras (
    id BIGSERIAL PRIMARY KEY,
    nome TEXT NOT NULL,
    cpf TEXT NOT NULL,
    codigo_carreira TEXT NOT NULL,
    cargo_emprego TEXT NOT NULL,
    uf CHAR(2) NOT NULL,
    orgao TEXT NOT NULL,
    mes_referencia TEXT NOT NULL,
    valor_remuneracao NUMERIC(12, 2) NOT NULL
);

COPY aposentados (
    nome, cpf, matricula, orgao, sigla_orgao, orgao_vinculacao,
    cargo_emprego, classe, padrao, referencia, nivel, tipo_aposentadoria,
    fundamento_legal, portaria_aposentadoria, data_inatividade,
    nome_ocorrencia, data_ingresso_servico_publico, valor_aposentadoria
)
FROM '/docker-entrypoint-initdb.d/data/aposentados.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', NULL '');

COPY carreiras (
    nome, cpf, codigo_carreira, cargo_emprego, uf, orgao, mes_referencia,
    valor_remuneracao
)
FROM '/docker-entrypoint-initdb.d/data/carreiras.csv'
WITH (FORMAT csv, HEADER true, DELIMITER ';', NULL '');

CREATE INDEX aposentados_nome_trgm_idx
    ON aposentados USING GIN (nome gin_trgm_ops);
CREATE INDEX aposentados_cargo_idx ON aposentados (cargo_emprego);
CREATE INDEX aposentados_orgao_idx ON aposentados (orgao);
CREATE INDEX aposentados_cpf_idx ON aposentados (cpf);

CREATE INDEX carreiras_nome_trgm_idx
    ON carreiras USING GIN (nome gin_trgm_ops);
CREATE INDEX carreiras_cargo_idx ON carreiras (cargo_emprego);
CREATE INDEX carreiras_uf_idx ON carreiras (uf);
CREATE INDEX carreiras_orgao_idx ON carreiras (orgao);
CREATE INDEX carreiras_cpf_idx ON carreiras (cpf);