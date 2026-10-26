import urllib.request,json,pathlib,time,hashlib,zipfile,concurrent.futures
base=pathlib.Path(__file__).resolve().parents[1]
refs=['bwandowando/shopee-app-reviews-from-google-store','rezkyyayang/reviews-of-indonesian-app-startups-on-playstore','bwandowando/lazada-app-reviews-from-google-store']
def run(ref):
 name=ref.replace('/','__');u='https://www.kaggle.com/api/v1/datasets/download/'+ref;path=base/'raw'/(name+'.zip');start=time.time()
 try:
  if not path.exists():
   with urllib.request.urlopen(u,timeout=90) as resp,open(path.with_suffix('.part'),'wb') as f:
    total=0
    while True:
     b=resp.read(1024*1024)
     if not b:break
     total+=len(b)
     if total>200*1024*1024:raise ValueError('download over 200MiB cap')
     f.write(b)
   path.with_suffix('.part').rename(path)
  z=zipfile.ZipFile(path);print(ref,path.stat().st_size,[(x.filename,x.file_size) for x in z.infolist()],flush=True)
  meta={'ref':ref,'url':u,'downloaded_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'compressed_bytes':path.stat().st_size,'files':[{'name':x.filename,'bytes':x.file_size} for x in z.infolist()]}
  (base/'metadata'/(name+'_download.json')).write_text(json.dumps(meta,indent=2));return meta
 except Exception as e:print(ref,'ERROR',str(e),flush=True);return {'ref':ref,'error':str(e)}
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:res=list(ex.map(run,refs))
(base/'metadata/download_results.json').write_text(json.dumps(res,indent=2))
