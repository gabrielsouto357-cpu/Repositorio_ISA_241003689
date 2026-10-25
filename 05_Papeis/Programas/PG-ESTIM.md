# PG-ESTIM – Programa de auditoria: Estimativas

**Versão:** v1.0 · **Estado:** programa de planejamento, com execução posterior parcial indicada nos papéis responsáveis. A presença da etapa neste programa não comprova sua execução. Aguarda revisão humana.
**Norma e itens:** NBC TA 330 (R1), it. 6–7, 18, 20–21 (F0001 p.381–384); NBC TA 300 (R1), it. 9 (p.240). Materialidade: MG 139.000 / ME 90.000 / CT 7.000 (D-014).
**Entidade / período / perímetro:** ISA Energia Brasil – 2025 – consolidado (D-007)

## Riscos cobertos (PT 315)
| Risco | Conta | Afirmação | RI | Significativo | Fonte |
|---|---|---|---|---|---|
| R01 | Ativos da concessão – mensuração | Avaliação | Alto (ext. sup.) | Sim | F0003 p.39, 44–45, 136 |
| R05 | Valores a receber – SEFAZ (Lei 4.819/58) | Avaliação; existência | Alto (ext. sup.) | Sim | F0003 p.69–72, 135 |
| R07 | Tributos diferidos | Exatidão; avaliação | Moderado | Não | F0003 p.24, nota 8 |
| R09 | Provisões e contingências | Integridade; avaliação | Moderado | Não | F0003 p.12, 24, 86 |
| R17 | Divulgação de sensibilidade do ativo contratual | Divulgação | Alto (D-026) | Não | F0003 p.39, 44–45 |

## Fundamento da extensão e da aplicabilidade
Extensão **ampla**. Dois riscos significativos (R01: 36.431.298, 262× a MG; R05: 2.760.806, 20× a MG) com incerteza e subjetividade elevadas (F0003 p.39, p.135–136). Os procedimentos detalhados ficam no PT 540.

## Procedimentos
| ID · risco · afirmação | Procedimento | Natureza · época | Extensão · população | Critério de exceção · evidência esperada | Modalidade · papel |
|---|---|---|---|---|---|
| EST-01 · R01 · Avaliação | Entender o modelo e as premissas (taxas implícitas de 4,2% a 9,9%, margens, RBSE) e compará-las com 2024 (revisão retrospectiva) | Indagação / análise · Final | Todas as premissas divulgadas · Notas 5 de 2024 e de 2025 | Mudança de premissa sem justificativa = indício de viés · F0003 p.39, 44–45; F0011 nota 5 | [RP] · PT 540 |
| EST-02 · R01 · Avaliação; exatidão | Recalcular a consistência interna da remuneração pela taxa/fator modal por contrato e componente (TD-05); não valida o fluxo contratual independente. | Recálculo · Final | 100% das linhas REMUNERACAO com base_calculo_brl preenchida; sem seleção por ME. · Contratos da base sintética | Taxa diferente da modal ou diferença superior à tolerância monetária de PARAMETROS_B08.json; avaliação agregada no PT 450. · Campos sintéticos de base, valor e taxa; fator modal derivado da própria população. | [SD] · PT 530 / PT 540 |
| EST-03 · R17 · Divulgação | Avaliar a divulgação de premissas e da sensibilidade (CPC 47 / ICPC 01) | Inspeção · Final | 100% da nota 5 · Nota 5 (dados reais) | Ausência de informação exigida · F0003 nota 5 | [RP] · PT 540 |
| EST-04 · R05 · Avaliação; existência | Analisar a movimentação do recebível (2.564.527 → 2.760.806) e a perda esperada constante de 516.255; avaliar a ênfase | Recálculo / análise · Final | 100% · Nota 9.2 | Movimento sem explicação; perda não reavaliada · F0003 p.69–72, 135 | [RP] · PT 540 |
| EST-05 · R05 · Avaliação | Obter a carta dos advogados sobre os processos da Lei 4.819/58 (minuta não enviada) | Confirmação · Final | Processos do recebível · Processos da nota 9 | Avaliação divergente da administração · Resposta do advogado | [PA] · PT 501 / PT 505 |
| EST-06 · R07 · Exatidão | Recálculo analítico de IR/CS diferidos (alíquota × diferenças temporárias) e de PIS/COFINS diferidos sobre o ativo contratual | Analítico substantivo · Final | Expectativa global; limiar = ME · Notas 8 e 21 | Diferença > ME · F0003 notas 8 e 21 | [RP] · PT 520 |
| EST-07 · R09 · Integridade; avaliação | Ler a nota 14, os eventos subsequentes e as atas; carta de advogados | Inspeção / confirmação · Final | Processos ≥ CT · Nota 14; F0056–F0074 | Processo provável não provisionado · F0003 p.86; atas | [RP]/[PA] · PT 501 / PT 560 |

## Resultado
A ser preenchido no papel responsável. **Nada executado até 20/10/2026.**

Preparado por: matrícula 241003689 em 2026-10-20 (execução assistida por IA)
Revisão humana: ____________________ (em branco) · Revisão automatizada: RV-B04-02

Atualização B12: o estado de execução por objetivo prevalece nos PT 330, 450, 500, 501–600 e na matriz de respostas. Modalidade [SD] não fornece evidência sobre o saldo real. Revisão automatizada RV-B12-01, sem assinatura de terceiro.

Atualização RV23B em 23/10/2026: coerência documental revista; dados, parâmetros e resultados históricos preservados. Revisão automatizada, sem assinatura de terceiro.
