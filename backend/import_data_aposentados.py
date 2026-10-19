import os
import pathlib
import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "servidores_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

def parse_ddmmaaaa(val):
    """Converte datas no formato DDMMAAAA para YYYY-MM-DD do PostgreSQL"""
    if pd.isna(val) or val is None or str(val).strip().lower() in ['nan', 'none', '']:
        return None
    val_str = str(val).split('.')[0].strip().zfill(8)
    if len(val_str) == 8:
        day = val_str[0:2]
        month = val_str[2:4]
        year = val_str[4:8]
        return f"{year}-{month}-{day}"
    return None

def clean_data(filepath):
    try:
        df = pd.read_csv(filepath, header=None, encoding='latin1', sep=';', dtype=str)
    except Exception:
        df = pd.read_csv(filepath, header=None, encoding='iso-8859-1', sep=';', dtype=str)

    column_names = {
        0: 'nome',
        1: 'cpf',
        2: 'matricula_do_servidor',
        3: 'nome_do_orgao',
        4: 'sigla_do_orgao',
        5: 'codigo_do_orgao_superior',
        6: 'cargo',
        7: 'classe',
        8: 'padrao',
        9: 'referencia',
        10: 'nivel',
        11: 'tipo_de_aposentadoria',
        12: 'fundamentacao_da_inatividade',
        13: 'nome_diploma_legal',
        14: 'data_publicacao_do_diploma_legal',
        15: 'ocorrencia_de_ingresso_no_servico_publico',
        16: 'data_de_ocorrencia_de_ingresso_no_servico_publico',
        17: 'valor_do_rendimento_liquido',
        18: 'uf'
    }
    df.rename(columns=column_names, inplace=True)

    # Tratamento das datas
    df['data_publicacao_do_diploma_legal'] = df['data_publicacao_do_diploma_legal'].apply(parse_ddmmaaaa)
    df['data_de_ocorrencia_de_ingresso_no_servico_publico'] = df['data_de_ocorrencia_de_ingresso_no_servico_publico'].apply(parse_ddmmaaaa)

    # Tratamento do Valor Monetário (de "9.516,59" para float 9516.59)
    if 'valor_do_rendimento_liquido' in df.columns:
        df['valor_do_rendimento_liquido'] = (
            df['valor_do_rendimento_liquido']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        df['valor_do_rendimento_liquido'] = pd.to_numeric(df['valor_do_rendimento_liquido'], errors='coerce').fillna(0.0)

    # Substitui NaNs por string vazia mantendo os zeros e strings normais intactas
    df.fillna('', inplace=True)

    return df

def run_import(csv_filepath):
    print(f"Lendo o arquivo de dados em: {csv_filepath}")
    df = clean_data(csv_filepath)
    
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME, user=DB_USER, password=DB_PASS, port=DB_PORT
    )
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO servidores_aposentados (
        nome, cpf, matricula_do_servidor, nome_do_orgao, sigla_do_orgao, codigo_do_orgao_superior,
        cargo, classe, padrao, referencia, nivel, tipo_de_aposentadoria,
        fundamentacao_da_inatividade, nome_diploma_legal, data_publicacao_do_diploma_legal,
        ocorrencia_de_ingresso_no_servico_publico, data_de_ocorrencia_de_ingresso_no_servico_publico,
        valor_do_rendimento_liquido, uf
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
    """

    data_tuples = [
        (
            row.get('nome', ''),
            row.get('cpf', ''),
            row.get('matricula_do_servidor', ''),
            row.get('nome_do_orgao', ''),
            row.get('sigla_do_orgao', ''),
            row.get('codigo_do_orgao_superior', ''),
            row.get('cargo', ''),
            row.get('classe', ''),
            row.get('padrao', ''),
            row.get('referencia', ''),
            row.get('nivel', ''),
            row.get('tipo_de_aposentadoria', ''),
            row.get('fundamentacao_da_inatividade', ''),
            row.get('nome_diploma_legal', ''),
            row.get('data_publicacao_do_diploma_legal'),
            row.get('ocorrencia_de_ingresso_no_servico_publico', ''),
            row.get('data_de_ocorrencia_de_ingresso_no_servico_publico'),
            float(row.get('valor_do_rendimento_liquido', 0.0)),
            row.get('uf') if 'uf' in df.columns else None
        )
        for _, row in df.iterrows()
    ]

    print(f"Inserindo {len(data_tuples)} registros no PostgreSQL...")
    execute_batch(cursor, insert_query, data_tuples, page_size=1000)
    conn.commit()
    cursor.close()
    conn.close()
    print("Importação concluída com sucesso!")

if __name__ == "__main__":
    # csv_path = BASE_DIR / "data" / "teste_2025_aposentados.csv"
    csv_path = BASE_DIR / "data" / "APOSENTADOS_112025.csv"
    run_import(csv_path)