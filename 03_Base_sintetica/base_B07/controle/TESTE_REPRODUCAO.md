# Teste de reprodução em pasta limpa (Bloco 07)

Executado em 20/10/2026 (Brasília). Pasta limpa: cópia **somente** de `codigo/`, `config/` e `dados_reais_derivados/` para uma pasta temporária vazia, seguida de `python -I codigo/run_all.py` (modo isolado).

**Resultado:** 28 de 28 arquivos idênticos às saídas da pasta de produção.

| Arquivo | Critério | Resultado |
|---|---|---|
| dados_sinteticos/SINTETICO_cadastro_fornecedores.csv | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_cadastro_usuarios_pagadores.csv | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_lancamentos_2025_REFERENCIA.csv.gz | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_lancamentos_2025_TESTE.csv.gz | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_lancamentos_2026_jan_fev_REFERENCIA.csv.gz | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_lancamentos_2026_jan_fev_TESTE.csv.gz | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_parametros_contratos.csv | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_saldos_REFERENCIA.csv | SHA-256 | IGUAL |
| dados_sinteticos/SINTETICO_saldos_TESTE.csv | SHA-256 | IGUAL |
| gabarito_LACRADO/LINHAS_ALTERADAS.csv | SHA-256 | IGUAL |
| gabarito_LACRADO/MAPA_IDS_TESTE_COM_ERRO.csv | SHA-256 | IGUAL |
| gabarito_LACRADO/PONTE_EFEITO_ERROS.xlsx | valores e fórmulas das células | IGUAL |
| gabarito_LACRADO/REGISTRO_ERROS.csv | SHA-256 | IGUAL |
| controle/CONCILIACAO_BASE_B07.xlsx | valores e fórmulas das células | IGUAL |
| controle/RELATORIO_VERIFICACOES.md | SHA-256 | IGUAL |
| controle/VERIFICACOES_RESULTADO.csv | SHA-256 | IGUAL |
| codigo/conciliar.py | SHA-256 | IGUAL |
| codigo/gerar_dicionario.py | SHA-256 | IGUAL |
| codigo/gerar_referencia.py | SHA-256 | IGUAL |
| codigo/inserir_erros.py | SHA-256 | IGUAL |
| codigo/requirements.txt | SHA-256 | IGUAL |
| codigo/run_all.py | SHA-256 | IGUAL |
| codigo/verificar.py | SHA-256 | IGUAL |
| config/config_B07.json | SHA-256 | IGUAL |
| dados_reais_derivados/REAL_catalogo_modulos_ANEEL_28_contratos.csv | SHA-256 | IGUAL |
| dados_reais_derivados/REAL_contratos_F0003_p36.csv | SHA-256 | IGUAL |
| DICIONARIO_DE_DADOS_SINTETICO.md | SHA-256 | IGUAL |
| DICIONARIO_DE_DADOS_SINTETICO.xlsx | valores e fórmulas das células | IGUAL |

Não comparados: EXECUCAO_LOG.json/.md e HASHES_SHA256.txt (contêm horários e durações) e README (escrito à mão). Arquivos .xlsx são comparados por fórmulas e valores digitados, porque o openpyxl grava a data nos metadados. Na produção, as fórmulas foram depois recalculadas no LibreOffice só para gravar valores em cache; as fórmulas não mudam.