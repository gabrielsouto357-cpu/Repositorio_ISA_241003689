# Dicionário de dados – base sintética de Ativos da concessão (definitivo, Bloco 07)

> SINTÉTICO DIDÁTICO – não são dados internos da ISA Energia Brasil. Totais por grupo reproduzem as DFs publicadas (F0003); a abertura em linhas é simulada.

- Formato: CSV UTF-8, separador `;`, **ponto decimal**. Valores gravados como texto exato a partir de centavos inteiros. Lançamentos em gzip.
- Mudança em relação ao B06 (§4 previa vírgula decimal): o ponto evita conversão de localidade. Os valores não mudam.

## Lançamentos (fluxos) – 31 campos

| Campo | Tipo | Descrição | Real × sintético | Regra | % preench. |
|---|---|---|---|---|---|
| id_lancamento | texto(11) | Chave primária do lançamento (L25 = arquivo 2025; L26 = arquivo jan–fev/2026), numerada em ordem cronológica | Sintético | Única; sem vazios; padrão L25/L26 + 8 dígitos | 100.0% |
| id_documento | texto | Documento-suporte. Prefixos: MED medição; AVC aviso de crédito/fatura ONS; REC aviso de recebimento; REM memória de remuneração; MEMO reclassificação; PROV provisão/estorno; PCLD perda esperada; MARCO marco contratual; RTP/EFI/REH atos ANEEL; SALDO abertura | Sintético (atos ANEEL citados são reais) | Repete só entre linhas do mesmo documento; (id_documento, seq_linha_documento) única | 100.0% |
| seq_linha_documento | inteiro | Sequência da linha no documento. Recebimento: linha 1 = parcela de O&M; linhas 2+ = ativo contratual | Sintético | ≥ 1; chave natural com id_documento | 100.0% |
| data_lancamento | data AAAA-MM-DD | Data do registro contábil | Sintético | 01/01–31/12/2025 no arquivo 2025; 01/01–28/02/2026 no arquivo 2026 | 100.0% |
| hora_lancamento | hora HH:MM | Hora do registro; preenchida só em lançamentos manuais | Sintético | Vazia nos lotes automáticos e nos saldos; manual em horário comercial na referência | 0.1% |
| data_documento | data AAAA-MM-DD | Data do documento/evento econômico | Sintético | ≤ data_lancamento, exceto REMUNERACAO (cálculo no último dia do mês, lançado no último dia útil); 31/12/2024 só nos saldos de abertura | 100.0% |
| competencia | texto AAAA-MM | Mês a que o evento pertence | Sintético | Igual ao mês do lançamento, exceto RECEBIMENTO (mês da fatura paga) e saldos de abertura (2024-12) | 100.0% |
| entidade | texto | Entidade do grupo titular do contrato | Real (F0003 p.36) | Coerente com o contrato (cadastro REAL_contratos) | 100.0% |
| grupo | texto | Controladora ou Controlada | Real (F0003 p.36) | {Controladora, Controlada}; coerente com o contrato | 100.0% |
| contrato | texto | Contrato de concessão ANEEL | Real (F0003 p.36) | FK para os 28 contratos consolidados | 100.0% |
| componente | texto | Subconta de Ativos da concessão (nota 5.3) | Real (F0003 p.45) | {OEM, SE_FIN, SE_ECO, IMPL} | 100.0% |
| tipo_movimento | texto | Natureza do fluxo; ver aba Tipos_movimento | Linhas da nota 5.5 (F0003 p.47) | 13 valores do domínio (aba Tipos_movimento) | 100.0% |
| valor_movimento_brl | decimal R$, 2 casas, ponto decimal | FLUXO: + aumenta o ativo; − reduz. Σ de todas as linhas (com saldos de abertura) = saldo de 31/12/2025 | Sintético; totais por grupo reais | Texto numérico exato (sem notação científica); sinal coerente com o tipo | 100.0% |
| id_obra_aneel | texto | Obra (IdeObr) da Lista de Módulos ANEEL 2025-2026 | Real (F0242) | Vazio quando o módulo não tem obra no catálogo real (3.213 de 4.471 módulos) | 33.6% |
| id_modulo_aneel | texto | Módulo (IdeMdl) ANEEL da medição | Real (F0242) | Obrigatório em RECEITA_INFRA; FK ao catálogo; módulo do mesmo contrato | 44.9% |
| tipo_receita_aneel | texto | Tipo de receita do módulo | Real (F0242) | Domínio do catálogo (RBL, RBNI, RBNIA, RBSE, RCDM, RCDMA, RMEL, RPC, RPEC) | 44.9% |
| fornecedor_id | texto | Fornecedor do documento de custo | Sintético | F00001–F02500 (cadastro SINTETICO_cadastro_fornecedores); obrigatório em RECEITA_INFRA | 44.8% |
| tipo_custo | texto | Natureza do gasto de obra | Sintético | 7 categorias de obra; obrigatório em RECEITA_INFRA | 44.8% |
| custo_documento_brl | decimal R$ | Custo do documento, sem margem | Sintético | valor_movimento = custo × (1 + margem), arredondado ao centavo | 44.8% |
| margem_construcao | decimal (fração) | Margem de construção do contrato | Sintético (arbitrado; CPC 47) | Faixa observada 0,020–0,077 (premissa 2%–9%) | 44.8% |
| usuario_pagador_id | texto | Usuário do sistema de transmissão (faturamento ONS) | Sintético | AG0001–AG0480; obrigatório em RECEITA_OEM e RECEBIMENTO | 55.0% |
| tipo_usuario | texto | Categoria do usuário | Sintético (categorias reais) | {Distribuidora, Geradora, Consumidor livre, Exportador/Importador} | 55.0% |
| data_vencimento | data | Vencimento da fatura | Sintético | Dia 15 do mês seguinte; só RECEITA_OEM e RECEBIMENTO | 55.0% |
| dias_atraso | inteiro | Atraso do recebimento em dias | Sintético | ≥ 0; só RECEBIMENTO | 36.9% |
| taxa_implicita_aa | decimal (fração a.a.) | Taxa implícita do contrato usada na remuneração | Sintético dentro da faixa real 4,2%–9,9% (F0003 p.44) | Só REMUNERACAO do componente IMPL | 0.1% |
| base_calculo_brl | decimal R$ | ESTOQUE de referência (saldo médio) usado no cálculo da remuneração do mês – NÃO SOMAR | Sintético | Informativo; nunca entra em totais nem em conciliação | 0.1% |
| origem | texto | AUTOMATICO (interfaces), MANUAL (lançamento humano) ou SALDO (abertura) | Sintético | {AUTOMATICO, MANUAL, SALDO} | 100.0% |
| usuario_sistema | texto | Quem registrou: INT_* interface; SISTEMA; U01–U15 pessoas | Sintético | Manual: usuário pessoal | 100.0% |
| aprovador | texto | Aprovador: WF_* fluxo; SISTEMA; Uxx pessoa | Sintético | Manual: aprovador ≠ usuario_sistema (segregação) | 100.0% |
| historico | texto | Descrição do lançamento | Sintético | Texto livre padronizado por tipo | 100.0% |
| natureza_dado | texto | Marca obrigatória de dado sintético | Marca (F0002 §3) | Valor único SINTETICO_DIDATICO | 100.0% |

## Saldos (estoques) – 8 campos

| Campo | Tipo | Descrição | Regra |
|---|---|---|---|
| data_base | data | 31/12/2024 ou 31/12/2025 | Somar só dentro da mesma data_base |
| grupo | texto | Controladora ou Controlada | Coerente com o contrato |
| contrato | texto | Contrato (real, F0003 p.36) | FK |
| componente | texto | Subconta | {OEM, SE_FIN, SE_ECO, IMPL} |
| saldo_brl | decimal R$ | ESTOQUE na data-base = abertura + Σ fluxos do contrato/componente | Σ por data_base = balanço (F0003 p.23) |
| parcela_circulante_brl | decimal R$ | Parte realizável em até 12 meses (premissa: recebimentos dos 12 meses seguintes, calibrada) | Σ 2025 = 4.106.084 mil; O&M 100% circulante |
| parcela_nao_circulante_brl | decimal R$ | Parte realizável após 12 meses | circulante + não circulante = saldo; ≥ 0 |
| natureza_dado | texto | Marca obrigatória | SINTETICO_DIDATICO |

## Tipos de movimento

| Tipo | Significado | Sinal | Linha da nota 5.5 | Linhas REF |
|---|---|---|---|---|
| SALDO_ABERTURA | Saldo bruto em 31/12/2024 por contrato e componente | + | Saldo de abertura | 55 |
| SALDO_ABERTURA_PERDA_ESPERADA | Perda esperada acumulada em 31/12/2024 (redutora do O&M) | − | Saldo de abertura | 22 |
| RECEITA_INFRA | Item de medição de obra (custo + margem) | + | Receita de infraestrutura | 269.369 |
| PROVISAO_MEDICAO | Medição executada pendente de aprovação no fim do mês | + | Receita de infraestrutura | 72 |
| ESTORNO_PROVISAO | Estorno da provisão do mês anterior | − | Receita de infraestrutura | 66 |
| AJUSTE_MANUAL | Ajuste manual de obra (domínio previsto; sem ocorrência na referência) | ± | Receita de infraestrutura | 0 |
| RECLASSIFICACAO | Transferência entre módulos do mesmo contrato; cada documento soma zero | ± | — | 440 |
| EFICIENCIA | Ganho/perda de eficiência na implementação | ± | Ganho (perda) de eficiência | 5 |
| REMUNERACAO | Remuneração mensal do ativo contratual; inclui o ajuste RBSE da REH 3.466/2025 | ± | Remuneração dos ativos de concessão | 361 |
| RTP | Revisão tarifária periódica | ± | RTP | 5 |
| RECEITA_OEM | Fatura mensal de O&M por usuário e contrato | + | Receita de O&M | 108.577 |
| PERDA_ESPERADA | Constituição de perda esperada (CPC 48) | − | Perda esperada | 6 |
| RECEBIMENTO | Pagamento de fatura; linha 1 O&M. linhas 2+ ativo contratual | − | Recebimentos | 221.672 |