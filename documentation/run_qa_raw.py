import json,pathlib,zipfile,csv,io,hashlib,time
B=pathlib.Path('/workspace/scratch/1ba9d8b39c55/collection');rs=[];counts=json.loads((B/'review_collection/metadata/cleaning_counts.json').read_text());ds=json.loads((B/'review_collection/source_manifest.json').read_text());lookup={x['source_id']:x for x in ds['sources']};hashes={}
for s in counts:
 p=B/'review_collection/raw'/(s['dataset_ref'].replace('/','__')+'.zip')
 if str(p) not in hashes:
  h=hashlib.sha256()
  with open(p,'rb') as f:
   for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
  hashes[str(p)]=h.hexdigest()
 with zipfile.ZipFile(p) as z,z.open(s['archive_member']) as f:
  reader=csv.DictReader(io.TextIOWrapper(f,encoding='utf-8-sig'))
  n=sum(1 for _ in reader)
 rs.append({'source_id':s['source_id'],'archive':p.name,'member':s['archive_member'],'actual_raw_rows':n,'expected_raw_rows':s['raw_rows'],'row_count_match':n==s['raw_rows'],'archive_sha256_match':hashes[str(p)]==lookup[s['source_id']]['download']['sha256'],'metadata_license':lookup[s['source_id']]['license']})
 print(s['source_id'],n,flush=True)
(B/'documentation/qa_raw_validation.json').write_text(json.dumps(rs,indent=2))
