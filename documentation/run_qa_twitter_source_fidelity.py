import pathlib,csv,gzip,zipfile,io,json
B=pathlib.Path('/workspace/scratch/1ba9d8b39c55/collection');raw=B/'x_collection/ready/raw/twcs_ecommerce_connected_original_rows.csv.gz';samples={}
with gzip.open(raw,'rt',encoding='utf8',newline='') as f:
 for i,r in enumerate(csv.DictReader(f)):
  if i%25000==0:samples[r['tweet_id']]=r
matches=0;scanned=0;mismatches=[];archive=B/'x_collection/raw/twcs_download.zip'
with zipfile.ZipFile(archive) as z,z.open('twcs/twcs.csv') as f:
 for r in csv.DictReader(io.TextIOWrapper(f,encoding='utf8',newline='')):
  scanned+=1
  if r['tweet_id']in samples:
   if r==samples[r['tweet_id']]:matches+=1
   else:mismatches.append(r['tweet_id'])
result={'source_full_csv_rows_scanned':scanned,'systematic_scoped_raw_samples':len(samples),'exact_field_value_matches':matches,'mismatch_ids':mismatches,'scope':'Original fieldvalues at systematically selected raw scoped rows; CSV byte serialization not identical by design'}
(B/'documentation/qa_twitter_source_fidelity.json').write_text(json.dumps(result,indent=2));print(result)
