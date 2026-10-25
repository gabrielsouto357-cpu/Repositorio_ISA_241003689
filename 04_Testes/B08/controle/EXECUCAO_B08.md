# Registro de execução – Bloco 08 (21/10/2026, horário de Brasília)

## Ambiente
- Python 3.13.16; Linux-6.18.44-fc-v139-x86_64-with-glibc2.39.
- Bibliotecas: numpy 2.5.3; pandas 3.0.5; scipy 1.18.1; openpyxl 3.1.5.
- LibreOffice usado só para recalcular as fórmulas.

## Sequência realmente executada
| Ordem | Horário | Comando / evento | Resultado |
|---|---|---|---|
| 1 | 02:29 | Congelamento do desenho (`DESENHO_TESTES_B08.md`, `PARAMETROS_B08.json`) | Hashes em CONGELAMENTO_DESENHO.json |
| 2 | ~02h30 | `python codigo/b08_testes.py` (1ª execução) | Falhou ao gravar o JSON (chave em tupla); corrigido sem mudar a lógica dos testes |
| 3 | ~02h31 | `python codigo/b08_testes.py` | 588 exceções; 543 linhas com distorção; MUS n = 710, 0 distorções (~22 s) |
| 4 | ~02h32 | `python codigo/b08_td06_adicional.py` | Verificação adicional do TD-06 (definida depois do resultado): inconclusiva |
| 5 | ~02h33 | `python codigo/b08_memoria.py` + recálculo LibreOffice | 1ª versão: #NAME? (GAMMA.INV); trocada por GAMMAINV. Regra do TD-06 na planilha corrigida para refletir o código (O&M novo). Final: 868 fórmulas, 0 erros |
| 6 | ~02h34 | Redação de `RESULTADOS_TESTES_B08.md` | Antes do gabarito |
| 7 | 02:35 | Congelamento dos resultados (15 arquivos) | CONGELAMENTO_RESULTADOS.json |
| 8 | depois de 7 | `grep` de termos proibidos no código de detecção | Nenhuma leitura proibida (AUDITORIA_CODIGO_SEM_GABARITO.md) |
| 9 | depois de 8 | `python codigo/b08_confronto_gabarito.py` (confere os hashes do item 7 antes de ler o gabarito) | 8 de 10 tipos detectados; 0 falsos positivos com distorção |
| 10 | depois de 9 | `python codigo/b08_confronto_planilha.py` + recálculo | 32 fórmulas, 0 erros |
| 11 | depois de 10 | Reprodução em pasta limpa **sem** gabarito, referência e parâmetros do gerador: `python -I 04_Testes/B08/codigo/b08_testes.py` | 7 de 7 saídas idênticas por SHA-256 |

## Hashes das saídas principais (SHA-256)
- `amostras/AMOSTRA_MUS.csv`: 6e1958531de970f071088dffb4e1deeba0d6c993b0ce1dd5681cbf49b44788aa
- `amostras/POPULACAO_ELEGIVEL_MUS.csv.gz`: 99cd1238d7f9a7f212d84f2e9c81c94ad7a990cd8abc8354f40a8c3f05b51979
- `confronto_PT450/CONFRONTO_GABARITO.csv`: 0c7252649db0bf376b84f4807562847fc5fe65c04eb18966ee02a4c1fee775dc
- `confronto_PT450/CONFRONTO_PT450.xlsx`: 635a182498e107eb7cf6cb9fd55afea43ef6ce992b0909c460a591ed2c402c16
- `confronto_PT450/CONFRONTO_RESUMO.json`: c60f667903cfa226d7ce99e6dba22d3ca7e39ca070201673e4659be958a5a594
- `resultados/DISTORCOES_ESTAGIO1.csv`: 1d843062f25d2cbdd3487b8041ca5ef6e0df2216ce2fac1aafd88af7295d24df
- `resultados/EXCECOES_EXAMINADAS_ESTAGIO1.csv`: 13c3769e9b60ff0996bfe459c133cbb8639f9b24e2a3b2ab35490c7d3b12e0d8
- `resultados/RESULTADOS_B08.json`: 6188724a26aa17e3f6d1c5d9d1595acd1969ab5df5d50615bca75a35e67582e3
- `resultados/TD05_REMUNERACAO_RECALCULO.csv`: 111c0317e287a05bb15eea661646e25ed159328b6112a946910a43a7d681905c
- `resultados/TD06_ADICIONAL_RECEBIMENTOS_2026.csv`: 1b93bd9c93abe62ca5be1be32761cda39936f00b933749e80e31250eaf5a3c47
- `resultados/TD06_CLASSIFICACAO.csv`: f5b10f5018e745dada386ca848328bb7d7def32c737709932d696c233b27d221
