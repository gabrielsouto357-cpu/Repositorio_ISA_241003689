# -*- coding: utf-8 -*-
"""
Cria o CENÁRIO DE TESTE (com erros controlados) a partir do cenário de REFERÊNCIA gravado, sem alterá-lo.
D-021: erros sem compensação (nenhuma linha é reduzida para esconder diferenças); nenhum marcador de erro na base;
registro separado em gabarito_LACRADO/ (NÃO usar como insumo de testes; abrir só no PT 450).
Uso: python inserir_erros.py
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

RAIZ = Path(__file__).resolve().parent.parent
CFG = json.load(open(RAIZ / 'config' / 'config_B07.json', encoding='utf-8'))
rng = np.random.default_rng(CFG['semente'] + 7)          # semente derivada, registrada
D = RAIZ / 'dados_sinteticos'; G = RAIZ / 'gabarito_LACRADO'; G.mkdir(exist_ok=True)

def cent(s):
    s = s.fillna('').astype(str)
    neg = s.str.startswith('-'); t = s.str.lstrip('-').str.split('.', expand=True)
    v = t[0].replace('', '0').astype(np.int64) * 100 + t[1].fillna('0').str.ljust(2, '0').replace('', '00').astype(np.int64)
    return np.where(neg, -v, v)
def reais(v):
    return [f"{'-' if x < 0 else ''}{abs(int(x)) // 100}.{abs(int(x)) % 100:02d}" for x in v]

R = pd.read_csv(D / 'SINTETICO_lancamentos_2025_REFERENCIA.csv.gz', sep=';', dtype=str, keep_default_na=False)
J = pd.read_csv(D / 'SINTETICO_lancamentos_2026_jan_fev_REFERENCIA.csv.gz', sep=';', dtype=str, keep_default_na=False)
SR = pd.read_csv(D / 'SINTETICO_saldos_REFERENCIA.csv', sep=';', dtype=str, keep_default_na=False)
T = R.copy(); T['v'] = cent(T.valor_movimento_brl); T['id_ref'] = T.id_lancamento; T['erro'] = ''
J2 = J.copy(); J2['v'] = cent(J2.valor_movimento_brl); J2['id_ref'] = J2.id_lancamento; J2['erro'] = ''
LOG = []; LIN = []
def reg(cod, tipo, desc, afirm, linhas, ef_saldo, ef_res, campo):
    LOG.append(dict(id_erro=cod, tipo=tipo, descricao=desc, afirmacao=afirm, n_linhas=linhas, campo_alterado=campo,
                    efeito_saldo_311225_brl=reais([ef_saldo])[0], efeito_resultado_2025_brl=reais([ef_res])[0]))
inf = T[(T.tipo_movimento == 'RECEITA_INFRA') & (T.origem == 'AUTOMATICO')]

# E01 – corte 2024 -> 2025: documentos de dez/2024 registrados em jan/2025 (situação do KAM real, F0003 p.136)
e = inf[(inf.contrato.isin(['059/2001', '008/2022'])) & (inf.data_lancamento.str.startswith('2025-01'))].sample(150, random_state=1).index
antes = T.loc[e, 'data_documento'].copy()
T.loc[e, 'data_documento'] = [f'2024-12-{d:02d}' for d in rng.integers(2, 24, len(e))]; T.loc[e, 'erro'] = 'E01'
for i in e: LIN.append(dict(id_erro='E01', id_lancamento_ref=T.at[i, 'id_ref'], campo='data_documento', antes=antes[i], depois=T.at[i, 'data_documento'], valor_brl=T.at[i, 'valor_movimento_brl']))
reg('E01', 'Corte (exercício anterior)', 'Serviços executados em dez/2024 (data do documento) registrados como receita de 2025', 'Corte; ocorrência (resultado)', len(e), 0, int(T.loc[e, 'v'].sum()), 'data_documento')

# E02 – corte 2025 -> 2026: medições de dez/2025 lançadas só em jan/2026 (saem do arquivo de 2025 e vão para o de 2026)
cand = inf[(inf.contrato.isin(['059/2001', '006/2023', '012/2023'])) & (inf.data_lancamento.str.startswith('2025-12')) & (T.loc[inf.index, 'erro'] == '')]
cand = cand.loc[cand.index.difference(e)]
alvo = 7_200_000_00; sel = []; acc = 0
for i in cand.sample(frac=1, random_state=2).index:
    if acc >= alvo: break
    if T.at[i, 'v'] < 400_000_00: sel.append(i); acc += int(T.at[i, 'v'])
mov = T.loc[sel].copy(); mov['data_lancamento'] = [f'2026-01-{d:02d}' for d in rng.integers(5, 21, len(sel))]; mov['competencia'] = '2026-01'; mov['erro'] = 'E02'
for i in sel: LIN.append(dict(id_erro='E02', id_lancamento_ref=T.at[i, 'id_ref'], campo='data_lancamento (movida para o arquivo de 2026)', antes=T.at[i, 'data_lancamento'], depois=mov.at[i, 'data_lancamento'], valor_brl=T.at[i, 'valor_movimento_brl']))
T = T.drop(index=sel); J2 = pd.concat([J2, mov], ignore_index=True)
reg('E02', 'Corte (exercício seguinte)', 'Medições de serviços de dez/2025 registradas só em jan/2026', 'Integridade; corte', len(sel), -acc, -acc, 'data_lancamento')

inf = T[(T.tipo_movimento == 'RECEITA_INFRA') & (T.origem == 'AUTOMATICO') & (T.erro == '')]
# E03 – duplicidade: mesma medição (documento, fornecedor, valor) lançada duas vezes
d3 = inf[(inf.contrato.isin(['006/2023', '012/2023', '059/2001'])) & (inf.v.between(8_000_000, 40_000_000))].sample(35, random_state=3)
dup = d3.copy(); dup['data_lancamento'] = (pd.to_datetime(dup.data_lancamento) + pd.to_timedelta(rng.integers(2, 7, len(dup)), unit='D')).clip(upper=pd.Timestamp('2025-12-31')).dt.strftime('%Y-%m-%d')
dup['competencia'] = dup.data_lancamento.str[:7]; dup['erro'] = 'E03'; dup['id_ref'] = ''
for i, r in dup.iterrows(): LIN.append(dict(id_erro='E03', id_lancamento_ref=r.id_lancamento, campo='linha nova (duplicata do documento)', antes='', depois=r.id_documento, valor_brl=r.valor_movimento_brl))
T = pd.concat([T, dup], ignore_index=True)
reg('E03', 'Duplicidade', 'Mesma medição (documento, fornecedor e valor) lançada duas vezes', 'Ocorrência', len(dup), int(dup.v.sum()), int(dup.v.sum()), 'linha adicional')

# E04 – digitação: transposição de dígitos (aumentando o valor) e um zero a mais; custo do documento mantido
inf = T[(T.tipo_movimento == 'RECEITA_INFRA') & (T.origem == 'AUTOMATICO') & (T.erro == '')]
e4 = inf[inf.v.between(2_000_000, 30_000_000)].sample(60, random_state=4).index; ef4 = 0; n4 = 0
for i in e4:
    if n4 >= 19: break
    s = str(T.at[i, 'v'] // 100)
    if len(s) >= 4 and s[-3] > s[-4]:
        novo = int(s[:-4] + s[-3] + s[-4] + s[-2:]) * 100 + T.at[i, 'v'] % 100
        LIN.append(dict(id_erro='E04', id_lancamento_ref=T.at[i, 'id_ref'], campo='valor_movimento_brl', antes=T.at[i, 'valor_movimento_brl'], depois=reais([novo])[0], valor_brl=reais([novo - T.at[i, 'v']])[0]))
        ef4 += novo - T.at[i, 'v']; T.at[i, 'v'] = novo; T.at[i, 'erro'] = 'E04'; n4 += 1
iz = inf[(inf.contrato == '008/2022') & (inf.v.between(70_000_000, 95_000_000))].index[:1]
v0 = int(T.at[iz[0], 'v']); LIN.append(dict(id_erro='E04', id_lancamento_ref=T.at[iz[0], 'id_ref'], campo='valor_movimento_brl', antes=T.at[iz[0], 'valor_movimento_brl'], depois=reais([v0 * 10])[0], valor_brl=reais([v0 * 9])[0]))
T.at[iz[0], 'v'] = v0 * 10; T.at[iz[0], 'erro'] = 'E04'; ef4 += v0 * 9
reg('E04', 'Digitação', f'{n4} transposições de dígitos e 1 valor com um zero a mais (valor ≠ custo × (1 + margem))', 'Exatidão', n4 + 1, ef4, ef4, 'valor_movimento_brl')

# E05 – lançamentos manuais de fim de período sem documento, mesmo usuário lança e aprova (indício de burla de controles)
base5 = dict(seq_linha_documento='1', data_lancamento='2025-12-30', data_documento='', competencia='2025-12', componente='IMPL', tipo_movimento='AJUSTE_MANUAL', id_documento='',
             origem='MANUAL', usuario_sistema='U11', aprovador='U11', historico='Ajuste margem obra - complemento', natureza_dado='SINTETICO_DIDATICO', erro='E05', id_ref='')
e5 = pd.DataFrame([dict(base5, contrato='006/2023', entidade='ISA Energia Brasil (Projeto Serra Dourada)', grupo='Controladora', hora_lancamento='23:41', v=1_200_000_000),
                   dict(base5, contrato='012/2023', entidade='ISA Energia Brasil (Projeto Itatiaia)', grupo='Controladora', hora_lancamento='23:47', v=350_000_000)])
T = pd.concat([T, e5], ignore_index=True)
for _, r in e5.iterrows(): LIN.append(dict(id_erro='E05', id_lancamento_ref='', campo='linha nova', antes='', depois=f"{r.contrato} {r.hora_lancamento}", valor_brl=reais([r.v])[0]))
reg('E05', 'Lançamento manual sem suporte', 'Dois ajustes manuais em 30/12/2025 após 23h, valores redondos, sem documento, lançados e aprovados por U11', 'Ocorrência (burla de controles – NBC TA 240 it. 32(a))', 2, int(e5.v.sum()), int(e5.v.sum()), 'linhas novas')

# E06 – remuneração com taxa implícita errada (9,9% em vez de 6,9%) no contrato 046/2017, out–dez
i6 = T[(T.tipo_movimento == 'REMUNERACAO') & (T.contrato == '046/2017') & (T.competencia.isin(['2025-10', '2025-11', '2025-12']))].index; ef6 = 0
for i in i6:
    base = int(cent(pd.Series([T.at[i, 'base_calculo_brl']]))[0]); dlt = int(round(base * ((1.099) ** (1 / 12) - (1.069) ** (1 / 12))))
    LIN.append(dict(id_erro='E06', id_lancamento_ref=T.at[i, 'id_ref'], campo='valor_movimento_brl; taxa_implicita_aa', antes=T.at[i, 'valor_movimento_brl'], depois=reais([T.at[i, 'v'] + dlt])[0], valor_brl=reais([dlt])[0]))
    T.at[i, 'v'] += dlt; T.at[i, 'taxa_implicita_aa'] = '0.099'; T.at[i, 'erro'] = 'E06'; ef6 += dlt
reg('E06', 'Estimativa', 'Remuneração de out–dez/2025 do 046/2017 com taxa implícita de 9,9% em vez de 6,9%', 'Avaliação', len(i6), ef6, ef6, 'valor; taxa')

# E07 – gastos de manutenção corretiva (O&M) registrados como obra no 059/2001
v7 = rng.lognormal(0, 0.7, 60); v7 = np.floor(v7 / v7.sum() * 460_000_000).astype(np.int64); v7[0] += 460_000_000 - v7.sum()
meses = rng.integers(1, 13, 60)
e7 = pd.DataFrame(dict(id_documento=[f'MED-0592001-{9100000 + j * 37:07d}' for j in range(60)], seq_linha_documento='1', data_lancamento=[f'2025-{m:02d}-{d:02d}' for m, d in zip(meses, rng.integers(3, 27, 60))],
    contrato='059/2001', entidade='ISA Energia Brasil', grupo='Controladora', componente='IMPL', tipo_movimento='RECEITA_INFRA', id_obra_aneel='', id_modulo_aneel='', tipo_receita_aneel='',
    fornecedor_id=[f'F{x:05d}' for x in rng.integers(40, 120, 60)], tipo_custo='Manutenção corretiva', margem_construcao='0.035', origem='AUTOMATICO', usuario_sistema='INT_MEDICOES',
    aprovador='WF_MEDICAO', historico='Receita de infraestrutura – medição aprovada', natureza_dado='SINTETICO_DIDATICO', erro='E07', id_ref='', v=v7))
e7['data_documento'] = e7.data_lancamento; e7['competencia'] = e7.data_lancamento.str[:7]; e7['custo_documento_brl'] = reais(np.round(v7 / 1.035))
T = pd.concat([T, e7], ignore_index=True)
for _, r in e7.iterrows(): LIN.append(dict(id_erro='E07', id_lancamento_ref='', campo='linha nova', antes='', depois=r.id_documento, valor_brl=reais([r.v])[0]))
reg('E07', 'Classificação / ocorrência', 'Manutenção corretiva (O&M, custo do período) registrada como receita de infraestrutura e ativo contratual', 'Ocorrência; classificação (CPC 47)', 60, int(v7.sum()), int(v7.sum()), 'linhas novas')

# E08 – recebimentos aplicados ao contrato errado (027/2017 -> 018/2017), ago/2025
i8 = T[(T.tipo_movimento == 'RECEBIMENTO') & (T.contrato == '027/2017') & (T.componente == 'IMPL') & (T.competencia == '2025-07')].sort_values('v').index[:8]
for i in i8: LIN.append(dict(id_erro='E08', id_lancamento_ref=T.at[i, 'id_ref'], campo='contrato; entidade', antes='027/2017', depois='018/2017', valor_brl=T.at[i, 'valor_movimento_brl']))
T.loc[i8, 'contrato'] = '018/2017'; T.loc[i8, 'entidade'] = 'IE Itaúnas'; T.loc[i8, 'erro'] = 'E08'
reg('E08', 'Classificação', 'Recebimentos do 027/2017 (IE Itaquerê) aplicados ao 018/2017 (IE Itaúnas)', 'Classificação; existência por contrato', len(i8), 0, 0, 'contrato')

# E09 – perda esperada subavaliada: constituição reduzida em R$ 1,2 milhão
i9 = T[T.tipo_movimento == 'PERDA_ESPERADA'].sort_values('v').index[0]; antes9 = T.at[i9, 'valor_movimento_brl']
T.at[i9, 'v'] += 120_000_000; T.at[i9, 'erro'] = 'E09'
LIN.append(dict(id_erro='E09', id_lancamento_ref=T.at[i9, 'id_ref'], campo='valor_movimento_brl', antes=antes9, depois=reais([T.at[i9, 'v']])[0], valor_brl='1200000.00'))
reg('E09', 'Estimativa', 'Perda esperada sobre faturas de O&M inadimplentes constituída a menor em R$ 1,2 milhão', 'Avaliação', 1, 120_000_000, 120_000_000, 'valor')

# ---------------------------------------------------- gravar cenário de TESTE (ids renumerados em ordem cronológica)
T['valor_movimento_brl'] = reais(T.v)
T = T.sort_values(['data_lancamento', 'contrato', 'tipo_movimento', 'id_documento', 'seq_linha_documento'], kind='stable').reset_index(drop=True)
T['id_lancamento'] = [f'L25{n:08d}' for n in range(1, len(T) + 1)]
J2['valor_movimento_brl'] = reais(J2.v); J2 = J2.sort_values(['data_lancamento', 'contrato', 'id_documento'], kind='stable').reset_index(drop=True)
J2['id_lancamento'] = [f'L26{n:08d}' for n in range(1, len(J2) + 1)]
cols = list(R.columns)
T[cols].to_csv(D / 'SINTETICO_lancamentos_2025_TESTE.csv.gz', index=False, sep=';', encoding='utf-8', compression={'method': 'gzip', 'mtime': 0})
J2[cols].to_csv(D / 'SINTETICO_lancamentos_2026_jan_fev_TESTE.csv.gz', index=False, sep=';', encoding='utf-8', compression={'method': 'gzip', 'mtime': 0})
# saldos do TESTE: saldo = abertura + fluxos do TESTE; circulante da referência; E10 desloca R$ 60 milhões do não circulante para o circulante
fe = T.assign(ref=T.tipo_movimento.str.startswith('SALDO_ABERTURA')).groupby(['contrato', 'componente']).v.sum()
ST = SR.copy(); ST['s'] = cent(ST.saldo_brl); ST['c'] = cent(ST.parcela_circulante_brl)
m25 = ST.data_base == '2025-12-31'
ST.loc[m25, 's'] = [int(fe.get((c, cp), 0)) for c, cp in zip(ST.loc[m25, 'contrato'], ST.loc[m25, 'componente'])]
ST.loc[m25 & (ST.componente == 'OEM'), 'c'] = ST.loc[m25 & (ST.componente == 'OEM'), 's']   # O&M: prazo < 30 dias, integralmente circulante
i10 = ST[m25 & (ST.contrato == '046/2017') & (ST.componente == 'IMPL')].index[0]
LIN.append(dict(id_erro='E10', id_lancamento_ref='(tabela de saldos)', campo='parcela_circulante_brl', antes=reais([ST.at[i10, 'c']])[0], depois=reais([ST.at[i10, 'c'] + 6_000_000_000])[0], valor_brl='60000000.00'))
ST.at[i10, 'c'] += 6_000_000_000
reg('E10', 'Apresentação', 'R$ 60 milhões do 046/2017 realizáveis após 12 meses classificados como circulante', 'Classificação / apresentação', 1, 0, 0, 'parcela_circulante')
ST['saldo_brl'] = reais(ST.s); ST['parcela_circulante_brl'] = reais(ST.c); ST['parcela_nao_circulante_brl'] = reais(ST.s - ST.c)
ST[list(SR.columns)].to_csv(D / 'SINTETICO_saldos_TESTE.csv', index=False, sep=';', encoding='utf-8')
# ---------------------------------------------------- gabarito (lacrado)
LG = pd.DataFrame(LOG); LG.to_csv(G / 'REGISTRO_ERROS.csv', index=False, sep=';', encoding='utf-8')
LI = pd.DataFrame(LIN)
mapa = T[T.erro != ''][['id_ref', 'id_lancamento', 'erro', 'id_documento', 'valor_movimento_brl']].rename(columns={'id_lancamento': 'id_lancamento_TESTE'})
LI.to_csv(G / 'LINHAS_ALTERADAS.csv', index=False, sep=';', encoding='utf-8')
mapa.to_csv(G / 'MAPA_IDS_TESTE_COM_ERRO.csv', index=False, sep=';', encoding='utf-8')
print(f'Registro de erros gravado em gabarito_LACRADO/ ({len(LG)} registros; conteúdo não exibido para não vazar o gabarito)')
print('TESTE linhas 2025:', len(T), '| 2026:', len(J2))
