import json
import requests

BASE_URL = "http://127.0.0.1:5000"

def testar_endpoints():
    print("--- 1. Testando Servidores Ativos ---")
    res1 = requests.get(f"{BASE_URL}/api/servidores?limit=2")
    print(f"Status: {res1.status_code}")
    # json.dumps converte o dicionário Python para uma string JSON formatada com aspas duplas
    print(json.dumps(res1.json(), indent=2, ensure_ascii=False))
    print("\n")

    print("--- 2. Testando Servidores Aposentados ---")
    res2 = requests.get(f"{BASE_URL}/api/servidores-aposentados?limit=2")
    print(f"Status: {res2.status_code}")
    print(json.dumps(res2.json(), indent=2, ensure_ascii=False))
    print("\n")

    print("--- 3. Testando Filtro por Nome em Aposentados ---")
    res3 = requests.get(f"{BASE_URL}/api/servidores-aposentados?nome=PAULO")
    print(f"Status: {res3.status_code}")
    print(json.dumps(res3.json(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    try:
        testar_endpoints()
    except requests.exceptions.ConnectionError:
        print("Erro: O servidor Flask não está rodando. Execute 'python backend/app.py' primeiro!")