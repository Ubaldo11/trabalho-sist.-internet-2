import os
import pathlib
import re
from flask import Flask, request, jsonify
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import psycopg2
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

app = Flask(__name__)

# Configuração do Rate Limiter
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://"
)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "servidores_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "postgres")
DB_PORT = os.getenv("DB_PORT", "5432")

ESTADOS_VALIDOS = {
    'AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA',
    'MT', 'MS', 'MG', 'PA', 'PB', 'PR', 'PE', 'PI', 'RJ', 'RN',
    'RS', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO'
}

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=RealDictCursor,
        connect_timeout=5
    )

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Página ou endpoint inexistente."}), 404

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "Excesso de requisições simultâneas."}), 429


# -----------------------------------------------------------------------------
# ENDPOINT 1: Servidores Ativos (`servidores`)
# -----------------------------------------------------------------------------
@app.route('/api/servidores', methods=['GET'])
@limiter.limit("30 per minute")
def buscar_servidores():
    nome = request.args.get('nome', '').strip()
    cargo = request.args.get('cargo', '').strip()
    uf = request.args.get('uf', '').strip().upper()
    orgao = request.args.get('orgao', '').strip()
    similar = request.args.get('similar', '').strip()

    try:
        page = max(1, int(request.args.get('page', 1)))
        limit = min(100, max(1, int(request.args.get('limit', 20))))
    except ValueError:
        return jsonify({"error": "Parâmetros 'page' ou 'limit' inválidos."}), 400

    offset = (page - 1) * limit

    if uf and uf not in ESTADOS_VALIDOS:
        return jsonify({"error": "UF inválida informada."}), 400

    conditions = []
    params = []

    if nome:
        conditions.append("nome ILIKE %s")
        params.append(f"%{nome}%")

    if similar:
        clean_similar = re.sub(r'[^a-zA-Z0-9%\s]', '', similar)
        conditions.append("nome ILIKE %s")
        params.append(f"%{clean_similar}%")

    if cargo:
        conditions.append("descricao_do_cargo_emprego ILIKE %s")
        params.append(f"%{cargo}%")

    if uf:
        conditions.append("uf_da_upag_de_vinculacao = %s")
        params.append(uf)

    if orgao:
        conditions.append("denominacao_do_orgao_de_atuacao ILIKE %s")
        params.append(f"%{orgao}%")

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query_count = f"SELECT COUNT(*) as total FROM servidores {where_clause};"
    query_data = f"""
        SELECT id, nome, cpf, codigo_da_carreira, descricao_do_cargo_emprego, 
               uf_da_upag_de_vinculacao AS uf, denominacao_do_orgao_de_atuacao AS orgao, 
               mes_de_referencia, valor_da_remuneracao 
        FROM servidores 
        {where_clause}
        ORDER BY nome ASC
        LIMIT %s OFFSET %s;
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query_count, tuple(params))
        total_records = cursor.fetchone()['total']

        if total_records == 0:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Nenhum registro encontrado.",
                "total": 0,
                "page": page,
                "data": []
            }), 200

        params_with_limits = params + [limit, offset]
        cursor.execute(query_data, tuple(params_with_limits))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "total": total_records,
            "page": page,
            "limit": limit,
            "total_pages": (total_records + limit - 1) // limit,
            "data": results
        }), 200

    except psycopg2.OperationalError:
        return jsonify({"error": "Tempo limite de conexão excedido ou banco indisponível."}), 504
    except Exception as e:
        return jsonify({"error": f"Erro interno no servidor: {str(e)}"}), 500


# -----------------------------------------------------------------------------
# ENDPOINT 2: Servidores Aposentados (`servidores_aposentados`)
# -----------------------------------------------------------------------------
@app.route('/api/servidores-aposentados', methods=['GET'])
@limiter.limit("30 per minute")
def buscar_servidores_aposentados():
    nome = request.args.get('nome', '').strip()
    cargo = request.args.get('cargo', '').strip()
    uf = request.args.get('uf', '').strip().upper()
    orgao = request.args.get('orgao', '').strip()
    similar = request.args.get('similar', '').strip()

    try:
        page = max(1, int(request.args.get('page', 1)))
        limit = min(100, max(1, int(request.args.get('limit', 20))))
    except ValueError:
        return jsonify({"error": "Parâmetros 'page' ou 'limit' inválidos."}), 400

    offset = (page - 1) * limit

    if uf and uf not in ESTADOS_VALIDOS:
        return jsonify({"error": "UF inválida informada."}), 400

    conditions = []
    params = []

    if nome:
        conditions.append("nome ILIKE %s")
        params.append(f"%{nome}%")

    if similar:
        clean_similar = re.sub(r'[^a-zA-Z0-9%\s]', '', similar)
        conditions.append("nome ILIKE %s")
        params.append(f"%{clean_similar}%")

    if cargo:
        conditions.append("cargo ILIKE %s")
        params.append(f"%{cargo}%")

    if uf:
        conditions.append("uf = %s")
        params.append(uf)

    if orgao:
        conditions.append("(nome_do_orgao ILIKE %s OR sigla_do_orgao ILIKE %s)")
        params.extend([f"%{orgao}%", f"%{orgao}%"])

    where_clause = ""
    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query_count = f"SELECT COUNT(*) as total FROM servidores_aposentados {where_clause};"
    query_data = f"""
        SELECT id, nome, cpf, matricula_do_servidor, nome_do_orgao, sigla_do_orgao, cargo, uf, 
               valor_do_rendimento_liquido, tipo_de_aposentadoria, data_publicacao_do_diploma_legal 
        FROM servidores_aposentados 
        {where_clause}
        ORDER BY nome ASC
        LIMIT %s OFFSET %s;
    """

    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute(query_count, tuple(params))
        total_records = cursor.fetchone()['total']

        if total_records == 0:
            cursor.close()
            conn.close()
            return jsonify({
                "message": "Nenhum registro encontrado.",
                "total": 0,
                "page": page,
                "data": []
            }), 200

        params_with_limits = params + [limit, offset]
        cursor.execute(query_data, tuple(params_with_limits))
        results = cursor.fetchall()

        cursor.close()
        conn.close()

        return jsonify({
            "total": total_records,
            "page": page,
            "limit": limit,
            "total_pages": (total_records + limit - 1) // limit,
            "data": results
        }), 200

    except psycopg2.OperationalError:
        return jsonify({"error": "Tempo limite de conexão excedido ou banco indisponível."}), 504
    except Exception as e:
        return jsonify({"error": f"Erro interno no servidor: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)