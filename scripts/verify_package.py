#!/usr/bin/env python3
"""Verify extracted payload checksums; optionally stream-count authoritative clean data."""
from pathlib import Path
import argparse,json,hashlib,gzip,csv
p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parents[1]);p.add_argument('--counts',action='store_true');a=p.parse_args()
def sha(path):
 h=hashlib.sha256()
 with path.open('rb') as f:
  for b in iter(lambda:f.read(2**20),b''):h.update(b)
 return h.hexdigest()
manifest=json.loads((a.root/'MANIFEST_FILES.json').read_text());bad=[]
for x in manifest:
 f=a.root/x['path']
 if not f.is_file() or f.stat().st_size!=x['bytes'] or sha(f)!=x['sha256']:bad.append(x['path'])
if bad:raise SystemExit('FAILED: '+repr(bad))
print('PASS payload checksums:',len(manifest))
if a.counts:
 s=json.loads((a.root/'RUN_SUMMARY.json').read_text());c={}
 with gzip.open(a.root/'datasets/app_reviews/clean/app_reviews.jsonl.gz','rt',encoding='utf-8') as f:c['app_reviews']=sum(1 for line in f if json.loads(line))
 with gzip.open(a.root/'datasets/twitter/clean/twcs_ecommerce_connected_clean.csv.gz','rt',encoding='utf-8',newline='') as f:c['historical_support_tweets']=sum(1 for row in csv.DictReader(f))
 with (a.root/'datasets/twitter/clean/zenodo_ecommerce_twitter_clean.jsonl').open() as f:c['published_zenodo_records']=sum(1 for line in f if json.loads(line))
 assert c==s['authoritative_clean_record_counts'],(c,s['authoritative_clean_record_counts'])
 print('PASS clean record counts:',json.dumps(c))
