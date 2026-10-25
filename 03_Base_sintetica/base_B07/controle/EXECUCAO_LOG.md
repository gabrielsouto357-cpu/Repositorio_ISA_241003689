# Registro de execução – base sintética (Bloco 07)

Base **SINTÉTICA** didática; não são dados internos da ISA Energia Brasil. Fonte estruturada: `EXECUCAO_LOG.json`.

## Ambiente

- Python 3.13.16; Linux-6.18.44-fc-v139-x86_64-with-glibc2.39
- numpy 2.5.3; pandas 3.0.5; openpyxl 3.1.5; LibreOffice (só para recalcular fórmulas)
- Semente: 20251231 (gerador PCG64 do numpy). Parâmetros: `config/config_B07.json` (hash em HASHES_SHA256.txt).

## Comandos realmente executados na execução registrada (horário de Brasília)

Início 2026-10-20T23:39:14-03:00; fim 2026-10-20T23:41:00-03:00; hashes relidos após o recálculo em 2026-10-20T23:41:21-03:00.

| Ordem | Comando | Retorno | Duração (s) | Última linha da saída |
|---|---|---|---|---|
| 1 | `python codigo/gerar_referencia.py` | 0 | 36.2 | EFICIENCIA                            5 |
| 2 | `python codigo/inserir_erros.py` | 0 | 19.3 | TESTE linhas 2025: 600474 / 2026: 26417 |
| 3 | `python codigo/conciliar.py` | 0 | 12.4 | REF (R$): 36,431,298,000.00 / TESTE (R$): 36,463,023,784.44 / diferença TESTE − publicado (R$ mil): 31725.78444 |
| 4 | `python codigo/verificar.py` | 0 | 26.2 | FALHAS DE GERAÇÃO: 0 |
| 5 | `python codigo/gerar_dicionario.py` | 0 | 10.5 | dicionário: 31 campos de fluxo; 8 de estoque; 13 tipos |
| 6 | `python recalc.py controle/CONCILIACAO_BASE_B07.xlsx` (LibreOffice) | status success | — | 449 fórmulas, 0 erros |
| 7 | `python recalc.py gabarito_LACRADO/PONTE_EFEITO_ERROS.xlsx` | status success | — | 5 fórmulas, 0 erros |
| 8 | `python codigo/run_all.py --so-hashes` | 0 | — | Hashes e contagens relidos dos arquivos gravados |
| 9 | Cópia de codigo/, config/ e dados_reais_derivados/ para pasta vazia + `python -I codigo/run_all.py` | 0 | ~95 | 28/28 arquivos idênticos (TESTE_REPRODUCAO.md) |

Durante o desenvolvimento, os scripts foram executados várias vezes e corrigidos (seção final). Valem os resultados da execução registrada acima.

## Confirmação por leitura dos arquivos gravados (contagem de linhas sem cabeçalho)

| Arquivo | Linhas | Bytes |
|---|---|---|
| controle/VERIFICACOES_RESULTADO.csv | 82 | 8.484 |
| dados_reais_derivados/REAL_catalogo_modulos_ANEEL_28_contratos.csv | 4.471 | 844.241 |
| dados_reais_derivados/REAL_contratos_F0003_p36.csv | 28 | 1.911 |
| dados_sinteticos/SINTETICO_cadastro_fornecedores.csv | 2.500 | 65.028 |
| dados_sinteticos/SINTETICO_cadastro_usuarios_pagadores.csv | 480 | 18.210 |
| dados_sinteticos/SINTETICO_lancamentos_2025_REFERENCIA.csv.gz | 600.650 | 12.489.738 |
| dados_sinteticos/SINTETICO_lancamentos_2025_TESTE.csv.gz | 600.474 | 12.488.376 |
| dados_sinteticos/SINTETICO_lancamentos_2026_jan_fev_REFERENCIA.csv.gz | 26.144 | 606.543 |
| dados_sinteticos/SINTETICO_lancamentos_2026_jan_fev_TESTE.csv.gz | 26.417 | 615.852 |
| dados_sinteticos/SINTETICO_parametros_contratos.csv | 28 | 5.106 |
| dados_sinteticos/SINTETICO_saldos_REFERENCIA.csv | 110 | 9.704 |
| dados_sinteticos/SINTETICO_saldos_TESTE.csv | 110 | 9.705 |
| gabarito_LACRADO/LINHAS_ALTERADAS.csv | 553 | 43.040 |
| gabarito_LACRADO/MAPA_IDS_TESTE_COM_ERRO.csv | 279 | 14.918 |
| gabarito_LACRADO/REGISTRO_ERROS.csv | 10 | 1.845 |

## Correções durante o desenvolvimento (não silenciosas)
- **conciliar.py:** as linhas de total sobrescreviam o último item de C2 e C4 (#VALUE! no recálculo). Os totais passaram a ficar em linha própria; depois disso, 0 erros.
- **inserir_erros.py:**
  - A duplicata de E03 passou a ter a competência do mês do novo lançamento.
  - No TESTE, o O&M ficou 100% circulante, como na referência. Antes, havia não circulante indevido, uma falha de geração e não um erro desejado.
  - Os IDs de documentos de E07 seguem o padrão numérico da base, para não servirem de marcador.
  - O script deixou de imprimir o efeito de cada erro, que entraria neste log não lacrado; agora imprime só a quantidade de registros do gabarito.
- **verificar.py:**
  - A N19 foi reescrita: usava a "primeira" linha pela ordem do arquivo, não a linha 1 do documento.
  - Foi acrescentada a N25.
  - A N04 foi refinada: as 74 coincidências de valor entre documentos distintos na referência ficaram como justificadas (I02), mantidas na base (D-023).
- **Formato:** ponto decimal (D-022).