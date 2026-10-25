---
title: "PT EX – Exemplo preenchido do modelo: conferência do ativo total consolidado (PDF × CVM)"
subtitle: "Exemplo de FORMA com informação pública verificada (Blocos 01–02). Será incorporado ao PT 500 como subsidiário PT 500.1."
lang: pt-BR
---

**Versão:** v1.0 · **Estado:** concluído pelo preparador; revisão humana pendente
**Norma e itens:** NBC TA 500 (R1), item 9 (avaliação de informações da entidade usadas como evidência), F0001 p.449, e material explicativo sobre relevância e confiabilidade, F0001 p.458–459. Nessas páginas o F0001 traz duas numerações de itens A (original e alterada); por isso a citação é por página. NBC TA 230 (R1), itens 8 e 9, F0001 p.133. Texto oficial compilado do CFC: não acessível ao leitor automático em 19/10/2026 (P03), por isso a citação segue o F0001. Os itens da NBC TA 500 ainda serão conferidos no PT 500.
**Entidade / período / perímetro:** ISA Energia Brasil S.A. – 31/12/2025 e 31/12/2024 – **consolidado** (D-001, D-007)

## 1. Objetivo e objeto
Verificar se o total do ativo consolidado apresentado no PDF das DFs de 2025 corresponde ao dado estruturado entregue à CVM, para a versão, a data e a escala corretas. O objeto é o **total do ativo consolidado** e o comparativo de 2024.

## 2. Afirmações relevantes e riscos
| Afirmação | Risco considerado | Referência |
|---|---|---|
| Apresentação (consistência entre versões publicadas) | Usar versão, escala ou exercício errados na base do trabalho | Controles de dados 1–2 do prompt mestre |
| Exatidão da transcrição | Erro de extração ou de digitação ao levar o valor para os papéis | NBC TA 500 it. 9(a) |

## 3. População, fontes e critérios de seleção
- **F0003**, DF 2025, p.23, coluna "Consolidado", linha "Total do ativo". Escala "Em milhares de reais" no cabeçalho em imagem.
- **F0037**, extrato `ISA_dfp_cia_aberta_BPA_con_2025.csv`, linhas 2–3. **F0018**, ZIP oficial da CVM, `dfp_cia_aberta_BPA_con_2025.csv`, linhas 8180–8181.
- **F0011**, DF 2024, p.22 (comparativo).
- Critério de seleção: item único (total), escolhido por ser o valor de referência indicado pelo aluno. Não há amostragem.

## 4. Procedimentos
| Nº | Procedimento | Modalidade | Norma/item | Evidência | Resultado | Marca |
|---|---|---|---|---|---|---|
| 1 | Ler o total do ativo consolidado no PDF e conferir a escala pela imagem da página | [RP] | NBC TA 500 it. 9(a) | F0003 p.23; `01_Dados_reais/EVID_F0003_p23_BP.png` | 47.201.372 (2025); 43.304.632 (2024) | [C] |
| 2 | Filtrar na CVM: CNPJ 02.998.611/0001-04, CD_CONTA = 1, grupo "DF Consolidado – BP Ativo", DT_FIM_EXERC 2025-12-31 (ÚLTIMO) e 2024-12-31 (PENÚLTIMO), VERSAO = 1 | [RP] | NBC TA 500 it. 9(a) | F0037 linhas 3 e 2 | 47.201.372; 43.304.632; escala MIL | [X] |
| 3 | Reextrair do ZIP oficial e comparar com o extrato | [RP] | NBC TA 500, material explicativo sobre confiabilidade (F0001 p.459) | F0018 linhas 8181 e 8180; script `b01_verificacoes.py` | Extrato idêntico ao ZIP (142 linhas) | [X] |
| 4 | Comparar o comparativo de 2024 com a DF 2024 publicada | [RP] | NBC TA 510 (será aprofundado no PT 510) | F0011 p.22 | 43.304.632 nas duas | [C] |
| 5 | Calcular as diferenças por fórmula | [RP] | — | `DR:CONF_B01_ATIVO_TOTAL_PDF_CVM!Conferencia!B11:C15` | 0 em todas | [S] |

## 5. Evidências e referências cruzadas
`DR:CONF_B01_ATIVO_TOTAL_PDF_CVM`; `DR:DADOS_REAIS_DF_2025_2024!Conc_PDF_CVM` (extensão para 552 conferências); → PT 500 (incorporação como PT 500.1); → PT 510 (saldos iniciais); RV-B01-08.

## 6. Resultados e exceções
- **Fato documentado:** valores idênticos no PDF, no extrato e no ZIP da CVM, com versão 1 e escala MIL. Nenhuma exceção.
- **Hipóteses:** nenhuma.
- **Resultados sintéticos:** não se aplica (só dados reais).

## 7. Conclusão
Com base nos procedimentos 1 a 5, o total do ativo consolidado usado no dossiê (R$ 47.201.372 mil em 31/12/2025) corresponde ao publicado em PDF e ao entregue à CVM (DFP versão 1). A conclusão vale só para esse total; não é opinião sobre as DFs.

## 8. Limitações
O procedimento mostra consistência entre duas publicações da própria companhia. **Não** prova a existência ou a valorização dos ativos, porque ambas as fontes são preparadas pela entidade.

## 9. Requisito × orientação × julgamento adotado
- **Requisito:** avaliar a confiabilidade da informação usada como evidência (NBC TA 500 it. 9) e registrar itens testados, preparador e revisão (NBC TA 230 it. 9).
- **Orientação:** materiais explicativos da NBC TA 500 sobre fontes externas e internas.
- **Julgamento adotado:** tratar o PDF como referência e a CVM como conferência (D-008).

Preparado por: matrícula 241003689 em 2026-10-19 (execução assistida por IA)
Revisão humana: ____________________ (em branco) · Revisão automatizada: RV-B01-08
