from pathlib import Path
import csv,gzip,json,hashlib
from decimal import Decimal
root=Path(__file__).resolve().parents[2]
out=[]
for name,expected_rows,expected_sum in [('REFERENCIA',600650,Decimal('36431298000.00')),('TESTE',600474,Decimal('36463023784.44'))]:
 p=root/'03_Base_sintetica/base_B07/dados_sinteticos'/f'SINTETICO_lancamentos_2025_{name}.csv.gz'
 count=0;total=Decimal(0);ids=set();duplicates=0
 with gzip.open(p,'rt',encoding='utf-8',newline='') as f:
  for row in csv.DictReader(f,delimiter=';'):
   count+=1;total+=Decimal(row['valor_movimento_brl']);key=row['id_lancamento'];duplicates+=key in ids;ids.add(key)
 out.append({'arquivo':str(p.relative_to(root)),'registros':count,'soma_brl':str(total),'ids_duplicados':duplicates,'aceite':count==expected_rows and total==expected_sum and duplicates==0})
print(json.dumps(out,ensure_ascii=False,indent=2))
if not all(x['aceite'] for x in out):raise SystemExit(1)
