from pathlib import Path
import csv,json,importlib.util
from decimal import Decimal
import argparse
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--output',type=Path);args=p.parse_args();R=args.root.resolve();W=args.output.resolve() if args.output else R/'04_Testes/B12/fechamento_22_10';f=R/'99_Trabalho/scripts_B02/b02_planilha_dados_reais.py'
spec=importlib.util.spec_from_file_location('b02_readonly',f);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
rows=list(csv.DictReader((W/'pdf_linhas_reextraidas.csv').open(encoding='utf-8'),delimiter=';'));rows=[r for r in rows if sum(r[k] not in ('',None) for k in ['CTRL_2025','CTRL_2024','CON_2025','CON_2024','CTRL_2023','CON_2023'])>=2]
for doc in ['F0003','F0011']:
 for q,lst in m.LAB.items():
  rr=[r for r in rows if r['doc']==doc and r['quadro']==q];codes=[c for c in lst if not(doc=='F0011' and c[0] in m.SKIP_F0011.get(q,[]))]
  if doc=='F0011' and q in m.EXTRA_F0011:
   apos,novo=m.EXTRA_F0011[q];k=[c[0] for c in codes].index(apos);codes=codes[:k+1]+[novo]+codes[k+1:]
  assert len(rr)==len(codes)
  for r,c in zip(rr,codes):r['cod']=c[0]
cv=list(csv.DictReader((R/'01_Dados_reais/extracao_B02/cvm_isa_dfp_2024_2025.csv').open(encoding='utf-8-sig'),delimiter=';'));print('CVM keys',list(cv[0]))
D=lambda v:Decimal(v or '0')
out=[]
for item in m.MAPA:
 dem=item[0]
 for abr,g,prefix in [('Consolidado','con','CON'),('Individual','ind','CTRL')]:
  cod,parts=(item[3],item[4]) if abr=='Individual' and len(item)>3 else (item[1],item[2])
  for dfp,doc in [('2025','F0003'),('2024','F0011')]:
   for ordem,ano in [('ÚLTIMO',dfp),('PENÚLTIMO',str(int(dfp)-1))]:
    arq=f'dfp_cia_aberta_{dem}_{g}_{dfp}.csv';dt=f'{ano}-12-31';pdf=sum((D(r.get(prefix+'_'+ano,'')) for r in rows if r['doc']==doc and r['cod'] in parts),Decimal(0)) if parts else Decimal(0)
    val=sum((D(r['VL_CONTA']) for r in cv if r['ARQUIVO']==arq and r['CD_CONTA'] in cod.split('+') and r['ORDEM_EXERC']==ordem and r['DT_FIM_EXERC']==dt),Decimal(0))
    out.append(dict(dem=dem,cod=cod,abrangencia=abr,dfp=dfp,ordem=ordem,data=dt,valor_pdf=str(pdf),valor_cvm=str(val),diferenca=str(pdf-val)))
nonzero=[r for r in out if Decimal(r['diferenca'])!=0];report={'conferencias':len(out),'diferencas':nonzero,'valores_pdf':sum(sum(r.get(k,'') not in ('',None) for k in ['CTRL_2025','CTRL_2024','CON_2025','CON_2024','CTRL_2023','CON_2023']) for r in rows),'linhas_cvm':len(cv),'resultados':out}
(W/'conferencia_552.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8');print('CHECKS',len(out),'nonzero',len(nonzero),str(nonzero[:3]))
