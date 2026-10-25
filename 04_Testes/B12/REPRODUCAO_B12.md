# Reprodução conferida no Bloco 12

Execute a partir de uma cópia do projeto, preservando os originais. Todos os dados de lançamento são sintéticos.

1. Instale Python e as versões de `03_Base_sintetica/base_B07/codigo/requirements.txt`. A execução B12 usou Python 3.12.14 no Windows, numpy 2.5.3, pandas 3.0.5 e openpyxl 3.1.5; a execução histórica usou Python 3.13.16 no Linux. Para os testes B08 também é necessário scipy; B12 usou scipy 1.18.1.
2. No Windows, habilite UTF-8 antes da execução: em PowerShell, `$env:PYTHONUTF8='1'`. No Linux, use `PYTHONUTF8=1` no ambiente. Isso evita falha apenas ao imprimir símbolos no terminal. Não altera dados ou sementes.
3. Na pasta `03_Base_sintetica/base_B07`, execute `python codigo/run_all.py`.
4. Na raiz `11_Elaboracao_do_trabalho`, execute `python 04_Testes/B08/codigo/b08_testes.py`. As pastas `04_Testes/B08/resultados` e `amostras` devem existir. O detector lê apenas as sete entradas autorizadas do desenho, sem gabarito ou base REFERENCIA.
5. Somente após preservar os resultados da detecção, execute o confronto `python 04_Testes/B08/codigo/b08_confronto_gabarito.py`. Isso verifica omissões e não transforma o teste em experimento cego.
6. Memórias editáveis: `b08_memoria.py` e `b08_confronto_planilha.py` reconstroem as planilhas a partir dos resultados; o Excel recalcula ao abrir. A reexecução B12 comparou também a amostra e o conteúdo das saídas, não apenas logs de sucesso.

Compare registros e valores, não apenas hashes: CSVs Windows/Linux podem usar CRLF/LF; cabeçalhos gzip dependem do nome e do terminador; XLSX contém metadados de gravação e caches de fórmulas. No B12, os 12 CSV/CSV.gz da geração e do gabarito tiveram os mesmos dados; três XLSX tiveram os mesmos valores e fórmulas. Se usar versões de numpy/pandas diferentes, a igualdade não é assegurada: uma tentativa B12 com versões diferentes gerou dados distintos e foi descartada.

Resultados esperados: REFERENCIA 600.650 linhas de 2025 e soma R$36.431.298.000,00; TESTE 600.474 e R$36.463.023.784,44; detecção 543 ajustes, 588 exceções examinadas e 710 itens MUS, sem distorção detectada pelos atributos da amostra. O limite Poisson é cálculo demonstrativo, não segurança sobre atributos não examinados.

O script B09 de comparação de políticas foi corrigido para usar `04_Testes/B09/dados/politicas_nota5_F0003.txt` e `politicas_nota5_F0011.txt` na ausência de argumentos; não depende da pasta temporária do assistente anterior. Scripts de construção dos documentos B01–B12 são registros históricos de autoria e não integram a cadeia portátil de geração e análise da base. A extração B02 foi reexecutada no encerramento de 22/10/2026 com Poppler 26.07.0: 277 linhas iguais e 552 cruzamentos sem diferenças. Provas e instruções complementares estão em fechamento_22_10. O registro anterior de falha foi superado pela reexecução bem-sucedida; nenhuma consulta interna foi simulada.

Publicação, README final do repositório, PDF final e acessibilidade ao professor continuam B13. Não foram executados no B12.
