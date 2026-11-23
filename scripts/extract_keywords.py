"""Re-extract scoped literal mentions from exact frozen private bodies."""
import argparse,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
CODEBOOK=json.loads((ROOT/'research/keyword-codebook.json').read_text())

def features(text):
 return {key:bool(re.search(pattern,text,re.I|re.ASCII)) for key,pattern in CODEBOOK.items()}

def extract(rows,annotations):
 index={r['jd_id']:r for r in annotations};out=[]
 for private in rows:
  record=index[private['jd_id']];body=private['body']
  if hashlib.sha256(body.encode()).hexdigest()!=record['body_sha256']:
   raise ValueError(f"Body hash mismatch: {record['jd_id']}")
  parts={}
  for s in record['sections']:
   a,z=s['start'],s['end']
   if not 0<=a<z<=len(body):raise ValueError('Invalid offsets')
   text=body[a:z]
   if hashlib.sha256(text.encode()).hexdigest()!=s['sha256']:raise ValueError('Section hash mismatch')
   parts.setdefault(s['label'],[]).append(text)
  out.append({'jd_id':record['jd_id'],'body_sha256':record['body_sha256'],'section_features':{k:features(' '.join(v)) for k,v in parts.items()},'features':features(' '.join(t for v in parts.values() for t in v))})
 return out

if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--annotations',required=True);p.add_argument('--output',required=True);args=p.parse_args()
 result=extract(json.loads(Path(args.input).read_text()),json.loads(Path(args.annotations).read_text()))
 Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
