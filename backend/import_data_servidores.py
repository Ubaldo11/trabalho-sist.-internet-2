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

def clean_data(filepath):
    # Lê o CSV gerado sem cabeçalho e separado por ';'
    try:
        df = pd.read_csv(filepath, header=None, encoding='utf-8', sep=';', dtype=str)
    except (UnicodeDecodeError, pd.errors.ParserError):
        df = pd.read_csv(filepath, header=None, encoding='iso-8859-1', sep=';', dtype=str)

    # Mapeamento posicional das 8 colunas do arquivo
    column_names = {
        0: 'nome',
        1: 'cpf',
        2: 'codigo_da_carreira',
        3: 'descricao_do_cargo_emprego',
        4: 'uf_da_upag_de_vinculacao',
        5: 'denominacao_do_orgao_de_atuacao',
        6: 'mes_de_referencia',
        7: 'valor_da_remuneracao'
    }
    df.rename(columns=column_names, inplace=True)

    # Tratamento do Valor Monetário (ex: "64.351,22" para float 64351.22)
    if 'valor_da_remuneracao' in df.columns:
        df['valor_da_remuneracao'] = (
            df['valor_da_remuneracao']
            .astype(str)
            .str.replace('.', '', regex=False)
            .str.replace(',', '.', regex=False)
        )
        df['valor_da_remuneracao'] = pd.to_numeric(df['valor_da_remuneracao'], errors='coerce').fillna(0.0)

    # Preenche valores nulos com string vazia
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
    INSERT INTO servidores (
        nome, cpf, codigo_da_carreira, descricao_do_cargo_emprego,
        uf_da_upag_de_vinculacao, denominacao_do_orgao_de_atuacao,
        mes_de_referencia, valor_da_remuneracao
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s);
    """

    data_tuples = [
        (
            row.get('nome', ''),
            row.get('cpf', ''),
            row.get('codigo_da_carreira', ''),
            row.get('descricao_do_cargo_emprego', ''),
            row.get('uf_da_upag_de_vinculacao', ''),
            row.get('denominacao_do_orgao_de_atuacao', ''),
            row.get('mes_de_referencia', ''),
            float(row.get('valor_da_remuneracao', 0.0))
        )
        for _, row in df.iterrows()
    ]

    print(f"Inserindo {len(data_tuples)} registros na tabela 'servidores'...")
    execute_batch(cursor, insert_query, data_tuples, page_size=1000)
    conn.commit()
    cursor.close()
    conn.close()
    print("Importação de servidores concluída com sucesso!")

if __name__ == "__main__":
    # csv_path = BASE_DIR / "data" / "teste_2025_servidores.csv"
    csv_path = BASE_DIR / "data" / "CARREIRA_112025.csv"
    run_import(csv_path)