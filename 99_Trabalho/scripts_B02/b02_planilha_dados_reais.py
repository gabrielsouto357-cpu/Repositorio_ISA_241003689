# -*- coding: utf-8 -*-
"""
Bloco 02 - Monta 01_Dados_reais/DADOS_REAIS_DF_2025_2024.xlsx a partir de:
  * linhas.csv  (saída de b02_extrair_dfs.py: valores dos PDFs F0003 e F0011, com página e texto original)
  * cvm_isa_long.csv (linhas da ISA nos ZIPs oficiais CVM F0018/F0017, com número da linha do CSV)
  * valores de notas transcritos (aba Notas_valores, com documento/página/nota)
Todas as visões e conciliações são FÓRMULAS (SUMIFS) sobre as abas de dados; nada é colado como resultado.
Uso: python b02_planilha_dados_reais.py linhas.csv cvm_isa_long.csv saida.xlsx
"""
import sys, csv
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter as L
from openpyxl.comments import Comment

F = "Arial"
HDR = PatternFill("solid", fgColor="1F3864")
SUB = PatternFill("solid", fgColor="D9E1F2")
BLUE = Font(name=F, size=9, color="0000FF")
BLK = Font(name=F, size=9)
NUMF = '#,##0;(#,##0);"-"'
PREP = "Preparado por: matrícula 241003689 (execução assistida por IA), 19/10/2026. Revisão humana: ______ (em branco). Unidade: R$ mil, salvo LPA (R$/ação)."

# ------------------------------------------------------------------ rótulos padronizados (ordem das linhas no F0003)
LAB = {
 "BP_ATIVO": [("A01","Caixa e equivalentes de caixa","I"),("A02","Aplicações financeiras","I"),("A03","Ativos da concessão (circulante)","I"),
   ("A04","Estoques (circulante)","I"),("A05","Tributos e contribuições a compensar","I"),("A06","Instrumentos financeiros derivativos (circulante)","I"),
   ("A07","Créditos com partes relacionadas","I"),("A08","Outros (circulante)","I"),("A09","Total do ativo circulante","S"),
   ("A10","Ativos da concessão (realizável a LP)","I"),("A11","Valores a receber - Secretaria da Fazenda","I"),("A12","Cauções e depósitos vinculados","I"),
   ("A13","Estoques (realizável a LP)","I"),("A14","Instrumentos financeiros derivativos (LP)","I"),("A15","Outros (realizável a LP)","I"),
   ("A16","Total do realizável a longo prazo","S"),("A17","Investimentos","I"),("A18","Imobilizado","I"),("A19","Intangível","I"),
   ("A20","Subtotal investimentos, imobilizado e intangível","S"),("A21","Total do ativo não circulante","S"),("A22","Total do ativo","S")],
 "BP_PASSIVO_PL": [("P01","Empréstimos e financiamentos (circulante)","I"),("P02","Debêntures (circulante)","I"),("P03","Arrendamento (circulante)","I"),
   ("P04","Fornecedores","I"),("P05","Tributos e encargos sociais a recolher","I"),("P06","Encargos regulatórios a recolher (circulante)","I"),
   ("P07","Juros sobre capital próprio e dividendos a pagar","I"),("P08","Obrigações trabalhistas","I"),("P09","Instrumentos financeiros derivativos (circulante)","I"),
   ("P10","Provisões - Capex","I"),("P11","Outros (circulante)","I"),("P12","Total do passivo circulante","S"),
   ("P13","Empréstimos e financiamentos (não circulante)","I"),("P14","Debêntures (não circulante)","I"),("P15","Arrendamento (não circulante)","I"),
   ("P16","PIS e COFINS diferidos","I"),("P17","Imposto de renda e contribuição social diferidos","I"),("P18","Encargos regulatórios a recolher (não circulante)","I"),
   ("P19","Provisões (não circulante)","I"),("P20","Instrumentos financeiros derivativos (não circulante)","I"),("P21","Outros (não circulante)","I"),
   ("P22","Total do passivo não circulante","S"),("P23","Capital social","I"),("P24","Reservas de capital","I"),("P25","Reservas e retenção de lucros","I"),
   ("P26","Dividendos adicionais propostos","I"),("P27","Outros resultados abrangentes","I"),("P28","Patrimônio líquido atribuível aos controladores","S"),
   ("P29","Participação de não controladores nos fundos de investimentos","I"),("P30","Total do patrimônio líquido","S"),("P31","Total do passivo e do patrimônio líquido","S")],
 "DRE": [("R01","Receita operacional líquida","S"),("R02","Receita de infraestrutura, O&M, ganho de eficiência e outras, líquidas","I"),
   ("R03","Remuneração dos ativos da concessão, líquida","I"),("R04","Custos dos serviços de implementação, O&M e serviços prestados","I"),
   ("R05","Lucro bruto","S"),("R06","Receitas – Revisão Tarifária Periódica, líquidas","I"),("R07","Gerais e administrativas","I"),
   ("R08","Honorários da administração","I"),("R09","Outras receitas (despesas) operacionais, líquidas","I"),("R10","Resultado de equivalência patrimonial","I"),
   ("R11","Total receitas (despesas) operacionais","S"),("R12","Lucro antes do resultado financeiro e dos impostos","S"),("R13","Receitas financeiras","I"),
   ("R14","Despesas financeiras","I"),("R15","Resultado financeiro","S"),("R16","Lucro antes do IR e da CS","S"),("R17","IR e CS correntes","I"),
   ("R18","IR e CS diferidos","I"),("R19","Total IR e CS","S"),("R20","Lucro líquido do exercício","S"),("R21","Atribuível aos acionistas controladores","I"),
   ("R22","Atribuível aos acionistas não controladores","I"),("R23","Lucro básico por ação (R$)","I"),("R24","Lucro diluído por ação (R$)","I")],
 "DRA": [("O01","Lucro líquido do exercício","I"),("O02","Benefício pós-emprego – superávit (déficit) atuarial","I"),("O03","Impostos diferidos sobre benefício pós-emprego","I"),
   ("O04","Ajuste instrumento financeiro de controladas (MEP), líquido","I"),("O05","Ajuste instrumento financeiro de controladas em conjunto (MEP), líquido","I"),
   ("O06","Ajuste instrumento financeiro da controladora, líquido","I"),("O07","Total de outros resultados abrangentes","S"),("O08","Total do resultado abrangente","S"),
   ("O09","Resultado abrangente atribuível aos controladores","I"),("O10","Resultado abrangente atribuível aos não controladores","I")],
 "DFC": [("C01","Lucro líquido do exercício","I"),("C02","PIS e COFINS diferidos","I"),("C03","Depreciação e amortização","I"),("C04","IR e CS diferidos","I"),
   ("C05","Demandas judiciais","I"),("C06","Custo residual de imobilizado/intangível baixado","I"),("C07","Benefício fiscal – ágio incorporado","I"),
   ("C08","Benefício a empregados – superávit/déficit atuarial","I"),("C09","Realização de ativo da concessão na aquisição de controlada","I"),
   ("C10","Resultado de equivalência patrimonial","I"),("C11","Ativos da concessão (receitas sem caixa, nota 5.3)","I"),("C12","Rendimento sobre aplicações financeiras","I"),
   ("C13","Juros e variações cambiais sobre empréstimos, financiamentos e debêntures","I"),("C14","Transações com acionistas não controladores","I"),
   ("C15","Instrumentos financeiros","I"),("C16","Juros e variações monetárias e cambiais sobre ativos e passivos","I"),
   ("C17","Subtotal: lucro ajustado (caixa gerado nas operações)","S"),("C18","Ativos da concessão (recebimentos)","I"),("C19","Estoques","I"),
   ("C20","Tributos e contribuições a compensar","I"),("C21","Valores a receber - Secretaria da Fazenda","I"),("C22","Outros (ativos)","I"),
   ("C23","Subtotal: (aumento) diminuição de ativos","S"),("C24","Fornecedores","I"),("C25","Tributos e encargos sociais a recolher","I"),
   ("C26","IR e CS pagos","I"),("C27","Obrigações trabalhistas","I"),("C28","Encargos regulatórios a recolher","I"),("C29","Provisões","I"),("C30","Outros (passivos)","I"),
   ("C31","Subtotal: aumento (diminuição) de passivos","S"),("C32","Fluxo de caixa das atividades operacionais","S"),("C33","Caixa restrito","I"),
   ("C34","Aplicações financeiras","I"),("C35","Resgates de aplicações financeiras","I"),("C36","Imobilizado","I"),("C37","Intangível","I"),
   ("C38","Aumento de capital em investidas","I"),("C39","Adiantamento para futuro aumento de capital","I"),("C40","Dividendos recebidos","I"),
   ("C41","Fluxo de caixa das atividades de investimento","S"),("C42","Adições de empréstimos e debêntures","I"),("C43","Pagamentos de empréstimos e debêntures (principal)","I"),
   ("C44","Pagamentos de empréstimos e debêntures (juros)","I"),("C45","Pagamentos de arrendamentos","I"),("C46","Instrumentos financeiros derivativos","I"),
   ("C47","Dividendos e JCP pagos","I"),("C48","Fluxo de caixa das atividades de financiamento","S"),("C49","Aumento (diminuição) líquido de caixa","S"),
   ("C50","Caixa e equivalentes em 1º de janeiro","I"),("C51","Caixa e equivalentes em 31 de dezembro","I"),("C52","Variação em caixa e equivalentes (fim − início)","S")],
}
# linhas do F0011 (DF 2024) ausentes em relação ao F0003, para alinhamento
SKIP_F0011 = {"BP_PASSIVO_PL": ["P10", "P26"], "DRA": ["O05"], "DFC": ["C15"]}
# linha existente só no F0011 (DF 2024): inserida após P19
EXTRA_F0011 = {"BP_PASSIVO_PL": ("P19", ("P19B", "Benefício pós-emprego – déficit atuarial (não circulante; linha só na DF 2024)", "I"))}
# subtotais: código -> lista de códigos somados (para recálculo)
SUBT = {
 "A09": ["A01","A02","A03","A04","A05","A06","A07","A08"], "A16": ["A10","A11","A12","A13","A14","A15"], "A20": ["A17","A18","A19"],
 "A21": ["A16","A20"], "A22": ["A09","A21"],
 "P12": ["P01","P02","P03","P04","P05","P06","P07","P08","P09","P10","P11"], "P22": ["P13","P14","P15","P16","P17","P18","P19","P20","P21"],  # P19B (só F0011) tratado na conciliação
 "P28": ["P23","P24","P25","P26","P27"], "P30": ["P28","P29"], "P31": ["P12","P22","P30"],
 "R01": ["R02","R03"], "R05": ["R01","R04"], "R11": ["R06","R07","R08","R09","R10"], "R12": ["R05","R11"], "R15": ["R13","R14"], "R16": ["R12","R15"],
 "R19": ["R17","R18"], "R20": ["R16","R19"],
 "O07": ["O02","O03","O04","O05","O06"], "O08": ["O01","O07"],
 "C17": ["C01","C02","C03","C04","C05","C06","C07","C08","C09","C10","C11","C12","C13","C14","C15","C16"],
 "C23": ["C18","C19","C20","C21","C22"], "C31": ["C24","C25","C26","C27","C28","C29","C30"], "C32": ["C17","C23","C31"],
 "C41": ["C33","C34","C35","C36","C37","C38","C39","C40"], "C48": ["C42","C43","C44","C45","C46","C47"], "C49": ["C32","C41","C48"],
}
SUBT_DIF = {"C52": ("C51", "C50")}  # fim - início

# mapa CVM -> linhas PDF
MAPA = [
 ("BPA","1",["A22"]),("BPA","1.01",["A09"]),("BPA","1.01.01",["A01"]),("BPA","1.01.02",["A02"]),("BPA","1.01.03",["A03"]),("BPA","1.01.04",["A04"]),
 ("BPA","1.01.06",["A05"]),("BPA","1.01.08",["A06","A07","A08"]),("BPA","1.02",["A21"]),("BPA","1.02.01",["A16"]),("BPA","1.02.01.04",["A10"]),
 ("BPA","1.02.01.05",["A13"],"1.02.01.05",[]),("BPA","1.02.01.10",["A11","A12","A14","A15"],"1.02.01.10",["A11","A12","A13","A14","A15"]),("BPA","1.02.02",["A17"]),("BPA","1.02.03",["A18"]),("BPA","1.02.04",["A19"]),
 ("BPP","2",["P31"]),("BPP","2.01",["P12"]),("BPP","2.01.01",["P08"]),("BPP","2.01.02",["P04"]),("BPP","2.01.03",["P05"]),("BPP","2.01.04",["P01","P02","P03"]),
 ("BPP","2.01.04.02",["P02"]),("BPP","2.01.05",["P06","P07","P09","P10","P11"]),("BPP","2.02",["P22"]),("BPP","2.02.01",["P13","P14","P15"]),
 ("BPP","2.02.01.02",["P14"]),("BPP","2.02.02",["P18","P19B","P20","P21"]),("BPP","2.02.03",["P16","P17"]),("BPP","2.02.04",["P19"]),("BPP","2.03",["P30"]),
 ("BPP","2.03.01",["P23"]),("BPP","2.03.02",["P24"]),("BPP","2.03.04",["P25","P26"]),("BPP","2.03.08",["P27"]),
 ("DRE","3.01",["R01"]),("DRE","3.01.01",["R02"]),("DRE","3.01.02",["R03"]),("DRE","3.02",["R04"]),("DRE","3.03",["R05"]),("DRE","3.04",["R11"]),
 ("DRE","3.04.01",["R06"]),("DRE","3.04.02",["R07","R08"]),("DRE","3.04.04+3.04.05",["R09"]),("DRE","3.04.06",["R10"]),("DRE","3.05",["R12"]),
 ("DRE","3.06",["R15"]),("DRE","3.06.01",["R13"]),("DRE","3.06.02",["R14"]),("DRE","3.07",["R16"]),("DRE","3.08",["R19"]),("DRE","3.08.01",["R17"]),
 ("DRE","3.08.02",["R18"]),("DRE","3.11",["R20"]),
 ("DRA","4.01",["O01"]),("DRA","4.02",["O07"]),("DRA","4.03",["O08"]),
 ("DFC_MI","6.01",["C32"]),("DFC_MI","6.01.01",["C17"]),("DFC_MI","6.01.01.01",["C01"]),("DFC_MI","6.01.01.08",["C11"],"6.01.01.16",["C11"]),("DFC_MI","6.01.02",["C23","C31"]),
 ("DFC_MI","6.01.02.02",["C18"]),("DFC_MI","6.02",["C41"]),("DFC_MI","6.03",["C48"]),("DFC_MI","6.03.08",["C47"],"6.03.07",["C47"]),("DFC_MI","6.05",["C49"]),
 ("DFC_MI","6.05.01",["C50"]),("DFC_MI","6.05.02",["C51"]),
]
EXPL = {
 ("BPA", "1.01.03", "Consolidado"): "Taxonomia CVM: 'Contas a Receber/Clientes/Ativo da Concessão' = linha 'Ativos da concessão' (circulante) do PDF.",
 ("BPA", "1.01.08", "Consolidado"): "CVM agrupa derivativos + créditos com partes relacionadas + outros (A06+A07+A08).",
 ("BPA", "1.02.01.05", "Individual"): "No individual a CVM classifica os estoques de LP em 1.02.01.10.10 (dentro de Outros Ativos Não Circulantes); por isso 1.02.01.05 = 0 e A13 foi somado em 1.02.01.10.",
 ("BPA", "1.02.01.10", "Individual"): "Inclui estoques de LP (A13) – ver 1.02.01.05.",
 ("BPP", "2.01.05", "Consolidado"): "CVM 'Outras Obrigações' = encargos regulatórios + JCP/dividendos + derivativos + Provisões-Capex + Outros (P06+P07+P09+P10+P11).",
 ("BPP", "2.03.04", "Consolidado"): "CVM 'Reservas de Lucros' inclui o dividendo adicional proposto (P25+P26).",
 ("DFC_MI", "6.01.01.08", "Individual"): "No individual o código é 6.01.01.16.",
 ("DFC_MI", "6.03.08", "Individual"): "No individual o código é 6.03.07.",
 ("DFC_MI", "6.01.02", "Consolidado"): "CVM soma variações de ativos e passivos (C23+C31).",
}
QUADRO_DE = {"BPA": "BP_ATIVO", "BPP": "BP_PASSIVO_PL", "DRE": "DRE", "DRA": "DRA", "DFC_MI": "DFC"}
POSICAO = {"BP_ATIVO", "BP_PASSIVO_PL"}

DOCINFO = {"F0003": ("DF 2025 individuais e consolidadas, com relatório do auditor (Deloitte, 24/02/2026)", "Arquivo RI 6429; SHA-256 b798833e…; aprovada pelo CA em 24/02/2026"),
           "F0011": ("DF 2024 individuais e consolidadas, com relatório do auditor (Deloitte, 24/02/2025)", "Arquivo RI 6028; SHA-256 16f71bfe…")}
ANOS = {"F0003": ("2025", "2024"), "F0011": ("2024", "2023")}


def hdr(ws, row, cab, widths):
    for j, c in enumerate(cab, 1):
        x = ws.cell(row, j, c); x.font = Font(name=F, bold=True, color="FFFFFF", size=9); x.fill = HDR
        x.alignment = Alignment(wrap_text=True, vertical="center")
        ws.column_dimensions[L(j)].width = widths[j - 1]
    ws.freeze_panes = ws.cell(row + 1, 1)


def titulo(ws, t, nota=PREP):
    ws["A1"] = t; ws["A1"].font = Font(name=F, bold=True, size=12)
    ws["A2"] = nota; ws["A2"].font = Font(name=F, italic=True, size=8)


def main(linhas_csv, cvm_csv, out):
    rows = list(csv.DictReader(open(linhas_csv, encoding="utf-8"), delimiter=";"))
    # descarta linha de rótulo sem valores (DRE 'Custos ... 17')
    # (linha só com o número da nota '17' capturado como valor: 1 único número na linha → não é linha de valores)
    rows = [r for r in rows if sum(r[k] not in ("", None) for k in ("CTRL_2025", "CTRL_2024", "CON_2025", "CON_2024", "CTRL_2023", "CON_2023")) >= 2]
    # atribui códigos
    for doc in ("F0003", "F0011"):
        for q, lst in LAB.items():
            rr = [r for r in rows if r["doc"] == doc and r["quadro"] == q]
            codes = [c for c in lst if not (doc == "F0011" and c[0] in SKIP_F0011.get(q, []))]
            if doc == "F0011" and q in EXTRA_F0011:
                apos, novo = EXTRA_F0011[q]
                k = [c[0] for c in codes].index(apos)
                codes = codes[:k + 1] + [novo] + codes[k + 1:]
            if len(rr) != len(codes):
                raise SystemExit(f"{doc} {q}: {len(rr)} linhas x {len(codes)} rótulos")
            for r, (c, lab, t) in zip(rr, codes):
                r["cod"], r["lab"], r["tipo"] = c, lab, t
    wb = Workbook(); wb.remove(wb.active)

    # ---------------- LEIA
    ws = wb.create_sheet("LEIA")
    titulo(ws, "Dados reais – DF ISA Energia Brasil 2025 e 2024 (PDF + CVM)")
    txt = [
     "Finalidade: base editável e rastreável dos quadros (BP, DRE, DRA, DFC) e de saldos/divulgações selecionados, com conciliação PDF × CVM, comparativos e notas.",
     "Referência principal: PDF das DFs (F0003 para 2025; F0011 para 2024). Conferência: dados abertos da CVM (ZIPs F0018 e F0017). Perímetro principal: CONSOLIDADO (decisão D-001, validada em 19/10/2026).",
     "Abas de DADOS (valores digitados por script a partir do texto do PDF/CSV, em azul): DF_linhas (uma linha por valor), CVM_ISA (linhas da ISA no CSV oficial), Notas_valores (transcrições de notas).",
     "Abas de FÓRMULAS (preto): Quadros_F0003, Conc_PDF_CVM, Conc_Comparativos, Conc_Cruzadas. Nenhum resultado foi colado: altere um valor de dado e as conciliações recalculam.",
     "Convenções: valores em R$ mil (LPA em R$/ação); despesas e saídas de caixa negativas, como no PDF. ABRANGENCIA = Individual (controladora) ou Consolidado. PERIODO: posição (saldo em DT_FIM) ou fluxo (DT_INI a DT_FIM).",
     "CVM: a seleção usa ARQUIVO (grupo con/ind e demonstração), CD_CONTA, ORDEM_EXERC (ÚLTIMO = exercício corrente; PENÚLTIMO = comparativo) e DT_FIM_EXERC — não apenas DT_REFER.",
     "Não misturar: DCR/regulatório (F0197), ITR/2T26 (F0109, F0122, F0126) e valores de 2026 NÃO constam desta planilha.",
     "Reprodução: 99_Trabalho/scripts_B02/b02_extrair_dfs.py → b02_planilha_dados_reais.py (ver README_B02 em 01_Dados_reais).",
     "Legenda de cores: azul = dado de fonte; preto = fórmula; verde = referência a outra aba. Coluna 'Situação' = OK / DIFERENÇA (explicada na coluna Explicação).",
    ]
    for i, t in enumerate(txt, 4):
        ws.cell(i, 1, t).font = BLK; ws.cell(i, 1).alignment = Alignment(wrap_text=True)
    ws.column_dimensions["A"].width = 160

    # ---------------- DF_linhas (longo)
    ws = wb.create_sheet("DF_linhas")
    titulo(ws, "DF_linhas – um registro por valor extraído do PDF (dados de fonte)")
    cab = ["ID_ENTRADA", "DOC", "DOCUMENTO", "VERSAO_DOC", "PAGINA_FISICA", "LINHA_NA_PAGINA", "QUADRO", "COD", "ROTULO_PADRONIZADO", "ROTULO_NO_PDF (extraído)",
           "NOTA", "TIPO", "ABRANGENCIA", "NATUREZA", "DT_INI", "DT_FIM", "COLUNA_NO_DOC", "UNIDADE", "VALOR", "TEXTO_ORIGINAL_DA_LINHA"]
    hdr(ws, 4, cab, [26, 7, 30, 26, 8, 8, 14, 6, 44, 40, 8, 6, 12, 9, 11, 11, 13, 8, 14, 70])
    i = 5
    for r in rows:
        doc = r["doc"]; a1, a0 = ANOS[doc]
        for abr, pref in (("Individual", "CTRL"), ("Consolidado", "CON")):
            for ano, col in ((a1, "corrente"), (a0, "comparativo")):
                v = r.get(f"{pref}_{ano}", "")
                if v in ("", None):
                    continue
                v = float(v) if "." in v else int(v)
                pos = r["quadro"] in POSICAO
                unid = "R$/ação" if r["cod"] in ("R23", "R24") else "R$ mil"
                vals = [f"{doc}-p{r['pagina_fisica']}-{r['cod']}-{'IND' if abr == 'Individual' else 'CON'}-{ano}", doc, DOCINFO[doc][0], DOCINFO[doc][1],
                        int(r["pagina_fisica"]), int(r["linha_pagina"]), r["quadro"], r["cod"], r["lab"], r["rotulo"], r["nota"],
                        "Subtotal" if r["tipo"] == "S" else "Item", abr, "Posição" if pos else "Fluxo",
                        "" if pos else f"{ano}-01-01", f"{ano}-12-31", col, unid, v, r["texto_original"]]
                for j, x in enumerate(vals, 1):
                    c = ws.cell(i, j, x); c.font = BLUE if j == 19 else BLK
                ws.cell(i, 19).number_format = NUMF if unid == "R$ mil" else "0.00000"
                i += 1
    last_df = i - 1
    ws.auto_filter.ref = f"A4:T{last_df}"

    # ---------------- CVM_ISA
    cv = list(csv.DictReader(open(cvm_csv, encoding="utf-8"), delimiter=";"))
    ws = wb.create_sheet("CVM_ISA")
    titulo(ws, "CVM_ISA – linhas da ISA (CNPJ 02.998.611/0001-04) nos CSV oficiais da DFP (dados de fonte)",
           PREP + " | Fonte: F0018 dfp_cia_aberta_2025.zip e F0017 dfp_cia_aberta_2024.zip (dados.cvm.gov.br), linhas originais preservadas.")
    cab = ["FONTE_ID", "ARQUIVO", "LINHA_CSV", "DEM", "ABRANGENCIA", "DT_REFER", "VERSAO", "GRUPO_DFP", "ESCALA_MOEDA", "ORDEM_EXERC", "DT_INI_EXERC", "DT_FIM_EXERC",
           "CD_CONTA", "DS_CONTA", "VL_CONTA", "ST_CONTA_FIXA"]
    hdr(ws, 4, cab, [8, 32, 9, 8, 12, 11, 7, 44, 8, 11, 11, 11, 13, 50, 14, 8])
    i = 5
    for r in cv:
        dem = r["ARQUIVO"].split("dfp_cia_aberta_")[1].rsplit("_", 2)[0]
        abr = "Consolidado" if "_con_" in r["ARQUIVO"] else "Individual"
        vals = [r["FONTE_ID"], r["ARQUIVO"], int(r["LINHA_CSV"]), dem, abr, r["DT_REFER"], int(r["VERSAO"]), r["GRUPO_DFP"], r["ESCALA_MOEDA"], r["ORDEM_EXERC"],
                r.get("DT_INI_EXERC", "") or "", r["DT_FIM_EXERC"], r["CD_CONTA"], r["DS_CONTA"], float(r["VL_CONTA"]), r["ST_CONTA_FIXA"]]
        for j, x in enumerate(vals, 1):
            c = ws.cell(i, j, x); c.font = BLUE if j == 15 else BLK
        ws.cell(i, 15).number_format = NUMF
        i += 1
    last_cv = i - 1
    ws.auto_filter.ref = f"A4:P{last_cv}"

    # ---------------- Notas_valores
    NV = [
     ("N01", "F0003", 45, "5.3", "Serviços de O&M (ativo financeiro)", "Individual", "2025-12-31", 95332), ("N02", "F0003", 45, "5.3", "Serviços de O&M (ativo financeiro)", "Individual", "2024-12-31", 136678),
     ("N03", "F0003", 45, "5.3", "Serviços de O&M (ativo financeiro)", "Consolidado", "2025-12-31", 158263), ("N04", "F0003", 45, "5.3", "Serviços de O&M (ativo financeiro)", "Consolidado", "2024-12-31", 193064),
     ("N05", "F0003", 45, "5.3", "Lei 12.783 SE – componente financeiro", "Consolidado", "2025-12-31", 3112255), ("N06", "F0003", 45, "5.3", "Lei 12.783 SE – componente financeiro", "Consolidado", "2024-12-31", 4990315),
     ("N07", "F0003", 45, "5.3", "Lei 12.783 SE – componente econômico", "Consolidado", "2025-12-31", 3111847), ("N08", "F0003", 45, "5.3", "Lei 12.783 SE – componente econômico", "Consolidado", "2024-12-31", 3113419),
     ("N09", "F0003", 45, "5.3", "Implementação da infraestrutura", "Consolidado", "2025-12-31", 30048933), ("N10", "F0003", 45, "5.3", "Implementação da infraestrutura", "Consolidado", "2024-12-31", 22750025),
     ("N11", "F0003", 45, "5.3", "Ativo contratual (total)", "Consolidado", "2025-12-31", 36273035), ("N12", "F0003", 45, "5.3", "Ativo contratual (total)", "Consolidado", "2024-12-31", 30853759),
     ("N13", "F0003", 45, "5.3", "Ativos da concessão (total)", "Consolidado", "2025-12-31", 36431298), ("N14", "F0003", 45, "5.3", "Ativos da concessão (total)", "Consolidado", "2024-12-31", 31046823),
     ("N15", "F0003", 45, "5.3", "Ativo contratual (total)", "Individual", "2025-12-31", 28156926), ("N16", "F0003", 45, "5.3", "Ativos da concessão (total)", "Individual", "2025-12-31", 28252258),
     ("N20", "F0003", 47, "5.5", "Saldo inicial 2025 (saldos em 2024)", "Consolidado", "2025", 31046823), ("N21", "F0003", 47, "5.5", "Receita de infraestrutura (nota 16.3)", "Consolidado", "2025", 6330048),
     ("N22", "F0003", 47, "5.5", "Perda de eficiência na implementação (nota 16.3)", "Consolidado", "2025", -10513), ("N23", "F0003", 47, "5.5", "Remuneração dos ativos da concessão (nota 16.3)", "Consolidado", "2025", 2949237),
     ("N24", "F0003", 47, "5.5", "Receita de operação e manutenção (nota 16.3)", "Consolidado", "2025", 1264867), ("N25", "F0003", 47, "5.5", "Receitas – RTP (nota 18)", "Consolidado", "2025", 159203),
     ("N26", "F0003", 47, "5.5", "Perda esperada para créditos de liquidação duvidosa", "Consolidado", "2025", -4286), ("N27", "F0003", 47, "5.5", "Recebimentos", "Consolidado", "2025", -5304081),
     ("N28", "F0003", 47, "5.5", "Saldo final 2025", "Consolidado", "2025", 36431298),
     ("N30", "F0003", 48, "6", "Debêntures", "Consolidado", "2025-12-31", 15192514), ("N31", "F0003", 48, "6", "Empréstimos e financiamentos", "Consolidado", "2025-12-31", 759199),
     ("N32", "F0003", 48, "6", "Arrendamento", "Consolidado", "2025-12-31", 55636), ("N33", "F0003", 48, "6", "Dívida bruta", "Consolidado", "2025-12-31", 16007349),
     ("N34", "F0003", 48, "6", "Dívida líquida", "Consolidado", "2025-12-31", 13842363), ("N35", "F0003", 48, "6", "Debêntures", "Consolidado", "2024-12-31", 12502473),
     ("N36", "F0003", 48, "6", "Dívida bruta", "Consolidado", "2024-12-31", 13273804), ("N37", "F0003", 48, "6", "Dívida líquida", "Consolidado", "2024-12-31", 9873062),
     ("N40", "F0003", 60, "7.2", "Equivalência patrimonial (movimentação dos investimentos)", "Individual", "2025", 1291105),
     ("N41", "F0003", 60, "7.2", "Realização de aquisição de controle", "Individual", "2025", 2960),
     ("N50", "F0003", 136, "Relatório do auditor (KAM)", "Ativo de contrato citado no KAM", "Consolidado", "2025-12-31", 36273035),
     ("N51", "F0003", 136, "Relatório do auditor (KAM)", "Ativo de contrato citado no KAM", "Individual", "2025-12-31", 28156926),
     ("N52", "F0011", 138, "Relatório do auditor (KAM)", "Ativo de contrato citado no KAM", "Consolidado", "2024-12-31", 22750025),
     ("N53", "F0003", 135, "Relatório do auditor (Ênfase) / nota 9", "Valores a receber Secretaria da Fazenda (Lei 4.819/58), líquidos", "Consolidado", "2025-12-31", 2760806),
     ("N60", "F0003", 3, "Relatório da Administração", "Lucro líquido IFRS citado na mensagem da administração (R$ milhões × 1.000)", "Individual", "2025", 2477900),
     ("N61", "F0003", 36, "1.2", "RAP total ISA Energia Brasil e controladas (ciclo 06/25)", "Consolidado", "2025-06", 5623324),
     ("N62", "F0003", 36, "1.2", "RAP total das controladas em conjunto (100%)", "Controladas em conjunto", "2025-06", 1533540),
     ("N63", "F0003", 36, "1.2", "Participação da Companhia na RAP das controladas em conjunto", "Controladas em conjunto", "2025-06", 775645),
    ]
    ws = wb.create_sheet("Notas_valores")
    titulo(ws, "Notas_valores – valores transcritos de notas e relatórios (dados de fonte; leitura do texto extraído do PDF)")
    cab = ["ID", "DOC", "PAGINA_FISICA", "NOTA/SECAO", "DESCRICAO", "ABRANGENCIA", "DATA/PERIODO", "VALOR (R$ mil)"]
    hdr(ws, 4, cab, [6, 7, 8, 26, 60, 18, 12, 16])
    for i, x in enumerate(NV, 5):
        for j, v in enumerate(x, 1):
            c = ws.cell(i, j, v); c.font = BLUE if j == 8 else BLK
        ws.cell(i, 8).number_format = NUMF
    nv_row = {x[0]: i for i, x in enumerate(NV, 5)}
    NVC = lambda k: f"Notas_valores!$H${nv_row[k]}"

    # helper de fórmula sobre DF_linhas
    def f_df(doc, cod, abr, ano):
        return (f'SUMIFS(DF_linhas!$S$5:$S${last_df},DF_linhas!$B$5:$B${last_df},"{doc}",DF_linhas!$H$5:$H${last_df},"{cod}",'
                f'DF_linhas!$M$5:$M${last_df},"{abr}",DF_linhas!$P$5:$P${last_df},"{ano}-12-31")')

    def f_cv(arq, cod, ordem, dtfim):
        cods = cod.split("+")
        return "+".join(f'SUMIFS(CVM_ISA!$O$5:$O${last_cv},CVM_ISA!$B$5:$B${last_cv},"{arq}",CVM_ISA!$M$5:$M${last_cv},"{c}",'
                        f'CVM_ISA!$J$5:$J${last_cv},"{ordem}",CVM_ISA!$L$5:$L${last_cv},"{dtfim}")' for c in cods)

    # ---------------- Quadros_F0003 (visão por fórmulas + recálculo dos subtotais)
    ws = wb.create_sheet("Quadros_F0003")
    titulo(ws, "Quadros da DF 2025 (F0003) – valores puxados de DF_linhas por fórmula; subtotais recalculados")
    cab = ["QUADRO", "COD", "ROTULO", "NOTA", "PÁG.", "TIPO", "IND 2025", "IND 2024", "CON 2025", "CON 2024",
           "Recalc IND 2025", "Recalc IND 2024", "Recalc CON 2025", "Recalc CON 2024", "Dif IND 2025", "Dif IND 2024", "Dif CON 2025", "Dif CON 2024"]
    hdr(ws, 4, cab, [12, 6, 50, 7, 5, 8] + [13] * 12)
    pos = {}
    i = 5
    f3 = [r for r in rows if r["doc"] == "F0003"]
    for r in f3:
        pos[r["cod"]] = i
        ws.cell(i, 1, r["quadro"]); ws.cell(i, 2, r["cod"]); ws.cell(i, 3, r["lab"]); ws.cell(i, 4, r["nota"]); ws.cell(i, 5, int(r["pagina_fisica"]))
        ws.cell(i, 6, "Subtotal" if r["tipo"] == "S" else "Item")
        for k, (abr, ano) in enumerate((("Individual", "2025"), ("Individual", "2024"), ("Consolidado", "2025"), ("Consolidado", "2024"))):
            c = ws.cell(i, 7 + k, "=" + f_df("F0003", r["cod"], abr, ano)); c.font = Font(name=F, size=9, color="008000")
            c.number_format = NUMF if r["cod"] not in ("R23", "R24") else "0.00000"
        if r["tipo"] == "S":
            for c in range(1, 19):
                ws.cell(i, c).fill = SUB
        for c in range(1, 7):
            ws.cell(i, c).font = BLK
        i += 1
    for cod, parts in list(SUBT.items()) + [(k, v) for k, v in SUBT_DIF.items()]:
        rr = pos[cod]
        for k in range(4):
            col = L(7 + k)
            if cod in SUBT_DIF:
                a, b = SUBT_DIF[cod]; fml = f"={col}{pos[a]}-{col}{pos[b]}"
            else:
                fml = "=" + "+".join(f"{col}{pos[p]}" for p in parts)
            ws.cell(rr, 11 + k, fml).number_format = NUMF
            ws.cell(rr, 15 + k, f"={col}{rr}-{L(11 + k)}{rr}").number_format = NUMF
            ws.cell(rr, 11 + k).font = BLK; ws.cell(rr, 15 + k).font = BLK
    last_q = i - 1
    ws.cell(last_q + 2, 1, "Total de diferenças nos subtotais (deve ser 0):").font = Font(name=F, bold=True, size=9)
    ws.cell(last_q + 2, 15, f"=SUMPRODUCT(ABS(O5:R{last_q}))").number_format = NUMF

    # ---------------- Conc_PDF_CVM
    ws = wb.create_sheet("Conc_PDF_CVM")
    titulo(ws, "Conciliação PDF (referência) × CVM (conferência) – por conta, abrangência, exercício e ORDEM_EXERC")
    cab = ["DEM", "CD_CONTA CVM", "DS_CONTA (CVM)", "Linhas PDF somadas", "ABRANGÊNCIA", "DFP (DT_REFER)", "ORDEM_EXERC", "DT_FIM_EXERC", "DOC PDF", "Coluna do PDF",
           "Valor PDF", "Valor CVM", "Diferença", "Situação", "Explicação"]
    hdr(ws, 4, cab, [7, 14, 40, 18, 12, 11, 11, 11, 7, 12, 14, 14, 12, 11, 60])
    dsmap = {}
    for r in cv:
        dsmap.setdefault((r["ARQUIVO"].split("dfp_cia_aberta_")[1].rsplit("_", 2)[0], r["CD_CONTA"]), r["DS_CONTA"])
    i = 5
    for item in MAPA:
        dem = item[0]
        for abr, g in (("Consolidado", "con"), ("Individual", "ind")):
            cod, parts = (item[3], item[4]) if (abr == "Individual" and len(item) > 3) else (item[1], item[2])
            for dfp, doc_main in (("2025", "F0003"), ("2024", "F0011")):
                for ordem, anodoc in (("ÚLTIMO", dfp), ("PENÚLTIMO", str(int(dfp) - 1))):
                    arq = f"dfp_cia_aberta_{dem}_{g}_{dfp}.csv"
                    dt = f"{anodoc}-12-31"
                    pdf = "+".join(f_df(doc_main, p, abr, anodoc) for p in parts) if parts else "0"
                    ws.cell(i, 1, dem); ws.cell(i, 2, cod); ws.cell(i, 3, dsmap.get((dem, cod.split("+")[0]), "")); ws.cell(i, 4, "+".join(parts))
                    ws.cell(i, 5, abr); ws.cell(i, 6, f"{dfp}-12-31"); ws.cell(i, 7, ordem); ws.cell(i, 8, dt); ws.cell(i, 9, doc_main)
                    ws.cell(i, 10, "corrente" if ordem == "ÚLTIMO" else "comparativo")
                    ws.cell(i, 11, "=" + pdf); ws.cell(i, 12, "=" + f_cv(arq, cod, ordem, dt))
                    ex = EXPL.get((dem, cod, abr), "")
                    ws.cell(i, 15, ex)
                    ws.cell(i, 13, f"=K{i}-L{i}"); ws.cell(i, 14, f'=IF(ABS(M{i})<0.5,"OK","DIFERENÇA")')
                    for c in (11, 12, 13):
                        ws.cell(i, c).number_format = NUMF
                    for c in range(1, 16):
                        ws.cell(i, c).font = BLK
                    i += 1
    last_c = i - 1
    ws.auto_filter.ref = f"A4:O{last_c}"
    ws.cell(last_c + 2, 1, "Linhas com DIFERENÇA:").font = Font(name=F, bold=True, size=9)
    ws.cell(last_c + 2, 4, f'=COUNTIF(N5:N{last_c},"DIFERENÇA")')
    ws.cell(last_c + 3, 1, "Linhas conciliadas:").font = Font(name=F, bold=True, size=9)
    ws.cell(last_c + 3, 4, f"=COUNTA(N5:N{last_c})")

    # ---------------- Conc_Comparativos (F0003 comparativo 2024 × F0011 corrente 2024)
    ws = wb.create_sheet("Conc_Comparativos")
    titulo(ws, "Comparativos: coluna 2024 do F0003 (DF 2025) × coluna 2024 do F0011 (DF 2024 originalmente publicada)")
    cab = ["QUADRO", "COD", "ROTULO", "ABRANGÊNCIA", "F0003 – 2024 (comparativo)", "F0011 – 2024 (original)", "Diferença", "Situação", "Explicação"]
    hdr(ws, 4, cab, [12, 6, 50, 12, 16, 16, 12, 11, 70])
    i = 5
    for r in f3:
        for abr in ("Individual", "Consolidado"):
            ws.cell(i, 1, r["quadro"]); ws.cell(i, 2, r["cod"]); ws.cell(i, 3, r["lab"]); ws.cell(i, 4, abr)
            ws.cell(i, 5, "=" + f_df("F0003", r["cod"], abr, "2024")); ws.cell(i, 6, "=" + f_df("F0011", r["cod"], abr, "2024"))
            ws.cell(i, 7, f"=E{i}-F{i}"); ws.cell(i, 8, f'=IF(ABS(G{i})<0.5,"OK","DIFERENÇA")')
            if r["cod"] in ("P10", "P11"):
                ws.cell(i, 9, "Reclassificação de apresentação: no F0011 (p.23) 'Outros' do passivo circulante incluía 'Provisões - Capex'; no F0003 (p.24) a linha foi aberta. P10+P11 do F0003 = P11 do F0011 (ver linha de soma abaixo). Sem efeito no total do passivo circulante.")
            for c in (5, 6, 7):
                ws.cell(i, c).number_format = NUMF if r["cod"] not in ("R23", "R24") else "0.00000"
            for c in range(1, 10):
                ws.cell(i, c).font = BLK
            i += 1
    for abr in ("Individual", "Consolidado"):
        ws.cell(i, 1, "BP_PASSIVO_PL"); ws.cell(i, 2, "P10+P11"); ws.cell(i, 3, "Provisões - Capex + Outros (circulante)"); ws.cell(i, 4, abr)
        ws.cell(i, 5, "=" + f_df("F0003", "P10", abr, "2024") + "+" + f_df("F0003", "P11", abr, "2024"))
        ws.cell(i, 6, "=" + f_df("F0011", "P10", abr, "2024") + "+" + f_df("F0011", "P11", abr, "2024"))
        ws.cell(i, 7, f"=E{i}-F{i}"); ws.cell(i, 8, f'=IF(ABS(G{i})<0.5,"OK","DIFERENÇA")')
        ws.cell(i, 9, "Soma conciliadora da reclassificação P10/P11")
        for c in (5, 6, 7):
            ws.cell(i, c).number_format = NUMF
        for c in range(1, 10):
            ws.cell(i, c).font = BLK
        i += 1
    last_cc = i - 1
    ws.cell(last_cc + 2, 1, "Linhas com DIFERENÇA:").font = Font(name=F, bold=True, size=9)
    ws.cell(last_cc + 2, 5, f'=COUNTIF(H5:H{last_cc},"DIFERENÇA")')

    # ---------------- Conc_Cruzadas (equação patrimonial, entre demonstrações e notas)
    ws = wb.create_sheet("Conc_Cruzadas")
    titulo(ws, "Conciliações cruzadas – equação patrimonial, entre demonstrações, com notas e com o relatório do auditor")
    cab = ["ID", "Verificação", "Fonte A", "Valor A", "Fonte B", "Valor B", "Diferença (A−B)", "Situação", "Explicação / tratamento"]
    hdr(ws, 4, cab, [6, 52, 30, 15, 34, 15, 13, 11, 70])
    Q = lambda cod, col: f"Quadros_F0003!{col}{pos[cod]}"  # col G=IND25 H=IND24 I=CON25 J=CON24
    X = [
     ("X01", "Equação patrimonial – CON 2025: Ativo = Passivo + PL", "A22 CON 2025", Q("A22", "I"), "P12+P22+P30 CON 2025", f"{Q('P12','I')}+{Q('P22','I')}+{Q('P30','I')}", ""),
     ("X02", "Equação patrimonial – CON 2024", "A22 CON 2024", Q("A22", "J"), "P12+P22+P30 CON 2024", f"{Q('P12','J')}+{Q('P22','J')}+{Q('P30','J')}", ""),
     ("X03", "Equação patrimonial – IND 2025", "A22 IND 2025", Q("A22", "G"), "P12+P22+P30 IND 2025", f"{Q('P12','G')}+{Q('P22','G')}+{Q('P30','G')}", ""),
     ("X04", "Equação patrimonial – IND 2024", "A22 IND 2024", Q("A22", "H"), "P12+P22+P30 IND 2024", f"{Q('P12','H')}+{Q('P22','H')}+{Q('P30','H')}", ""),
     ("X05", "PL dos controladores: individual = consolidado (nota 2.1, F0003 p.39) – 2025", "P28 IND 2025", Q("P28", "G"), "P28 CON 2025", Q("P28", "I"), ""),
     ("X06", "Lucro: DRE × DRA – CON 2025", "R20 CON 2025 (p.25)", Q("R20", "I"), "O01 CON 2025 (p.26)", Q("O01", "I"), ""),
     ("X07", "Lucro: DRE × DFC – CON 2025", "R20 CON 2025 (p.25)", Q("R20", "I"), "C01 CON 2025 (p.29)", Q("C01", "I"),
      "Diferença de R$ 1 mil: arredondamento na DFC consolidada (2.511.014 × 2.511.015). Imaterial; registrar como observação (sem ajuste)."),
     ("X08", "Lucro: DRE × DFC – IND 2025", "R20 IND 2025", Q("R20", "G"), "C01 IND 2025", Q("C01", "G"), ""),
     ("X09", "Lucro atribuído: controladores + não controladores = lucro – CON 2025", "R21+R22", f"{Q('R21','I')}+{Q('R22','I')}", "R20", Q("R20", "I"), ""),
     ("X10", "Lucro dos controladores: CON (R21) = IND (R20)", "R21 CON 2025", Q("R21", "I"), "R20 IND 2025", Q("R20", "G"), ""),
     ("X11", "Caixa final DFC = caixa no BP – CON 2025", "C51 CON 2025 (p.30)", Q("C51", "I"), "A01 CON 2025 (p.23)", Q("A01", "I"), ""),
     ("X12", "Caixa inicial DFC 2025 = caixa no BP 2024 – CON", "C50 CON 2025", Q("C50", "I"), "A01 CON 2024", Q("A01", "J"), ""),
     ("X13", "Caixa final DFC = caixa no BP – IND 2025", "C51 IND 2025", Q("C51", "G"), "A01 IND 2025", Q("A01", "G"), ""),
     ("X14", "Equivalência: DRE × DFC – IND 2025", "R10 IND 2025 (p.25)", Q("R10", "G"), "−C10 IND 2025 (p.29)", f"-{Q('C10','G')}",
      "Diferença 2.961 = realização de aquisição de controle 2.960 (nota 7.2, p.60) incluída na DRE + 1 de arredondamento (nota 7.2 total 1.291.105 × DFC 1.291.104). Ver X15."),
     ("X15", "Equivalência DRE IND = nota 7.2 (equivalência + realização aquisição de controle)", "R10 IND 2025", Q("R10", "G"), "N40+N41 (nota 7.2 p.60)", f"{NVC('N40')}+{NVC('N41')}", ""),
     ("X16", "Nota 5.3: ativos da concessão total = BP circulante + não circulante – CON 2025", "N13 (p.45)", NVC("N13"), "A03+A10 CON 2025", f"{Q('A03','I')}+{Q('A10','I')}", ""),
     ("X17", "Nota 5.3 – CON 2024", "N14 (p.45)", NVC("N14"), "A03+A10 CON 2024", f"{Q('A03','J')}+{Q('A10','J')}", ""),
     ("X18", "Nota 5.3: ativo contratual = SE financeiro + SE econômico + implementação – CON 2025", "N11", NVC("N11"), "N05+N07+N09", f"{NVC('N05')}+{NVC('N07')}+{NVC('N09')}", ""),
     ("X19", "Nota 5.3: total = ativo financeiro O&M + ativo contratual – CON 2025", "N13", NVC("N13"), "N03+N11", f"{NVC('N03')}+{NVC('N11')}", ""),
     ("X20", "Nota 5.5: saldo inicial + movimentos = saldo final – CON 2025", "N20+…+N27", "+".join(NVC(k) for k in ["N20","N21","N22","N23","N24","N25","N26","N27"]), "N28 (p.47)", NVC("N28"), ""),
     ("X21", "Nota 5.5 recebimentos = DFC 'Ativos da concessão' (variação de ativos) – CON 2025", "−N27", f"-{NVC('N27')}", "C18 CON 2025 (p.29)", Q("C18", "I"), ""),
     ("X22", "Nota 5.5 movimentos sem caixa (exceto PECLD) = DFC ajuste 'Ativos da concessão' – CON 2025", "N21+N22+N23+N24+N25+N26", "+".join(NVC(k) for k in ["N21","N22","N23","N24","N25","N26"]), "−C11 CON 2025", f"-{Q('C11','I')}",
      "O ajuste da DFC (10.688.556) iguala os movimentos de receita da nota 5.5 líquidos da perda esperada (4.286)."),
     ("X23", "KAM 2025: ativo de contrato consolidado = nota 5.3 ativo contratual", "N50 (F0003 p.136)", NVC("N50"), "N11 (p.45)", NVC("N11"), ""),
     ("X24", "KAM 2025: ativo de contrato da controladora = nota 5.3", "N51 (p.136)", NVC("N51"), "N15 (p.45)", NVC("N15"), ""),
     ("X25", "KAM 2024 (F0011 p.138) × nota 5.3 ativo contratual total 2024", "N52", NVC("N52"), "N12 (F0003 p.45)", NVC("N12"),
      "O KAM de 2024 cita 22.750.025 = apenas 'Implementação da infraestrutura' 2024 (N10), não o ativo contratual total (30.853.759). Critério de citação diferente entre os relatórios de 2024 e 2025; não é erro de saldo. Ver X26."),
     ("X26", "KAM 2024 = componente 'Implementação da infraestrutura' 2024", "N52", NVC("N52"), "N10", NVC("N10"), ""),
     ("X27", "Diferença BP × KAM 2025 explicada pelo ativo financeiro O&M (resolve P05)", "(A03+A10) − N50", f"{Q('A03','I')}+{Q('A10','I')}-{NVC('N50')}", "N03 Serviços de O&M", NVC("N03"), ""),
     ("X28", "Nota 6: dívida bruta = empréstimos + debêntures + arrendamentos do BP – CON 2025", "N33 (p.48)", NVC("N33"),
      "P01+P02+P03+P13+P14+P15", "+".join(Q(c, "I") for c in ["P01","P02","P03","P13","P14","P15"]), ""),
     ("X29", "Nota 6: debêntures = circulante + não circulante – CON 2025", "N30", NVC("N30"), "P02+P14", f"{Q('P02','I')}+{Q('P14','I')}", ""),
     ("X30", "Nota 6: dívida líquida = dívida bruta − caixa − aplicações – CON 2025", "N34", NVC("N34"), "N33−A01−A02", f"{NVC('N33')}-{Q('A01','I')}-{Q('A02','I')}", ""),
     ("X31", "Ênfase do auditor (p.135) = BP valores a receber SEFAZ – CON 2025", "N53", NVC("N53"), "A11 CON 2025", Q("A11", "I"), ""),
     ("X32", "Relatório da Administração (p.3): 'lucro líquido IFRS de R$ 2.477,9 milhões' × DRE", "N60", NVC("N60"), "R20 IND 2025 (p.25)", Q("R20", "G"),
      "Diferença de R$ 30,0 milhões: o RA cita 2.477,9; a DRE apresenta 2.447,9 (controladora) e 2.511,0 (consolidado). Indício de erro de digitação em 'outras informações' (relevante para NBC TA 720, fora do escopo 200–600, e para o PT 520). Fato registrado; não alterado."),
     ("X33", "DRE RTP (R06) × nota 5.5 RTP – CON 2025", "R06 CON 2025", Q("R06", "I"), "N25", NVC("N25"),
      "Diferença 260 a explicar pela nota 18 (p.102–104): a DRE apresenta valor líquido de tributos/outros componentes. Pendência P12."),
    ]
    for i, (idn, desc, fa, va, fb, vb, ex) in enumerate(X, 5):
        ws.cell(i, 1, idn); ws.cell(i, 2, desc); ws.cell(i, 3, fa); ws.cell(i, 4, "=" + va); ws.cell(i, 5, fb); ws.cell(i, 6, "=" + vb)
        ws.cell(i, 7, f"=D{i}-F{i}"); ws.cell(i, 8, f'=IF(ABS(G{i})<0.5,"OK","DIFERENÇA")'); ws.cell(i, 9, ex)
        for c in (4, 6, 7):
            ws.cell(i, c).number_format = NUMF
        for c in range(1, 10):
            ws.cell(i, c).font = BLK; ws.cell(i, c).alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(out)
    print("ok", last_df - 4, "valores PDF;", last_cv - 4, "linhas CVM;", last_c - 4, "conciliações PDF×CVM")


if __name__ == "__main__":
    main(*sys.argv[1:4])
