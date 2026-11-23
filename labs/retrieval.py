"""BM25 and ranking metrics. No model calls and no claims about dense retrieval."""
import argparse,collections,hashlib,json,math,re,unicodedata
from pathlib import Path

def tokens(text):
    text=unicodedata.normalize('NFKC',text).casefold()
    # English-token fixture only. Chinese requires a tested tokenizer, not this regex.
    return re.findall(r'[a-z0-9]+',text)

class BM25:
    def __init__(self,documents,k1=1.5,b=0.75):
        self.docs=documents;self.k1=k1;self.b=b
        ids=[d['id'] for d in documents]
        if len(set(ids))!=len(ids):raise ValueError('duplicate document IDs')
        self.counts=[collections.Counter(tokens(d['text'])) for d in documents]
        self.lengths=[sum(c.values()) for c in self.counts]
        self.avg=sum(self.lengths)/len(self.lengths) if self.lengths else 0
        self.df=collections.Counter(t for c in self.counts for t in c)
    def search(self,query,k=3,scope=None):
        ranked=[];n=len(self.docs)
        for d,c,length in zip(self.docs,self.counts,self.lengths):
            if scope is not None and d['scope']!=scope:continue
            score=0.0
            for t in set(tokens(query)):
                tf=c[t]
                if not tf:continue
                idf=math.log(1+(n-self.df[t]+0.5)/(self.df[t]+0.5))
                score+=idf*tf*(self.k1+1)/(tf+self.k1*(1-self.b+self.b*length/self.avg))
            if score>0:ranked.append((d['id'],score))
        return [id for id,_ in sorted(ranked,key=lambda x:(-x[1],x[0]))[:k]]

def metrics(ranking,qrels,k):
    if k<1:raise ValueError('k must be positive')
    if len(ranking)!=len(set(ranking)):raise ValueError('duplicate ranking IDs')
    relevant={id:g for id,g in qrels.items() if g>0}
    if not relevant:
        # Relevance metrics are undefined here; do not silently reward a no-answer case.
        return {'recall':None,'ndcg':None,'empty_result':not ranking}
    ranked=ranking[:k]
    recall=len(set(ranked)&set(relevant))/len(relevant)
    dcg=sum((2**qrels.get(id,0)-1)/math.log2(i+2) for i,id in enumerate(ranked))
    ideal=sum((2**g-1)/math.log2(i+2) for i,g in enumerate(sorted(relevant.values(),reverse=True)[:k]))
    return {'recall':recall,'ndcg':dcg/ideal,'empty_result':not ranking}

def evaluate(data,split,k):
    ids={d['id'] for d in data['documents']};index=BM25(data['documents']);rows=[]
    for q in data['queries']:
        if q['split']!=split:continue
        if set(q['qrels'])-ids:raise ValueError('qrel references an unknown document')
        ranking=index.search(q['query'],k,scope=q['scope'])
        rows.append({'query_id':q['id'],'slice':q['slice'],'ranking':ranking,**metrics(ranking,q['qrels'],k)})
    if not rows:raise ValueError('empty evaluation split')
    answered=[x for x in rows if x['recall'] is not None];empty=[x for x in rows if x['recall'] is None]
    return {'split':split,'n_queries':len(rows),'n_answerable':len(answered),'n_unanswerable':len(empty),
            'recall_at_k':sum(x['recall'] for x in answered)/len(answered) if answered else None,
            'ndcg_at_k':sum(x['ndcg'] for x in answered)/len(answered) if answered else None,
            'unanswerable_empty_result_rate':sum(x['empty_result'] for x in empty)/len(empty) if empty else None,
            'rows':rows,'k':k,'kind':'synthetic teaching fixture; not an enterprise benchmark'}

def main():
    p=argparse.ArgumentParser();p.add_argument('--split',choices=['dev','holdout'],default='dev');p.add_argument('--k',type=int,default=3);a=p.parse_args()
    path=Path(__file__).with_name('retrieval-fixture.json');raw=path.read_bytes();out=evaluate(json.loads(raw),a.split,a.k)
    out['dataset_sha256']=hashlib.sha256(raw).hexdigest();out['ranker']='bm25-reference-v1'
    print(json.dumps(out,indent=2))
if __name__=='__main__':main()
