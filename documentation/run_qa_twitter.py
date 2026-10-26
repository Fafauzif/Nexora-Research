import csv,gzip,json,hashlib,collections,pathlib,time
B=pathlib.Path('/workspace/scratch/1ba9d8b39c55/collection');p=B/'x_collection/ready/clean/twcs_ecommerce_connected_clean.csv.gz';mp=B/'x_collection/ready/metadata/twcs_manifest.json';m=json.loads(mp.read_text());seen=set();conv=set();issues=collections.Counter();counts=collections.Counter();dates=[];n=0;keys=None
with gzip.open(p,'rt',encoding='utf8',newline='') as f:
 reader=csv.DictReader(f);keys=reader.fieldnames
 for r in reader:
  n+=1
  if r['record_id'] in seen:issues['duplicate_record_id']+=1
  seen.add(r['record_id']);conv.add(r['conversation_id']);counts[r['stratum']]+=1
  if not r['text'].strip():issues['empty_text']+=1
  if hashlib.sha256(r['text'].casefold().encode()).hexdigest()!=r['text_sha256']:issues['text_hash_mismatch']+=1
  if r['language']!='und':issues['individual_language_not_unknown']+=1
  if r['country']!='unknown':issues['country_inferred']+=1
  if r.get('company_types') not in ['marketplace','courier','retail_adjacent','courier|marketplace','marketplace|retail_adjacent','courier|retail_adjacent','courier|marketplace|retail_adjacent']:issues['unexpected_company_types']+=1
  if not r.get('inbound_as_reported') in ['True','False']:issues['missing_source_inbound']+=1
  dates.append(r['created_at_utc'])
rawp=B/'x_collection/ready/raw/twcs_ecommerce_connected_original_rows.csv.gz'
with gzip.open(rawp,'rt',encoding='utf8',newline='') as f:
 reader=csv.DictReader(f);rawfields=reader.fieldnames;raw_n=sum(1 for _ in reader)
result={'file':str(p.relative_to(B)),'actual_clean_records':n,'expected_clean_records':m['clean_tweet_records'],'count_match':n==m['clean_tweet_records'],'unique_record_ids':len(seen),'unique_components':len(conv),'components_match':len(conv)==m['unique_conversation_components'],'schema':keys,'actual_stratum_counts':dict(counts),'stratum_counts_match':dict(counts)==m['records_by_stratum_additive'],'date_range':[min(dates),max(dates)],'date_range_matches':min(dates)==m['earliest_created_at'] and max(dates)==m['latest_created_at'],'issues':dict(issues),'actual_scoped_raw_records':raw_n,'raw_count_match':raw_n==m['raw_selected_rows'],'raw_fields':rawfields,'hash_definition':'SHA256 of casefolded normalized/redacted text, not app-review hash definition'}
(B/'documentation/qa_twitter_validation.json').write_text(json.dumps(result,indent=2));print(json.dumps(result,indent=2))
