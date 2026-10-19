import pandas as pd
import pathlib

BASE_DIR = pathlib.Path(__file__).resolve().parent.parent

txt_path = BASE_DIR / "data" / "CARREIRA_112025.txt"
csv_path = BASE_DIR / "data" / "CARREIRA_112025.csv"

# 1. Lê o TXT ignorando a primeira linha (cabeçalho original)
df = pd.read_csv(txt_path, sep=';', encoding='latin1', dtype=str, header=0)

# 2. Remove colunas nulas (geradas pelo ';' do final da linha)
df = df.dropna(how='all', axis=1)

# 3. Limpa espaços extras em cada célula de texto
for col in df.columns:
    df[col] = df[col].astype(str).str.strip()

# 4. Salva o CSV sem o cabeçalho (header=False)
df.to_csv(csv_path, index=False, header=False, sep=';', encoding='utf-8')

print(f"Arquivo CSV sem cabeçalho gerado com sucesso em: {csv_path}")
print(f"Total de registros exportados: {len(df)}")