# Dados reais – Bloco 02 (como reproduzir)

Arquivos:
- `DADOS_REAIS_DF_2025_2024.xlsx`: planilha principal. Leia primeiro a aba `LEIA`.
- `extracao_B02/pdf_linhas_F0003_F0011.csv`: linhas extraídas dos PDFs, com página física, número da linha na página e texto original.
- `extracao_B02/cvm_isa_dfp_2024_2025.csv`: linhas da ISA (CNPJ 02.998.611/0001-04) nos CSV oficiais da DFP, com nome do arquivo e número da linha.

Reprodução (Python 3 com pandas e openpyxl; utilitário `pdftotext` do Poppler):
1. `python b02_extrair_dfs.py F0003.pdf F0011.pdf linhas.csv`. Os PDFs são `01_Demonstracoes_2025/6429-...pdf` e `02_Demonstracoes_2024/6028-...pdf`.
2. Gere `cvm_isa_long.csv` filtrando o CNPJ nos ZIPs `03_CVM_DFP_e_cadastro/Dados_estruturados/dfp_cia_aberta_2025.zip` e `..._2024.zip`. Use os arquivos BPA, BPP, DRE, DRA e DFC_MI, con e ind. A linha do CSV é o índice + 2.
3. `python b02_planilha_dados_reais.py linhas.csv cvm_isa_long.csv DADOS_REAIS_DF_2025_2024.xlsx`.
4. Abra no Excel ou LibreOffice para recalcular (as fórmulas não têm valores gravados pelo script).

Resultados da execução de 19/10/2026: 1.076 valores do PDF; 2.522 linhas da CVM; 552 conferências PDF×CVM sem diferença; 28 subtotais recalculados sem diferença. Nos comparativos, uma reclassificação foi explicada. Das 33 verificações cruzadas, 28 estão OK e 5 têm diferença explicada ou pendente.
