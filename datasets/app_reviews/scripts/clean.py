import json,pathlib,zipfile,csv,io,hashlib,re,unicodedata,collections,datetime
base=pathlib.Path(__file__).resolve().parents[1]
sources=[
 {'id':'kaggle_bwandowando_shopee','ref':'bwandowando/shopee-app-reviews-from-google-store','member':'SHOPEE_REVIEWS.csv','platform':'Shopee','license':'CC BY-NC-SA 4.0','text':'review_text','date':'review_datetime_utc','rating':'review_rating','helpful':'review_likes','version':'author_app_version','timezone':'UTC','geography':'Not specified per review; international app corpus'},
 {'id':'kaggle_bwandowando_lazada','ref':'bwandowando/lazada-app-reviews-from-google-store','member':'LAZADA_REVIEWS.csv','platform':'Lazada','license':'CC BY-NC-SA 4.0','text':'review_text','date':'review_datetime_utc','rating':'review_rating','helpful':'review_likes','version':'author_app_version','timezone':'UTC','geography':'Not specified per review; international app corpus'},
]
for app in ['tokopedia','bukalapak','blibli']:
 sources.append({'id':'kaggle_rezkyyayang_'+app,'ref':'rezkyyayang/reviews-of-indonesian-app-startups-on-playstore','member':app+'.csv','platform':app.title(),'license':'CC0: Public Domain','text':'content','date':'created_at','rating':'score','helpful':'thumbsUpCount','version':None,'timezone':'unknown','geography':'Dataset curator describes Indonesian applications; reviewer location unknown'})
counts=[];seen=set();excluded=collections.Counter()
with open(base/'clean/app_reviews.jsonl','w',encoding='utf-8') as out,open(base/'clean/exclusions.jsonl','w',encoding='utf-8') as exc:
 for s in sources:
  p=base/'raw'/(s['ref'].replace('/','__')+'.zip');stats={'source_id':s['id'],'dataset_ref':s['ref'],'archive_member':s['member'],'platform':s['platform'],'raw_rows':0,'retained_rows':0,'empty_text_excluded':0,'duplicates_excluded':0,'invalid_date_retained':0,'earliest_date':None,'latest_date':None,'rating_values':collections.Counter()}
  with zipfile.ZipFile(p) as z, z.open(s['member']) as f:
   reader=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig',errors='strict'))
   for i,r in enumerate(reader):
    stats['raw_rows']+=1
    text=unicodedata.normalize('NFC',r.get(s['text'],'') or '');text=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]',' ',text);text=re.sub(r'\s+',' ',text).strip()
    reason=None
    if not text or text.casefold() in ['null','nan','none']:reason='empty_text';stats['empty_text_excluded']+=1
    date=(r.get(s['date'],'')or'').strip();score=(r.get(s['rating'],'')or'').strip()
    native_review_id=None # Source row ids are not guaranteed platform-native review ids.
    dupkey='|'.join([s['platform'].casefold(),date,score,text])
    h=hashlib.sha256(dupkey.encode()).hexdigest()
    if not reason and h in seen:reason='exact_app_date_rating_text_duplicate';stats['duplicates_excluded']+=1
    if reason:
     exc.write(json.dumps({'source_id':s['id'],'source_row_index':i,'reason':reason},ensure_ascii=False)+'\n');continue
    seen.add(h)
    try:rating=int(float(score)) if score else None
    except ValueError:rating=None
    try:helpful=int(float(r.get(s['helpful'],'')or 0))
    except ValueError:helpful=None
    try:
     parsed=datetime.datetime.fromisoformat(date.replace('Z','+00:00'));dateonly=parsed.date().isoformat()
     stats['earliest_date']=min(stats['earliest_date'] or dateonly,dateonly);stats['latest_date']=max(stats['latest_date'] or dateonly,dateonly)
    except ValueError:dateonly=None;stats['invalid_date_retained']+=1
    obj={'record_id':s['id']+':'+str(i),'source_id':s['id'],'source_url':'https://www.kaggle.com/datasets/'+s['ref'],'source_archive_member':s['member'],'source_row_index':i,'native_review_id':native_review_id,'collection_stratum':'supplementary_public_app_reviews','record_type':'google_play_app_review','platform_discussed':s['platform'],'published_at_source':date,'published_date':dateonly,'source_timezone':s['timezone'],'text':text,'rating':rating,'helpful_votes':helpful,'app_version':r.get(s['version']) if s['version'] else None,'language':None,'reviewer_country':None,'geography_note':s['geography'],'license_declared_by_dataset':s['license'],'text_sha256':hashlib.sha256(text.encode()).hexdigest(),'dedup_key_sha256':h,'collection_mode':'downloaded_existing_public_dataset','nexora_data':False,'sentiment_or_topic_analysis_performed':False}
    out.write(json.dumps(obj,ensure_ascii=False)+'\n');stats['retained_rows']+=1;stats['rating_values'][str(rating)]+=1
  counts.append(stats);print(stats,flush=True)
(base/'metadata/cleaning_counts.json').write_text(json.dumps(counts,indent=2,ensure_ascii=False))
(base/'metadata/accepted_sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False))
print('TOTAL',sum(x['raw_rows'] for x in counts),sum(x['retained_rows'] for x in counts),flush=True)
