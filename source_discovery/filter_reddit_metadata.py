"""Extract a metadata-only e-commerce discovery lead list; never writes source bodies."""
import csv,json,re,hashlib,datetime,collections
from pathlib import Path
ROOT=Path(__file__).parent
source=ROOT/'indonesia2026_comments_download'
OUT=ROOT/'deliverables';OUT.mkdir(exist_ok=True)
patterns={
 'shopee':r'\bshopee\b|\bsyopi\b|\bsopi\b',
 'tokopedia':r'\btokopedia\b|\btokped\b|\btoped\b',
 'lazada':r'\blazada\b',
 'bukalapak':r'\bbukalapak\b',
 'blibli':r'\bblibli\b',
 'tiktok_shop':r'\btiktok\s*shop\b|\bkeranjang\s*kuning\b',
 'marketplace':r'\bmarketplace\b|\be[ -]?commerce\b|\bolshop\b|\btoko\s+online\b|\bbelanja\s+online\b',
 'shipping_terms':r'\bongkir\b|\bgratis\s+ongkir\b|\bcod\b'
}
compiled={k:re.compile(v,re.I) for k,v in patterns.items()}
fields=['archive_source_id','source_row_number','archive_comment_id','archive_thread_id','archive_parent_id','source_archive_url','original_permalink_available','created_utc_original','created_at_utc','keyword_screen_matches','screening_status','archive_version']
seen=set();n=0;m=0;clean=0;dup=0;dates=[]
csv.field_size_limit(50_000_000)
with source.open(newline='',encoding='utf-8') as f,(OUT/'reddit_indonesia2026_discovery_raw_metadata.csv').open('w',newline='',encoding='utf-8') as raw,(OUT/'reddit_indonesia2026_discovery_clean_metadata.csv').open('w',newline='',encoding='utf-8') as cl:
 r=csv.DictReader(f);rw=csv.DictWriter(raw,fieldnames=fields);cw=csv.DictWriter(cl,fieldnames=fields);rw.writeheader();cw.writeheader()
 for n,row in enumerate(r,1):
  matches=[k for k,p in compiled.items() if p.search(row.get('body',''))]
  if not matches:continue
  cid=row.get('comment_id','').removeprefix('t1_');tid=row.get('thread_id','').removeprefix('t3_')
  dt=''
  try:
   t=float(row.get('created_utc',''));dt=datetime.datetime.fromtimestamp(t,datetime.timezone.utc).isoformat().replace('+00:00','Z');dates.append(t)
  except (ValueError,OverflowError):
   try:
    parsed=datetime.datetime.fromisoformat(row.get('created_utc','').replace('Z','+00:00'))
    if parsed.tzinfo is None: parsed=parsed.replace(tzinfo=datetime.timezone.utc)
    t=parsed.timestamp();dt=parsed.astimezone(datetime.timezone.utc).isoformat().replace('+00:00','Z');dates.append(t)
   except ValueError:pass
  url='https://www.kaggle.com/datasets/bwandowando/reddit-rindonesia-subreddit-dataset-2026'
  o={'archive_source_id':'kaggle_bwandowando_indonesia2026_v283','source_row_number':n,'archive_comment_id':cid,'archive_thread_id':tid,'archive_parent_id':row.get('parent_id',''),'source_archive_url':url,'original_permalink_available':'false','created_utc_original':row.get('created_utc',''),'created_at_utc':dt,'keyword_screen_matches':'|'.join(matches),'screening_status':'keyword_candidate_not_manually_validated','archive_version':row.get('version','')}
  rw.writerow(o);m+=1
  if cid and cid not in seen:
   cw.writerow(o);seen.add(cid);clean+=1
  else:dup+=1
stats={'source_id':'kaggle_bwandowando_indonesia2026_v283','source_file':'indonesia_subreddit_comments.csv','source_snapshot_version':283,'source_rows_screened':n,'raw_matched_metadata_rows':m,'clean_unique_comment_ids':clean,'duplicate_or_missing_id_rows_excluded':dup,'retained_text_records':0,'retained_usernames':0,'archive_ids_are_uuid_not_live_reddit_ids':True,'live_reddit_permalinks_retained':0,'earliest_matched_utc':datetime.datetime.fromtimestamp(min(dates),datetime.timezone.utc).isoformat() if dates else None,'latest_matched_utc':datetime.datetime.fromtimestamp(max(dates),datetime.timezone.utc).isoformat() if dates else None,'patterns':patterns,'license_status':'Kaggle lists Reddit API Terms; no open redistribution license established. Source bodies deliberately excluded.','scope':'Archive screening metadata only; source IDs are pseudonymous UUIDs and cannot resolve live Reddit content. Query terms deliberately broad and not proof of relevance or mechanisms; not the analysis corpus.'}
(OUT/'reddit_metadata_screening_report.json').write_text(json.dumps(stats,indent=2));print(json.dumps(stats,indent=2))
