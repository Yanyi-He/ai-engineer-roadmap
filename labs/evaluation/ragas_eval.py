"""Run actual Ragas ID metrics; semantic judge mode requires an explicit flag/model."""
import argparse
import asyncio
import importlib.metadata
import json
import math
import os
from pathlib import Path
from .regression import HERE,load,validate_run,parse_output

# Avoid anonymous telemetry for the local teaching fixtures.
os.environ.setdefault('RAGAS_DO_NOT_TRACK','true')


def numeric(value):
    value = float(value)
    if not math.isfinite(value) or not 0 <= value <= 1:
        raise ValueError('Metric result is missing, non-finite or outside [0,1]')
    return value


async def id_metrics(dataset,run):
    from ragas import SingleTurnSample
    from ragas.metrics import IDBasedContextPrecision,IDBasedContextRecall
    validate_run(dataset,run)
    index = {r['case_id']:r for r in run['cases']}
    precision,recall = IDBasedContextPrecision(),IDBasedContextRecall()
    rows = []
    for case in dataset['cases']:
        row = index[case['case_id']]
        sample = SingleTurnSample(retrieved_context_ids=row['retrieved_context_ids'],
                                  reference_context_ids=case['reference_context_ids'])
        scores = {'id_precision':None,'id_recall':None}
        skipped = {}
        if row['retrieved_context_ids']:
            scores['id_precision'] = numeric(await precision.single_turn_ascore(sample))
        else:
            skipped['id_precision'] = 'empty retrieved set; denominator is zero'
        if case['reference_context_ids']:
            scores['id_recall'] = numeric(await recall.single_turn_ascore(sample))
        else:
            skipped['id_recall'] = 'no positive reference IDs; evaluate abstention separately'
        rows.append(dict(case_id=case['case_id'],scores=scores,skipped=skipped))
    return dict(mode='ragas-id',ragas_version=importlib.metadata.version('ragas'),
                dataset_revision=dataset['dataset_revision'],system_revision=run['system_revision'],
                cases=rows,semantic_judge='not_run',performance='not_measured')


async def judge_metrics(dataset,run,model,limit):
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics.collections import Faithfulness,ContextPrecision,ContextRecall,FactualCorrectness
    validate_run(dataset,run)
    if not model or not 1 <= limit <= len(dataset['cases']):
        raise ValueError('Supply a judge model and a positive case limit')
    if not os.environ.get('OPENAI_API_KEY'):
        raise ValueError('Set OPENAI_API_KEY for the explicitly selected judge endpoint')
    options = dict(timeout=30.0,max_retries=0)
    if os.environ.get('AIE_EVAL_JUDGE_BASE_URL'):
        options['base_url'] = os.environ['AIE_EVAL_JUDGE_BASE_URL']
    index = {r['case_id']:r for r in run['cases']}
    selected = [c for c in dataset['cases'] if c['reference'] and not c['requires_abstention']][:limit]
    rows = []
    async with AsyncOpenAI(**options) as client:
        llm = llm_factory(model,client=client,max_retries=1)
        metrics = {'faithfulness':Faithfulness(llm=llm),
                   'context_precision':ContextPrecision(llm=llm),
                   'context_recall':ContextRecall(llm=llm),
                   'factual_correctness':FactualCorrectness(llm=llm)}
        for case in selected:
            row = index[case['case_id']]
            output = parse_output(row['output'])
            if output is None or not row['retrieved_contexts'] or output['abstained']:
                rows.append(dict(case_id=case['case_id'],error='invalid output, empty context or abstention; inspect contract checks'))
                continue
            arguments = {
                'faithfulness':dict(user_input=case['user_input'],response=output['answer'],retrieved_contexts=row['retrieved_contexts']),
                'context_precision':dict(user_input=case['user_input'],reference=case['reference'],retrieved_contexts=row['retrieved_contexts']),
                'context_recall':dict(user_input=case['user_input'],reference=case['reference'],retrieved_contexts=row['retrieved_contexts']),
                'factual_correctness':dict(response=output['answer'],reference=case['reference']),
            }
            scores,errors = {},{}
            for name,metric in metrics.items():
                try:
                    result = await asyncio.wait_for(metric.ascore(**arguments[name]),timeout=60)
                    scores[name] = numeric(result.value)
                except Exception as e:
                    # Errors remain errors; an unavailable judge never becomes a zero or passing score.
                    scores[name] = None
                    errors[name] = type(e).__name__
            rows.append(dict(case_id=case['case_id'],scores=scores,errors=errors))
    return dict(mode='ragas-judge',ragas_version=importlib.metadata.version('ragas'),
                judge_model=model,dataset_revision=dataset['dataset_revision'],
                system_revision=run['system_revision'],cases=rows,
                selection='first eligible labeled cases, for integration smoke only',
                n_selected=len(selected),n_total=len(dataset['cases']),
                judge_cost='not_collected; add provider usage before using a cost gate',
                passed_runtime=bool(rows) and all(not r.get('error') and not r.get('errors') for r in rows))


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset',type=Path,default=HERE/'dataset.json')
    p.add_argument('--run',type=Path,default=HERE/'baseline.json')
    p.add_argument('--mode',choices=['id','judge'],default='id')
    p.add_argument('--judge-model')
    p.add_argument('--limit',type=int,default=2)
    p.add_argument('--output',type=Path,required=True)
    args = p.parse_args()
    dataset,run = load(args.dataset),load(args.run)
    if args.mode=='id':
        result = asyncio.run(id_metrics(dataset,run))
    else:
        result = asyncio.run(judge_metrics(dataset,run,args.judge_model,args.limit))
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,ensure_ascii=False,indent=2,allow_nan=False)+'\n')
    print(json.dumps(dict(mode=result['mode'],ragas_version=result['ragas_version'],cases=len(result['cases']))))
    if args.mode=='judge' and not result['passed_runtime']:
        raise SystemExit(1)


if __name__=='__main__':
    main()
