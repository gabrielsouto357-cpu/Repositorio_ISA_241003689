# -*- coding: utf-8 -*-
"""
Bloco 08 – Testes de detalhes na base SINTÉTICA (cenário TESTE): Estágio 1 (100% e itens específicos) e Estágio 2 (MUS estatística).
Segue o desenho congelado (desenho/DESENHO_TESTES_B08.md; controle/CONGELAMENTO_DESENHO.json).
NÃO lê: gabarito_LACRADO, arquivos *_REFERENCIA, geradores (gerar_referencia.py, inserir_erros.py), parâmetros do gerador, resultados do verificar.py.
Uso (de qualquer pasta): python b08_testes.py
"""
import json, hashlib
from pathlib import Path
import numpy as np, pandas as pd
from scipy.stats import gamma

B8 = Path(__file__).resolve().parent.parent; P11 = B8.parent.parent
PAR = json.load(open(B8 / 'desenho' / 'PARAMETROS_B08.json', encoding='utf-8'))
PERM = set(PAR['entradas_permitidas']); LIDOS = []
def ler(rel, **kw):
    assert rel in PERM, f'entrada não permitida: {rel}'
    for proib in ('gabarito', 'REFERENCIA', 'inserir_erros', 'gerar_referencia', 'parametros_contratos', 'VERIFICACOES'):
        assert proib not in rel, rel
    LIDOS.append(rel); return pd.read_csv(P11 / rel, sep=';', dtype=str, keep_default_na=False, **kw)
def cent(s):
    s = s.astype(str).replace('', '0'); neg = s.str.startswith('-'); t = s.str.lstrip('-').str.split('.', expand=True)
    if 1 not in t.columns: t[1] = '0'
    v = t[0].astype(np.int64) * 100 + t[1].fillna('0').str.ljust(2, '0').str[:2].astype(np.int64)
    return pd.Series(np.where(neg, -v, v), index=s.index)
BASE = '03_Base_sintetica/base_B07/'
T = ler(BASE + 'dados_sinteticos/SINTETICO_lancamentos_2025_TESTE.csv.gz'); J6 = ler(BASE + 'dados_sinteticos/SINTETICO_lancamentos_2026_jan_fev_TESTE.csv.gz')
S = ler(BASE + 'dados_sinteticos/SINTETICO_saldos_TESTE.csv'); FO = ler(BASE + 'dados_sinteticos/SINTETICO_cadastro_fornecedores.csv')
US = ler(BASE + 'dados_sinteticos/SINTETICO_cadastro_usuarios_pagadores.csv'); CT = ler(BASE + 'dados_reais_derivados/REAL_contratos_F0003_p36.csv')
MOD = ler(BASE + 'dados_reais_derivados/REAL_catalogo_modulos_ANEEL_28_contratos.csv')
for df in (T, J6): df['v'] = cent(df.valor_movimento_brl)
CTm = PAR['materialidade_mil']['CT'] * 100_000; ME = PAR['materialidade_mil']['ME'] * 100_000
R = B8 / 'resultados'; A = B8 / 'amostras'
DIST = {}   # id_lancamento -> registro de distorção (uma por linha; precedência)
EXC = []    # todas as exceções examinadas (inclusive sem distorção atribuída)
def exc(teste, regra, row, obs, dist_saldo=0, dist_res=0, tipo='factual', prior=0, arq='2025'):
    EXC.append(dict(teste=teste, regra=regra, arquivo=arq, id_lancamento=row.id_lancamento, id_documento=row.id_documento, contrato=row.contrato, tipo_movimento=row.tipo_movimento,
                    valor_brl=row.v / 100, observacao=obs, dist_saldo_brl=dist_saldo / 100, dist_resultado_brl=dist_res / 100))
    if dist_saldo or dist_res:
        k = (arq, row.id_lancamento)
        if k not in DIST or prior > DIST[k]['prior']:
            DIST[k] = dict(teste=teste, regra=regra, arquivo=arq, id_lancamento=row.id_lancamento, contrato=row.contrato, valor_brl=row.v / 100,
                           dist_saldo=dist_saldo, dist_res=dist_res, classificacao=tipo, prior=prior, natureza=obs)

# ================= TD-01: triagem 100% dos débitos de receita de infraestrutura
P1 = T[T.tipo_movimento.isin(PAR['tipos_populacao_infra']) & (T.v > 0)].copy()
P1N = T[T.tipo_movimento.isin(PAR['tipos_populacao_infra'] + ['ESTORNO_PROVISAO']) & (T.v <= 0)].copy()
zeros = P1N[P1N.v == 0]
# R6 sem documento
for r in P1[(P1.id_documento == '') | (P1.data_documento == '')].itertuples(): exc('TD-01', 'R6', r, 'Sem documento-suporte', r.v, r.v, prior=5)
# R4 (só medições RECEITA_INFRA)
med = P1[P1.tipo_movimento == 'RECEITA_INFRA']
mc = MOD[['id_modulo_aneel', 'contrato']].drop_duplicates().rename(columns={'contrato': 'ct_mod'})
mm = med.merge(mc, on='id_modulo_aneel', how='left')
mm.index = med.index
r4 = (med.id_modulo_aneel == '') | mm.ct_mod.isna() | (mm.ct_mod != med.contrato) | (~med.tipo_custo.isin(PAR['tipos_custo_obra'])) | (~med.fornecedor_id.isin(FO.fornecedor_id))
for r in med[r4].itertuples(): exc('TD-01', 'R4', r, f'Medição sem vínculo de obra válido (módulo "{r.id_modulo_aneel}", tipo de custo "{r.tipo_custo}")', r.v, r.v, prior=4)
# R1 duplicidade
dk = P1[(P1.id_documento != '')].sort_values('id_lancamento')
rep = dk[dk.duplicated(['id_documento', 'seq_linha_documento'], keep=False)]
for (d, s), g in rep.groupby(['id_documento', 'seq_linha_documento']):
    g = g.sort_values(['data_lancamento', 'id_lancamento'])
    for i, r in enumerate(g.itertuples()):
        if i == 0: exc('TD-01', 'R1', r, 'Primeira ocorrência do documento repetido (examinada; sem distorção)')
        else: exc('TD-01', 'R1', r, f'Documento {d} lançado novamente', r.v, r.v, prior=3)
kf = ['contrato', 'fornecedor_id', 'id_modulo_aneel', 'tipo_custo', 'v']
m2 = med[~med.id_lancamento.isin(rep.id_lancamento)].copy(); m2['d'] = pd.to_datetime(m2.data_lancamento)
cand = m2[m2.duplicated(kf, keep=False)].sort_values(kf + ['d'])
for _, g in cand.groupby(kf):
    g = g.sort_values('d'); gaps = g.d.diff().dt.days
    for (i, r), gp in zip(g.iterrows(), gaps):
        if pd.notna(gp) and gp <= PAR['tolerancias']['janela_duplicidade_dias']:
            exc('TD-01', 'R1', r, f'Mesmo contrato/fornecedor/módulo/tipo/valor {int(gp)} dia(s) após outro documento', r.v, r.v, prior=3)
# R5 corte – documento do exercício anterior
for r in P1[(P1.data_documento != '') & (P1.data_documento < '2025-01-01')].itertuples():
    exc('TD-01', 'R5', r, f'Documento de {r.data_documento} (exercício anterior) registrado como receita de 2025', 0, r.v, prior=2)
# R2 recálculo (medições com custo)
mc2 = med[med.custo_documento_brl != '']
calc = (cent(mc2.custo_documento_brl) * (1 + mc2.margem_construcao.replace('', '0').astype(float))).round().astype(np.int64)
dif = mc2.v - calc
for (i, r), d in zip(mc2.iterrows(), dif):
    if abs(d) > PAR['tolerancias']['recalculo_margem_brl'] * 100:
        exc('TD-01', 'R2', r, f'Valor difere do custo × (1 + margem) em R$ {d/100:,.2f}', int(d), int(d), prior=1)
med_sem_custo = med[med.custo_documento_brl == '']

# ================= TD-02: lançamentos manuais (2025 + 2026 até 15/01)
tol = PAR['tolerancias']; ini, fim = tol['janela_fim_periodo']
M = pd.concat([T.assign(arq='2025'), J6.assign(arq='2026')]); M = M[M.origem == 'MANUAL']
M = M[(M.arq == '2025') | (M.data_lancamento <= fim)]
freq = M.groupby('usuario_sistema').size()
for r in M.itertuples():
    mot = []
    if r.id_documento == '' or r.data_documento == '': mot.append('sem documento')
    if r.usuario_sistema == r.aprovador: mot.append('mesmo usuário lança e aprova')
    if r.hora_lancamento == '' or not (tol['lancamento_manual_horario'][0] <= r.hora_lancamento <= tol['lancamento_manual_horario'][1]): mot.append(f'hora {r.hora_lancamento or "vazia"}')
    if freq[r.usuario_sistema] <= tol['usuario_incomum_max_lancamentos_ano']: mot.append(f'usuário incomum ({freq[r.usuario_sistema]} lançamentos)')
    if ini <= r.data_lancamento <= fim and abs(r.v) >= CTm: mot.append('fim de período com valor ≥ CT')
    if mot:
        sem_sup = 'sem documento' in mot
        exc('TD-02', 'JE', r, 'Lançamento manual: ' + '; '.join(mot) + ('' if sem_sup else ' – suporte existente, examinado'), r.v if sem_sup else 0, r.v if sem_sup else 0, prior=5, arq=r.arq)

# ================= TD-03: corte – exercício seguinte
c6 = J6[(J6.tipo_movimento == 'RECEITA_INFRA') & (J6.data_documento != '') & (J6.data_documento <= '2025-12-31')]
for r in c6.itertuples(): exc('TD-03', 'CORTE-2026', r, f'Serviço com documento de {r.data_documento} lançado em {r.data_lancamento}', -r.v, -r.v, prior=2, arq='2026')
aj = J6[J6.tipo_movimento == 'ESTORNO_PROVISAO'].groupby('contrato').v.sum()   # estorno da provisão de dez + medição efetiva de dez
TRUEUP = [dict(contrato=c, diferenca_brl=v / 100, abs_menor_que_CT=abs(v) < CTm) for c, v in aj.items()]

# ================= TD-04: recebimentos – contrato por documento
rb = T[T.tipo_movimento == 'RECEBIMENTO']; l1 = rb[rb.seq_linha_documento == '1'].set_index('id_documento').contrato
rb = rb.assign(ct1=rb.id_documento.map(l1)); dif4 = rb[rb.contrato != rb.ct1]
for r in dif4.itertuples(): exc('TD-04', 'CONTRATO', r, f'Linha aplicada ao {r.contrato}; documento pertence ao {r.ct1}', 0, 0, tipo='classificação')
CLASS4 = dif4.groupby(['ct1', 'contrato']).v.sum()

# ================= TD-05: remuneração – recálculo
rm = T[(T.tipo_movimento == 'REMUNERACAO') & (T.base_calculo_brl != '')].copy(); rm['b'] = cent(rm.base_calculo_brl)
rm['f'] = rm.v / rm.b
REM = []
for (c, cp), g in rm.groupby(['contrato', 'componente']):
    tx_mod = g.taxa_implicita_aa.mode().iloc[0]; f_mod = g.f.round(10).mode().iloc[0]
    for r in g.itertuples():
        esp = int(round(r.b * f_mod)); d = r.v - esp
        if r.taxa_implicita_aa != tx_mod or abs(d) > tol['remuneracao_brl'] * 100:
            exc('TD-05', 'REM', r, f'Taxa {r.taxa_implicita_aa} (modal {tx_mod}); esperado R$ {esp/100:,.2f}', int(d), int(d), prior=2)
        REM.append(dict(contrato=c, componente=cp, competencia=r.competencia, base_brl=r.b / 100, valor_brl=r.v / 100, fator=r.f, fator_modal=f_mod, taxa=r.taxa_implicita_aa, taxa_modal=tx_mod, esperado_brl=esp / 100, diferenca_brl=d / 100))

# ================= TD-06: classificação circulante × não circulante
st = S.copy()
for k in ['saldo_brl', 'parcela_circulante_brl', 'parcela_nao_circulante_brl']: st[k] = cent(st[k])
p = st.pivot_table(index=['contrato', 'componente'], columns='data_base', values=['saldo_brl', 'parcela_circulante_brl'], aggfunc='sum')
CLS = []
for (c, cp), r in p.iterrows():
    s4, s5 = r[('saldo_brl', '2024-12-31')], r[('saldo_brl', '2025-12-31')]; c4, c5 = r[('parcela_circulante_brl', '2024-12-31')], r[('parcela_circulante_brl', '2025-12-31')]
    i4 = c4 / s4 if s4 else 0; i5 = c5 / s5 if s5 else 0; esp = int(round(s5 * i4)); d = c5 - esp
    flag = (cp == 'OEM' and s5 != c5) or (abs(i5 - i4) * 100 > tol['classificacao_pp'] and abs(d) >= tol['classificacao_valor_minimo_mil'] * 100_000)
    CLS.append(dict(contrato=c, componente=cp, indice_2024=i4, indice_2025=i5, circulante_2025_brl=c5 / 100, circulante_esperado_brl=esp / 100, diferenca_brl=d / 100, excecao=bool(flag)))
# ================= TD-07: estornos de provisão (2025)
pv = T[T.tipo_movimento == 'PROVISAO_MEDICAO'][['contrato', 'competencia', 'v', 'id_lancamento']]
es = T[T.tipo_movimento == 'ESTORNO_PROVISAO'].copy()
es['comp_ant'] = (pd.to_datetime(es.competencia + '-01') - pd.DateOffset(months=1)).dt.strftime('%Y-%m')
pk = set(zip(pv.contrato, pv.competencia, pv.v))
for r in es.itertuples():
    if (r.contrato, r.comp_ant, -r.v) not in pk: exc('TD-07', 'ESTORNO', r, 'Estorno sem provisão correspondente no mês anterior', r.v, r.v, prior=1)
prov_dez = pv[pv.competencia == '2025-12']

# ================= consolidar Estágio 1
D1 = pd.DataFrame(DIST.values()); E1 = pd.DataFrame(EXC)
cls_exc = pd.DataFrame(CLS); cls_f = cls_exc[cls_exc.excecao]
soma_saldo = int(D1.dist_saldo.abs().sum()) if len(D1) else 0; soma_res = int(D1.dist_res.abs().sum()) if len(D1) else 0
especificos = set(E1[(E1.arquivo == '2025') & E1.teste.isin(['TD-01', 'TD-02'])].id_lancamento)

# ================= Estágio 2: MUS no restante
mus = PAR['mus']; FC = lambda k: float(gamma.ppf(mus['confianca'], k + 1))
TMa = ME - max(soma_saldo, soma_res); EE = mus['erro_esperado_mil'] * 100_000; FE = mus['fator_expansao_erro_esperado']
pop = P1[~P1.id_lancamento.isin(especificos)].sort_values('id_lancamento').copy()
if TMa - EE * FE <= 0: raise SystemExit('MUS não aplicável: examinar 100% (530 A7)')
topo = pop.iloc[0:0]
for _ in range(20):   # iterar estrato superior (itens ≥ J)
    res_ = pop[~pop.id_lancamento.isin(topo.id_lancamento)]; VC = int(res_.v.sum())
    n = int(np.ceil(VC * FC(0) / (TMa - EE * FE))); Jint = VC // n
    novo = pop[pop.v >= Jint]
    if set(novo.id_lancamento) == set(topo.id_lancamento): break
    topo = novo
res_ = pop[~pop.id_lancamento.isin(topo.id_lancamento)].copy(); VC = int(res_.v.sum())
rng = np.random.default_rng(mus['semente_selecao']); inicio = int(rng.integers(1, Jint + 1))
res_['acum'] = res_.v.cumsum(); res_['acum_ini'] = res_.acum - res_.v
pontos = np.arange(inicio, VC + 1, Jint, dtype=np.int64)
idx = np.searchsorted(res_.acum.values, pontos, side='left')
amo = res_.iloc[idx].copy(); amo['ponto_selecao_centavos'] = pontos
assert amo.id_lancamento.is_unique, 'item selecionado duas vezes abaixo de J'
# procedimentos por item (A1–A5); provisões: procedimento alternativo (estorno no mês seguinte ou ajuste em jan/2026)
modset = set(zip(MOD.id_modulo_aneel, MOD.contrato)); doc_cont = P1.groupby(['id_documento', 'seq_linha_documento']).size()
es_all = pd.concat([T[T.tipo_movimento == 'ESTORNO_PROVISAO'], J6[J6.tipo_movimento == 'ESTORNO_PROVISAO']])
es_key = set(zip(es_all.contrato, es_all.v))
def inspecionar(r):
    falhas = []; dist = 0
    if r.tipo_movimento == 'PROVISAO_MEDICAO':
        if (r.contrato, -r.v) not in es_key: falhas.append('A1/alt: provisão sem estorno/ajuste posterior'); dist = r.v
        return falhas, dist
    if r.id_documento == '' or doc_cont.get((r.id_documento, r.seq_linha_documento), 0) > 1: falhas.append('A1 documento ausente/repetido'); dist = r.v
    if r.custo_documento_brl == '' or abs(r.v - round(int(cent(pd.Series([r.custo_documento_brl]))[0]) * (1 + float(r.margem_construcao or 0)))) > 2:
        falhas.append('A2 recálculo'); dist = max(dist, r.v - (round(int(cent(pd.Series([r.custo_documento_brl or '0']))[0]) * (1 + float(r.margem_construcao or 0)))))
    if (r.id_modulo_aneel, r.contrato) not in modset or r.tipo_custo not in PAR['tipos_custo_obra'] or r.fornecedor_id not in set(FO.fornecedor_id): falhas.append('A3 vínculo de obra'); dist = r.v
    if not ('2025-01-01' <= r.data_documento <= r.data_lancamento): falhas.append('A4 data'); dist = r.v
    if r.aprovador == '' or r.aprovador == r.usuario_sistema: falhas.append('A5 aprovação'); dist = r.v
    return falhas, int(dist)
FOset = set(FO.fornecedor_id)
res_insp = [inspecionar(r) for r in amo.itertuples()]
amo['resultado'] = ['; '.join(f) if f else 'Sem exceção' for f, _ in res_insp]; amo['distorcao_centavos'] = [d for _, d in res_insp]
amo['tainting'] = amo.distorcao_centavos / amo.v
tt = sorted(amo.tainting[amo.tainting > 0], reverse=True)
BP = FC(0) * Jint; PM = sum(t * Jint for t in tt); IA = sum(t * (FC(i + 1) - FC(i) - 1) * Jint for i, t in enumerate(tt))
ULM = BP + PM + IA
topo_dist = 0  # estrato superior examinado com os mesmos procedimentos
for r in topo.itertuples(): topo_dist += inspecionar(r)[1]
RES = dict(
    entradas_lidas=LIDOS,
    populacao_TD01=dict(linhas=len(P1), valor_brl=int(P1.v.sum()) / 100, por_tipo={k: [int(g.v.size), int(g.v.sum()) / 100] for k, g in P1.groupby('tipo_movimento')}),
    negativos_e_zeros=dict(linhas=len(P1N), valor_brl=int(P1N.v.sum()) / 100, zeros=len(zeros)),
    completude=dict(soma_P1_mais_negativos_brl=(int(P1.v.sum()) + int(P1N.v.sum())) / 100, nota='= linha Receita de infraestrutura do razão TESTE (CONCILIACAO_BASE_B07, aba C_TESTE)'),
    medicoes_sem_custo=len(med_sem_custo),
    estagio1=dict(excecoes_examinadas=len(E1), linhas_com_distorcao=len(D1), soma_abs_efeito_saldo_brl=soma_saldo / 100, soma_abs_efeito_resultado_brl=soma_res / 100,
                  efeito_liquido_saldo_brl=int(D1.dist_saldo.sum()) / 100, efeito_liquido_resultado_brl=int(D1.dist_res.sum()) / 100,
                  por_teste={'|'.join(k): dict(linhas=int(len(g)), saldo_brl=int(g.dist_saldo.sum()) / 100, resultado_brl=int(g.dist_res.sum()) / 100) for k, g in D1.groupby(['teste', 'regra'])} if len(D1) else {},
                  classificacao_contratos_TD04_brl=int(CLASS4.sum()) / 100 if len(CLASS4) else 0, classificacao_circulante_TD06=cls_f.to_dict('records'),
                  ajustes_provisao_dez_2026=TRUEUP),
    mus=dict(TM_base_brl=ME / 100, TM_amostra_brl=TMa / 100, EE_brl=EE / 100, FE=FE, FC0=FC(0), itens_especificos_excluidos=len(especificos & set(P1.id_lancamento)),
             estrato_superior_itens=len(topo), estrato_superior_valor_brl=int(topo.v.sum()) / 100, estrato_superior_distorcao_brl=topo_dist / 100,
             VC_restante_brl=VC / 100, linhas_restante=len(res_), n_calculado=n, J_brl=Jint / 100, inicio_aleatorio_centavos=inicio, n_selecionado=len(amo),
             distorcoes_na_amostra=int((amo.distorcao_centavos > 0).sum()), soma_distorcoes_amostra_brl=int(amo.distorcao_centavos.sum()) / 100,
             precisao_basica_brl=BP / 100, distorcao_projetada_brl=PM / 100, acrescimo_brl=IA / 100, limite_superior_brl=ULM / 100,
             conclusao='limite superior ≤ TM_amostra' if ULM <= TMa else 'limite superior > TM_amostra: ampliar (A23)'),
    tamanho_referencia_B06=int(np.ceil(int(P1.v.sum()) * FC(0) / (ME - EE * FE))))
# gravar
pop.assign(estrato=np.where(pop.id_lancamento.isin(topo.id_lancamento), 'SUPERIOR_100', 'RESTANTE_MUS'))[['id_lancamento', 'tipo_movimento', 'contrato', 'valor_movimento_brl', 'estrato']] \
    .to_csv(A / 'POPULACAO_ELEGIVEL_MUS.csv.gz', sep=';', index=False, compression={'method': 'gzip', 'mtime': 0})
amo[['ponto_selecao_centavos', 'id_lancamento', 'id_documento', 'contrato', 'tipo_movimento', 'valor_movimento_brl', 'acum_ini', 'acum', 'resultado', 'distorcao_centavos', 'tainting']] \
    .to_csv(A / 'AMOSTRA_MUS.csv', sep=';', index=False)
E1.to_csv(R / 'EXCECOES_EXAMINADAS_ESTAGIO1.csv', sep=';', index=False)
D1.assign(dist_saldo_brl=D1.dist_saldo / 100, dist_resultado_brl=D1.dist_res / 100).drop(columns=['dist_saldo', 'dist_res', 'prior']).to_csv(R / 'DISTORCOES_ESTAGIO1.csv', sep=';', index=False)
pd.DataFrame(REM).to_csv(R / 'TD05_REMUNERACAO_RECALCULO.csv', sep=';', index=False)
cls_exc.to_csv(R / 'TD06_CLASSIFICACAO.csv', sep=';', index=False)
json.dump(RES, open(R / 'RESULTADOS_B08.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1, default=str)
print(json.dumps({k: RES[k] for k in ['estagio1', 'mus']}, ensure_ascii=False, indent=1, default=str)[:6000])
