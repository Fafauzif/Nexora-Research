#!/usr/bin/env python3
"""Bounded read-only Agent Reach public-web discovery; no account/session backend."""
import subprocess,json,datetime,time,threading,concurrent.futures
from pathlib import Path
root=Path(__file__).resolve().parents[1]
exe='/workspace/scratch/1ba9d8b39c55/tmp/agent-reach-env/bin/agent-reach'
(root/'agentreach_raw').mkdir(exist_ok=True)
queries=[
('seller_fees','Shopee biaya admin penjual potongan'),
('seller_fees','Tokopedia biaya layanan seller margin'),
('seller_fees','TikTok Shop biaya komisi penjual'),
('seller_fees','Shopee seller biaya admin 2024 2025'),
('seller_fees','Tokopedia seller biaya admin 2024 2025'),
('seller_fees','Shopee seller masih untung biaya admin'),
('seller_fees','marketplace seller higher fees worth it'),
('seller_fees','Etsy seller fees value worth it'),
('buyer_value','Tokopedia voucher gratis ongkir minimum belanja'),
('buyer_value','Shopee gratis ongkir cashback biaya layanan'),
('buyer_value','Tokopedia voucher bisa dipakai puas'),
('buyer_value','Shopee promo masih murah belanja'),
('buyer_value','Lazada promo ongkir pengalaman belanja'),
('switching','pindah Tokopedia Shopee belanja'),
('switching','tetap Tokopedia Shopee pilihan belanja'),
('switching','jualan beberapa marketplace toko yang sama harga'),
('switching','marketplace buying directly seller fees'),
('logistics','Shopee SPX pilihan kurir pengalaman'),
('logistics','Tokopedia kurir rekomendasi pengiriman'),
('logistics','Shopee kurir cepat puas pengalaman'),
('logistics','Shopee seller retur ongkir pengembalian'),
('logistics','Tokopedia seller pickup biaya pengiriman'),
('discovery','Shopee seller iklan boncos penjualan'),
('discovery','Tokopedia seller iklan untung penjualan'),
('discovery','TikTok Shop live affiliate jualan pengalaman'),
('discovery','TikTok Shop pencarian barang Shopee Tokopedia'),
('discovery','marketplace organic visibility seller ads'),
('positive','Shopee seller bisnis sukses untung'),
('positive','Tokopedia lebih bagus Shopee hobi'),
('positive','Shopee lebih murah puas pengiriman'),
('international','ShopeePH seller fees shipping profit'),
('international','ecommerce marketplace fees customer acquisition value'),
]
# Separate X access checks: preserve empty/error records, no restricted fallback.
xqueries=[('access_pilot','Shopee'),('access_pilot','Tokopedia biaya admin'),('access_pilot','TikTok Shop komisi')]
jobs=[{'index':i+1,'platform':'reddit','theme':t,'query':q} for i,(t,q) in enumerate(queries)]
jobs += [{'index':len(jobs)+i+1,'platform':'twitter','theme':t,'query':q} for i,(t,q) in enumerate(xqueries)]
stop=threading.Event();lock=threading.Lock()
def run(j):
 if stop.is_set():return dict(j,status='not_run_stop_flag')
 start=datetime.datetime.now(datetime.timezone.utc).isoformat();args=[exe,j['platform'],'search',j['query'],'--limit','10','--backend','public-web','--timeout','20']
 prefix=root/'agentreach_raw'/f"{j['index']:03}_{j['platform']}"
 try:
  p=subprocess.run(args,capture_output=True,text=True,timeout=55)
  raw=p.stdout;err=p.stderr
  prefix.with_suffix('.stdout.json').write_text(raw);prefix.with_suffix('.stderr.txt').write_text(err)
  try:d=json.loads(raw)
  except Exception:d={}
  text=(raw+' '+err).lower()
  if '429' in text or 'rate limit' in text:stop.set()
  row=dict(j,start_utc=start,end_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),command=args,returncode=p.returncode,ok=d.get('ok'),item_count=len(d.get('items') or []),error=d.get('error'),stdout_file=str(prefix.relative_to(root))+'.stdout.json',stderr_file=str(prefix.relative_to(root))+'.stderr.txt',status='completed')
 except Exception as e:row=dict(j,start_utc=start,status='exception',error=str(e))
 with lock:
  with open(root/'logs/agentreach_queries.jsonl','a') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
  print(json.dumps({k:row.get(k) for k in ['index','platform','query','ok','item_count','status']},ensure_ascii=False),flush=True)
 return row
with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
 for row in pool.map(run,jobs):pass
print('COMPLETE',flush=True)
