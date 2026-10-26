#!/usr/bin/env python3
"""Normalize publicly indexed social-source excerpts; no sentiment/causal analysis.
The search service returns selected excerpts, NOT complete posts or comment exports.
Full provider responses are not redistributed. Reddit excerpts are preserved as
retrieved; X capture is limited to metadata plus <=20 words of source heading.
"""
from pathlib import Path
import json,re,hashlib,csv,datetime,urllib.parse,collections,shutil
root=Path(__file__).resolve().parents[1]
scratch=root.parents[1]/'tmp/social_provider_responses'
scratch.mkdir(exist_ok=True)
source_re=re.compile(r'^(.+?) \((https?://[^\n]+)\)\n【([^】]+)】',re.S)
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
occ=[];reads=[]
def canonical(url):
 p=urllib.parse.urlparse(url)
 if 'reddit.com' in p.netloc:
  m=re.search(r'/r/([^/]+)/comments/([a-z0-9]+)',p.path)
  if m:return f'https://www.reddit.com/r/{m[1].lower()}/comments/{m[2]}/'
 if p.netloc in ['x.com','mobile.x.com','twitter.com']:
  m=re.search(r'/([^/]+)/status/(\d+)',p.path)
  if m:return f'https://x.com/{m[1]}/status/{m[2]}'
 return urllib.parse.urlunparse((p.scheme,p.netloc,p.path,'','',''))
for p in sorted(root.joinpath('raw').glob('search_*.json')):
 j=json.loads(p.read_text());out=[]
 if 'results' in j:out=j['results']
 else:
  (scratch/p.name).write_text(p.read_text())
  text='\n'.join(x.get('text','') for x in j.get('content',[]) if x.get('type')=='text')
  for block in text.split('\n--------------------------------------------------------------------------------\n'):
   m=source_re.search(block.strip())
   if not m:continue
   title,url,ref=m.groups();title=title.strip()
   if not ('reddit.com' in urllib.parse.urlparse(url).netloc or urllib.parse.urlparse(url).netloc in ['x.com','mobile.x.com','twitter.com']):continue
   is_reddit='reddit.com' in urllib.parse.urlparse(url).netloc
   d={'url':url,'canonical_url':canonical(url),'source_ref':ref,'capture_file':p.name,'representation':'search_index_excerpt' if is_reddit else 'search_index_metadata_and_short_heading','retrieved_at_utc':now}
   if is_reddit:d.update(title=title,provider_excerpt=block.strip())
   else:d.update(title=' '.join(title.split()[:20]),provider_excerpt='',capture_note='Only indexed URL and a maximum 20-word source heading retained; no full tweet or thread was captured.')
   out.append(d)
  p.write_text(json.dumps({'capture_type':'public_search_index_results','complete_platform_export':False,'results':out},ensure_ascii=False,indent=2))
 occ.extend(out)
for p in sorted(root.joinpath('raw').glob('thread_reads_*.json')):
 j=json.loads(p.read_text())
 if 'results' in j:out=j['results']
 else:
  (scratch/p.name).write_text(p.read_text());out=[]
  text='\n'.join(x.get('text','') for x in j.get('content',[]) if x.get('type')=='text')
  for block in text.split('\n--------------------------------------------------------------------------------\n'):
   m=source_re.search(block.strip())
   if not m:continue
   title,url,ref=m.groups()
   if 'reddit.com' not in urllib.parse.urlparse(url).netloc:continue
   out.append({'url':url,'canonical_url':canonical(url),'title':title,'source_ref':ref,'capture_file':p.name,'representation':'partial_thread_page_text','retrieved_at_utc':now,'provider_excerpt':block.strip()})
  p.write_text(json.dumps({'capture_type':'public_indexed_page_read','full_thread_capture':False,'results':out},ensure_ascii=False,indent=2))
 reads.extend(out)
# Remove legacy intermediate file containing duplicated full-provider headers.
(root/'clean/search_candidates.json').unlink(missing_ok=True)
unique={}
for d in occ:
 key=d['canonical_url']
 if key not in unique:unique[key]=dict(d,appearances=1,source_refs=[d['source_ref']],capture_files=[d['capture_file']])
 else:
  unique[key]['appearances']+=1;unique[key]['source_refs'].append(d['source_ref']);unique[key]['capture_files'].append(d['capture_file'])
  if len(d['provider_excerpt'])>len(unique[key]['provider_excerpt']):
   unique[key]['provider_excerpt']=d['provider_excerpt'];unique[key]['title']=d['title']
records=[]
for url,d in unique.items():
 isreddit='reddit.com' in urllib.parse.urlparse(url).netloc
 sub=re.search(r'/r/([^/]+)/comments/([a-z0-9]+)',url)
 status=re.search(r'/status/(\d+)',url)
 excerpt=d['provider_excerpt']
 # Strip search header; do not split comments without platform comment IDs.
 body=excerpt.split('\n',2)[-1] if excerpt else ''
 text=re.sub(r'\s+',' ',body).strip()
 rec={'record_id':hashlib.sha256(url.encode()).hexdigest()[:20],'platform':'reddit' if isreddit else 'x','canonical_url':url,'original_url':d['url'],'title':d['title'],'text_excerpt':text,'record_unit':'indexed_thread_excerpt' if isreddit else 'indexed_post_metadata','subreddit':sub[1] if sub else '', 'platform_post_id':sub[2] if sub else status[1] if status else '', 'forum_scope':'indonesian_context' if sub and sub[1].lower() in ['indonesia','indotech','indonesiabebas','finansial'] else 'international_comparator_or_unverified','author_location':'unknown','created_utc':None,'date_label':(re.search(r'(?:Published|Crawled): ([^;\n]+)',excerpt).group(1) if re.search(r'(?:Published|Crawled): ([^;\n]+)',excerpt) else ''),'retrieved_at_utc':d['retrieved_at_utc'],'collection_method':'public_web_search_index','coverage':'partial; not exhaustive; no account authentication','source_refs':d['source_refs'],'capture_files':d['capture_files'],'search_appearances':d['appearances'],'screening_status':'candidate; not substantively coded','sha256_clean_text':hashlib.sha256(text.encode()).hexdigest()}
 records.append(rec)
for name,data in [('social_index_records',records),('reddit_thread_read_excerpts',reads)]:
 with open(root/f'clean/{name}.jsonl','w') as f:
  for d in data:f.write(json.dumps(d,ensure_ascii=False)+'\n')
 if data:
  with open(root/f'clean/{name}.csv','w',newline='') as f:
   writer=csv.DictWriter(f,fieldnames=list(data[0]));writer.writeheader()
   for d in data:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in d.items()})
stats={'candidate_result_appearances':len(occ),'unique_indexed_source_records':len(records),'by_platform':dict(collections.Counter(r['platform'] for r in records)),'by_forum_scope':dict(collections.Counter(r['forum_scope'] for r in records)),'partial_reddit_thread_reads':len(reads),'full_reddit_or_x_platform_scrape':False,'agent_reach_executed':False,'created_at_utc':now,'notes':'Record counts are technical inventory counts, not findings; candidate relevance requires future screening.'}
(root/'logs/collection_inventory.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
