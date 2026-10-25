# PG-REC – Programa de auditoria: Receitas

**Versão:** v1.0 · **Estado:** programa de planejamento, com execução posterior parcial indicada nos papéis responsáveis. A presença da etapa neste programa não comprova sua execução. Aguarda revisão humana.
**Norma e itens:** NBC TA 330 (R1), it. 6–7, 18, 20–21 (F0001 p.381–384); NBC TA 300 (R1), it. 9 (p.240). Materialidade: MG 139.000 / ME 90.000 / CT 7.000 (D-014).
**Entidade / período / perímetro:** ISA Energia Brasil – 2025 – consolidado (D-007)

## Riscos cobertos (PT 315)
| Risco | Conta | Afirmação | RI | Significativo | Fonte |
|---|---|---|---|---|---|
| R02 | Receita de infraestrutura e custos de construção | Ocorrência; corte | Alto (ext. sup.) | Sim | F0003 p.25, 136 |
| R03 | Remuneração dos ativos da concessão | Exatidão, ocorrência, corte e integridade | Alto | Sim (V12-01) | F0003 p.25, 136; PT 240/330 |
| R04 | Receitas de RTP | Ocorrência; exatidão | Moderado | Não | F0003 p.12, 25 |

## Fundamento da extensão e da aplicabilidade
Extensão **ampla**. A receita de 9.411.153 é 68× a MG, e R02/R03 são riscos significativos, com fraude presumida (PT 240 §2.1) e deficiência de controle relatada (F0003 p.136). Abordagem só substantiva, com testes de detalhes, porque risco significativo exige procedimento específico e a abordagem não usa controles (NBC TA 330 it. 21, F0001 p.384).

## Procedimentos
| ID · risco · afirmação | Procedimento | Natureza · época | Extensão · população | Critério de exceção · evidência esperada | Modalidade · papel |
|---|---|---|---|---|---|
| REC-01 · R02 · Ocorrência | Conferir atributos sintéticos de suporte, vínculo de obra, recálculo, datas e aprovação (TD-01/MUS); não inspeciona documentos autênticos. | Teste de detalhes · Final | Triagem de 269.265 itens positivos; excluir 302 específicos; examinar 1 item ≥ intervalo J e selecionar 710 por MUS no restante (PT 530). · Débitos positivos de infraestrutura de 2025, base TESTE B07 (D-019–D-021); negativos/estornos tratados à parte. | Falhas nos atributos A1–A5 e regras TD-01; projeção restrita aos atributos sintéticos testados. · Campos da base, cadastros e vínculos sintéticos; não são medições/contratos originais. | [SD] · PT 530 / PT 500 |
| REC-02 · R02 · Corte | Conferir documentos anteriores a 2025 em débitos positivos de infraestrutura de 2025 (R5) e receitas de jan–fev/2026 com documento até 31/12/2025 (TD-03). | Teste de detalhes · Final | 100% das populações descritas, sem filtro por CT; exame dos estornos de provisões em separado. · P1 de 2025 (R5) e RECEITA_INFRA de jan–fev/2026 com data de documento preenchida (TD-03), base TESTE. | Competência diferente do período de registro = exceção · Datas da medição e do lançamento | [SD] · PT 530 |
| REC-03 · R02 · Corte | Inspecionar medições de obra posteriores a 31/12 (dados reais) | Inspeção · Final | Contratos com medição ≥ ME · Medições jan–fev/2026 | Medição de 2025 registrada em 2026 · Boletins de medição | [PA] · PT 560 |
| REC-04 · R03 · Exatidão, ocorrência, corte e integridade | Análise global pública como planejamento; testar detalhes da remuneração por contrato com termos autênticos, principal, taxa, índice e período, rastreamento ao suporte, integridade dos dados e autorização, incluindo burla | Analítico de planejamento [RP]; teste de detalhes [PA] · Final | Análise global das notas; seleção e extensão dos detalhes a definir com população real e materialidade, sem amostra fictícia | Divergência contratual, dado incompleto, corte ou suporte ausente exige investigação; expectativa global não tem precisão substantiva demonstrada · Contratos, suportes e razão reais ainda não obtidos | [RP]/[PA] · PT 520/540/500; TD-05 sintético não substitui contrato |
| REC-05 · R04 · Ocorrência; exatidão | Conciliar a receita de RTP de 159.463 com os atos da ANEEL (Despacho 1.228/25; REH 3.470 e 3.475) | Inspeção / recálculo · Final | 100% dos atos · Atos de 2025 citados no F0003 p.12 | Valor sem ato correspondente · Atos ANEEL (não obtidos: P08, P11) | [PA] · PT 540 / PT 250 |
| REC-06 · R02 · Apresentação | Conciliar a abertura da receita (nota 16) com a DRE e com o KAM (6.330.048) | Recálculo · Final | 100% · Nota 16 e DRE (dados reais) | Diferença > CT · F0003 p.25, 136, nota 16 | [RP] · PT 500 |

## Resultado
A ser preenchido no papel responsável. **Registro histórico em 20/10/2026.** Estado atual por objetivo nos PT 330/500; a ampliação REC-04 de 22/10/2026 é planejamento, sem execução real.

Preparado por: matrícula 241003689 em 2026-10-20 (execução assistida por IA)
Revisão humana: ____________________ (em branco) · Revisão automatizada: RV-B04-02

Atualização B12: o estado de execução por objetivo prevalece nos PT 330, 450, 500, 501–600 e na matriz de respostas. Modalidade [SD] não fornece evidência sobre o saldo real. Revisão automatizada RV-B12-01, sem assinatura de terceiro.

R03 passou a significativo, mantido RI Alto e sem alterar saldos ou escores. A presunção de fraude na remuneração não é refutada. REC-04 mantém a análise global pública [RP] somente como planejamento e inclui teste de detalhes por contrato [PA]: obter termos autênticos, conferir principal, taxa, índice e período, recalcular remuneração, rastrear aos suportes e testar integridade dos dados, ocorrência, corte e autorização, considerando burla. Seleção e extensão dependerão da população real e do risco/materialidade; não se inventa tamanho amostral. Esse teste não foi executado; TD-05 sintético não comprova taxa contratual independente. Atende ao desenho requerido pela NBC TA 330.21, sem alegar evidência real suficiente.

Atualização RV23B em 23/10/2026: coerência documental revista; dados, parâmetros e resultados históricos preservados. Revisão automatizada, sem assinatura de terceiro.
