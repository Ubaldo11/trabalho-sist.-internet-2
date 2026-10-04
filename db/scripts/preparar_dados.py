#!/usr/bin/env python3
"""Unifica e normaliza os arquivos de servidores baixados do dados.gov.br.

Os arquivos de origem sao de largura fixa. O ponto e virgula faz parte do
layout, portanto o parser usa as posicoes do separador em vez de split(';').
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import unicodedata
from collections import Counter
from pathlib import Path


APOSENTADOS_FIELDS = [
    "nome",
    "cpf",
    "matricula",
    "orgao",
    "sigla_orgao",
    "orgao_vinculacao",
    "cargo_emprego",
    "classe",
    "padrao",
    "referencia",
    "nivel",
    "tipo_aposentadoria",
    "fundamento_legal",
    "portaria_aposentadoria",
    "data_inatividade",
    "nome_ocorrencia",
    "data_ingresso_servico_publico",
    "valor_aposentadoria",
]

CARREIRAS_FIELDS = [
    "nome",
    "cpf",
    "codigo_carreira",
    "cargo_emprego",
    "uf",
    "orgao",
    "mes_referencia",
    "valor_remuneracao",
]

# Os offsets sao os mesmos em todos os registros de cada conjunto.
APOSENTADOS_OFFSETS = (61, 73, 86, 127, 138, 144, 185, 187, 191, 194, 198, 226, 267, 328, 337, 388, 397)
CARREIRAS_OFFSETS = (61, 73, 77, 118, 121, 162, 165)

ALLOWED_TEXT = re.compile(r"[^A-Za-z0-9*. ]+")
DATE_FIELDS = {"data_inatividade", "data_ingresso_servico_publico"}
MONEY_FIELDS = {"valor_aposentadoria", "valor_remuneracao"}


def clean_text(value: str) -> str:
    """Converte para ASCII e mantem somente caracteres seguros para CSV/SQL."""
    value = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    value = value.replace(";", " ")
    value = ALLOWED_TEXT.sub(" ", value)
    return " ".join(value.split())


def clean_date(value: str) -> str:
    digits = re.sub(r"\D", "", value)
    if len(digits) == 8:
        return f"{digits[4:]}-{digits[2:4]}-{digits[:2]}"
    return clean_text(value)


def clean_money(value: str) -> str:
    value = value.replace("\x00", "").strip().rstrip(";").strip().replace(".", "").replace(",", ".")
    return value if re.fullmatch(r"\d+(?:\.\d{1,2})?", value) else ""


def normalize_record(fields: list[str], names: list[str]) -> dict[str, str]:
    record = {}
    for name, value in zip(names, fields):
        if name in DATE_FIELDS:
            record[name] = clean_date(value)
        elif name in MONEY_FIELDS:
            record[name] = clean_money(value)
        else:
            record[name] = clean_text(value)
    return record


def split_fixed_width(line: str, offsets: tuple[int, ...]) -> list[str] | None:
    if len(line) < offsets[-1]:
        return None
    starts = (0, *offsets)
    return [line[start:end] for start, end in zip(starts, offsets + (len(line),))]


def read_dataset(files: list[Path], offsets: tuple[int, ...], names: list[str], header_lines: int = 0) -> tuple[list[dict[str, str]], Counter, list[str]]:
    records: list[dict[str, str]] = []
    stats: Counter = Counter()
    rejected: list[str] = []

    for path in files:
        stats["arquivos"] += 1
        with path.open("r", encoding="latin-1", errors="replace", newline="") as source:
            for line_number, raw_line in enumerate(source, 1):
                line = raw_line.rstrip("\r\n")
                if not line or line_number <= header_lines:
                    stats["cabecalhos_ou_vazias"] += 1
                    continue
                fields = split_fixed_width(line, offsets)
                if fields is None:
                    stats["rejeitadas"] += 1
                    rejected.append(f"{path}:{line_number}")
                    continue
                if clean_text(fields[0]).lower() == "nome":
                    stats["cabecalhos_ou_vazias"] += 1
                    continue
                records.append(normalize_record(fields, names))
                stats["linhas_lidas"] += 1
    return records, stats, rejected


def deduplicate(records: list[dict[str, str]]) -> tuple[list[dict[str, str]], int]:
    unique: list[dict[str, str]] = []
    seen: set[tuple[str, ...]] = set()
    for record in records:
        key = tuple(record.values())
        if key in seen:
            continue
        seen.add(key)
        unique.append(record)
    return unique, len(records) - len(unique)


def write_csv(path: Path, records: list[dict[str, str]], fields: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as output:
        writer = csv.DictWriter(output, fieldnames=fields, delimiter=";", lineterminator="\n")
        writer.writeheader()
        writer.writerows(records)


def prepare(aposentados_dir: Path, carreiras_file: Path, output_dir: Path) -> dict:
    aposentados_files = sorted(aposentados_dir.glob("*.csv"))
    aposentados, aposentados_stats, aposentados_rejected = read_dataset(
        aposentados_files, APOSENTADOS_OFFSETS, APOSENTADOS_FIELDS
    )
    carreiras, carreiras_stats, carreiras_rejected = read_dataset(
        [carreiras_file], CARREIRAS_OFFSETS, CARREIRAS_FIELDS, header_lines=2
    )

    aposentados, aposentados_duplicates = deduplicate(aposentados)
    carreiras, carreiras_duplicates = deduplicate(carreiras)
    write_csv(output_dir / "aposentados.csv", aposentados, APOSENTADOS_FIELDS)
    write_csv(output_dir / "carreiras.csv", carreiras, CARREIRAS_FIELDS)

    report = {
        "deduplicacao": "exata apos normalizacao; snapshots mensais do mesmo servidor sao preservados",
        "aposentados": {
            **aposentados_stats,
            "duplicadas_removidas": aposentados_duplicates,
            "registros_exportados": len(aposentados),
            "linhas_rejeitadas": aposentados_rejected,
        },
        "carreiras": {
            **carreiras_stats,
            "duplicadas_removidas": carreiras_duplicates,
            "registros_exportados": len(carreiras),
            "linhas_rejeitadas": carreiras_rejected,
        },
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "relatorio_preparacao.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--aposentados-dir", type=Path, required=True)
    parser.add_argument("--carreiras-file", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()
    report = prepare(args.aposentados_dir, args.carreiras_file, args.output_dir)
    for dataset, values in report.items():
        if isinstance(values, dict):
            print(f"{dataset}: {values['registros_exportados']} registros exportados")
            print(f"  duplicadas removidas: {values['duplicadas_removidas']}")
            print(f"  rejeitadas: {len(values['linhas_rejeitadas'])}")


if __name__ == "__main__":
    main()