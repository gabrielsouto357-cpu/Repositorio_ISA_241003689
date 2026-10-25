# -*- coding: utf-8 -*-
"""
Executa a cadeia completa da base SINTÉTICA (Bloco 07) e registra ambiente, versões, parâmetros, duração, saídas e hashes.
Ordem: gerar_referencia.py -> inserir_erros.py -> conciliar.py -> verificar.py -> gerar_dicionario.py
Uso (a partir da pasta base_B07):  python codigo/run_all.py
Dependências: requirements.txt (testado com Python 3.13.16; numpy, pandas, openpyxl com versões fixadas). Caminhos relativos à pasta base_B07; sem senhas nem acesso à rede.
"""
import hashlib, json, platform, subprocess, sys, time, gzip
from datetime import datetime, timezone, timedelta
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
C = RAIZ / 'controle'; C.mkdir(exist_ok=True)
BRT = timezone(timedelta(hours=-3))
ETAPAS = ['gerar_referencia.py', 'inserir_erros.py', 'conciliar.py', 'verificar.py', 'gerar_dicionario.py']

def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()
def linhas(p):
    op = gzip.open if p.suffix == '.gz' else open
    with op(p, 'rt', encoding='utf-8') as f: return sum(1 for _ in f) - 1   # exclui cabeçalho

import numpy, pandas, openpyxl
log = dict(projeto='Base SINTÉTICA de Ativos da concessão – ISA Energia Brasil 2025 (didática; não são dados internos da companhia)',
           inicio_brasilia=datetime.now(BRT).isoformat(timespec='seconds'),
           ambiente=dict(python=sys.version.split()[0], sistema=platform.platform(), numpy=numpy.__version__, pandas=pandas.__version__, openpyxl=openpyxl.__version__),
           config=json.load(open(RAIZ / 'config' / 'config_B07.json', encoding='utf-8')), etapas=[])
SO_HASHES = '--so-hashes' in sys.argv   # recalcula só hashes e contagens (ex.: depois de recalcular fórmulas do .xlsx no LibreOffice)
if SO_HASHES:
    log = json.load(open(C / 'EXECUCAO_LOG.json', encoding='utf-8')); log['hashes_atualizados_brasilia'] = datetime.now(BRT).isoformat(timespec='seconds')
for e in ([] if SO_HASHES else ETAPAS):
    t0 = time.time(); r = subprocess.run([sys.executable, str(RAIZ / 'codigo' / e)], cwd=RAIZ, capture_output=True, text=True)
    log['etapas'].append(dict(comando=f'python codigo/{e}', retorno=r.returncode, duracao_s=round(time.time() - t0, 1), saida_final=r.stdout.strip().splitlines()[-12:], erros=r.stderr.strip()[-2000:]))
    print(f'{e}: retorno {r.returncode} em {time.time() - t0:.1f}s')
    if r.returncode != 0: print(r.stderr); sys.exit(1)
arqs = sorted([p for d in ['dados_sinteticos', 'dados_reais_derivados', 'gabarito_LACRADO', 'config', 'codigo'] for p in (RAIZ / d).glob('*') if p.is_file()] +
              [C / 'CONCILIACAO_BASE_B07.xlsx', C / 'RELATORIO_VERIFICACOES.md', C / 'VERIFICACOES_RESULTADO.csv', RAIZ / 'DICIONARIO_DE_DADOS_SINTETICO.xlsx', RAIZ / 'DICIONARIO_DE_DADOS_SINTETICO.md'])
log['arquivos'] = [dict(arquivo=str(p.relative_to(RAIZ)).replace('\\', '/'), bytes=p.stat().st_size, sha256=sha(p),
                        linhas_dados=linhas(p) if p.suffix in ('.csv', '.gz') else None) for p in arqs]
if not SO_HASHES: log['fim_brasilia'] = datetime.now(BRT).isoformat(timespec='seconds')
log['observacao_hashes'] = ('CSV e CSV.gz são determinísticos (semente fixa; gzip com mtime 0). Arquivos .xlsx guardam data de gravação nos metadados: '
                            'a reprodução compara os valores das células, não o hash do .xlsx.')
json.dump(log, open(C / 'EXECUCAO_LOG.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
with open(C / 'HASHES_SHA256.txt', 'w', encoding='utf-8') as f:
    for a in log['arquivos']: f.write(f"{a['sha256']}  {a['arquivo']}\n")
print('log: controle/EXECUCAO_LOG.json; hashes: controle/HASHES_SHA256.txt')
