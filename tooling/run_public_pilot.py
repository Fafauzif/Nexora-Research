import subprocess,json,time,datetime,pathlib
root=pathlib.Path(__file__).resolve().parent
exe=str(root.parent.parent/'tmp/agent-reach-env/bin/agent-reach')
cmds=[['reddit','search','Shopee Tokopedia biaya admin ongkir','--limit','10','--backend','public-web','--timeout','20'],['twitter','search','Shopee Tokopedia biaya admin ongkir','--limit','10','--backend','public-web','--timeout','20']]
with (root/'agentreach_access_log.jsonl').open('w') as f:
 for i,args in enumerate(cmds):
  start=datetime.datetime.now(datetime.timezone.utc).isoformat()
  p=subprocess.run([exe]+args,capture_output=True,text=True,timeout=30)
  (root/f'pilot_{i+1}_stdout.json').write_text(p.stdout);(root/f'pilot_{i+1}_stderr.txt').write_text(p.stderr)
  f.write(json.dumps({'started_utc':start,'args':args,'exit_code':p.returncode,'stdout_file':f'pilot_{i+1}_stdout.json','stderr_file':f'pilot_{i+1}_stderr.txt'})+'\n');f.flush()
  print(args[0],p.returncode,p.stdout[:1200],flush=True)
