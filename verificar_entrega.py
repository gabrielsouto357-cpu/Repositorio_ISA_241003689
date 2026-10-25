"""Confere se os arquivos deste repositório estão completos e íntegros.

Compara o tamanho e o SHA-256 de cada arquivo com INVENTARIO_FINAL.csv.
Uso, na pasta do repositório:  py -3.12 verificar_entrega.py   (ou python3 verificar_entrega.py)
Não precisa instalar bibliotecas. Integridade não equivale a validação técnica do conteúdo.
"""
import csv
import hashlib
import json
from pathlib import Path

RAIZ = Path(__file__).resolve().parent
INVENTARIO = RAIZ / 'INVENTARIO_FINAL.csv'


def sha256(caminho):
    h = hashlib.sha256()
    with caminho.open('rb') as f:
        for bloco in iter(lambda: f.read(1 << 20), b''):
            h.update(bloco)
    return h.hexdigest()


falhas = []
conferidos = 0
with INVENTARIO.open(encoding='utf-8-sig', newline='') as f:
    for linha in csv.DictReader(f, delimiter=';'):
        caminho = RAIZ / linha['arquivo']
        conferidos += 1
        if not caminho.is_file():
            falhas.append({'arquivo': linha['arquivo'], 'erro': 'ausente'})
        elif caminho.stat().st_size != int(linha['bytes']):
            falhas.append({'arquivo': linha['arquivo'], 'erro': 'tamanho diferente'})
        elif sha256(caminho) != linha['sha256']:
            falhas.append({'arquivo': linha['arquivo'], 'erro': 'SHA-256 diferente'})

print(json.dumps({'arquivos_conferidos': conferidos, 'falhas': falhas,
                  'resultado': 'OK' if not falhas else 'FALHA'}, ensure_ascii=False, indent=2))
raise SystemExit(1 if falhas else 0)
