from pathlib import Path
import json,gzip,shutil,hashlib,time
b=Path(__file__).resolve().parents[1]
p=b/'clean/app_reviews.jsonl';gz=b/'clean/app_reviews.jsonl.gz'
if p.exists():
 with open(p,'rb') as src,gzip.GzipFile(filename='',mode='wb',fileobj=open(gz,'wb'),compresslevel=4,mtime=0) as dst:shutil.copyfileobj(src,dst,length=1024*1024)
 p.unlink()
counts=json.loads((b/'metadata/cleaning_counts.json').read_text())
sources=json.loads((b/'metadata/accepted_sources.json').read_text())
for s in sources:
 s.update(next(x for x in counts if x['source_id']==s['id']))
 meta=json.loads((b/'metadata'/(s['ref'].replace('/','__')+'.json')).read_text());dl=json.loads((b/'metadata'/(s['ref'].replace('/','__')+'_download.json')).read_text())
 s['dataset_title']=meta['title'];s['dataset_version']=meta.get('currentVersionNumber');s['dataset_last_updated']=meta.get('lastUpdated');s['dataset_creator']=meta.get('creatorName');s['source_page']='https://www.kaggle.com/datasets/'+s['ref'];s['download']=dl
 s['language_declared_per_record']=False;s['reviewer_geography_known']=False;s['native_review_id_available']=False
manifest={'collection_stratum':'supplementary_public_app_reviews','scope':'Historical publicly shared Google Play app-review datasets; not Reddit/X; no Nexora internal observations','collection_completed_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),'raw_selected_member_rows':sum(s['raw_rows'] for s in sources),'retained_clean_rows':sum(s['retained_rows'] for s in sources),'empty_text_exclusions':sum(s['empty_text_excluded'] for s in sources),'exact_duplicate_exclusions':sum(s['duplicates_excluded'] for s in sources),'analysis_performed':False,'sources':sources,'clean_file':{'path':'clean/app_reviews.jsonl.gz','bytes':gz.stat().st_size,'sha256':hashlib.sha256(gz.read_bytes()).hexdigest()},'notes':['One multiapp original archive is preserved in full; only Tokopedia, Bukalapak, and Blibli members contribute clean records. Non-ecommerce members are excluded.','Corpus spans older history and does not claim 2025-2026 platform representativeness.','No language or role inference, no topic/sentiment model, no positivity/negativity selection.']}
(b/'source_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2))
print(json.dumps({k:v for k,v in manifest.items() if k!='sources'},indent=2))
