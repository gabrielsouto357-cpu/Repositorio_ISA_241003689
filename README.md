# Auditoria acadêmica — ISA Energia Brasil — exercício 2025

**Matrícula 241003689** · Auditoria 1 (CCA0024), turma 02, 2026.2 · UnB · P2.

Dossiê de auditoria da ISA Energia Brasil S.A. (antiga CTEEP; ISAE3/ISAE4, antes TRPL3/TRPL4) sobre as demonstrações contábeis de 2025, com a NBC TA Estrutura Conceitual e as NBC TA 200 a 600. Trabalho acadêmico: não emite opinião profissional independente nem asseguração sobre a companhia. Os lançamentos da base de dados são **sintéticos**, criados para simulação, e estão separados dos documentos públicos.

## Onde está cada item pedido no enunciado

| Item | Arquivo |
| --- | --- |
| Dossiê em PDF (167 páginas, 27 papéis com referências cruzadas) | [Dossie_ISA_2025_241003689.pdf](Dossie_ISA_2025_241003689.pdf) · Word editável: [Dossie_ISA_2025_241003689.docx](Dossie_ISA_2025_241003689.docx) |
| Base simulada (≥ 500.000 linhas) | [SINTETICO_lancamentos_2025_TESTE.csv.gz](03_Base_sintetica/base_B07/dados_sinteticos/SINTETICO_lancamentos_2025_TESTE.csv.gz) — 600.474 registros · [SINTETICO_lancamentos_2025_REFERENCIA.csv.gz](03_Base_sintetica/base_B07/dados_sinteticos/SINTETICO_lancamentos_2025_REFERENCIA.csv.gz) — 600.650 registros |
| Dicionário de variáveis | [DICIONARIO_DE_DADOS_SINTETICO.md](03_Base_sintetica/base_B07/DICIONARIO_DE_DADOS_SINTETICO.md) (e `.xlsx`) |
| Código de geração e análise | `03_Base_sintetica/base_B07/codigo`, `04_Testes/B08/codigo`, `04_Testes/B09/codigo` e [reproduzir_entrega.py](reproduzir_entrega.py) |
| Planilhas editáveis | Materialidade: `02_Planejamento/MATERIALIDADE_PT320.xlsx` · Amostragem: `04_Testes/B08/resultados/MEMORIA_CALCULO_B08.xlsx` e `04_Testes/B08/amostras/AMOSTRA_MUS.csv` · Analíticos e demais papéis: `04_Testes/B09/planilhas` e `04_Testes/B10/planilhas` · Conciliação da base: `03_Base_sintetica/base_B07/controle/CONCILIACAO_BASE_B07.xlsx` |
| Matriz de cobertura das normas | `00_Controle/MATRIZ_COBERTURA.xlsx` (versões das normas: `00_Controle/MAPA_NORMATIVO.xlsx`) |
| Fontes utilizadas e links | [08_Fontes/INDICE_FONTES.csv](08_Fontes/INDICE_FONTES.csv) e `00_Controle/FONTES_USADAS.xlsx` |
| Programas por ciclo | `05_Papeis/Programas` (receitas, disponibilidades, estoques, imobilizado, passivos, estimativas e consolidação) |
| Conclusão integrada | Parte F do dossiê e [CONCLUSAO_INTEGRADA.md](CONCLUSAO_INTEGRADA.md) |

## Organização

| Pasta | Conteúdo |
| --- | --- |
| `00_Controle` | Matriz de cobertura, mapa normativo, fontes usadas, riscos e respostas, decisões e registros de revisão |
| `01_Dados_reais` | Extração das DFs 2025/2024 e conferência PDF × dados da CVM |
| `02_Planejamento` | Materialidade, matriz de riscos, estrutura do grupo |
| `03_Base_sintetica/base_B07` | Base sintética, dicionário, código, parâmetros, conciliação e registro dos erros inseridos (`gabarito_LACRADO`) |
| `04_Testes` | Testes e amostragem sobre a base (B08), planilhas dos papéis (B09, B10) e conferências de reprodução (B12) |
| `05_Papeis` | Texto dos 27 papéis, programas por ciclo, modelos e minutas não enviadas |
| `08_Fontes` | Documentos públicos (CVM, B3, RI, CFC) e índice com URL, data de consulta e hash |
| `99_Trabalho` | Scripts auxiliares de extração e conferência |

`INVENTARIO_FINAL.csv` lista cada arquivo com tamanho e SHA-256.

## A base de dados

A base representa a conta de maior materialidade do ativo: ativos da concessão (ativo contratual e serviços de O&M), R$ 36.431.298 mil em 31/12/2025, 77% do ativo total (DF 2025, p.23 e p.45). Cada linha é um lançamento analítico (medição, recebimento, remuneração, O&M, saldo de abertura etc.), com o campo `natureza_dado = SINTETICO_DIDATICO`.

- **REFERENCIA**: base sem erros; soma R$ 36.431.298.000,00, igual ao saldo publicado.
- **TESTE**: a mesma base com erros inseridos de propósito, usada nos testes. O registro desses erros e o confronto com as exceções encontradas estão em `03_Base_sintetica/base_B07/gabarito_LACRADO` e `04_Testes/B08/confronto_PT450`.

Os arquivos `.csv.gz` são CSV compactados (cerca de 12 MB cada). No GitHub, abra o arquivo e use **Download raw file**; o site não mostra a prévia de arquivos desse tamanho. Para abrir, descompacte com um programa compatível com gzip (por exemplo, 7-Zip). Separador `;`, valores em reais com ponto decimal.

## Como reproduzir

Requer Python 3.12 ou 3.13 e as versões fixadas em [requirements.txt](requirements.txt) (numpy 2.5.3, pandas 3.0.5, scipy 1.18.1, openpyxl 3.1.5). Outras versões podem gerar dados diferentes. No Windows, abra o PowerShell na pasta do repositório e execute um comando por vez:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
$env:PYTHONUTF8='1'
.\.venv\Scripts\python.exe reproduzir_entrega.py
```

No Linux ou macOS, use `python3 -m venv .venv` e `.venv/bin/python`.

O programa cria uma pasta nova em `_reproducao/`, gera a base (semente 20251231, em `03_Base_sintetica/base_B07/config/config_B07.json`), insere os erros sintéticos, concilia, executa os testes e a amostragem, faz o confronto com o registro de erros e compara tudo com os arquivos entregues. Os originais não são alterados. O resultado fica em `RELATORIO_REPRODUCAO.json`, que deve indicar `aceite: true`.

Para só conferir se os arquivos baixados estão completos e íntegros, sem instalar bibliotecas: `py -3.12 verificar_entrega.py`. Ele compara cada arquivo com o tamanho e o SHA-256 registrados em `INVENTARIO_FINAL.csv` e deve terminar com `"resultado": "OK"`.

### Resultados esperados

| Conferência | Resultado |
| --- | --- |
| Base REFERENCIA 2025 | 600.650 registros; soma R$ 36.431.298.000,00; nenhum ID repetido |
| Base TESTE 2025 | 600.474 registros; soma R$ 36.463.023.784,44; nenhum ID repetido |
| Testes de 100% (Estágio 1) | 588 exceções examinadas; 543 linhas com distorção |
| Amostra MUS (PT 530) | 710 itens; distorção projetada zero; limite superior R$ 27.106.254,52 |
| Distorções sintéticas (PT 450) | Efeito líquido R$ 30.525.784,48 no saldo e R$ 34.053.305,62 no resultado |

Materialidade do dossiê: MG 139.000, ME 90.000 e CT 7.000, em **R$ mil**. Nas bases, os valores estão em **reais**.

## Limitações

Cada procedimento do dossiê é classificado como realizado com evidência pública [RP], planejado por falta de acesso [PA] ou simulado com dados sintéticos [SD]. Não houve contato com a companhia, seus auditores ou terceiros: confirmações, carta de representação e comunicações são minutas não enviadas. Os resultados dos testes sintéticos demonstram os procedimentos, não constatações sobre a ISA Energia Brasil. A pesquisa de eventos subsequentes tem corte em 21/10/2026. O consolidado de normas do curso não é republicado; as normas citadas estão identificadas em `08_Fontes/INDICE_FONTES.csv`.

O histórico de revisões do trabalho está no PT 220 do dossiê e nos registros de revisão em `00_Controle`.
