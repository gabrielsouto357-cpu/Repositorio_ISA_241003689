# -*- coding: utf-8 -*-
"""PT 450 (parte simulada) – CONFRONTO com o gabarito lacrado. Executar SÓ depois de controle/CONGELAMENTO_RESULTADOS.json.
Confere antes que os resultados não mudaram (hash). Lê o gabarito e a referência apenas para medir detecções, omissões e falsos positivos."""
import json, hashlib
from pathlib import Path
import pandas as pd
B8 = Path(__file__).resolve().parent.parent; BB = B8.parent.parent / '03_Base_sintetica/base_B07'
cong = json.load(open(B8 / 'controle/CONGELAMENTO_RESULTADOS.json', encoding='utf-8'))
for f, h in cong['arquivos'].items():
    assert hashlib.sha256(open(B8 / f, 'rb').read()).hexdigest() == h, f'resultado alterado após congelamento: {f}'
G = BB / 'gabarito_LACRADO'
REG = pd.read_csv(G / 'REGISTRO_ERROS.csv', sep=';', dtype=str); LIN = pd.read_csv(G / 'LINHAS_ALTERADAS.csv', sep=';', dtype=str, keep_default_na=False)
MAP = pd.read_csv(G / 'MAPA_IDS_TESTE_COM_ERRO.csv', sep=';', dtype=str, keep_default_na=False)
REF = pd.read_csv(BB / 'dados_sinteticos/SINTETICO_lancamentos_2025_REFERENCIA.csv.gz', sep=';', dtype=str, keep_default_na=False)
J6 = pd.read_csv(BB / 'dados_sinteticos/SINTETICO_lancamentos_2026_jan_fev_TESTE.csv.gz', sep=';', dtype=str, keep_default_na=False)
D = pd.read_csv(B8 / 'resultados/DISTORCOES_ESTAGIO1.csv', sep=';', dtype=str); X = pd.read_csv(B8 / 'resultados/EXCECOES_EXAMINADAS_ESTAGIO1.csv', sep=';', dtype=str)
C6 = pd.read_csv(B8 / 'resultados/TD06_CLASSIFICACAO.csv', sep=';', dtype=str); AM = pd.read_csv(B8 / 'amostras/AMOSTRA_MUS.csv', sep=';', dtype=str)
# conjunto de linhas com erro (arquivo, id)
err = {('2025', r.id_lancamento_TESTE): r.erro for r in MAP.itertuples()}
e2 = LIN[LIN.id_erro == 'E02'].id_lancamento_ref
k2 = REF[REF.id_lancamento.isin(e2)][['id_documento', 'seq_linha_documento']]
j2 = J6.merge(k2, on=['id_documento', 'seq_linha_documento'])
for i in j2.id_lancamento: err[('2026', i)] = 'E02'
det = {(r.arquivo, r.id_lancamento): r for r in D.itertuples()}
exc_ids = {(r.arquivo, r.id_lancamento) for r in X.itertuples()}
amo = set(AM.id_lancamento)
linhas = []
for e in REG.itertuples():
    ks = [k for k, v in err.items() if v == e.id_erro]
    d_ = [k for k in ks if k in det]; x_ = [k for k in ks if k in exc_ids]
    testes = sorted({f'{det[k].teste} {det[k].regra}' for k in d_} | {f'{r.teste} {r.regra}' for r in X.itertuples() if (r.arquivo, r.id_lancamento) in set(x_)})
    val = sum(float(det[k].dist_saldo_brl) for k in d_); valr = sum(float(det[k].dist_resultado_brl) for k in d_)
    if e.id_erro == 'E10':
        flag = C6[(C6.contrato == '046/2017') & (C6.componente == 'IMPL')].excecao.iloc[0] == 'True'
        linhas.append(dict(id_erro='E10', tipo=e.tipo, linhas_inseridas=1, linhas_sinalizadas=int(flag), linhas_com_distorcao=0, testes='TD-06' if flag else '—',
                           efeito_saldo_inserido=float(e.efeito_saldo_311225_brl), efeito_saldo_detectado=0.0, efeito_resultado_inserido=float(e.efeito_resultado_2025_brl), efeito_resultado_detectado=0.0,
                           situacao='Detectado' if flag else 'NÃO detectado (regra TD-06 não sinalizou)', na_amostra_MUS=0)); continue
    n = len(ks); sit = 'Detectado' if (len(d_) == n or len(x_) == n) and n else ('Parcial' if (d_ or x_) else 'NÃO detectado')
    linhas.append(dict(id_erro=e.id_erro, tipo=e.tipo, linhas_inseridas=n, linhas_sinalizadas=len(x_), linhas_com_distorcao=len(d_), testes='; '.join(testes) or '—',
                       efeito_saldo_inserido=float(e.efeito_saldo_311225_brl), efeito_saldo_detectado=round(val, 2), efeito_resultado_inserido=float(e.efeito_resultado_2025_brl),
                       efeito_resultado_detectado=round(valr, 2), situacao=sit, na_amostra_MUS=len([k for k in ks if k[1] in amo])))
CF = pd.DataFrame(linhas)
fp = [k for k in det if k not in err]
fp_exc = [k for k in exc_ids if k not in err]
fp_d = X[[ (r.arquivo, r.id_lancamento) in set(fp_exc) for r in X.itertuples()]].groupby(['teste', 'regra']).size().to_dict()
amo_err = len([1 for k in err if k[1] in amo])
res = dict(linhas_com_erro=len(err), linhas_com_distorcao_atribuida=len(det), verdadeiros_positivos=len([k for k in det if k in err]), falsos_positivos_com_distorcao=len(fp),
           excecoes_sem_erro_examinadas=dict((f'{a} {b}', c) for (a, b), c in fp_d.items()), td06_sinalizados=C6[C6.excecao == 'True'][['contrato', 'componente']].values.tolist(),
           itens_com_erro_na_amostra_MUS=amo_err, soma_efeito_saldo_inserido=float(CF.efeito_saldo_inserido.sum()), soma_efeito_saldo_detectado=float(CF.efeito_saldo_detectado.sum()))
CF.to_csv(B8 / 'confronto_PT450/CONFRONTO_GABARITO.csv', sep=';', index=False)
json.dump(res, open(B8 / 'confronto_PT450/CONFRONTO_RESUMO.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
print(CF.to_string(index=False)); print(json.dumps(res, ensure_ascii=False, indent=1))
