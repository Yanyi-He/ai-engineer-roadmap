"""Reproduce separate China/NA mention statistics and title-level counts."""
import collections,csv,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def summary(rows):
 return {'n':len(rows),'employers':len({r['company'] for r in rows}),'country':dict(collections.Counter(r['country'] for r in rows)),'sector':dict(collections.Counter(r['sector'] for r in rows)),'source_grade':dict(collections.Counter(r['source_grade'] for r in rows)),'seniority':dict(collections.Counter(r['seniority'] for r in rows)),'archetype':dict(collections.Counter(r['archetype'] for r in rows)),'active_status':dict(collections.Counter(r['active_status'] for r in rows))}
def main():
 rows=json.loads((ROOT/'research/jds.json').read_text());keys=list(rows[0]['features']);records=[]
 for key in keys:
  item={'keyword':key}
  for field,value,prefix in [('market','CN','CN'),('market','NA','NA'),('country','CA','CA'),('country','US','US')]:
   cohort=[r for r in rows if r[field]==value];n=len(cohort);count=sum(r['features'][key] for r in cohort);employers=sorted({r['company'] for r in cohort})
   item.update({prefix+'_n':n,prefix+'_count':count,prefix+'_pct':round(count/n*100,2) if n else None,prefix+'_employer_balanced_pct':round(100*sum(sum(r['features'][key] for r in cohort if r['company']==c)/sum(r['company']==c for r in cohort) for c in employers)/len(employers),2) if employers else None})
  records.append(item)
 with (ROOT/'research/keyword-counts.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=records[0]);w.writeheader();w.writerows(records)
 report={'collection_window':'2026-11-18 to 2026-11-19','scope':'Application/systems AI engineering; purposive descriptions, not national active totals','overall':summary(rows),'markets':{m:summary([r for r in rows if r['market']==m]) for m in ['CN','NA']},'countries':{c:summary([r for r in rows if r['country']==c]) for c in ['CN','CA','US']}}
 (ROOT/'research/sample-summary.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
 for field in ['market','sector','seniority','archetype']:
  groups={value:{'n':len(sub),'counts':{k:sum(r['features'][k] for r in sub) for k in keys}} for value in sorted({r[field] for r in rows}) if (sub:=[r for r in rows if r[field]==value])}
  (ROOT/f'research/by-{field}.json').write_text(json.dumps(groups,ensure_ascii=False,indent=2)+'\n')
 print(json.dumps({'n':len(rows),'CN':report['markets']['CN']['n'],'NA':report['markets']['NA']['n'],'countries':report['overall']['country'],'employers':report['overall']['employers']},ensure_ascii=False))
if __name__=='__main__':main()
