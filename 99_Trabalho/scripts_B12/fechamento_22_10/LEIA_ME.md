# Reprodução do fechamento financeiro B12

Executar em cópia de trabalho, com Python, pandas/openpyxl das instruções B02 e `pdftotext` Poppler 26.07.0 disponível no PATH. Nunca substituir os PDFs-fonte. Os três argumentos do extrator são o PDF F0003, o PDF F0011 e um caminho novo de saída CSV.

1. Localize F0003 e F0011 pelo inventário do projeto e execute `python b02_extrair_dfs.py "PDF_F0003" "PDF_F0011" "PASTA_NOVA/pdf_linhas_reextraidas.csv"`, usando o script original em 99_Trabalho/scripts_B02.
2. Execute `python comparar_financeiro.py --root "PASTA_11_Elaboracao_do_trabalho" --output "PASTA_NOVA"`. Compara cada campo da nova extração com o CSV histórico; a contagem também deve ser igual.
3. Execute `python reconferir_552.py --root "PASTA_11_Elaboracao_do_trabalho" --output "PASTA_NOVA"`. Usa os mapeamentos explícitos do script B02 e os CSV oficiais salvos, sem executar o autor de planilha. Resultado esperado: 552 comparações, zero diferenças, 277 linhas extraídas e 1.076 valores numéricos. O relatório informa 2.522 linhas CVM.

Os scripts podem ficar em qualquer pasta quando --root/--output são fornecidos; sem argumentos esperam esta estrutura de projeto. Não dependem da pasta temporária da sessão. O binário Poppler não integra o pacote acadêmico; sua procedência e hashes constam do JSON de evidências. A reprodução não comprova a realidade das operações da companhia.
