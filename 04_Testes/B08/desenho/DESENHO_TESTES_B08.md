# Desenho dos testes do Bloco 08: amostragem e testes de detalhes na base sintética

**Estado:** desenho **congelado antes da execução**. O hash SHA-256 e o horário estão em `controle/CONGELAMENTO_DESENHO.json`.
- Parâmetros: `PARAMETROS_B08.json`.
- Preparado por: matrícula 241003689 (execução assistida por IA), 21/10/2026.
- Revisão humana: ____________ (em branco).

**Aviso de independência.** A mesma IA desenhou a base, os erros inseridos (B06/B07) e estes testes. O exercício **não** é um experimento cego independente. O que garante a separação é só o procedimento: o código de detecção não lê o gabarito, a referência, o gerador nem os rótulos, e o desenho fica congelado antes da execução. Mesmo assim, as regras podem refletir conhecimento do desenho. O resultado mede o **método no ambiente sintético**, não a eficácia em dados reais.

## 1. Normas e o que é exigência × julgamento
| Tema | Exigência normativa | Julgamento (didático) neste desenho |
|---|---|---|
| Definição e finalidade da amostra | 530 it. 6 e A4–A9 (p.535–538): considerar a finalidade e a população; A5 exige obter evidência de que a população está completa (500 it. 8) | População = débitos de receita de infraestrutura (abaixo) |
| Tamanho | 530 it. 7 e A10–A11: reduzir o risco de amostragem a nível aceitável; fórmula ou julgamento | Fórmula MUS; 95% de confiança; fator de expansão 1,6; erro esperado de 9.000 |
| Seleção | 530 it. 8, A12–A13 e Apêndice 4: cada unidade com a mesma chance | Seleção sistemática por unidade monetária, com início aleatório e semente |
| Execução, itens sem evidência | 530 it. 9–11: item sem evidência = distorção | Lançamento sem documento = distorção do valor integral |
| Natureza e causa; anomalia | 530 it. 12–13 e A17: anomalia exige alto grau de certeza | Nenhuma anomalia é presumida |
| Projeção e avaliação | 530 it. 14–15, A18–A23 e Apêndice 1 §3–4 (estratos projetados separadamente) | Método de Poisson / Stringer (fatores exatos) |
| Meios de seleção | 500 it. 10 e A63–A67 (p.449, 467–468): 100%, itens específicos ou amostragem. **Itens específicos não são amostragem e não se projetam** (A66) | Estágio 1 = 100% e itens específicos; Estágio 2 = amostragem do restante |
| Risco significativo | 330 it. 21 (p.384): só substantivos ⇒ incluir testes de detalhes. 330 it. 20(b): examinar lançamentos | Sem confiança em controles (PT 330 proc. 3) |
| Acumulação e avaliação | 450 it. 5–6, 10–11 e A6–A8 (p.429–434): distorções factuais, de julgamento e projetadas; reavaliar o plano se o total se aproxima da materialidade | Comparar com CT 7.000, ME 90.000 e MG 139.000 |

## 2. Testes de controles × testes de detalhes; estatística × não estatística
- **Testes de controles: não serão feitos.** A abordagem do PT 330 é só substantiva (proc. 3), sem confiança nos controles. Por isso não há taxa tolerável de desvio nem amostragem de atributos.
  - Se houvesse confiança, o teste seria de atributos. Exemplo: aprovação independente de lançamentos manuais, com taxa tolerável de 5%, taxa esperada de 0% e 95% de confiança, o que daria n ≈ 3,0 / 0,05 = 60 (Poisson). Isso é **só ilustração; não será executado**.
  - O teste de lançamentos manuais do Estágio 1 é **teste de detalhes** (330 it. 20(b); 240 it. 32(a)). Não é teste de controle.
- **Amostragem estatística:** só o Estágio 2 (MUS). Tem os dois atributos de 530 it. 5: (a) seleção aleatória, porque o início sistemático é aleatório e cada unidade monetária tem probabilidade conhecida, n/VC; (b) avaliação pela teoria das probabilidades (Poisson), com mensuração do risco de amostragem.
- **Amostragem não estatística:** não será usada.
- **100% e itens específicos:** não são amostragem e não têm risco de amostragem. O risco não resultante da amostragem continua (530 A1).

## 3. Testes definidos antes da execução
População e completude: cenário TESTE, arquivos de 2025 e de jan–fev/2026, e tabela de saldos.

| ID | Risco / afirmação (PT 315/330) | População | Meio de seleção | Exceção (critério fixado agora) | Quantificação da distorção |
|---|---|---|---|---|---|
| TD-01 | R02 ocorrência e exatidão (REC-01) | Débitos de receita de infraestrutura: RECEITA_INFRA, PROVISAO_MEDICAO e AJUSTE_MANUAL com valor > 0 | **100%: triagem por regras** (500 A64, cálculo repetitivo) que gera **itens específicos** (A65) | R1 a R6 (abaixo) | Ver §4 |
| TD-02 | R16 lançamentos (GER-02; 240 it. 32(a)) | Todos os lançamentos manuais de 2025 e de jan/2026 até 15/01 | 100% | Manual **e** pelo menos um destes: sem documento; mesmo usuário lança e aprova; fora de 07h–20h; usuário com ≤ 4 lançamentos no ano; na janela de 26/12 a 15/01 com valor ≥ CT | Sem suporte = valor integral |
| TD-03 | R02 corte, exercício seguinte (REC-02) | Arquivo jan–fev/2026 | 100% | RECEITA_INFRA lançada em 2026 com data do documento ≤ 31/12/2025 (serviço de 2025 não registrado em 2025). Ajustes de provisão de dez/2025 (ESTORNO_PROVISAO) analisados à parte | −valor (subavaliação) |
| TD-04 | Classificação por contrato (recebimentos) | Documentos de recebimento de 2025 | 100% | Linhas de um mesmo documento em contratos diferentes do da linha 1 | Valor reclassificável entre contratos (efeito 0 no total) |
| TD-05 | R01 avaliação e exatidão (EST-02) | Remuneração de 2025 (28 contratos × 12 meses + SE) | 100%: recálculo | Taxa implícita diferente da taxa modal do contrato no ano, ou valor ≠ base × fator modal do contrato (tolerância de R$ 1,00) | Valor − base × fator modal |
| TD-06 | Apresentação: circulante × não circulante (PT 500) | Tabela de saldos 2024/2025 | 100% | O&M com não circulante ≠ 0; ou participação do circulante que varia > 10 p.p. contra 2024 **e** diferença ≥ CT | Reclassificação de julgamento: circulante − saldo × índice de 2024 |
| TD-07 | R02 corte e exatidão das provisões | ESTORNO_PROVISAO de 2025 | 100% | Estorno sem provisão do mês anterior, do mesmo contrato e valor | Valor não pareado |
| TD-08 | Conciliação (500 it. 9; 330 it. 20(a)) | Totais do TESTE × publicado | 100% | Diferença não explicada pelas distorções de TD-01 a TD-07 | Resíduo a investigar |
| MUS | R02 ocorrência e exatidão: restante da população de TD-01 | População de TD-01 **menos** os itens específicos de TD-01/TD-02 e menos o estrato de itens ≥ J | **Amostragem estatística MUS** (Estágio 2) | Procedimentos A1–A5 por item (§5) | Contaminação (*tainting*) × J |

**Fora deste bloco:** perda esperada × envelhecimento (PT 540) e RAP × faturamento (PT 520). A falta desses testes é **limitação de escopo**, não falha de detecção.

## 4. TD-01: regras de triagem (itens específicos) e quantificação
| Regra | Condição | Distorção atribuída (ordem de precedência: R6 > R4 > R1 > R5 > R2) |
|---|---|---|
| R1 | Chave natural (documento, linha) repetida; ou mesmos contrato, fornecedor, módulo, tipo de custo e valor com até 10 dias de distância | Valor das ocorrências **posteriores** à primeira (a primeira é examinada e não recebe distorção) |
| R2 | Valor ≠ custo do documento × (1 + margem) com diferença > R$ 0,02 | Valor − custo × (1 + margem) |
| R4 | Módulo ANEEL vazio, inexistente ou de outro contrato; tipo de custo fora do domínio de obra; fornecedor não cadastrado | Valor integral (não é receita de construção) |
| R5 | Data do documento < 01/01/2025 (serviço do exercício anterior) | Resultado de 2025: +valor. Saldo de 31/12/2025: 0 (afeta abertura) |
| R6 | Sem documento-suporte (id ou data vazios) | Valor integral (530 it. 11, por analogia; 500 it. 9) |

## 5. Estágio 2: MUS no restante da população de TD-01
- **Objetivo e afirmação:** concluir, com 95% de confiança, se a superavaliação do restante dos débitos de receita de infraestrutura (ocorrência e exatidão) não excede a distorção tolerável da amostra.
- **População:** débitos de TD-01 menos os itens específicos (exceções de R1–R6 e de TD-02, examinados individualmente e não projetados) e menos o estrato superior (itens ≥ J, examinados a 100%).
- **Completude:** Σ população TD-01 + Σ estornos (TD-07) = linha "Receita de infraestrutura" do razão TESTE. Contagem por tipo conferida. A diferença do razão para a DF publicada é tratada em TD-08.
- **Unidade amostral:** o real (unidade monetária). O item examinado é o lançamento que contém a unidade sorteada.
- **Saldos nulos e negativos:**
  - itens com valor 0 não têm chance de seleção pela MUS; se existirem, são listados e examinados à parte;
  - itens negativos (estornos) são excluídos da MUS, que não detecta bem subavaliação, e tratados em TD-07;
  - a subavaliação (integridade) é tratada em TD-03.
- **Itens selecionados mais de uma vez:** os itens ≥ J vão para o estrato superior (100%) antes da seleção. Abaixo de J, um item não pode ser sorteado duas vezes na seleção sistemática.
- **Dimensionamento:**
  - TM_amostra = 90.000 − max(Σ|efeito no saldo|; Σ|efeito no resultado|) das distorções do Estágio 1 (presumidas não corrigidas);
  - n = ⌈VC_restante × FC / (TM_amostra − EE × FE)⌉, com FC = 2,9957 (Poisson, 0 erros, 95%), EE = 9.000 e FE = 1,6;
  - J = ⌊VC_restante / n⌋;
  - se TM_amostra − EE × FE ≤ 0, a MUS não se aplica e o restante passa a 100% (530 A7).
  - O tamanho de referência da B06 (≈ 252, sem Estágio 1) é registrado só para comparação.
- **Seleção:** sistemática com intervalo J, início aleatório em [1, J] (semente 2025123108) e ordem por id_lancamento.
- **Procedimentos por item (simulam a inspeção da medição; o "documento" são os campos de custo, data, fornecedor, módulo e aprovação):**
  - A1: documento existe e não está repetido;
  - A2: recálculo custo × (1 + margem);
  - A3: módulo e contrato, tipo de custo capitalizável, fornecedor cadastrado;
  - A4: data do documento em 2025 e ≤ lançamento;
  - A5: aprovação registrada (WF ou pessoa diferente do lançador).
- **Avaliação:**
  - contaminação t = distorção / valor contábil;
  - distorção projetada = Σ t × J;
  - precisão básica = FC(0) × J;
  - acréscimo = Σ t₍ᵢ₎ ordenadas × (FC(i) − FC(i−1) − 1) × J;
  - limite superior = precisão básica + projetada + acréscimo;
  - estrato superior e itens específicos entram pelo valor real, sem projeção.
- **Regra de decisão:** se o limite superior ≤ TM_amostra, a amostra dá base razoável (A22). Se não, aplica-se A23: propor e documentar a ampliação **antes** de concluir.
- **Limitação conhecida já no desenho:** os itens da amostra passam pelas mesmas verificações de dados da triagem. Se não houver erro no restante, a MUS tende a não achar distorções. O limite superior então mede o **risco de amostragem** sobre o restante, não a qualidade documental real.

## 6. Avaliação conjunta (PT 450, parte simulada)
- **Classificação** (450 A6):
  - distorções **factuais**: TD-01 a TD-03, TD-05, TD-07;
  - **de julgamento**: TD-06, classificação;
  - **projetadas**: MUS.
- Cada item é registrado com efeito no saldo de 31/12/2025 e no resultado de 2025.
- **Totais calculados separadamente:**
  - soma das distorções detectadas;
  - distorção projetada;
  - limite superior (risco de amostragem).
- Itens abaixo do CT 7.000 por item continuam acumulados quando fazem parte de um padrão; diferenças de estimativa isoladas abaixo do CT são registradas como claramente triviais.
- A conferência com o gabarito lacrado **só** ocorre depois de os resultados estarem congelados (hash), por código separado (`b08_confronto_gabarito.py`).
