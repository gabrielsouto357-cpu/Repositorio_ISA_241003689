# -*- coding: utf-8 -*-
"""Checa se cada PT tem os campos do MODELO_PT e se todo procedimento tem modalidade. Uso: python b03_checar_pts.py PT_EC.md PT_200.md ..."""
import re, sys, json
REQ = {"Código/título": r"^# PT ", "Versão/estado": r"\*\*Versão:\*\*.*\*\*Estado:\*\*", "Norma e itens": r"\*\*Norma e itens:\*\*",
       "Entidade/período/perímetro": r"\*\*Entidade / período / perímetro:\*\*", "1 Objetivo": r"^## 1\. Objetivo", "2 Afirmações e riscos": r"^## 2\. Afirmações",
       "3 População/fontes": r"^## 3\. População", "4 Procedimentos": r"^## 4\. Procedimentos", "5 Evidências/ref.": r"^## 5\. Evidências",
       "6 Resultados/exceções": r"^## 6\. Resultados", "7 Conclusão": r"^## 7\. Conclusão", "8 Limitações": r"^## 8\. Limitações",
       "9 Requisito×orientação×julgamento": r"^## 9\. Requisito", "Preparador e data": r"Preparado por: matrícula 241003689 em \d{4}-\d{2}-\d{2}",
       "Revisão humana em branco": r"Revisão humana: _+ \(em branco\)", "Revisão automatizada": r"Revisão automatizada: RV-"}
res = {}
for f in sys.argv[1:]:
    s = open(f, encoding="utf-8").read()
    falt = [k for k, p in REQ.items() if not re.search(p, s, re.M)]
    sec = s[s.find("## 4. Procedimentos"):s.find("## 5.")]
    linhas = [l for l in sec.splitlines() if re.match(r"^\| \d+ \|", l)]
    sem_mod = [l[:40] for l in linhas if not re.search(r"\[(RP|PA|SD)\]", l)]
    res[f.split("/")[-1]] = {"campos_faltantes": falt, "procedimentos": len(linhas), "procedimentos_sem_modalidade": sem_mod}
print(json.dumps(res, ensure_ascii=False, indent=1))
