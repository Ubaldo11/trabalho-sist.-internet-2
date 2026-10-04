# Preparacao dos dados

O script `preparar_dados.py` le os arquivos originais de largura fixa, remove
acentos e caracteres fora do conjunto permitido, corrige datas e valores,
elimina duplicatas exatas e gera CSVs separados por ponto e virgula.

Execute a partir da raiz do trabalho:

```bash
python3 projeto/db/scripts/preparar_dados.py \
  --aposentados-dir Aposentados \
  --carreiras-file Carreiras/CARREIRA_082026.txt \
  --output-dir projeto/db/data/preparados
```

Saidas:

- `aposentados.csv`
- `carreiras.csv`
- `relatorio_preparacao.json`, com contagens e linhas rejeitadas

As duplicatas removidas sao apenas registros identicos depois da
normalizacao. Registros de meses diferentes nao sao unidos por CPF, pois
podem representar snapshots validos do servidor.