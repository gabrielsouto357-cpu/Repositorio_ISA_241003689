---
title: "Modelo uniforme de papel de trabalho (PT)"
subtitle: "Dossiê acadêmico ISA Energia Brasil 2025 – matrícula 241003689 – versão 1.0 do modelo (B03, 19/10/2026)"
lang: pt-BR
---

# 1. Finalidade e fontes de forma

Este modelo padroniza todos os papéis do dossiê. Ele atende à estrutura mínima do enunciado (F0002, p.1–2, item 4) e às exigências de documentação da NBC TA 230, itens 8 e 9 (F0001, p.133). Foi construído **a partir da forma** de quatro modelos públicos (ver `00_Controle/REFERENCIAS_MODELOS.xlsx`), sem reaproveitar saldos, conclusões ou fatos dos casos ilustrativos:

- **Matriz "teste × avaliação × evidência/PT ref. × observações" e conclusão geral:** CGU, Modelo de Papel de Trabalho de Análise (F0281, aba "PT Análise", células A1–K6).
- **Elementos essenciais e numeração PT principal/subsidiário:** CGU, Orientação Prática – Serviços de Auditoria, nov/2022 (F0282). Elementos na p.72; Figura 3 (padrão "PT1.1-0") na p.73; referenciação nas p.74–75.
- **Colunas "afirmações / executado por / ref. PT / comentários":** programa de auditoria do Guia IFAC, Volume II, 4ª ed., 2018 (F0283, p. física 210 = p. impressa 203).
- **Lista de verificação de conclusão do arquivo:** Guia IFAC 4ª ed. (F0283, p. física 215–217); tradução CFC, 2ª ed., out/2010 (F0280, p.284–285, quadro 18.1-1).

Esses materiais não são normas. A CGU trata de auditoria interna governamental; os guias IFAC/CFC são anteriores às NBC TA 220 (R3), 315 (R2), 540 (R2) e 600 (R2). As NBC TA aplicáveis a 2025 prevalecem (MAPA_NORMATIVO; decisão D-002).

# 2. Campos obrigatórios de cada PT

| # | Campo | Conteúdo exigido | Base |
|---|---|---|---|
| 1 | Código e título | "PT 320 – Materialidade". Subsidiários: PT 320.1, PT 320.2… | Enunciado item 5; CGU p.73 (adaptado) |
| 2 | Norma e itens utilizados | Norma com revisão, itens e página física no F0001, mais a situação da conferência com o texto oficial (D-002) | Enunciado item 4; F0002 p.3 ("versão consultada") |
| 3 | Objetivo e objeto | Conta, processo ou divulgação examinada, com perímetro (consolidado/individual/componente) e período | Enunciado item 4 |
| 4 | Afirmações e riscos | Tabela afirmação × risco, com ligação à MATRIZ_RISCOS_RESPOSTAS | Enunciado item 4 |
| 5 | População, fontes e seleção | IDs Fxxxx/WEB-xxx/DR-xx com página e critério de seleção | Enunciado item 4; NBC TA 230 item 9(a) |
| 6 | Procedimentos | Tabela com **uma modalidade por procedimento** | Enunciado itens 2 e 4 |
| 7 | Evidências e referências cruzadas | Remissões padronizadas (seção 4) | Enunciado item 4; CGU p.74–75 |
| 8 | Resultados e exceções | Separando fato documentado, hipótese e resultado sintético | Prompt mestre, controle 7 |
| 9 | Conclusão | Somente sobre o que foi feito; sem opinião profissional | Enunciado item 6 |
| 10 | Limitações | Acesso, fontes públicas, dados sintéticos e versões de norma | Enunciado item 6 |
| 11 | Requisito × orientação × julgamento | Distingue o que a norma exige, o que é material explicativo e o que é escolha do preparador | Prompt mestre |
| 12 | Preparador e data | "Preparado por: matrícula 241003689 em AAAA-MM-DD (execução assistida por IA)" | Enunciado item 4; NBC TA 230 item 9(b) |
| 13 | Revisão | "Revisão humana: ______ (em branco)" e "Revisão automatizada: ID no REGISTRO_REVISAO". Sem assinatura ou revisão de terceiros simulada | Enunciado item 4; NBC TA 230 item 9(c) |
| 14 | Versão e estado | v0.x rascunho, v1.0 concluído pelo preparador; estado no índice do PT 230 | Escolha do projeto (PT 230) |

# 3. Modalidades por procedimento (enunciado, item 2)

| Sigla | Modalidade | Quando usar |
|---|---|---|
| **[RP]** | Realizado com evidência pública | Executado com documentos e informações efetivamente disponíveis (CVM, B3, RI) |
| **[PA]** | Planejado por falta de acesso | Detalhado, mas não executado por depender de informação interna, confirmação, entrevista, inspeção ou sistema |
| **[SD]** | Simulado para fins didáticos | Executado sobre dados sintéticos, identificados e separados dos reais |

Um PT pode combinar modalidades, desde que cada procedimento tenha a sua (prompt mestre, controle 5).

# 4. Referências cruzadas (por ID)

| Formato | Significado | Exemplo |
|---|---|---|
| `F0003 p.23` | Fonte do inventário, página **física** do PDF; se a página impressa for diferente, `p.326 (impr. 322)` | `F0053 p.326 (impr. 322)` |
| `WEB-EXEMPLO-007` | Consulta web registrada em FONTES_USADAS, sem arquivo baixado | `WEB-EXEMPLO-006` |
| `DR:arquivo!aba!célula` | Dado real em planilha do projeto | `DR:DADOS_REAIS_DF_2025_2024!Conc_Cruzadas!X32` |
| `→ PT 320 §6` | Remissão a outro papel e seção | `→ PT 230 §3` |
| `NBC TA 230 it. 8 (F0001 p.133)` | Item normativo e página no consolidado | — |
| `D-007`, `P12`, `RV-B02-03` | Decisão, pendência ou registro de revisão | — |

# 5. Legenda de marcações

| Marca | Código | Significado |
|---|---|---|
| ✓ | C | Conferido com o documento-fonte (valor, data ou texto idêntico) |
| Σ | S | Soma ou recálculo conferido |
| ⇄ | X | Cruzado com fonte independente (por exemplo, PDF × CVM) |
| ↔ | R | Referência cruzada a outro PT ou planilha |
| ⚠ | E | Exceção ou diferença, explicada no próprio PT |
| ◐ | L | Limitação: evidência indisponível ou parcial |
| ◇ | H | Hipótese ou julgamento do preparador (não é fato documentado) |
| ▣ | D | Dado ou documento simulado: base sintética ou minuta didática não enviada |

Use o código em letra quando o símbolo não for exibido; por exemplo, "47.201.372 [C][X]".

# 6. Esqueleto a copiar

```
PT [código] – [título]                                   Versão: v0.1 | Estado: em elaboração
Norma e itens: [NBC TA xxx (Rn), itens …; F0001 p.…; texto oficial CFC: conferido/não acessível]
Entidade/período/perímetro: ISA Energia Brasil S.A. – exercício 2025 – [consolidado/individual/componente]

1. Objetivo e objeto
2. Afirmações relevantes e riscos            (tabela)
3. População, fontes e critérios de seleção
4. Procedimentos                              (tabela: nº | procedimento | modalidade | norma/item | evidência | resultado | marca)
5. Evidências e referências cruzadas
6. Resultados e exceções                      (fato / hipótese / sintético)
7. Conclusão
8. Limitações
9. Requisito × orientação × julgamento adotado
Preparado por: matrícula 241003689 em AAAA-MM-DD (execução assistida por IA)
Revisão humana: ____________________ (em branco)   Revisão automatizada: RV-…
```
