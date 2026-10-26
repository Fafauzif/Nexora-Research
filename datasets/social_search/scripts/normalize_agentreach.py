#!/usr/bin/env python3
"""Normalize Agent Reach public-web search envelopes; no substantive analysis."""
from pathlib import Path
import json,re,datetime,hashlib,csv,collections,urllib.parse
root=Path(__file__).resolve().parents[1]
paths=sorted(root.glob('agentreach_raw/*.stdout.json'))
# Root pilot remains its own raw file; normalized provenance points to original.
pilot=root.parent/'tooling/pilot_1_stdout.json'
if pilot.exists():paths.insert(0,pilot)
rows=[];exclude=[];byurl={};queries=[]
log=root/'logs/agentreach_queries.jsonl'
if log.exists():queries=[json.loads(x) for x in log.read_text().splitlines() if x.strip()]
querymap={str(root/q['stdout_file']):q for q in queries if q.get('stdout_file')}
def canon(url):
 p=urllib.parse.urlparse(url);m=re.search(r'/r/([^/]+)/comments/([a-z0-9]+)',p.path)
 if m:return 'https://www.reddit.com/r/'+m[1].lower()+'/comments/'+m[2]+'/'
 return urllib.parse.urlunparse((p.scheme,p.netloc,p.path,'','',''))
for p in paths:
 try:d=json.loads(p.read_text())
 except Exception:continue
 for n,item in enumerate(d.get('items') or []):
  url=item.get('url','');key=canon(url)
  if not url:exclude.append({'raw_file':str(p),'item_index':n,'reason':'missing_source_url'});continue
  m=re.search(r'/r/([^/]+)/comments/([a-z0-9]+)',key)
  channel=d.get('channel','');q=querymap.get(str(p),{})
  occ={'raw_file':str(p.relative_to(root.parent)) if p.is_relative_to(root.parent) else str(p),'item_index':n,'query':q.get('query','root public-web pilot'),'query_theme':q.get('theme','root_pilot')}
  text=item.get('text') or ''
  # Keep line breaks and source words; collapse redundant horizontal whitespace.
  text='\n'.join(re.sub(r'[ \t]+',' ',line).strip() for line in text.splitlines()).strip()
  author=item.get('author') or ''
  rec={'record_id':hashlib.sha256(key.encode()).hexdigest()[:20],'platform':'reddit' if channel=='reddit' else channel,'canonical_url':key,'original_url':url,'title':item.get('title',''),'text_excerpt':text,'published_at_source':item.get('published_at'),'subreddit':m[1] if m else '', 'platform_post_id':m[2] if m else '', 'author_pseudonym':hashlib.sha256(author.encode()).hexdigest()[:16] if author else '', 'forum_scope':'indonesian_context' if m and m[1].lower() in ['indonesia','indotech','indonesiabebas','finansial'] else 'international_comparator_or_unverified','author_location':'unknown','collection_method':'AgentReach1.6 public-web backend','content_scope':item.get('raw',{}).get('content_scope','search_results'),'access':item.get('raw',{}).get('access','public'),'completeness_verified':False,'record_unit':'indexed_thread_excerpt' if m else 'indexed_source_excerpt','screening_status':'candidate_not_substantively_coded','source_occurrences':[occ],'sha256_clean_text':hashlib.sha256(text.encode()).hexdigest()}
  if key not in byurl:byurl[key]=rec
  else:
   byurl[key]['source_occurrences'].append(occ)
   if len(text)>len(byurl[key]['text_excerpt']):
    for f in ['text_excerpt','sha256_clean_text','title']:byurl[key][f]=rec[f]
rows=list(byurl.values())
(root/'agentreach_clean').mkdir(exist_ok=True)
with open(root/'agentreach_clean/agentreach_publicweb_records.jsonl','w') as f:
 for r in rows:f.write(json.dumps(r,ensure_ascii=False)+'\n')
if rows:
 with open(root/'agentreach_clean/agentreach_publicweb_records.csv','w',newline='') as f:
  writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader()
  for r in rows:writer.writerow({k:json.dumps(v,ensure_ascii=False) if isinstance(v,(dict,list)) else v for k,v in r.items()})
summary={'raw_query_envelopes':len(paths),'query_log_rows':len(queries),'successful_query_envelopes':sum(q.get('ok') is True for q in queries),'source_item_appearances':sum(len(r['source_occurrences']) for r in rows),'unique_indexed_source_records':len(rows),'by_platform':dict(collections.Counter(r['platform'] for r in rows)),'by_forum_scope':dict(collections.Counter(r['forum_scope'] for r in rows)),'exclusions':exclude,'full_platform_scrape':False,'note':'Counts are technical inventory, not substantive findings; public-web search is bounded and partial.'}
(root/'logs/agentreach_inventory.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
