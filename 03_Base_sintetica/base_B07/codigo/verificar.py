# -*- coding: utf-8 -*-
"""
Verificações de integridade da base SINTÉTICA (Bloco 07). Não lê o gabarito lacrado.
Dois grupos de verificação:
  G – INTEGRIDADE DE GERAÇÃO (estrutura): devem passar nos DOIS cenários; falha = defeito do gerador (bloqueia a entrega).
  N – REGRAS DE NEGÓCIO / ECONÔMICAS: devem passar na REFERÊNCIA; no TESTE, ocorrências são EXCEÇÕES A INVESTIGAR
      (o cenário contém erros inseridos de propósito); não indicam falha de geração.
Saída: controle/RELATORIO_VERIFICACOES.md e controle/VERIFICACOES_RESULTADO.csv
Uso: python verificar.py
"""
import json, re
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CFG = json.load(open(RAIZ / 'config' / 'config_B07.json', encoding='utf-8'))
D = RAIZ / 'dados_sinteticos'; RL = RAIZ / 'dados_reais_derivados'; C = RAIZ / 'controle'; C.mkdir(exist_ok=True)
CT = pd.read_csv(RL / 'REAL_contratos_F0003_p36.csv', sep=';', dtype=str, keep_default_na=False)
MOD = pd.read_csv(RL / 'REAL_catalogo_modulos_ANEEL_28_contratos.csv', sep=';', dtype=str, keep_default_na=False)
US = pd.read_csv(D / 'SINTETICO_cadastro_usuarios_pagadores.csv', sep=';', dtype=str, keep_default_na=False)
FO = pd.read_csv(D / 'SINTETICO_cadastro_fornecedores.csv', sep=';', dtype=str, keep_default_na=False)
COLS = ['id_lancamento', 'id_documento', 'seq_linha_documento', 'data_lancamento', 'hora_lancamento', 'data_documento', 'competencia', 'entidade', 'grupo',
        'contrato', 'componente', 'tipo_movimento', 'valor_movimento_brl', 'id_obra_aneel', 'id_modulo_aneel', 'tipo_receita_aneel', 'fornecedor_id', 'tipo_custo',
        'custo_documento_brl', 'margem_construcao', 'usuario_pagador_id', 'tipo_usuario', 'data_vencimento', 'dias_atraso', 'taxa_implicita_aa', 'base_calculo_brl',
        'origem', 'usuario_sistema', 'aprovador', 'historico', 'natureza_dado']
TIPOS = {'SALDO_ABERTURA': 0, 'SALDO_ABERTURA_PERDA_ESPERADA': -1, 'RECEITA_INFRA': 1, 'PROVISAO_MEDICAO': 1, 'ESTORNO_PROVISAO': -1, 'RECEITA_OEM': 1,
         'RECEBIMENTO': -1, 'REMUNERACAO': 0, 'RTP': 0, 'EFICIENCIA': 0, 'PERDA_ESPERADA': -1, 'RECLASSIFICACAO': 0, 'AJUSTE_MANUAL': 0}
COMPS = {'OEM', 'SE_FIN', 'SE_ECO', 'IMPL'}
CUSTOS = {'Fiscalização e meio ambiente', 'Serviço de montagem', 'Equipamento', 'Material', 'Engenharia e projeto', 'Obra civil', 'Mão de obra própria'}
RES = []

def cent(s):
    s = s.astype(str); neg = s.str.startswith('-'); t = s.str.lstrip('-').str.split('.', expand=True)
    v = t[0].astype(np.int64) * 100 + t[1].str.ljust(2, '0').astype(np.int64)
    return pd.Series(np.where(neg, -v, v), index=s.index)
def chk(cen, grupo, cod, desc, n_ocorr, exemplo=''):
    if grupo == 'G' or cen == 'REFERENCIA':
        st = 'OK' if n_ocorr == 0 else 'FALHA DE GERAÇÃO'
    else:
        st = 'OK' if n_ocorr == 0 else 'EXCEÇÃO A INVESTIGAR'
    RES.append(dict(cenario=cen, grupo=grupo, codigo=cod, verificacao=desc, ocorrencias=int(n_ocorr), status=st, exemplo_ids=exemplo))
def ex(df, k=3): return ', '.join(df.id_lancamento.head(k)) if len(df) else ''

def verificar(cen):
    a25 = D / f'SINTETICO_lancamentos_2025_{cen}.csv.gz'; a26 = D / f'SINTETICO_lancamentos_2026_jan_fev_{cen}.csv.gz'
    L = pd.read_csv(a25, sep=';', dtype=str, keep_default_na=False); J = pd.read_csv(a26, sep=';', dtype=str, keep_default_na=False)
    S = pd.read_csv(D / f'SINTETICO_saldos_{cen}.csv', sep=';', dtype=str, keep_default_na=False)
    # ---------- G: integridade de geração
    chk(cen, 'G', 'G01', 'Esquema: 31 colunas na ordem do dicionário (2025 e 2026)', int(list(L.columns) != COLS) + int(list(J.columns) != COLS))
    chk(cen, 'G', 'G02', f'Contagem 2025 ≥ 500.000 linhas de dados (lidas: {len(L):,})'.replace(',', '.'), int(len(L) < 500_000))
    chk(cen, 'G', 'G03', 'Chave primária id_lancamento única e não vazia (2025 + 2026)', int(pd.concat([L.id_lancamento, J.id_lancamento]).duplicated().sum() + (L.id_lancamento == '').sum()))
    chk(cen, 'G', 'G04', 'Formato do id_lancamento (L25/L26 + 8 dígitos)', int((~L.id_lancamento.str.fullmatch(r'L25\d{8}')).sum() + (~J.id_lancamento.str.fullmatch(r'L26\d{8}')).sum()))
    chk(cen, 'G', 'G05', 'natureza_dado = SINTETICO_DIDATICO em todas as linhas', int((L.natureza_dado != 'SINTETICO_DIDATICO').sum() + (J.natureza_dado != 'SINTETICO_DIDATICO').sum()))
    v = L.valor_movimento_brl; bad = ~v.str.fullmatch(r'-?\d+\.\d{2}')
    chk(cen, 'G', 'G06', 'valor_movimento_brl numérico com exatamente 2 casas (sem notação científica)', int(bad.sum()), ex(L[bad]))
    obr = ['data_lancamento', 'competencia', 'entidade', 'grupo', 'contrato', 'componente', 'tipo_movimento', 'valor_movimento_brl', 'origem', 'usuario_sistema', 'aprovador', 'historico']
    nul = (L[obr] == '').any(axis=1)
    chk(cen, 'G', 'G07', 'Campos obrigatórios gerais preenchidos (12 campos)', int(nul.sum()), ex(L[nul]))
    dt = pd.to_datetime(L.data_lancamento, format='%Y-%m-%d', errors='coerce')
    chk(cen, 'G', 'G08', 'data_lancamento válida e dentro de 2025 (arquivo 2025)', int((dt.isna() | (dt.dt.year != 2025)).sum()))
    d6 = pd.to_datetime(J.data_lancamento, format='%Y-%m-%d', errors='coerce')
    chk(cen, 'G', 'G09', 'data_lancamento do arquivo 2026 entre 01/01 e 28/02/2026', int((d6.isna() | (d6 < '2026-01-01') | (d6 > '2026-02-28')).sum()))
    chk(cen, 'G', 'G10', 'Domínios: componente, grupo, origem', int((~L.componente.isin(COMPS)).sum() + (~L.grupo.isin({'Controladora', 'Controlada'})).sum() + (~L.origem.isin({'AUTOMATICO', 'MANUAL', 'SALDO'})).sum()))
    chk(cen, 'G', 'G11', 'Domínio tipo_movimento (13 tipos do dicionário)', int((~L.tipo_movimento.isin(TIPOS)).sum()))
    fk = ~L.contrato.isin(CT.contrato)
    chk(cen, 'G', 'G12', 'FK contrato ∈ 28 contratos reais (F0003 p.36)', int(fk.sum()), ex(L[fk]))
    st = S.copy()
    for k in ['saldo_brl', 'parcela_circulante_brl', 'parcela_nao_circulante_brl']: st[k] = cent(st[k])
    chk(cen, 'G', 'G13', 'Tabela de saldos: circulante + não circulante = saldo (por linha)', int((st.parcela_circulante_brl + st.parcela_nao_circulante_brl != st.saldo_brl).sum()))
    chk(cen, 'G', 'G14', 'Tabela de saldos: chave (data_base, contrato, componente) única', int(st.duplicated(['data_base', 'contrato', 'componente']).sum()))
    # ---------- N: regras de negócio e consistência econômica
    L['v'] = cent(L.valor_movimento_brl)
    ent = L.merge(CT[['contrato', 'entidade', 'grupo']], on='contrato', how='left', suffixes=('', '_ct'))
    m = (ent.entidade != ent.entidade_ct) | (ent.grupo != ent.grupo_ct)
    chk(cen, 'N', 'N01', 'Entidade e grupo coerentes com o contrato (F0003 p.36)', int(m.sum()), ex(ent[m]))
    dk = L[L.id_documento != ''].duplicated(['id_documento', 'seq_linha_documento'], keep=False)
    chk(cen, 'N', 'N02', 'Chave natural (id_documento, seq_linha_documento) única', int(dk.sum()), ex(L[L.id_documento != ''][dk]))
    idn = L.drop(columns=['id_lancamento', 'v']).duplicated(keep=False)
    chk(cen, 'N', 'N03', 'Linhas idênticas (todas as colunas exceto id_lancamento)', int(idn.sum()), ex(L[idn]))
    inf = L[L.tipo_movimento == 'RECEITA_INFRA']
    kf = ['contrato', 'fornecedor_id', 'id_modulo_aneel', 'tipo_custo', 'valor_movimento_brl', 'custo_documento_brl']
    cand = inf[inf.duplicated(kf, keep=False)].copy(); cand['d'] = pd.to_datetime(cand.data_lancamento)
    cand['gap'] = cand.sort_values('d').groupby(kf).d.diff().dt.days
    gr = cand.groupby(kf).agg(gmin=('gap', 'min'), nd=('id_documento', 'nunique'), n=('id_documento', 'size'))
    ruins = gr[(gr.nd < gr.n) | (gr.gmin <= 10)].index
    forte = inf.set_index(kf).index.isin(ruins)
    chk(cen, 'N', 'N04', 'Duplicidade indevida em RECEITA_INFRA: mesmos contrato, fornecedor, módulo, tipo de custo, valor e custo, com mesmo documento ou lançados com até 10 dias de distância', int(forte.sum()), ex(inf[forte]))
    fraca = inf.duplicated(['contrato', 'fornecedor_id', 'valor_movimento_brl', 'custo_documento_brl'], keep=False) & ~forte
    jd = inf[fraca].groupby(['contrato', 'fornecedor_id', 'valor_movimento_brl']).agg(nd=('id_documento', 'nunique'), nm=('id_modulo_aneel', 'nunique'), n=('id_documento', 'size'))
    RES.append(dict(cenario=cen, grupo='I', codigo='I02', verificacao='Duplicidade aparente justificada: mesmo contrato, fornecedor e valor, mas documentos distintos e sem o padrão do N04 (coincidência de valores em itens pequenos de fornecedor frequente)',
                    ocorrencias=int(fraca.sum()), status='INFORMATIVO (justificada)' if bool((jd.nd == jd.n).all()) else 'REVER', exemplo_ids=ex(inf[fraca])))
    sem_doc = (L.id_documento == '') | ((L.data_documento == '') & (L.origem != 'SALDO'))
    chk(cen, 'N', 'N05', 'Lançamento sem documento-suporte (id_documento ou data_documento vazio)', int(sem_doc.sum()), ex(L[sem_doc]))
    s = np.sign(L.v); exp = L.tipo_movimento.map(TIPOS)
    sg = ((exp == 1) & (s < 0)) | ((exp == -1) & (s > 0)) | ((L.tipo_movimento == 'SALDO_ABERTURA') & (s < 0))
    chk(cen, 'N', 'N06', 'Sinal coerente com o tipo (receitas > 0; recebimentos, estornos e perdas < 0)', int(sg.sum()), ex(L[sg]))
    inf = L[L.tipo_movimento == 'RECEITA_INFRA']
    mod = (inf.id_modulo_aneel == '') | (~inf.id_modulo_aneel.isin(MOD.id_modulo_aneel)) | (inf.tipo_receita_aneel == '')
    chk(cen, 'N', 'N07', 'RECEITA_INFRA com módulo ANEEL válido (FK ao catálogo real F0242)', int(mod.sum()), ex(inf[mod]))
    mc = MOD[['id_modulo_aneel', 'contrato']].drop_duplicates()
    jm = inf[inf.id_modulo_aneel != ''].merge(mc, on='id_modulo_aneel', how='left', suffixes=('', '_m'))
    mm = jm.contrato != jm.contrato_m
    chk(cen, 'N', 'N08', 'Módulo ANEEL pertence ao contrato do lançamento', int(mm.sum()), ex(jm[mm]))
    fkf = (inf.fornecedor_id == '') | (~inf.fornecedor_id.isin(FO.fornecedor_id)) | (~inf.tipo_custo.isin(CUSTOS))
    chk(cen, 'N', 'N09', 'RECEITA_INFRA com fornecedor cadastrado e tipo de custo do domínio de obra', int(fkf.sum()), ex(inf[fkf]))
    cu = cent(inf.custo_documento_brl.replace('', '0')); mg = inf.margem_construcao.replace('', '0').astype(float)
    rc = (cu * (1 + mg)).round(); dif = (inf.v - rc).abs() > np.maximum(2, (1 + mg).values)
    chk(cen, 'N', 'N10', 'Recálculo: valor = custo do documento × (1 + margem), tolerância de arredondamento ≤ R$ 0,02', int(dif.sum()), ex(inf[dif]))
    oe = L[L.tipo_movimento.isin(['RECEITA_OEM', 'RECEBIMENTO'])]
    fu = (oe.usuario_pagador_id == '') | (~oe.usuario_pagador_id.isin(US.usuario_pagador_id))
    chk(cen, 'N', 'N11', 'Faturas e recebimentos com usuário pagador cadastrado', int(fu.sum()), ex(oe[fu]))
    dd = pd.to_datetime(L.data_documento, errors='coerce')
    di = (dd.dt.year == 2024) & (L.origem != 'SALDO') & (L.tipo_movimento != 'RECEBIMENTO')
    chk(cen, 'N', 'N12', 'Corte: documento de 2024 lançado como movimento de 2025', int(di.sum()), ex(L[di]))
    pos = (dd > dt) & (L.tipo_movimento != 'REMUNERACAO')
    chk(cen, 'N', 'N13', 'Data do documento posterior ao lançamento (exceto remuneração, calculada no fim do mês e lançada no último dia útil)', int(pos.sum()), ex(L[pos]))
    nm = (L.competencia != L.data_lancamento.str[:7]) & (~L.tipo_movimento.isin(['RECEBIMENTO', 'SALDO_ABERTURA', 'SALDO_ABERTURA_PERDA_ESPERADA']))
    chk(cen, 'N', 'N14', 'Competência = mês do lançamento (recebimentos usam o mês da fatura; aberturas 2024-12)', int(nm.sum()), ex(L[nm]))
    man = L[L.origem == 'MANUAL']
    hr = man.hora_lancamento; fora = (hr == '') | (hr > '20:00') | (hr < '07:00')
    chk(cen, 'N', 'N15', 'Lançamento manual fora do horário 07h–20h ou sem hora', int(fora.sum()), ex(man[fora]))
    sod = (man.usuario_sistema == man.aprovador)
    chk(cen, 'N', 'N16', 'Segregação: lançamento manual aprovado pelo próprio usuário', int(sod.sum()), ex(man[sod]))
    red = man[(man.v.abs() % 100_000_00 == 0) & (man.v.abs() >= 1_000_000_00) & (man.tipo_movimento != 'RECLASSIFICACAO')]
    RES.append(dict(cenario=cen, grupo='I', codigo='I01', verificacao='Informativo: lançamentos manuais (exceto reclassificações) com valor redondo ≥ R$ 1 milhão (há marcos contratuais legítimos)',
                    ocorrencias=len(red), status='INFORMATIVO', exemplo_ids=ex(red)))
    rec = L[L.tipo_movimento == 'RECLASSIFICACAO'].groupby('id_documento').v.sum()
    chk(cen, 'N', 'N17', 'Reclassificações: cada documento soma zero', int((rec != 0).sum()))
    rm = L[L.tipo_movimento == 'REMUNERACAO']; tx = pd.to_numeric(rm.taxa_implicita_aa.replace('', np.nan), errors='coerce')
    ft = tx.notna() & ((tx < 0.042) | (tx > 0.099))
    chk(cen, 'N', 'N18', 'Taxa implícita da remuneração dentro da faixa divulgada 4,2%–9,9% a.a. (F0003 p.44)', int(ft.sum()), ex(rm[ft]))
    rb = L[L.tipo_movimento == 'RECEBIMENTO']; p1 = rb[(rb.seq_linha_documento == '1') & (rb.componente != 'OEM')]
    sem1 = set(rb.id_documento) - set(rb[rb.seq_linha_documento == '1'].id_documento)
    chk(cen, 'N', 'N19', 'Recebimentos: linha 1 de cada documento quita O&M e todo documento tem linha 1', len(p1) + len(sem1), ex(p1))
    cr = rb.groupby('id_documento').contrato.nunique()
    chk(cen, 'N', 'N25', 'Recebimentos: todas as linhas de um documento no mesmo contrato', int((cr > 1).sum()))
    # consistência estoque × fluxo
    fe = L.groupby(['contrato', 'componente']).v.sum(); s25 = st[st.data_base == '2025-12-31'].set_index(['contrato', 'componente']).saldo_brl
    ab = L[L.tipo_movimento.str.startswith('SALDO_ABERTURA')].groupby(['contrato', 'componente']).v.sum(); s24 = st[st.data_base == '2024-12-31'].set_index(['contrato', 'componente']).saldo_brl
    k = sorted(set(fe.index) | set(s25.index)); d1 = sum(int(fe.get(x, 0) != s25.get(x, 0)) for x in k); d0 = sum(int(ab.get(x, 0) != s24.get(x, 0)) for x in sorted(set(ab.index) | set(s24.index)))
    chk(cen, 'N', 'N20', 'Saldo 31/12/2025 (tabela) = abertura + Σ fluxos, por contrato e componente; abertura = saldo 31/12/2024', d0 + d1)
    neg = st[(st.parcela_nao_circulante_brl < 0) | (st.parcela_circulante_brl < 0)]
    chk(cen, 'N', 'N21', 'Parcelas circulante e não circulante não negativas', len(neg))
    oc = st[(st.componente == 'OEM') & (st.parcela_nao_circulante_brl != 0)]
    chk(cen, 'N', 'N22', 'O&M (prazo < 30 dias) integralmente circulante', len(oc))
    tot = int(L.v.sum()); pub = CFG['metas_mil']['publicado_total']['2025'] * 100_000
    chk(cen, 'N', 'N23', f'Σ base 2025 = saldo publicado 36.431.298 mil (diferença em R$ mil: {(tot - pub) / 100_000:,.3f})'.replace(',', 'X').replace('.', ',').replace('X', '.'), int(tot != pub))
    cir = int(st[st.data_base == '2025-12-31'].parcela_circulante_brl.sum()); pc = CFG['metas_mil']['circulante']['2025']['consolidado'] * 100_000
    chk(cen, 'N', 'N24', f'Σ circulante 31/12/2025 = 4.106.084 mil (diferença em R$ mil: {(cir - pc) / 100_000:,.3f})'.replace(',', 'X').replace('.', ',').replace('X', '.'), int(cir != pc))
    return len(L), len(J), len(S), tot

tam = {c: verificar(c) for c in ['REFERENCIA', 'TESTE']}
R = pd.DataFrame(RES); R.to_csv(C / 'VERIFICACOES_RESULTADO.csv', index=False, sep=';', encoding='utf-8')
falhas = R[R.status == 'FALHA DE GERAÇÃO']
md = ['# Relatório de verificações da base sintética (Bloco 07)', '',
      'Gerado por `codigo/verificar.py` (não lê o gabarito lacrado). Base **SINTÉTICA** didática [SD]; não são dados internos da ISA Energia Brasil.', '',
      '**Critério de classificação:**',
      '- **G – integridade de geração:** tem de passar nos dois cenários. Uma ocorrência é **falha de geração** e bloqueia a entrega.',
      '- **N – regras de negócio e econômicas:** têm de passar na referência (ocorrência = falha de geração). No cenário de TESTE, ocorrências são **exceções a investigar**: o cenário contém erros inseridos de propósito, mas o relatório não diz quais. Também não se presume que toda exceção seja erro, porque há situações incomuns legítimas.',
      '- **I – informativo:** só contagem. Não é critério de aprovação.', '',
      f"**Resultado:** {len(falhas)} falha(s) de geração. " + ('Entrega liberada.' if len(falhas) == 0 else 'ENTREGA BLOQUEADA.'), '']
for c in ['REFERENCIA', 'TESTE']:
    n25, n26, ns, tot = tam[c]
    br = lambda x, d=0: f'{x:,.{d}f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    md += [f'## Cenário {c}', '', f'Linhas lidas: 2025 = {br(n25)}; 2026 (jan–fev) = {br(n26)}; saldos = {ns}. Σ 2025 = R$ {br(tot / 100, 2)}.', '',
           '| Código | Verificação | Ocorrências | Status |', '|---|---|---|---|']
    for r in R[R.cenario == c].itertuples(): md.append(f'| {r.codigo} | {r.verificacao} | {r.ocorrencias:,} | {r.status} |'.replace(',', '.'))
    md.append('')
md += ['IDs de exemplo de cada ocorrência: `controle/VERIFICACOES_RESULTADO.csv` (coluna exemplo_ids).']
open(C / 'RELATORIO_VERIFICACOES.md', 'w', encoding='utf-8').write('\n'.join(md))
print(R[['cenario', 'codigo', 'ocorrencias', 'status']].to_string(index=False)); print('FALHAS DE GERAÇÃO:', len(falhas))
