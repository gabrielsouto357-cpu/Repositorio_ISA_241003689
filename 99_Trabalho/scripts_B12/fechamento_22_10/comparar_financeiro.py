from pathlib import Path
import csv,json
import argparse
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[3]);p.add_argument('--output',type=Path);args=p.parse_args();R=args.root.resolve();W=args.output.resolve() if args.output else R/'04_Testes/B12/fechamento_22_10'
def read(p):
 with p.open(encoding='utf-8-sig',newline='') as f:return list(csv.DictReader(f,delimiter=';'))
a=read(R/'01_Dados_reais/extracao_B02/pdf_linhas_F0003_F0011.csv');b=read(W/'pdf_linhas_reextraidas.csv');print('ROWS',len(a),len(b),'HEADERS',list(a[0]))
diffs=[]
for i,(x,y) in enumerate(zip(a,b)):
 for k in x:
  if x[k]!=y.get(k):diffs.append({'row':i+2,'field':k,'old':x[k],'new':y.get(k)})
print('DIFFS',len(diffs));print(json.dumps(diffs[:15],ensure_ascii=False,indent=1))
(W/'comparacao_reextracao.json').write_text(json.dumps({'original_rows':len(a),'new_rows':len(b),'differences':diffs},ensure_ascii=False,indent=2),encoding='utf-8')
