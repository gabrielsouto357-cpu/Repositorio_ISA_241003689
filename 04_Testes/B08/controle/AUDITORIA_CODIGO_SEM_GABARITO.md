# Verificação de que o código de detecção não usa o gabarito (21/10/2026, antes do confronto)

Comando executado: `grep -n -i "gabarito|REFERENCIA|inserir_erros|parametros_contratos|MAPA_IDS|REGISTRO_ERROS|LINHAS_ALTERADAS" codigo/b08_testes.py codigo/b08_memoria.py codigo/b08_td06_adicional.py`

Ocorrências encontradas, nenhuma delas é leitura:
- `b08_testes.py` linha 18: é a **lista de bloqueio** da função `ler()`. Se algum caminho contiver um desses termos, o programa para (assert).
- `b08_testes.py` linha 212 e `b08_memoria.py` linha 43: variável `tamanho_referencia_B06`, que é o tamanho de amostra de referência do projeto B06, não o arquivo de referência.
- `b08_memoria.py` linhas 2 e 17: texto informativo.

As entradas efetivamente lidas estão em `resultados/RESULTADOS_B08.json` (chave `entradas_lidas`): os 7 arquivos permitidos do desenho.

O script `b08_confronto_gabarito.py` é o único que lê o gabarito. Foi criado e executado **depois** do congelamento dos resultados (`CONGELAMENTO_RESULTADOS.json`).
