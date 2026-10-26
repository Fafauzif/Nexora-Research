import csv,gzip,json,hashlib,collections,datetime,pathlib,time
B=pathlib.Path('/workspace/scratch/1ba9d8b39c55/collection');result={};start=time.time()
p=B/'review_collection/clean/app_reviews.jsonl.gz';expected=json.loads((B/'review_collection/metadata/cleaning_counts.json').read_text());expected_n=sum(x['retained_rows'] for x in expected)
c=collections.Counter();issues=collections.Counter();ids=set();dates={};sha=hashlib.sha256();sample=[]
with gzip.open(p,'rt',encoding='utf8') as f:
 for i,line in enumerate(f):
  try:r=json.loads(line)
  except Exception:issues['json_parse_error']+=1;continue
  if r['record_id'] in ids:issues['duplicate_record_id']+=1
  ids.add(r['record_id']);c[r['source_id']]+=1
  if not r.get('text','').strip():issues['empty_text']+=1
  if r.get('rating') not in range(1,6):issues['rating_outside_1_5']+=1
  if r.get('language') is not None:issues['language_not_unknown']+=1
  if r.get('reviewer_country') is not None:issues['country_not_unknown']+=1
  if r.get('nexora_data') is not False:issues['fictional_boundary_flag_error']+=1
  if r.get('sentiment_or_topic_analysis_performed') is not False:issues['analysis_flag_error']+=1
  if hashlib.sha256(r['text'].encode()).hexdigest()!=r['text_sha256']:issues['text_hash_mismatch']+=1
  sid=r['source_id'];d=r.get('published_date')
  if d:
   if sid not in dates:dates[sid]=[d,d]
   else:dates[sid]=[min(dates[sid][0],d),max(dates[sid][1],d)]
  if len(sample)<3:sample.append({'record_id':r['record_id'],'keys':list(r),'text_case_preserved':r['text']!=r['text'].lower()})
actual=sum(c.values());result['app_reviews']={'file':str(p.relative_to(B)),'actual_records':actual,'expected_records':expected_n,'counts_match':actual==expected_n,'by_source':dict(c),'date_ranges':dates,'issues':dict(issues),'unique_record_ids':len(ids),'sample_schema':sample}
print('App validation complete',actual,dict(issues),flush=True)
result['elapsed_seconds']=round(time.time()-start,2)
(B/'documentation/qa_validation.json').write_text(json.dumps(result,indent=2))
