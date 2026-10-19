-- Habilita extensão para busca por similaridade (trigramas)
CREATE EXTENSION IF NOT EXISTS pg_trgm;

--------------------------------------------------------------------------------------------
-- TABELA: SERVIDORES APOSENTADOS
--------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS servidores_aposentados CASCADE;

CREATE TABLE servidores_aposentados (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(20),
    matricula_do_servidor VARCHAR(50),
    nome_do_orgao VARCHAR(255),
    sigla_do_orgao VARCHAR(50),
    codigo_do_orgao_superior VARCHAR(50),
    cargo VARCHAR(255),
    classe VARCHAR(10),
    padrao VARCHAR(10),
    referencia VARCHAR(10),
    nivel VARCHAR(10),
    tipo_de_aposentadoria VARCHAR(255),
    fundamentacao_da_inatividade VARCHAR(255),
    nome_diploma_legal VARCHAR(255),
    data_publicacao_do_diploma_legal DATE,
    ocorrencia_de_ingresso_no_servico_publico VARCHAR(255),
    data_de_ocorrencia_de_ingresso_no_servico_publico DATE,
    valor_do_rendimento_liquido NUMERIC(16, 2),
    uf VARCHAR(2)
);

-- Índices para servidores_aposentados
CREATE INDEX IF NOT EXISTS idx_aposentados_nome ON servidores_aposentados (nome);
CREATE INDEX IF NOT EXISTS idx_aposentados_cargo ON servidores_aposentados (cargo);
CREATE INDEX IF NOT EXISTS idx_aposentados_orgao ON servidores_aposentados (nome_do_orgao);
CREATE INDEX IF NOT EXISTS idx_aposentados_uf ON servidores_aposentados (uf);
CREATE INDEX IF NOT EXISTS idx_aposentados_nome_trgm ON servidores_aposentados USING gin (nome gin_trgm_ops);

--------------------------------------------------------------------------------------------
-- TABELA: SERVIDORES ATIVOS
--------------------------------------------------------------------------------------------
DROP TABLE IF EXISTS servidores CASCADE;

CREATE TABLE servidores (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    cpf VARCHAR(20),
    codigo_da_carreira VARCHAR(50),
    descricao_do_cargo_emprego VARCHAR(255),
    uf_da_upag_de_vinculacao VARCHAR(2),
    denominacao_do_orgao_de_atuacao VARCHAR(255),
    mes_de_referencia VARCHAR(10),
    valor_da_remuneracao NUMERIC(16, 2)
);

-- Índices para servidores
CREATE INDEX IF NOT EXISTS idx_servidores_nome ON servidores (nome);
CREATE INDEX IF NOT EXISTS idx_servidores_cargo ON servidores (descricao_do_cargo_emprego);
CREATE INDEX IF NOT EXISTS idx_servidores_orgao ON servidores (denominacao_do_orgao_de_atuacao);
CREATE INDEX IF NOT EXISTS idx_servidores_uf ON servidores (uf_da_upag_de_vinculacao);
CREATE INDEX IF NOT EXISTS idx_servidores_nome_trgm ON servidores USING gin (nome gin_trgm_ops);