from pathlib import Path
import csv, json,re,html,unicodedata,hashlib,fitz,shutil
from datetime import datetime
from email.utils import parsedate_to_datetime
p=Path(__file__).resolve().parent.parent;out=p/'ready';(out/'raw').mkdir(parents=True,exist_ok=True);(out/'clean').mkdir(exist_ok=True);(out/'metadata').mkdir(exist_ok=True)
records=[];raw_extracted=[];counts={};datepat=re.compile(r'(?m)^\s*(\d{2}/\d{2}/\d{4}|\d{1,2}-[A-Za-z]{3}-\d{2})\s*')
for pdf in sorted((p/'raw').glob('zenodo_15845921*.pdf')):
 shutil.copy2(pdf,out/'raw'/pdf.name)
 d=fitz.open(pdf);rawcount=0
 for pi,page in enumerate(d):
  s=page.get_text(sort=False);raw_extracted.append({'source_file':pdf.name,'page':pi+1,'text':s})
  matches=list(datepat.finditer(s))
  for ri,m in enumerate(matches):
   rawtext=s[m.end():matches[ri+1].start() if ri+1<len(matches) else len(s)].strip()
   date=m[1];rawcount+=1
   try:dt=datetime.strptime(date,'%d/%m/%Y' if '/' in date else '%d-%b-%y').date().isoformat()
   except Exception:dt=''
   records.append({'record_id':f'zenodo15845921:{pdf.stem}:p{pi+1}:r{ri+1}','source_id':'zenodo_15845921','source_record_id':f'{pdf.name}:page{pi+1}:row{ri+1}','source_url':'https://zenodo.org/records/15845921','source_platform':'Twitter','record_type':'tweet_transcribed_from_published_pdf','stratum':'historical_multilingual_ecommerce_twitter_pdf','country':'unknown','geography_basis':'not inferred; source contains multilingual promotional and discussion posts','created_at_utc':dt,'text_raw_extracted':rawtext,'source_page':pi+1,'source_file':pdf.name,'source_license':'CC-BY-4.0','retrieval_method':'public_Zenodo_published_PDF_import_natural_reading_order_date_delimited','cleaning_flags':'pdf_extraction_not_tweet_ID_verified|source_encoding_artifacts_possible'})
 counts[pdf.name]={'pages':len(d),'raw_date_delimited_rows':rawcount}
with (out/'raw/zenodo_15845921_pages_original_extraction.jsonl').open('w') as f:
 for r in raw_extracted:f.write(json.dumps(r,ensure_ascii=False)+'\n')
f=p/'raw/zenodo_18198239_sentiment_analysis_data_1.csv';shutil.copy2(f,out/'raw'/f.name)
rows=list(csv.DictReader(f.open(encoding='utf-8-sig')));counts[f.name]={'raw_csv_records':len(rows)}
for i,r in enumerate(rows):
 try:date=parsedate_to_datetime(r['created_at']).isoformat()
 except Exception:date=''
 records.append({'record_id':'zenodo18198239:'+r.get('id_str',str(i)),'source_id':'zenodo_18198239','source_record_id':r.get('id_str',''),'source_url':'https://zenodo.org/records/18198239','source_platform':'Twitter/X','record_type':'tweet','stratum':'multilingual_ecommerce_twitter_2026_published_sample','country':'unknown','geography_basis':'not inferred from language','created_at_utc':date,'text_raw_extracted':r.get('full_text',''),'source_language':r.get('lang',''),'tweet_url_reported':r.get('tweet_url',''),'source_license':'CC-BY-4.0','retrieval_method':'public_Zenodo_published_CSV_import','cleaning_flags':'source_tweet_url_contains_undefined_username' if '/undefined/' in r.get('tweet_url','') else ''})
clean=[];seen=set();rejected=[]
for r in records:
 t=html.unescape(unicodedata.normalize('NFC',r['text_raw_extracted']));t=re.sub(r'\s+',' ',t).strip()
 if not t:rejected.append({'record_id':r['record_id'],'reason':'empty_text'});continue
 h=hashlib.sha256(t.casefold().encode()).hexdigest();key=(r['source_id'],h)
 if key in seen:rejected.append({'record_id':r['record_id'],'reason':'duplicate_normalized_text_within_source'});continue
 seen.add(key)
 # Preserve exact content in raw; flag instead of silently fixing broken encoding or interpreting adverts.
 t,nemail=re.subn(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b','[EMAIL]',t)
 if nemail:r['cleaning_flags']+='|email_redacted'
 # Published PDF includes occasional street addresses; clean view redacts the complete recognizable address span only.
 t,naddress=re.subn(r'(?i)\b(?:Jl\.|Jalan)\s+[^\n]{10,180}?(?=(?:https?://|Instagram|$))','[ADDRESS_REDACTED] ',t)
 if naddress:r['cleaning_flags']+='|public_address_span_redacted'
 t,nphone=re.subn(r'(?<!\w)(?:\+?\d[\d(). -]{7,}\d)(?!\w)','[NUMBER_SEQUENCE]',t)
 if nphone:r['cleaning_flags']+='|long_numeric_sequence_redacted'
 r=dict(r);r.pop('text_raw_extracted');r['text']=t;r['text_sha256']=hashlib.sha256(t.casefold().encode()).hexdigest();clean.append(r)
with (out/'clean/zenodo_ecommerce_twitter_clean.jsonl').open('w',encoding='utf-8') as f:
 for r in clean:f.write(json.dumps(r,ensure_ascii=False)+'\n')
fields=list(dict.fromkeys(k for r in clean for k in r))
with (out/'clean/zenodo_ecommerce_twitter_clean.csv').open('w',encoding='utf-8',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader();w.writerows(clean)
(out/'metadata/zenodo_cleaning_exclusions.json').write_text(json.dumps(rejected,indent=2))
manifest={'raw_source_details':counts,'raw_parsed_records':len(records),'clean_records':len(clean),'clean_by_source':{sid:sum(r['source_id']==sid for r in clean) for sid in ['zenodo_15845921','zenodo_18198239']},'excluded_rows':len(rejected),'cleaning':'NFC, HTML unescape, whitespace normalization; exact text duplicate removal within source; conservative email/address/numeric-sequence redaction; source encodings not repaired; no sentiment or topic labels added.','scope':'Published keyword samples contain mixed countries/languages, promotions, social posts and discussion; source title is not a verified topical relevance label. No claim that these are representative Indonesian sellers/buyers.','pdf_extraction_limit':'Date-delimited original reading order. Source IDs and original tweet URLs absent in PDF. Page and row locators retained; encoding artifacts and extraction errors possible.','date_notes':'PDF source posts appear January2024; dataset publication2025. CSV publicationJan2026 and its tweet timestamps are Jan2026. Dates recorded per row.'}
(out/'metadata/zenodo_manifest.json').write_text(json.dumps(manifest,indent=2));print(json.dumps(manifest,indent=2))
for f in (p/'metadata').glob('zenodo_*.json'):shutil.copy2(f,out/'metadata'/f.name)
