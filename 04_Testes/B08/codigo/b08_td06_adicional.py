# -*- coding: utf-8 -*-
"""Verificação ADICIONAL da exceção do TD-06 (definida APÓS o resultado do TD-06; não estava no desenho congelado – 530 it. 12 e A17).
Compara o circulante de 31/12/2025 com os recebimentos de jan–fev/2026 anualizados (× 6), por contrato e componente.
Lê só arquivos permitidos do cenário TESTE."""
import json
from pathlib import Path
import numpy as np, pandas as pd
B8 = Path(__file__).resolve().parent.parent; P11 = B8.parent.parent; BASE = P11 / '03_Base_sintetica/base_B07/dados_sinteticos'
J6 = pd.read_csv(BASE / 'SINTETICO_lancamentos_2026_jan_fev_TESTE.csv.gz', sep=';', dtype=str, keep_default_na=False)
S = pd.read_csv(BASE / 'SINTETICO_saldos_TESTE.csv', sep=';', dtype=str, keep_default_na=False)
rec = J6[J6.tipo_movimento == 'RECEBIMENTO'].assign(v=lambda d: -d.valor_movimento_brl.astype(float)).groupby(['contrato', 'componente']).v.sum()
s5 = S[S.data_base == '2025-12-31'].assign(c=lambda d: d.parcela_circulante_brl.astype(float), s=lambda d: d.saldo_brl.astype(float)).set_index(['contrato', 'componente'])
t = s5[['s', 'c']].join(rec.rename('receb_jan_fev'), how='left').fillna(0)
t['receb_anualizado'] = t.receb_jan_fev * 6; t['dif'] = t.c - t.receb_anualizado; t['dif_rel'] = np.where(t.receb_anualizado > 0, t.dif / t.receb_anualizado, np.nan)
t = t[t.componente if False else t.index.get_level_values(1) != 'OEM'] if False else t
t.reset_index().to_csv(B8 / 'resultados/TD06_ADICIONAL_RECEBIMENTOS_2026.csv', sep=';', index=False)
print(t.sort_values('dif_rel', key=lambda x: -x.abs()).head(12).to_string())
print(t.loc[('059/2001', 'SE_FIN')])
