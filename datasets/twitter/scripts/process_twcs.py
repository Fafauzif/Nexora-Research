from pathlib import Path
import csv,io,zipfile,json,hashlib,re,html,unicodedata,collections,gzip,time
from array import array
from email.utils import parsedate_to_datetime
p=Path(__file__).resolve().parent.parent;out=p/'ready';(out/'raw').mkdir(parents=True,exist_ok=True);(out/'clean').mkdir(exist_ok=True);(out/'metadata').mkdir(exist_ok=True)
z=zipfile.ZipFile(p/'raw/twcs_download.zip');name='twcs/twcs.csv'
# Original 2017 dataset uses numeric surrogate tweet IDs, not live Twitter status IDs.
parent=array('I',range(4000000))
def ensure(i):
 if i>=len(parent):parent.extend(range(len(parent),i+10000))
def find(i):
 while parent[i]!=i:
  parent[i]=parent[parent[i]];i=parent[i]
 return i
def union(a,b):
 ensure(max(a,b));a=find(a);b=find(b)
 if a!=b:parent[max(a,b)]=min(a,b)
brands={'AmazonHelp':'marketplace','AskeBay':'marketplace','UPSHelp':'courier','AskTarget':'retail_adjacent','ArgosHelpers':'retail_adjacent','NeweggService':'retail_adjacent','Walmart':'retail_adjacent','NikeSupport':'retail_adjacent'}
seeds=[];n=0;author_counts=collections.Counter()
with z.open(name) as f:
 for r in csv.DictReader(io.TextIOWrapper(f,encoding='utf-8')):
  n+=1;tid=int(r['tweet_id']);ensure(tid)
  refs=[r['in_response_to_tweet_id']]+r['response_tweet_id'].split(',')
  for ref in refs:
   if ref.strip().isdigit():union(tid,int(ref))
  if r['author_id'] in brands:seeds.append((tid,r['author_id']));author_counts[r['author_id']]+=1
print('Pass1',n,len(seeds),flush=True)
root_brands=collections.defaultdict(set)
for tid,brand in seeds:root_brands[find(tid)].add(brand)
root_strata={root:sorted({brands[b] for b in bs}) for root,bs in root_brands.items()}
fieldnames=['tweet_id','author_id','inbound','created_at','text','response_tweet_id','in_response_to_tweet_id']
cleanfields=['record_id','source_id','source_record_id','source_url','source_platform','record_type','stratum','country','geography_basis','language','language_basis','created_at_utc','author_id_source','author_role','text','text_sha256','conversation_id','company_handles','company_types','inbound_as_reported','response_record_ids','in_response_to_record_id','retrieval_method','source_license','source_year','cleaning_flags']
seen=set();count=0;dups=0;empty=0;mint=None;maxt=None;company_count=collections.Counter();stratum_count=collections.Counter();text_hashes=collections.Counter();conv_ids=set()
with gzip.open(out/'raw/twcs_ecommerce_connected_original_rows.csv.gz','wt',encoding='utf-8',newline='') as rf,gzip.open(out/'clean/twcs_ecommerce_connected_clean.csv.gz','wt',encoding='utf-8',newline='') as cf:
 rw=csv.DictWriter(rf,fieldnames=fieldnames);rw.writeheader();cw=csv.DictWriter(cf,fieldnames=cleanfields);cw.writeheader()
 with z.open(name) as f:
  for r in csv.DictReader(io.TextIOWrapper(f,encoding='utf-8')):
   tid=int(r['tweet_id']);root=find(tid)
   if root not in root_brands:continue
   rw.writerow(r)
   if r['tweet_id'] in seen:dups+=1;continue
   seen.add(r['tweet_id']);flags=[]
   text=html.unescape(unicodedata.normalize('NFC',r['text']));text=re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f]','',text);text=re.sub(r'\s+',' ',text).strip()
   if not text:empty+=1;continue
   # Remove publicly posted contact details from clean view; original source cells remain in raw.
   text,nmail=re.subn(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b','[EMAIL]',text)
   text,nphone=re.subn(r'(?<!\w)(?:\+?\d[\d(). -]{7,}\d)(?!\w)','[NUMBER_SEQUENCE]',text)
   if nmail:flags.append('email_redacted')
   if nphone:flags.append('long_numeric_sequence_redacted')
   h=hashlib.sha256(text.casefold().encode()).hexdigest();text_hashes[h]+=1
   try:dt=parsedate_to_datetime(r['created_at']);date=dt.isoformat();mint=date if mint is None else min(mint,date);maxt=date if maxt is None else max(maxt,date)
   except Exception:date='';flags.append('unparsed_date')
   bs=sorted(root_brands[root]);strata=root_strata[root];stratum='historical_international_'+('core_marketplace_courier' if any(x in ['marketplace','courier'] for x in strata) else 'retail_adjacent')
   row={'record_id':'twcs:'+r['tweet_id'],'source_id':'thoughtvector_twcs_v10','source_record_id':r['tweet_id'],'source_url':'https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter','source_platform':'Twitter','record_type':'tweet','stratum':stratum,'country':'unknown','geography_basis':'not inferred; English historical international comparator','language':'und','language_basis':'individual language not classified; source is predominantly English but multilingual','created_at_utc':date,'author_id_source':r['author_id'],'author_role':'company_support' if r['author_id'] in brands else ('customer_or_other_inbound' if r['inbound']=='True' else 'other_support_or_participant'),'text':text,'text_sha256':h,'conversation_id':'twcs_component:'+str(root),'company_handles':'|'.join(bs),'company_types':'|'.join(strata),'inbound_as_reported':r['inbound'],'response_record_ids':r['response_tweet_id'],'in_response_to_record_id':r['in_response_to_tweet_id'],'retrieval_method':'public_Kaggle_published_dataset_import_connected_component_filter','source_license':'CC-BY-NC-SA-4.0','source_year':'2017','cleaning_flags':'|'.join(flags)}
   cw.writerow(row);count+=1;conv_ids.add(root);stratum_count[stratum]+=1
   for b in bs:company_count[b]+=1
meta={'source_rows_scanned':n,'raw_selected_rows':count+dups+empty,'clean_tweet_records':count,'unique_conversation_components':len(conv_ids),'unique_clean_text_hashes':len(text_hashes),'duplicate_id_rows_removed':dups,'empty_rows_removed':empty,'selected_company_seed_handles':brands,'selected_company_support_seed_counts':dict(author_counts),'records_by_connected_company_nonadditive':dict(company_count),'records_by_stratum_additive':dict(stratum_count),'earliest_created_at':mint,'latest_created_at':maxt,'source_dataset_version':10,'source_last_updated':'2017-12-03T23:44:27.157Z','source_license':'CC BY-NC-SA 4.0','archive_sha256':hashlib.sha256((p/'raw/twcs_download.zip').read_bytes()).hexdigest(),'archive_bytes':(p/'raw/twcs_download.zip').stat().st_size,'source_dataset_url':'https://www.kaggle.com/datasets/thoughtvector/customer-support-on-twitter','selection_method':'Union all source tweet reply edges, retain components containing at least one selected company-authored tweet. Numeric tweet_id is source surrogate, not live Twitter status ID.','counting_note':'Records are individual source tweets; conversation count is distinct connected reply components; exact repeated text retained to preserve conversational context; cross-company record counts are nonadditive.'}
(out/'metadata/twcs_manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps(meta,indent=2),flush=True)
