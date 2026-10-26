from pathlib import Path
import urllib.request, json, hashlib, time, csv
p=Path(__file__).resolve().parent.parent;(p/'raw').mkdir(exist_ok=True);(p/'logs').mkdir(exist_ok=True)
log=[]
def download(url,path,timeout=90):
 start=time.time()
 try:
  req=urllib.request.Request(url,headers={'User-Agent':'NexoraResearchCollection/1.0 public-research'})
  with urllib.request.urlopen(req,timeout=timeout) as r:
   with path.open('wb') as f:
    while True:
     b=r.read(1024*1024)
     if not b:break
     f.write(b)
   h={'status':r.status,'content_type':r.headers.get('Content-Type'),'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
  row={'url':url,'destination':str(path),'collected_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'elapsed_seconds':round(time.time()-start,2),'ok':True,**h};log.append(row);print(row,flush=True)
 except Exception as e:
  row={'url':url,'destination':str(path),'ok':False,'error':str(e)};log.append(row);print(row,flush=True)
 (p/'logs/downloads.json').write_text(json.dumps(log,indent=2));return row['ok']
for i in [18198239,15845921]:
 d=json.loads((p/'metadata'/f'zenodo_{i}.json').read_text())
 for f in d['files']:
  name=f['key'].replace(' ','_').replace('(','').replace(')','')
  download(f['links']['self'],p/'raw'/f'zenodo_{i}_{name}')
url='https://www.kaggle.com/api/v1/datasets/list?search=customer-support-on-twitter'
download(url,p/'metadata/kaggle_twcs_search.json')
download('https://www.kaggle.com/api/v1/datasets/download/thoughtvector/customer-support-on-twitter',p/'raw/twcs_download.zip',timeout=120)
