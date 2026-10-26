#!/usr/bin/env python3
"""Build provenance-only registry across two partial discovery streams."""
from pathlib import Path
import json,csv,collections
root=Path(__file__).resolve().parents[1]
registry={}
for stream,p in [('web_search_service',root/'clean/social_index_records.jsonl'),('AgentReach_publicweb',root/'agentreach_clean/agentreach_publicweb_records.jsonl')]:
 if not p.exists():continue
 for line in p.read_text().splitlines():
  d=json.loads(line);u=d['canonical_url']
  r=registry.setdefault(u,{'canonical_url':u,'platform':d['platform'],'streams':[],'record_ids':[]})
  r['streams'].append(stream);r['record_ids'].append(d['record_id'])
with open(root/'clean/social_source_url_registry.csv','w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=['canonical_url','platform','streams','record_ids']);w.writeheader()
 for r in registry.values():w.writerow({k:json.dumps(v) if isinstance(v,list) else v for k,v in r.items()})
summary={'unique_source_urls_across_discovery_streams':len(registry),'by_platform':dict(collections.Counter(x['platform'] for x in registry.values())),'URLs_appearing_in_both_streams':sum(len(x['streams'])>1 for x in registry.values()),'note':'Do not sum discovery-stream rows as independent source conversations. Does not deduplicate against externally downloaded corpora.'}
(root/'logs/cross_stream_inventory.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary,indent=2))
