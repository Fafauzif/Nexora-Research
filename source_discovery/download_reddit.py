import urllib.request,json,time,hashlib
from pathlib import Path
root=Path(__file__).parent
u='https://www.kaggle.com/api/v1/datasets/download/bwandowando/reddit-rindonesia-subreddit-dataset-2026/indonesia_subreddit_comments.csv?datasetVersionNumber=283'
log={'url':u,'started_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime())}
try:
 with urllib.request.urlopen(u,timeout=60) as r:
  log.update({'status':r.status,'content_type':r.headers.get('Content-Type'),'content_length':r.headers.get('Content-Length')});print(log,flush=True)
  p=root/'indonesia2026_comments_download';n=0;h=hashlib.sha256()
  with p.open('wb') as f:
   while True:
    b=r.read(1024*1024)
    if not b:break
    f.write(b);h.update(b);n+=len(b)
  log.update({'bytes':n,'sha256':h.hexdigest(),'path':str(p)});print(log,flush=True)
except Exception as e:log['error']=repr(e);print(log,flush=True)
(root/'reddit_download_log.json').write_text(json.dumps(log,indent=2))
