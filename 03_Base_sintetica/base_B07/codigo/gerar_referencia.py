# -*- coding: utf-8 -*-
"""
BASE SINTÉTICA – Ativos da concessão (ISA Energia Brasil, 2025) – CENÁRIO DE REFERÊNCIA (sem erros).
Projeto aprovado: D-019 (conta = Ativos da concessão, R$ 36.431.298 mil), D-020 (unidade de registro), D-021 (premissas).

Os registros são SINTÉTICOS (fins didáticos). NÃO são dados internos da ISA Energia Brasil.
Reais: totais por grupo/componente/movimento (F0003 p.45, p.47), contratos e RAP (F0003 p.36), catálogo de módulos ANEEL (F0242).
Sintéticos: abertura por contrato, mês, linha, usuário, fornecedor, datas, taxas, margens.

Precisão: todos os valores são calculados em CENTAVOS INTEIROS (int64); totais distribuídos por "maiores restos".
Uso:  python gerar_referencia.py        (caminhos relativos à pasta base_B07)
"""
import json, sys, time, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CFG = json.load(open(RAIZ / 'config' / 'config_B07.json', encoding='utf-8'))
rng = np.random.default_rng(CFG['semente'])
MIL = 100_000                     # R$ mil -> centavos
M = CFG['metas_mil']
OUT = RAIZ / 'dados_sinteticos'; OUT.mkdir(exist_ok=True)

def alloc(total, w):
    """Distribui 'total' (centavos, int) pelos pesos w com soma exata (método dos maiores restos)."""
    w = np.asarray(w, dtype=float)
    if total == 0 or w.sum() == 0: return np.zeros(len(w), dtype=np.int64)
    w = w / w.sum(); raw = w * total; base = np.floor(raw).astype(np.int64)
    rest = int(total - base.sum()); idx = np.argsort(-(raw - base), kind='stable')[:abs(rest)]
    base[idx] += np.sign(rest); return base

# ------------------------------------------------------------------ contratos (reais) + parâmetros (sintéticos)
CR = pd.read_csv(RAIZ / 'dados_reais_derivados' / 'REAL_contratos_F0003_p36.csv', sep=';', dtype=str)
CR['rap'] = CR.rap_ciclo_2025_26_mil.astype(int)
# fase: OP = operação o ano todo; ENER = energizado em 2025 (F0003 p.7 e p.33: Riacho Grande, Água Vermelha, Piraquê bloco 1); CONS = em obra
FASE = {'008/2022': ('ENER', [10, 11]), '005/2021': ('ENER', list(range(5, 12))), '014/2023': ('ENER', list(range(6, 12))),
        '006/2023': ('CONS', []), '012/2023': ('CONS', []), '011/2022': ('CONS', [])}
# infraestrutura 2025 por contrato (R$ mil) – alocação sintética que fecha com os totais reais por grupo
INFRA = {'059/2001': 1850000, '012/2016': 25000, '008/2022': 1580000, '006/2023': 1250000, '012/2023': 977056,
         '004/2007': 2500, '001/2008': 6000, '015/2008': 8000, '026/2009': 4000, '018/2017': 9000, '026/2017': 3000, '027/2017': 7500,
         '046/2017': 11000, '012/2018': 6500, '021/2018': 3492, '001/2020': 60000, '006/2020': 30000, '007/2020': 55000,
         '005/2021': 215000, '011/2022': 115000, '014/2023': 112000}
EFIC = {'008/2022': -10000, '006/2023': -8000, '012/2023': -7884, '005/2021': 9000, '014/2023': 6371}
RTP = {'059/2001': 166331, '004/2007': -1500, '026/2009': -2128, '026/2017': -2000, '001/2020': -1500}
ABERT_ISA = {'059/2001': 9700000, '012/2016': 1950000, '008/2022': 2350000, '006/2023': 900000, '012/2023': 569771}
TAXA = dict(zip(CR.contrato, np.round(rng.uniform(0.042, 0.099, len(CR)), 4)))      # faixa real 4,2%–9,9% (F0003 p.44)
TAXA['046/2017'] = 0.069
MARGEM = dict(zip(CR.contrato, np.round(rng.uniform(0.02, 0.09, len(CR)), 3)))
CR['fase'] = [FASE.get(c, ('OP', None))[0] for c in CR.contrato]
CR['meses_ativos'] = [FASE.get(c, ('OP', list(range(12))))[1] if c in FASE else list(range(12)) for c in CR.contrato]
rank = CR.rap.rank(pct=True)
CR['n_usuarios'] = np.where(CR.contrato == '059/2001', 480, np.where(CR.fase == 'CONS', 0, (330 + 120 * rank).round().astype(int)))
CR['taxa_implicita'] = CR.contrato.map(TAXA); CR['margem_construcao'] = CR.contrato.map(MARGEM)
CR['infra_mil'] = CR.contrato.map(INFRA).fillna(0).astype(int); CR['efic_mil'] = CR.contrato.map(EFIC).fillna(0).astype(int)
CR['rtp_mil'] = CR.contrato.map(RTP).fillna(0).astype(int)
for g in ('Controladora', 'Controlada'):
    s = CR[CR.grupo == g]
    assert s.infra_mil.sum() == M['IMPL'][g]['infraestrutura'] and s.efic_mil.sum() == M['IMPL'][g]['eficiencia'] and s.rtp_mil.sum() == M['IMPL'][g]['rtp'], g
isa = CR.grupo == 'Controladora'
CR['abert_impl'] = 0
CR.loc[isa, 'abert_impl'] = alloc(M['IMPL']['Controladora']['abertura'] * MIL, CR.loc[isa, 'contrato'].map(ABERT_ISA))
wctl = CR.loc[~isa, 'rap'] * CR.loc[~isa, 'fase'].map({'OP': 9.0, 'ENER': 6.0, 'CONS': 4.0})
CR.loc[~isa, 'abert_impl'] = alloc(M['IMPL']['Controlada']['abertura'] * MIL, wctl)
CR.drop(columns=['meses_ativos']).assign(natureza_dado='SINTETICO_DIDATICO (parâmetros; RAP e contrato são reais)').to_csv(
    OUT / 'SINTETICO_parametros_contratos.csv', index=False, sep=';', decimal=',', encoding='utf-8')
K = CR.set_index('contrato')

# ------------------------------------------------------------------ dimensões sintéticas
NU = CFG['usuarios_pagadores_total']
USU = pd.DataFrame({'usuario_pagador_id': [f'AG{n:04d}' for n in range(1, NU + 1)],
                    'tipo_usuario': rng.choice(['Distribuidora', 'Geradora', 'Consumidor livre', 'Exportador/Importador'], size=NU, p=[0.12, 0.62, 0.24, 0.02])})
wu = (1 / np.arange(1, NU + 1) ** 1.05) * np.where(USU.tipo_usuario == 'Distribuidora', 4.0, 1.0); USU['peso'] = wu / wu.sum()
USU.drop(columns='peso').assign(natureza_dado='SINTETICO_DIDATICO').to_csv(OUT / 'SINTETICO_cadastro_usuarios_pagadores.csv', index=False, sep=';', encoding='utf-8')
NF = 2500; wf = 1 / np.arange(1, NF + 1) ** 0.9; wf /= wf.sum()
pd.DataFrame({'fornecedor_id': [f'F{n:05d}' for n in range(1, NF + 1)], 'natureza_dado': 'SINTETICO_DIDATICO'}).to_csv(OUT / 'SINTETICO_cadastro_fornecedores.csv', index=False, sep=';', encoding='utf-8')
MOD = pd.read_csv(RAIZ / 'dados_reais_derivados' / 'REAL_catalogo_modulos_ANEEL_28_contratos.csv', sep=';', dtype=str)

MESES = pd.period_range('2025-01', '2025-12', freq='M')
BD = {m: pd.bdate_range(m.start_time, m.end_time) for m in pd.period_range('2024-12', '2026-02', freq='M')}
def dias(m_idx, n, max_lag=5):
    """datas de documento e de lançamento (dias úteis) para n itens no mês m_idx (0=jan/2025)."""
    b = BD[MESES[m_idx]] if isinstance(m_idx, (int, np.integer)) else BD[m_idx]
    i = (rng.random(n) * len(b)).astype(int); j = np.minimum(len(b) - 1, i + rng.integers(0, max_lag + 1, n))
    return b[i], b[j]
regs = []
COLS = ['id_documento', 'seq_linha_documento', 'data_lancamento', 'hora_lancamento', 'data_documento', 'competencia', 'entidade', 'grupo', 'contrato',
        'componente', 'tipo_movimento', 'valor_cent', 'id_obra_aneel', 'id_modulo_aneel', 'tipo_receita_aneel', 'fornecedor_id', 'tipo_custo',
        'custo_cent', 'margem_construcao', 'usuario_pagador_id', 'tipo_usuario', 'data_vencimento', 'dias_atraso', 'taxa_implicita_aa',
        'base_calculo_cent', 'origem', 'usuario_sistema', 'aprovador', 'historico']
def add(df): regs.append(df)

# ------------------------------------------------------------------ 1) saldos de abertura (31/12/2024)
sa = []
for c, k in K.iterrows():
    sa.append(dict(contrato=c, componente='IMPL', tipo_movimento='SALDO_ABERTURA', valor_cent=int(k.abert_impl), historico='Saldo de abertura em 01/01/2025 (implementação)'))
sa.append(dict(contrato='059/2001', componente='SE_FIN', tipo_movimento='SALDO_ABERTURA', valor_cent=M['SE_FIN']['abertura'] * MIL, historico='Saldo de abertura – Lei 12.783 SE, componente financeiro'))
sa.append(dict(contrato='059/2001', componente='SE_ECO', tipo_movimento='SALDO_ABERTURA', valor_cent=M['SE_ECO']['abertura'] * MIL, historico='Saldo de abertura – Lei 12.783 SE, componente econômico'))

# ------------------------------------------------------------------ 2) O&M: receita (faturamento ONS por usuário), recebimentos, perda esperada
FAT = np.array([CFG['fator_rap_jan_jun']] * 6 + [1.0] * 6)
oem_rows = []; rec_docs = []      # documentos de recebimento: (contrato, usuario, data, valor_oem, mes_ref)
oem_plan = {}
for g in ('Controladora', 'Controlada'):
    mg = M['OEM'][g]; ops = K[(K.grupo == g) & (K.fase != 'CONS')]
    w_rev = ops.rap * ops.index.map(lambda c: len(FASE[c][1]) if c in FASE else 12) / 12
    rev = dict(zip(ops.index, alloc(mg['receita'] * MIL, w_rev)))
    op_dez24 = ops[ops.fase == 'OP']
    gross_open = dict(zip(op_dez24.index, alloc((mg['abertura_liquida'] - mg['perda_abertura']) * MIL, op_dez24.rap)))
    perda_close = mg['perda_abertura'] + mg['perda_movimento']
    gross_close = dict(zip(ops.index, alloc((mg['fechamento_liquido'] - perda_close) * MIL, ops.rap)))
    for c in ops.index:
        oem_plan[c] = dict(grupo=g, rev=rev[c], open=gross_open.get(c, 0), close=gross_close[c])
    oem_plan[('perda', g)] = (mg['perda_abertura'] * MIL, mg['perda_movimento'] * MIL)
for c, k in K[K.fase != 'CONS'].iterrows():
    p = oem_plan[c]; meses = FASE[c][1] if c in FASE else list(range(12)); nu = int(k.n_usuarios)
    idx = np.sort(rng.choice(NU, size=nu, replace=False, p=USU.peso.values)); wv = USU.peso.values[idx] * rng.uniform(0.95, 1.05, nu)
    mt = np.zeros(12); mt[meses] = FAT[meses]; rev_m = alloc(p['rev'], mt)
    bill = {}                                            # (mes, i_usuario) -> valor
    for m in meses:
        v = alloc(int(rev_m[m]), wv); bill.update({(m, i): int(x) for i, x in enumerate(v)})
        d = BD[MESES[m]][-1]
        oem_rows.append(pd.DataFrame(dict(id_documento=[f"AVC-{c.replace('/', '')}-2025{m + 1:02d}-{USU.usuario_pagador_id[u]}" for u in idx], seq_linha_documento=1,
            data_lancamento=d, data_documento=d, competencia=str(MESES[m]), contrato=c, componente='OEM', tipo_movimento='RECEITA_OEM', valor_cent=v,
            usuario_pagador_id=USU.usuario_pagador_id.values[idx], tipo_usuario=USU.tipo_usuario.values[idx],
            data_vencimento=(MESES[m] + 1).start_time + pd.Timedelta(days=CFG['vencimento_dia'] - 1), origem='AUTOMATICO',
            usuario_sistema='INT_FATURAMENTO_ONS', aprovador='WF_FATURAMENTO', historico='Receita de O&M faturada (aviso de crédito ONS)')))
    # composição do saldo inicial e final do O&M (bruto)
    dez24 = alloc(min(p['open'], int(round(rev_m[meses[0]] * 0.98))) if p['open'] else 0, wv)
    disputa_ini = p['open'] - int(dez24.sum())
    dez25 = sum(bill.get((11, i), 0) for i in range(nu))
    residual = p['close'] - dez25                        # parte do saldo final além da fatura de dezembro/2025
    pagos = {}                                           # (mes_ref, i) -> valor pago em 2025
    for i in range(nu):
        if dez24[i]: pagos[(-1, i)] = int(dez24[i])      # fatura de dez/2024 paga em jan/2025
    for (m, i), v in bill.items():
        if m < 11: pagos[(m, i)] = v
    antecip = 0
    if residual < 0:                                     # parte da fatura de dez/2025 paga antecipadamente em dez/2025
        antecip = -residual; residual = 0
        vd = alloc(antecip, [bill.get((11, i), 0) for i in range(nu)])
        for i in range(nu):
            if vd[i]: pagos[(11, i)] = int(vd[i])
    nova_inad = residual - disputa_ini
    recuperado = 0
    if nova_inad < 0: recuperado = -nova_inad; nova_inad = 0
    if nova_inad > 0:                                    # faturas de 2025 não pagas até 31/12 (inadimplência / discussão judicial – F0003 p.47)
        cand = [(m, i) for (m, i) in pagos if 0 <= m < 11]; order = rng.permutation(len(cand)); falta = nova_inad
        for t in order:
            if falta <= 0: break
            key = cand[t]
            v = pagos[key]; tira = min(v, falta); pagos[key] = v - tira; falta -= tira
        assert falta == 0
    p.update(disputa_ini=disputa_ini, nova_inad=nova_inad, recuperado=recuperado, antecip=antecip, idx=idx, wv=wv)
    for (m, i), v in pagos.items():
        if v <= 0: continue
        venc = (MESES[m] + 1).start_time + pd.Timedelta(days=CFG['vencimento_dia'] - 1) if m >= 0 else pd.Timestamp('2025-01-15')
        atraso = int(rng.integers(1, 41)) if rng.random() < CFG['prob_atraso'] else 0
        if m == 11: venc = pd.Timestamp('2025-12-30'); atraso = 0
        dt = min(venc + pd.Timedelta(days=atraso), pd.Timestamp('2025-12-31'))
        rec_docs.append((c, int(idx[i]), dt, v, m, venc, (dt - venc).days))
    if recuperado:
        rec_docs.append((c, int(idx[0]), pd.Timestamp('2025-09-22'), recuperado, -9, pd.Timestamp('2024-06-15'), (pd.Timestamp('2025-09-22') - pd.Timestamp('2024-06-15')).days))
    sa.append(dict(contrato=c, componente='OEM', tipo_movimento='SALDO_ABERTURA', valor_cent=p['open'], historico='Saldo de abertura – serviços de O&M (bruto)'))
OEM = pd.concat(oem_rows, ignore_index=True)
# perda esperada: abertura e movimento por grupo, distribuídos pelos contratos com saldo em discussão/inadimplência
for g in ('Controladora', 'Controlada'):
    p_ab, p_mov = oem_plan[('perda', g)]
    cs = [c for c in oem_plan if isinstance(c, str) and oem_plan[c]['grupo'] == g]
    w_ab = [max(oem_plan[c]['disputa_ini'], 0) + 1 for c in cs]; w_mv = [oem_plan[c]['nova_inad'] + 1 for c in cs]
    for c, v in zip(cs, alloc(p_ab, w_ab)):
        if v: sa.append(dict(contrato=c, componente='OEM', tipo_movimento='SALDO_ABERTURA_PERDA_ESPERADA', valor_cent=int(v), historico='Perda esperada acumulada em 31/12/2024 (redutora)'))
    pe = pd.DataFrame(dict(contrato=cs, valor_cent=alloc(p_mov, w_mv)))
    pe = pe[pe.valor_cent != 0]
    add(pe.assign(id_documento=[f"PCLD-{c.replace('/', '')}-2025" for c in pe.contrato], seq_linha_documento=1, data_lancamento=pd.Timestamp('2025-12-31'),
        data_documento=pd.Timestamp('2025-12-31'), competencia='2025-12', componente='OEM', tipo_movimento='PERDA_ESPERADA', origem='MANUAL', hora_lancamento='18:10',
        usuario_sistema='U06', aprovador='U09', historico='Constituição de perda esperada sobre faturas de O&M sem garantia (CPC 48)'))
add(OEM)
SA = pd.DataFrame(sa); SA['id_documento'] = ['SALDO-' + c.replace('/', '') + '-' + cp + ('-PE' if 'PERDA' in t else '') for c, cp, t in zip(SA.contrato, SA.componente, SA.tipo_movimento)]
SA['seq_linha_documento'] = 1; SA['data_lancamento'] = pd.Timestamp('2025-01-01'); SA['data_documento'] = pd.Timestamp('2024-12-31'); SA['competencia'] = '2024-12'
SA['origem'] = 'SALDO'; SA['usuario_sistema'] = 'SISTEMA'; SA['aprovador'] = 'SISTEMA'
add(SA)

# ------------------------------------------------------------------ 3) recebimentos: parcela O&M + parcela do ativo contratual (mesmo documento)
RD = pd.DataFrame(rec_docs, columns=['contrato', 'u', 'data', 'v_oem', 'mes_ref', 'venc', 'atraso'])
RD['doc'] = [f"REC-{c.replace('/', '')}-{(str(MESES[m]) if m >= 0 else ('2024-12' if m == -1 else 'DISPUTA')).replace('-', '')}-{USU.usuario_pagador_id[u]}" for c, m, u in zip(RD.contrato, RD.mes_ref, RD.u)]
assert RD.doc.is_unique
rec_lines = [pd.DataFrame(dict(id_documento=RD.doc, seq_linha_documento=1, data_lancamento=RD.data, data_documento=RD.data,
    competencia=[str(MESES[m]) if m >= 0 else '2024-12' for m in RD.mes_ref], contrato=RD.contrato, componente='OEM', tipo_movimento='RECEBIMENTO',
    valor_cent=-RD.v_oem.astype(np.int64), usuario_pagador_id=USU.usuario_pagador_id.values[RD.u], tipo_usuario=USU.tipo_usuario.values[RD.u],
    data_vencimento=RD.venc, dias_atraso=RD.atraso, origem='AUTOMATICO', usuario_sistema='INT_TESOURARIA', aprovador='WF_TESOURARIA',
    historico=np.where(RD.mes_ref == -9, 'Recebimento de fatura de O&M em discussão (acordo/decisão)', 'Recebimento – parcela de O&M')))]
# metas de recebimento do ativo contratual por contrato
rec_ac = {}
for g in ('Controladora', 'Controlada'):
    s = K[(K.grupo == g) & (K.fase != 'CONS')]
    w = s.rap * s.index.map(lambda c: len(FASE[c][1]) if c in FASE else 12)
    rec_ac.update(dict(zip(s.index, alloc(-M['IMPL'][g]['recebimentos'] * MIL, w))))
segs = {'IMPL': None}
for c, tot in rec_ac.items():
    msk = (RD.contrato == c) & (RD.mes_ref != -9)
    sub = RD[msk]
    partes = [('IMPL', int(tot))]
    if c == '059/2001': partes += [('SE_FIN', -M['SE_FIN']['recebimentos'] * MIL), ('SE_ECO', -M['SE_ECO']['recebimentos'] * MIL)]
    for seq, (cp, t) in enumerate(partes, start=2):
        v = alloc(t, sub.v_oem.values.astype(float))
        rec_lines.append(pd.DataFrame(dict(id_documento=sub.doc.values, seq_linha_documento=seq, data_lancamento=sub.data.values, data_documento=sub.data.values,
            competencia=[str(MESES[m]) if m >= 0 else '2024-12' for m in sub.mes_ref], contrato=c, componente=cp, tipo_movimento='RECEBIMENTO', valor_cent=-v,
            usuario_pagador_id=USU.usuario_pagador_id.values[sub.u], tipo_usuario=USU.tipo_usuario.values[sub.u], data_vencimento=sub.venc.values,
            dias_atraso=sub.atraso.values, origem='AUTOMATICO', usuario_sistema='INT_TESOURARIA', aprovador='WF_TESOURARIA',
            historico='Recebimento – parcela do ativo contratual' + (' (RBSE – Lei 12.783)' if cp != 'IMPL' else ''))))
REC = pd.concat(rec_lines, ignore_index=True); add(REC)

# ------------------------------------------------------------------ 4) receita de infraestrutura: itens de medição vinculados a módulos reais ANEEL
saz = np.array(CFG['sazonalidade_obras']); saz /= saz.sum()
TIPOS = ['Material', 'Serviço de montagem', 'Obra civil', 'Equipamento', 'Engenharia e projeto', 'Mão de obra própria', 'Fiscalização e meio ambiente']
wt = np.array([0.30, 0.20, 0.17, 0.15, 0.08, 0.06, 0.04])
infra_tot = sum(INFRA.values()) * MIL
n_alvo = int(infra_tot / 100 / CFG['valor_medio_item_medicao_brl'])
# provisões de medição (projetos em obra/energização), reclassificações e marcos (lançamentos manuais legítimos)
man = []
for c in [c for c in K.index if K.loc[c, 'fase'] in ('CONS', 'ENER')]:
    for m in range(12):
        x = int(rng.uniform(0.5, 3.0) * 1e6) * 100; d = BD[MESES[m]][-1]
        man.append(dict(id_documento=f"PROV-{c.replace('/', '')}-2025{m + 1:02d}", contrato=c, tipo_movimento='PROVISAO_MEDICAO', valor_cent=x, data_lancamento=d, data_documento=d,
                        competencia=str(MESES[m]), usuario_sistema='U03', aprovador='U08', historico='Provisão de medição pendente de aprovação', hora_lancamento='17:30'))
        if m < 11:
            d2 = BD[MESES[m + 1]][0]
            man.append(dict(id_documento=f"PROV-{c.replace('/', '')}-2025{m + 1:02d}-EST", contrato=c, tipo_movimento='ESTORNO_PROVISAO', valor_cent=-x, data_lancamento=d2, data_documento=d2,
                            competencia=str(MESES[m + 1]), usuario_sistema='U03', aprovador='U08', historico='Estorno da provisão de medição do mês anterior', hora_lancamento='09:05'))
MAN = pd.DataFrame(man); MAN['seq_linha_documento'] = 1; MAN['componente'] = 'IMPL'; MAN['origem'] = 'MANUAL'
MARCOS = [('059/2001', 5_000_000), ('008/2022', 2_500_000), ('006/2023', 10_000_000), ('012/2023', 4_000_000), ('059/2001', 1_000_000), ('005/2021', 3_000_000)]
mk = []
for j, (c, v) in enumerate(MARCOS):
    m = int(rng.integers(3, 12)); d = BD[MESES[m]][-3]; md = MOD[MOD.contrato == c].sample(1, random_state=j).iloc[0]
    mk.append(dict(id_documento=f"MARCO-{c.replace('/', '')}-{j:02d}", seq_linha_documento=1, contrato=c, componente='IMPL', tipo_movimento='RECEITA_INFRA', valor_cent=v * 100,
                   data_lancamento=d, data_documento=d, competencia=str(MESES[m]), id_obra_aneel=md.id_obra_aneel, id_modulo_aneel=md.id_modulo_aneel, tipo_receita_aneel=md.tipo_receita_aneel,
                   fornecedor_id=f'F{int(rng.integers(1, 30)):05d}', tipo_custo='Equipamento', custo_cent=int(round(v * 100 / (1 + K.loc[c, 'margem_construcao']))), margem_construcao=K.loc[c, 'margem_construcao'],
                   origem='MANUAL', hora_lancamento='15:40', usuario_sistema='U05', aprovador='U08', historico='Medição de marco contratual (evento de pagamento previsto em contrato; valor redondo)'))
MK = pd.DataFrame(mk)
prov_liq = MAN.groupby('contrato').valor_cent.sum(); marco = MK.groupby('contrato').valor_cent.sum()
inf = []
for c, k in K[K.infra_mil > 0].iterrows():
    alvo = int(k.infra_mil * MIL - prov_liq.get(c, 0) - marco.get(c, 0))
    n = max(80, int(round(n_alvo * k.infra_mil * MIL / infra_tot)))
    mods = MOD[MOD.contrato == c]; wm = rng.dirichlet(np.ones(len(mods)) * 0.6)
    pick = rng.choice(len(mods), size=n, p=wm)
    mes = rng.choice(12, size=n, p=saz)
    v = alloc(alvo, rng.lognormal(0, CFG['sigma_lognormal_medicao'], n))
    v = np.maximum(v, 1)
    v = alloc(alvo, v.astype(float))                      # reajuste exato após piso
    dd = np.empty(n, dtype='datetime64[ns]'); dl = np.empty(n, dtype='datetime64[ns]')
    for m in range(12):
        sel = np.where(mes == m)[0]
        if len(sel): a, b = dias(m, len(sel)); dd[sel] = a.values; dl[sel] = b.values
    mg = k.margem_construcao
    inf.append(pd.DataFrame(dict(id_documento=[f"MED-{c.replace('/', '')}-{j:07d}" for j in range(n)], seq_linha_documento=1, data_lancamento=dl, data_documento=dd,
        competencia=pd.to_datetime(dd).to_period('M').astype(str), contrato=c, componente='IMPL', tipo_movimento='RECEITA_INFRA', valor_cent=v,
        id_obra_aneel=mods.id_obra_aneel.values[pick], id_modulo_aneel=mods.id_modulo_aneel.values[pick], tipo_receita_aneel=mods.tipo_receita_aneel.values[pick],
        fornecedor_id=[f'F{x:05d}' for x in rng.choice(np.arange(1, NF + 1), size=n, p=wf)], tipo_custo=rng.choice(TIPOS, size=n, p=wt),
        custo_cent=np.round(v / (1 + mg)).astype(np.int64), margem_construcao=mg, origem='AUTOMATICO', usuario_sistema='INT_MEDICOES', aprovador='WF_MEDICAO',
        historico='Receita de infraestrutura – medição aprovada')))
INF = pd.concat(inf, ignore_index=True)
# reclassificações entre módulos do mesmo contrato (pares que somam zero)
rc = []
for j in range(220):
    c = rng.choice(INF.contrato.unique()); x = int(rng.lognormal(11.5, 1.0)) * 100; m = int(rng.integers(0, 12)); d = BD[MESES[m]][-int(rng.integers(1, 8))]
    mods = MOD[MOD.contrato == c].sample(2, replace=len(MOD[MOD.contrato == c]) < 2, random_state=j)
    for s, (_, md) in zip((1, -1), mods.iterrows()):
        rc.append(dict(id_documento=f'MEMO-RCL-{j:04d}', seq_linha_documento=1 if s == 1 else 2, contrato=c, componente='IMPL', tipo_movimento='RECLASSIFICACAO', valor_cent=s * x,
                       data_lancamento=d, data_documento=d, competencia=str(MESES[m]), id_obra_aneel=md.id_obra_aneel, id_modulo_aneel=md.id_modulo_aneel, tipo_receita_aneel=md.tipo_receita_aneel,
                       origem='MANUAL', hora_lancamento='16:00', usuario_sistema=f'U0{int(rng.integers(1, 7))}', aprovador='U08', historico='Reclassificação entre módulos do mesmo contrato'))
add(INF); add(MAN); add(MK); add(pd.DataFrame(rc))

# ------------------------------------------------------------------ 5) eficiência, RTP e remuneração
ev = []
for c, k in K.iterrows():
    if k.efic_mil:
        ev.append(dict(id_documento=f"EFI-{c.replace('/', '')}-2025", contrato=c, componente='IMPL', tipo_movimento='EFICIENCIA', valor_cent=int(k.efic_mil) * MIL, data_lancamento=pd.Timestamp('2025-11-28'),
                       data_documento=pd.Timestamp('2025-11-28'), competencia='2025-11', historico='Ganho/perda de eficiência na implementação (real por grupo: F0003 p.47)'))
    if k.rtp_mil:
        d = pd.Timestamp('2025-09-30') if c == '059/2001' else pd.Timestamp('2025-07-31')
        ev.append(dict(id_documento=f"RTP-{c.replace('/', '')}-2025", contrato=c, componente='IMPL', tipo_movimento='RTP', valor_cent=int(k.rtp_mil) * MIL, data_lancamento=d, data_documento=d,
                       competencia=str(d.to_period('M')), historico='Revisão Tarifária Periódica – ' + ('Despacho ANEEL 1.228/25' if c == '059/2001' else 'REH ANEEL 3.470/3.475')))
ev.append(dict(id_documento='REH-3466-2025', contrato='059/2001', componente='SE_FIN', tipo_movimento='REMUNERACAO', valor_cent=M['SE_FIN']['evento_REH_3466'] * MIL,
               data_lancamento=pd.Timestamp('2025-06-30'), data_documento=pd.Timestamp('2025-06-16'), competencia='2025-06', historico='Ajuste RBSE – REH ANEEL 3.466/2025 (valor real: F0003 p.47)'))
EV = pd.DataFrame(ev); EV['seq_linha_documento'] = 1; EV['origem'] = 'MANUAL'; EV['hora_lancamento'] = '16:20'; EV['usuario_sistema'] = 'U02'; EV['aprovador'] = 'U09'; add(EV)
ipca_m = (1 + CFG['ipca_anual_premissa']) ** (1 / 12) - 1
infra_m = INF.assign(m=pd.to_datetime(INF.data_lancamento).dt.month - 1).groupby(['contrato', 'm']).valor_cent.sum()
rm = []
for c, k in K.iterrows():
    saldo = float(k.abert_impl)
    for m in range(12):
        add_m = float(infra_m.get((c, m), 0)); base = saldo + add_m / 2
        rm.append(dict(contrato=c, m=m, grupo=k.grupo, bruto=base * ((1 + k.taxa_implicita) ** (1 / 12) - 1 + ipca_m), base=int(round(base)), taxa=k.taxa_implicita)); saldo += add_m
RM = pd.DataFrame(rm); RM['valor_cent'] = 0
for g in ('Controladora', 'Controlada'):
    msk = RM.grupo == g; RM.loc[msk, 'valor_cent'] = alloc(M['IMPL'][g]['remuneracao'] * MIL, RM.loc[msk, 'bruto'])
se = []
for cp, tot, w in (('SE_FIN', M['SE_FIN']['remuneracao_bruta'], np.linspace(1.0, 0.85, 12)), ('SE_ECO', M['SE_ECO']['remuneracao'], np.ones(12))):
    for m, v in enumerate(alloc(tot * MIL, w)): se.append(dict(contrato='059/2001', m=m, componente=cp, valor_cent=int(v)))
RMS = pd.concat([RM.assign(componente='IMPL'), pd.DataFrame(se)], ignore_index=True)
RMS = pd.DataFrame(dict(id_documento=[f"REM-{c.replace('/', '')}-{cp}-2025{m + 1:02d}" for c, cp, m in zip(RMS.contrato, RMS.componente, RMS.m)], seq_linha_documento=1,
    data_lancamento=[BD[MESES[m]][-1] for m in RMS.m], data_documento=[MESES[m].end_time.normalize() for m in RMS.m], competencia=[str(MESES[m]) for m in RMS.m],
    contrato=RMS.contrato, componente=RMS.componente, tipo_movimento='REMUNERACAO', valor_cent=RMS.valor_cent.astype(np.int64),
    taxa_implicita_aa=RMS.get('taxa'), base_calculo_cent=RMS.get('base'), origem='AUTOMATICO', usuario_sistema='INT_ATIVO_CONTRATUAL', aprovador='WF_FECHAMENTO',
    historico=np.where(RMS.componente == 'IMPL', 'Remuneração do ativo contratual (taxa implícita + IPCA)', 'Atualização/remuneração RBSE – Lei 12.783 (SE)')))
add(RMS)

# ------------------------------------------------------------------ montar 2025, chaves e checagens de fechamento
B = pd.concat(regs, ignore_index=True)
for c in COLS:
    if c not in B: B[c] = np.nan
B['entidade'] = B.contrato.map(K.entidade); B['grupo'] = B.contrato.map(K.grupo)
B['data_lancamento'] = pd.to_datetime(B.data_lancamento); B = B.sort_values(['data_lancamento', 'contrato', 'tipo_movimento', 'id_documento', 'seq_linha_documento'], kind='stable').reset_index(drop=True)
B.insert(0, 'id_lancamento', [f'L25{n:08d}' for n in range(1, len(B) + 1)])
B['valor_cent'] = B.valor_cent.astype(np.int64)
def total(df, **f):
    q = df
    for k_, v_ in f.items(): q = q[q[k_].isin(v_ if isinstance(v_, (list, tuple)) else [v_])]
    return int(q.valor_cent.sum())
assert total(B) == M['publicado_total']['2025'] * MIL, ('total', total(B))
assert total(B, grupo='Controladora') == M['publicado_total']['controladora_2025'] * MIL
assert total(B, componente=['IMPL', 'SE_FIN', 'SE_ECO']) == M['publicado_total']['ativo_contratual_2025'] * MIL
assert total(B, tipo_movimento=['RECEITA_INFRA', 'PROVISAO_MEDICAO', 'ESTORNO_PROVISAO', 'RECLASSIFICACAO']) == 6330048 * MIL

# ------------------------------------------------------------------ 6) lançamentos de jan–fev/2026 (corte)
j26 = []
for c in ['059/2001', '008/2022', '006/2023', '012/2023', '011/2022', '005/2021']:
    n = int(4500 * K.loc[c, 'infra_mil'] / 1850000) + 300; mods = MOD[MOD.contrato == c]; pick = rng.integers(0, len(mods), n)
    mes = rng.integers(0, 2, n); dd = np.empty(n, dtype='datetime64[ns]'); dl = np.empty(n, dtype='datetime64[ns]')
    for m, per in enumerate(['2026-01', '2026-02']):
        sel = np.where(mes == m)[0]; a, b = dias(pd.Period(per, 'M'), len(sel)); dd[sel] = a.values; dl[sel] = b.values
    v = np.maximum(np.round(rng.lognormal(np.log(CFG['valor_medio_item_medicao_brl'] * 100) - 0.85, CFG['sigma_lognormal_medicao'], n)), 100).astype(np.int64); mg = K.loc[c, 'margem_construcao']
    j26.append(pd.DataFrame(dict(id_documento=[f"MED26-{c.replace('/', '')}-{j:07d}" for j in range(n)], seq_linha_documento=1, data_lancamento=dl, data_documento=dd,
        competencia=pd.to_datetime(dd).to_period('M').astype(str), contrato=c, componente='IMPL', tipo_movimento='RECEITA_INFRA', valor_cent=v,
        id_obra_aneel=mods.id_obra_aneel.values[pick], id_modulo_aneel=mods.id_modulo_aneel.values[pick], tipo_receita_aneel=mods.tipo_receita_aneel.values[pick],
        fornecedor_id=[f'F{x:05d}' for x in rng.choice(np.arange(1, NF + 1), size=n, p=wf)], tipo_custo=rng.choice(TIPOS, size=n, p=wt), custo_cent=np.round(v / (1 + mg)).astype(np.int64),
        margem_construcao=mg, origem='AUTOMATICO', usuario_sistema='INT_MEDICOES', aprovador='WF_MEDICAO', historico='Receita de infraestrutura – medição aprovada')))
est = MAN[MAN.competencia == '2025-12'].copy(); est['valor_cent'] = -est.valor_cent; est['data_lancamento'] = BD[pd.Period('2026-01', 'M')][0]; est['competencia'] = '2026-01'
est['tipo_movimento'] = 'ESTORNO_PROVISAO'; est['id_documento'] = est.id_documento + '-EST'; est['historico'] = 'Estorno da provisão de medição do mês anterior'; est['hora_lancamento'] = '09:05'; j26.append(est)
dez = OEM[OEM.competencia == '2025-12'].copy()             # faturas de dez/2025 pagas em jan/2026 (parcela O&M), exceto antecipações
antec = RD[RD.mes_ref == 11].assign(usuario_pagador_id=lambda d: USU.usuario_pagador_id.values[d.u]).set_index(['contrato', 'usuario_pagador_id']).v_oem
dez['valor_cent'] = dez.valor_cent - [int(antec.get((c, u), 0)) for c, u in zip(dez.contrato, dez.usuario_pagador_id)]
dez = dez[dez.valor_cent > 0]
dez['tipo_movimento'] = 'RECEBIMENTO'; dez['valor_cent'] = -dez.valor_cent; dez['data_lancamento'] = pd.Timestamp('2026-01-15'); dez['data_documento'] = pd.Timestamp('2026-01-15')
dez['id_documento'] = dez.id_documento.str.replace('AVC-', 'REC26-', regex=False); dez['usuario_sistema'] = 'INT_TESOURARIA'; dez['aprovador'] = 'WF_TESOURARIA'; dez['dias_atraso'] = 0
dez['historico'] = 'Recebimento – parcela de O&M (fatura de dez/2025)'; j26.append(dez)
J = pd.concat(j26, ignore_index=True)
for c in COLS:
    if c not in J: J[c] = np.nan
J['entidade'] = J.contrato.map(K.entidade); J['grupo'] = J.contrato.map(K.grupo); J['data_lancamento'] = pd.to_datetime(J.data_lancamento)
J = J.sort_values(['data_lancamento', 'contrato', 'id_documento'], kind='stable').reset_index(drop=True); J.insert(0, 'id_lancamento', [f'L26{n:08d}' for n in range(1, len(J) + 1)])
J['valor_cent'] = J.valor_cent.astype(np.int64)

# ------------------------------------------------------------------ 7) saldos (estoque) por contrato × componente × data-base, com circulante
def saldos(df):
    ab = df[df.tipo_movimento.str.startswith('SALDO_ABERTURA')].groupby(['contrato', 'componente']).valor_cent.sum()
    fe = df.groupby(['contrato', 'componente']).valor_cent.sum()
    rec12 = -df[(df.tipo_movimento == 'RECEBIMENTO')].groupby(['contrato', 'componente']).valor_cent.sum()
    S = []
    for ano, ser in (('2024-12-31', ab), ('2025-12-31', fe)):
        t = ser.rename('saldo_cent').reset_index(); t['data_base'] = ano
        t['grupo'] = t.contrato.map(K.grupo)
        t['circ_cent'] = 0
        for g in ('Controladora', 'Controlada'):
            circ_tot = (M['circulante'][ano[:4]]['controladora'] if g == 'Controladora' else M['circulante'][ano[:4]]['consolidado'] - M['circulante'][ano[:4]]['controladora']) * MIL
            oem = t[(t.grupo == g) & (t.componente == 'OEM')]
            t.loc[oem.index, 'circ_cent'] = oem.saldo_cent                    # O&M: prazo < 30 dias (F0003 p.45) – todo circulante
            resto = circ_tot - int(oem.saldo_cent.sum())
            ac = t[(t.grupo == g) & (t.componente != 'OEM')]
            w = [max(rec12.get((c, cp), 0), 0) + 1 for c, cp in zip(ac.contrato, ac.componente)]
            t.loc[ac.index, 'circ_cent'] = alloc(resto, w)
        t['nao_circ_cent'] = t.saldo_cent - t.circ_cent; S.append(t)
    return pd.concat(S, ignore_index=True)
S = saldos(B)
assert int(S[S.data_base == '2024-12-31'].saldo_cent.sum()) == M['publicado_total']['2024'] * MIL
assert int(S[S.data_base == '2025-12-31'].circ_cent.sum()) == M['circulante']['2025']['consolidado'] * MIL
assert (S.nao_circ_cent >= 0).all(), S[S.nao_circ_cent < 0]

# ------------------------------------------------------------------ gravação (centavos -> reais com 2 casas, texto exato)
def reais(x):
    x = pd.Series(x).astype('Int64')
    return x.map(lambda v: '' if pd.isna(v) else f"{'-' if v < 0 else ''}{abs(int(v)) // 100}.{abs(int(v)) % 100:02d}")
FINAL = ['id_lancamento', 'id_documento', 'seq_linha_documento', 'data_lancamento', 'hora_lancamento', 'data_documento', 'competencia', 'entidade', 'grupo', 'contrato', 'componente',
         'tipo_movimento', 'valor_movimento_brl', 'id_obra_aneel', 'id_modulo_aneel', 'tipo_receita_aneel', 'fornecedor_id', 'tipo_custo', 'custo_documento_brl', 'margem_construcao',
         'usuario_pagador_id', 'tipo_usuario', 'data_vencimento', 'dias_atraso', 'taxa_implicita_aa', 'base_calculo_brl', 'origem', 'usuario_sistema', 'aprovador', 'historico', 'natureza_dado']
def formatar(df):
    o = df.copy()
    o['valor_movimento_brl'] = reais(o.valor_cent).values; o['custo_documento_brl'] = reais(o.custo_cent).values; o['base_calculo_brl'] = reais(o.base_calculo_cent).values
    for c in ('data_lancamento', 'data_documento', 'data_vencimento'): o[c] = pd.to_datetime(o[c]).dt.strftime('%Y-%m-%d').fillna('')
    o['dias_atraso'] = o.dias_atraso.astype('Int64'); o['natureza_dado'] = 'SINTETICO_DIDATICO'
    o['id_obra_aneel'] = o.id_obra_aneel.fillna('').astype(str).str.replace(r'\.0$', '', regex=True); o['id_modulo_aneel'] = o.id_modulo_aneel.fillna('').astype(str)
    return o[FINAL]
if __name__ == '__main__':
    t0 = time.time()
    formatar(B).to_csv(OUT / 'SINTETICO_lancamentos_2025_REFERENCIA.csv.gz', index=False, sep=';', encoding='utf-8', compression={'method': 'gzip', 'mtime': 0})
    formatar(J).to_csv(OUT / 'SINTETICO_lancamentos_2026_jan_fev_REFERENCIA.csv.gz', index=False, sep=';', encoding='utf-8', compression={'method': 'gzip', 'mtime': 0})
    So = S.copy(); So['saldo_brl'] = reais(So.saldo_cent).values; So['parcela_circulante_brl'] = reais(So.circ_cent).values; So['parcela_nao_circulante_brl'] = reais(So.nao_circ_cent).values
    So['natureza_dado'] = 'SINTETICO_DIDATICO'
    So[['data_base', 'grupo', 'contrato', 'componente', 'saldo_brl', 'parcela_circulante_brl', 'parcela_nao_circulante_brl', 'natureza_dado']].to_csv(OUT / 'SINTETICO_saldos_REFERENCIA.csv', index=False, sep=';', encoding='utf-8')
    print(f'REFERENCIA: {len(B)} linhas 2025; {len(J)} linhas 2026; {len(S)} saldos; soma 2025 = {total(B)/100:.2f} R$; {time.time()-t0:.1f}s de gravação')
    print(B.tipo_movimento.value_counts().to_string())
