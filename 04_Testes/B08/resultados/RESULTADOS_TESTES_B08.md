# Resultados dos testes do Bloco 08, antes do confronto com o gabarito

Base **SINTÉTICA** (cenário TESTE); não são dados da ISA Energia Brasil. [SD]
- Executado por `codigo/b08_testes.py` em 21/10/2026, conforme o desenho congelado às 02h29 (`controle/CONGELAMENTO_DESENHO.json`).
- Entradas lidas (registradas em `RESULTADOS_B08.json`): somente os 7 arquivos permitidos. O gabarito **não** foi aberto.
- Memória de cálculo: `MEMORIA_CALCULO_B08.xlsx` (868 fórmulas, 0 erros).

## 1. População e completude
| Item | Linhas | Valor (R$) |
|---|---|---|
| Débitos de receita de infraestrutura (TD-01): RECEITA_INFRA 269.191; PROVISAO_MEDICAO 72; AJUSTE_MANUAL 2 | 269.265 | 6.477.413.245,75 |
| Estornos de provisão (negativos; TD-07) | 66 | −121.857.113,00 |
| Itens com valor zero | 0 | — |
| **Soma = linha "Receita de infraestrutura" do razão TESTE** | | **6.355.556.132,75** |

- A soma confere com a conciliação do PT 500 (aba C_TESTE).
- O razão TESTE difere da DF publicada (6.330.048 mil) em 25.508 mil. Essa diferença é tratada como item de conciliação (TD-08), não como problema de completude da população.
- Medições sem custo do documento: 0.

## 2. Estágio 1: 100% e itens específicos (não é amostragem; sem projeção, 500 A66)
| Teste / regra | Exceções examinadas | Com distorção | Efeito no saldo (R$) | Efeito no resultado (R$) |
|---|---|---|---|---|
| TD-01 R1 documento repetido | 70 (35 pares) | 35 | 4.893.510,12 | 4.893.510,12 |
| TD-01 R2 recálculo custo × (1 + margem) | 20 | 20 | 7.716.140,92 | 7.716.140,92 |
| TD-01 R4 sem vínculo de obra | 60 | 60 | 4.600.000,00 | 4.600.000,00 |
| TD-01 R5 documento de 2024 | 150 | 150 | 0,00 | 3.527.521,14 |
| TD-01 R6 e TD-02 lançamento manual sem suporte | 2 | 2 | 15.500.000,00 | 15.500.000,00 |
| TD-03 corte (serviço de 2025 lançado em 2026) | 273 | 273 | −7.201.518,28 | −7.201.518,28 |
| TD-04 recebimento no contrato errado | 8 | (classificação) | 0 (reclassificação de 1.986.044,78) | 0 |
| TD-05 remuneração | 3 | 3 | 5.017.651,72 | 5.017.651,72 |
| TD-06 classificação circulante | 1 | 0 (explicada) | 0 | 0 |
| TD-07 estornos sem provisão | 0 | 0 | 0 | 0 |
| **Total líquido** | **588** | **543** | **30.525.784,48** | **34.053.305,62** |
| Total absoluto | | | 44.928.821,04 | 48.456.342,18 |

### Natureza, causa possível e verificações adicionais (530 it. 12; A17)
- **R1 (35 pares)**
  - Achado: mesmo documento e linha lançados duas vezes, de 2 a 6 dias depois, nos contratos 059/2001 (19), 006/2023 (10) e 012/2023 (6).
  - Verificação adicional: para cada par, conferi fornecedor, módulo, custo e valor. São idênticos.
  - Causa possível: reprocessamento da interface de medições.
  - Padrão comum: obras em andamento. Segundo A17, isso justifica estender o exame a todo o lote de interface, o que já foi feito, porque a triagem cobriu 100%.
- **R2 (20)**
  - Achado: 19 diferenças pequenas, compatíveis com transposição de dígitos, e 1 diferença de R$ 7.649.540,91 (valor ≈ 10 × custo, um "zero a mais").
  - A diferença de R$ 7,65 milhões excede **sozinha** o CT (R$ 7 milhões).
  - Causa possível: digitação, ou ajuste manual de valor sem revisão.
- **R4 (60)**
  - Achado: medições no 059/2001 com tipo de custo "Manutenção corretiva", sem módulo nem obra ANEEL.
  - Causa possível: gasto de O&M (despesa do período) capitalizado como ativo contratual (CPC 47).
  - Afirmações: ocorrência e classificação.
- **R5 (150)**
  - Achado: documentos de dezembro de 2024 lançados em janeiro de 2025, nos contratos 059/2001 e 008/2022.
  - Efeito: superavalia a receita de 2025 e subavalia o saldo de abertura. Não altera o saldo de 31/12/2025.
  - É o mesmo tipo de situação descrito no relatório real do auditor (F0003 p.136). Aqui é só um paralelo didático.
- **R6 e TD-02 (2 lançamentos)**
  - Achado: AJUSTE_MANUAL em 30/12/2025 às 23h41 (R$ 12.000.000) e às 23h47 (R$ 3.500.000). Ambos sem documento, com valores redondos, lançados e aprovados pelo usuário U11, que só tem esses 2 lançamentos no ano.
  - Não há suporte; pelo it. 11 do 530 e pelo it. 9 do 500, o valor integral é tratado como distorção.
  - **É indício de burla de controles** (240 it. 32(a)). Pelo 240 it. 35 e pelo 450 A22, a avaliação é qualitativa, independentemente do valor.
- **TD-03 (273 linhas)**
  - Achado: medições com documento de dezembro de 2025 lançadas entre 5 e 20/01/2026, nos contratos 059/2001, 006/2023 e 012/2023. Nenhuma tinha provisão em dezembro.
  - Efeito: subavaliação de R$ 7,2 milhões no saldo e no resultado.
  - **Ajustes de provisão de dez/2025**, analisados à parte: nos 6 contratos com provisão, a diferença entre o provisionado e a medição efetiva lançada em jan/2026 vai de −1.442.686 a +686.226 (líquido de −1.377.738).
    - É ajuste normal de estimativa; cada diferença fica abaixo do CT e não há padrão de viés (os sinais se alternam).
    - Por isso foi registrado como **claramente trivial** e não acumulado (450 A2).
- **TD-04 (8 linhas)**
  - Achado: 8 linhas de recebimento do documento REC-0272017-202507 (IE Itaquerê) aplicadas ao contrato 018/2017 (IE Itaúnas).
  - Efeito: nenhum no total; distorce o saldo por contrato e por entidade.
  - Causa possível: erro de baixa na tesouraria.
- **TD-05 (3 linhas)**
  - Achado: no contrato 046/2017, a remuneração de out–dez/2025 usa taxa de 9,9%; nos outros 9 meses, 6,9%.
  - A taxa implícita "é determinada no início dos contratos/projetos e não sofre alterações posteriores" (F0003 p.100).
  - Distorção: R$ 5.017.651,72. Causa possível: parâmetro alterado no sistema de cálculo.
- **TD-06 (1 exceção, explicada)**
  - Achado: o índice de circulante do 059/2001 SE financeiro passou de 24,3% para 44,9%.
  - Verificação adicional, **definida depois do resultado** (não estava no desenho): comparar com os recebimentos de jan–fev/2026 × 6. Foi **inconclusiva**, porque o arquivo de 2026 só tem recebimentos de O&M.
  - Explicação por evidência pública: o pagamento do componente financeiro do RBSE termina em 2028 (F0003 p.37). Os componentes financeiro e econômico têm prazos de realização distintos (p.46). Com o fim do fluxo se aproximando, a parcela de 12 meses aumenta.
  - Conclusão: exceção **explicada**, sem distorção registrada.
  - Nenhum outro contrato foi sinalizado pela regra fixada. Não acrescentei outra regra de classificação depois de ver os resultados.
- **TD-07:** todos os 66 estornos têm provisão correspondente no mês anterior.

## 3. Estágio 2: MUS no restante (amostragem estatística)
| Parâmetro | Valor | Natureza |
|---|---|---|
| ME | 90.000.000,00 | Norma (530 A3) + D-014 |
| TM da amostra = ME − 48.456.342,18 | 41.543.657,82 | Julgamento: presume distorções não corrigidas |
| EE / FE / confiança | 9.000.000 / 1,6 / 95% | Julgamento didático |
| FC(0) (Poisson) | 2,9957 | Cálculo |
| Itens específicos excluídos | 302 | 500 A65–A66 |
| Estrato superior (≥ J) | 1 item, R$ 10.000.000 (marco contratual MARCO-0062023-02): examinado, sem exceção | Valor real; sem projeção |
| VC do restante | 6.424.285.941,99 em 268.962 linhas | |
| **n** | **710** (fórmula = código) | 530 it. 7 |
| **J** | 9.048.290,05 | |
| Início aleatório | 519.156.127 centavos (semente 2025123108) | 530 it. 8 |
| Itens: RECEITA_INFRA / PROVISAO_MEDICAO | 694 / 16 | Provisões: procedimento alternativo, que é o estorno no mês seguinte (530 it. 10) |
| **Distorções encontradas na amostra** | **0** | |
| **Soma das distorções detectadas na amostra** | **R$ 0,00** | |
| **Distorção projetada** | **R$ 0,00** | 530 it. 14 |
| **Limite superior (precisão básica)** | **R$ 27.106.254,52** | Risco de amostragem |
| Folga contra o TM da amostra | 14.437.403,30 | Limite ≤ TM: base razoável (A22) |

Para comparação: sem o Estágio 1 e com TM = ME, o tamanho seria 257 (B06: ≈ 252, com VC da DF).

**Por que a projeção é zero e o que isso significa:**
- Nenhum item da amostra teve distorção, e não há distorção a projetar.
- O resultado era **mecanicamente esperado** pelo desenho: os itens da amostra passam pelos mesmos atributos de dados que a triagem já aplicou ao restante.
- O limite superior (27,1 milhões) mede o **risco de amostragem** sobre as distorções que só um exame documental real revelaria (por exemplo, medição fictícia com documento aparentemente regular). Ele **não** mede a eficácia do exame.
- As distorções do Estágio 1 **não são projetadas**: vêm de 100% ou de itens específicos (500 A66; 530 Apêndice 1 §3–4).

## 4. Avaliação conjunta (antes do gabarito; detalhes na aba Agregacao_PT450)
| Componente (R$) | Saldo 31/12/2025 | Resultado 2025 |
|---|---|---|
| (1) Distorções factuais (100% e itens específicos) | 30.525.784,48 | 34.053.305,62 |
| (2) Distorções de julgamento | 0 | 0 |
| (3) Distorção projetada (MUS) | 0 | 0 |
| (4) Melhor estimativa | 30.525.784,48 | 34.053.305,62 |
| (5) Margem para risco de amostragem | 27.106.254,52 | 27.106.254,52 |
| (6) Limite superior agregado | 57.632.039,00 (64% da ME) | 61.159.560,14 (68% da ME) |

- **Conciliação (PT 500):**
  - a diferença TESTE × publicado é de 31.725.784,44;
  - as distorções factuais explicam 30.525.784,48;
  - **ficam sem explicação R$ 1.199.999,96**, concentrados em O&M e perda esperada (C2/C4 da aba C_TESTE).
  - A perda esperada não foi testada neste bloco (PT 540). A diferença fica **em aberto** e não pode ser declarada trivial sem investigação.
- **Quantitativo:**
  - (4) fica abaixo da ME e da MG; (6) também fica abaixo da ME;
  - a distância até a ME diminui se somadas as distorções ainda não testadas (perda esperada) e o risco não resultante da amostragem.
  - Pelo 450 it. 6(b) e A8, **não** se afirma suficiência sem o PT 540.
- **Qualitativo:**
  - os dois lançamentos manuais sem suporte (U11) indicam possível fraude. O 240 it. 35–36 exige reavaliar o risco R16 e os procedimentos;
  - a distorção de R$ 7,65 milhões (zero a mais) supera o CT sozinha.

## 5. Ajustes propostos antes de afirmar suficiência (530 A23; 450 it. 6)
1. **Lançamentos (R16):** estender o TD-02 a todo o arquivo de jan–fev/2026, e não só até 15/01, e a todos os lançamentos de U11 e dos aprovadores U08/U09 fora do padrão.
   - Os lançamentos de U11 já foram cobertos a 100% na base: são só 2.
   - [PA] obter a explicação da administração para os lançamentos, que não pode ser obtida (sem contato com a companhia).
2. **Perda esperada (PT 540):** testar o envelhecimento × perda esperada para explicar a diferença de R$ 1,2 milhão. É **condição** para concluir sobre a conta.
3. **Classificação (TD-06):** obter o cronograma de recebimentos do RBSE [PA] para fechar a explicação do 059/2001 SE financeiro.
4. **MUS:** não é preciso ampliar. O limite superior está abaixo do TM da amostra.
   - Se a administração corrigir as distorções factuais (simulação: proposta, não executada), o TM da amostra volta a 90.000.000 e a folga aumenta.

## 6. Limitações
- A mesma IA desenhou os erros e os testes. As regras podem refletir esse conhecimento, e o exercício não é cego.
- A "inspeção documental" é simulada por campos da própria base.
- Os resultados não se estendem aos registros reais da ISA.
