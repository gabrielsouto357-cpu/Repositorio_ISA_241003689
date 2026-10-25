# -*- coding: utf-8 -*-
"""
Bloco 02 - Extração rastreável dos quadros (BP, DRE, DRA, DFC) das DFs da ISA Energia Brasil.

Lê o texto de cada página física com `pdftotext -layout` e atribui cada valor à coluna
(Controladora/Consolidado x exercício) pela posição horizontal do número em relação aos anos do cabeçalho.
Cada linha extraída guarda: documento (ID Fxxxx), página física, texto original da linha, nota, rótulo.
Não corrige valores: linhas que não fecham são sinalizadas na conciliação.

Uso: python b02_extrair_dfs.py <F0003.pdf> <F0011.pdf> <saida.csv>
"""
import csv, re, subprocess, sys

NUM = re.compile(r"^\(?-?\d{1,3}(?:\.\d{3})*(?:,\d+)?\)?$|^-$")

QUADROS = {  # (doc, pdf_idx) -> lista de (pagina, quadro)
    "F0003": [(23, "BP_ATIVO"), (24, "BP_PASSIVO_PL"), (25, "DRE"), (26, "DRA"), (29, "DFC"), (30, "DFC")],
    "F0011": [(22, "BP_ATIVO"), (23, "BP_PASSIVO_PL"), (24, "DRE"), (25, "DRA"), (28, "DFC"), (29, "DFC")],
}
ANOS = {"F0003": ("2025", "2024"), "F0011": ("2024", "2023")}


def valor(tok):
    if tok == "-":
        return 0
    neg = tok.startswith("(") or tok.startswith("-")
    t = tok.strip("()-").replace(".", "")
    v = float(t.replace(",", ".")) if "," in t else int(t)
    return -v if neg else v


def texto_pagina(pdf, p):
    return subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), pdf, "-"],
                          capture_output=True, check=True).stdout.decode("utf-8")


def tokens(linha):
    """Retorna lista de (inicio, fim, texto) para blocos separados por 2+ espaços."""
    return [(m.start(), m.end(), m.group(0)) for m in re.finditer(r"\S+(?: \S+)*", linha)]


def extrair(doc, pdf):
    a1, a0 = ANOS[doc]
    saida = []
    for pag, quadro in QUADROS[doc]:
        linhas = texto_pagina(pdf, pag).splitlines()
        # cabeçalho: linha com os quatro anos
        cols = None
        for l in linhas:
            anos = [(m.end()) for m in re.finditer(r"\b(%s|%s)\b" % (a1, a0), l)]
            if len(anos) == 4:
                cols = anos
                break
        if not cols:
            raise SystemExit(f"cabeçalho não encontrado {doc} p{pag}")
        nomes = ["CTRL_" + a1, "CTRL_" + a0, "CON_" + a1, "CON_" + a0]
        pend, secao, meia = [], "", None
        for nl, l in enumerate(linhas, 1):
            if not l.strip() or re.search(r"\b%s\b.*\b%s\b" % (a1, a0), l) or "Controladora" in l:
                continue
            tk = tokens(l)
            nums = [t for t in tk if NUM.match(t[2].replace(" ", "")) and t[0] > cols[0] - 25]
            # números colados por um só espaço (ex.: '(41.132) 409.297') — separar
            exp = []
            for s, e, t in nums:
                partes = t.split(" ")
                pos = s
                for pt in partes:
                    exp.append((pos, pos + len(pt), pt))
                    pos += len(pt) + 1
            nums = [x for x in exp if NUM.match(x[2])]
            rot_tk = [t for t in tk if t[1] <= (nums[0][0] if nums else 10**6) and not NUM.match(t[2].replace(" ", ""))]
            rot = " ".join(t[2] for t in rot_tk)
            nota = ""
            m = re.search(r"\s(\d{1,2}(?:\.\d{1,2}){0,2}(?: e)?|\d{1,2}\.\d \(\w+\))$", " " + rot)
            if m and nums:
                nota = m.group(1)
                rot = rot[: len(rot) - len(nota)].strip()
            if not nums:
                pend.append(l.strip())
                continue
            vals = {}
            for s, e, t in nums:
                c = min(range(4), key=lambda i: abs(cols[i] - e))
                vals[nomes[c]] = valor(t)
            if len(vals) == 2 and meia is None and len(nums) == 2 and not re.search(r"controladores|por ação", rot):
                meia = (vals, rot, nota, nl, l)  # linha partida em duas (ex.: honorários)
                continue
            if meia is not None and set(meia[0]) & set(vals):
                # colunas coincidem: a linha anterior era completa por si (ex.: controladores/não controladores)
                v0, r0, n0, nl0, l0 = meia
                saida.append({"doc": doc, "pagina_fisica": pag, "linha_pagina": nl0, "quadro": quadro, "secao": secao,
                              "rotulo": re.sub(r"\s+", " ", r0), "nota": n0, **{k: v0.get(k, "") for k in nomes},
                              "texto_original": re.sub(r"\s{2,}", "  ", l0.strip())})
                meia = None
            if meia is not None:
                v0, r0, n0, nl0, l0 = meia
                vals = {**v0, **vals}
                rot = (r0 + " " + rot).strip()
                nota = (n0 + " " + nota).strip()
                l = l0.rstrip() + " || " + l.strip()
                meia = None
            # rótulo: se a linha não tem texto, ou começa minúscula, junta com linhas pendentes
            if pend and (not rot or rot[0].islower() or pend[-1].endswith((",", "e", "de", "da", "do", "ao", "pelas", "para o", "nos", "na", "sobre", "–", "-"))):
                rot = " ".join(pend + [rot]).strip()
                pend = []
            elif pend:
                secao = pend[-1]
                pend = []
            saida.append({"doc": doc, "pagina_fisica": pag, "linha_pagina": nl, "quadro": quadro, "secao": secao,
                          "rotulo": re.sub(r"\s+", " ", rot), "nota": nota, **{k: vals.get(k, "") for k in nomes},
                          "texto_original": re.sub(r"\s{2,}", "  ", l.strip())})
    return saida


if __name__ == "__main__":
    f3, f11, out = sys.argv[1:4]
    linhas = extrair("F0003", f3) + extrair("F0011", f11)
    campos = ["doc", "pagina_fisica", "linha_pagina", "quadro", "secao", "rotulo", "nota",
              "CTRL_2025", "CTRL_2024", "CON_2025", "CON_2024", "CTRL_2023", "CON_2023", "texto_original"]
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        for r in linhas:
            w.writerow({k: r.get(k, "") for k in campos})
    print(len(linhas), "linhas extraídas")
