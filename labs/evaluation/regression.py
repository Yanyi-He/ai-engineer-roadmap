"""Deterministic contracts and paired retrieval regression; no model or SDK needed."""
import argparse
import hashlib
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
METRIC_REVISION = 'id-set-and-contract-v1'


def load(path):
    return json.loads(Path(path).read_text())


def validate_run(dataset, run):
    if dataset['dataset_revision'] != run['dataset_revision']:
        raise ValueError('Dataset revisions differ; re-run both systems on the same dataset')
    labels = [c['case_id'] for c in dataset['cases']]
    if len(labels) != len(set(labels)):
        raise ValueError('Duplicate golden case IDs')
    expected = set(labels)
    actual = [c['case_id'] for c in run['cases']]
    if len(actual) != len(set(actual)) or set(actual) != expected:
        raise ValueError('Missing, duplicate or extra case IDs')
    for row in run['cases']:
        ids = row['retrieved_context_ids']
        if len(ids) != len(set(ids)) or not all(isinstance(x,str) for x in ids):
            raise ValueError('Retrieved IDs must be unique strings')
        if len(ids) != len(row['retrieved_contexts']):
            raise ValueError('Context IDs/text lengths differ')
        if not isinstance(row['output'],str):
            raise ValueError('Preserve the raw output string for contract validation')


def parse_output(raw):
    try:
        value = json.loads(raw)
    except (json.JSONDecodeError,TypeError):
        return None
    if not isinstance(value,dict) or set(value) != {'answer','citations','abstained'}:
        return None
    if not isinstance(value['answer'],str) or type(value['abstained']) is not bool:
        return None
    citations = value['citations']
    if not isinstance(citations,list) or not all(isinstance(x,str) for x in citations):
        return None
    if len(citations) != len(set(citations)):
        return None
    return value


def score_case(case, row):
    retrieved = set(row['retrieved_context_ids'])
    gold = set(case['reference_context_ids'])
    allowed = set(case['allowed_context_ids'])
    output = parse_output(row['output'])
    checks = {'schema':output is not None, 'authorized_context':retrieved <= allowed}
    checks['citation_membership'] = bool(output is not None and
        set(output['citations']) <= (retrieved & allowed) and
        (output['abstained'] or bool(output['citations'])))
    checks['required_abstention'] = bool(output is not None and
        (not case['requires_abstention'] or output['abstained']))
    scores = {
        'id_precision':len(retrieved & gold)/len(retrieved) if retrieved else None,
        'id_recall':len(retrieved & gold)/len(gold) if gold else None,
    }
    return dict(case_id=case['case_id'],slice=case['slice'],checks=checks,scores=scores)


def summarize(rows):
    summary = {}
    for key in ['id_precision','id_recall']:
        values = [r['scores'][key] for r in rows if r['scores'][key] is not None]
        summary[key] = dict(mean=math.fsum(values)/len(values) if values else None,
                            n_scored=len(values),n_total=len(rows))
    return summary


def score_run(dataset, run):
    validate_run(dataset,run)
    index = {r['case_id']:r for r in run['cases']}
    rows = [score_case(case,index[case['case_id']]) for case in dataset['cases']]
    return dict(metric_revision=METRIC_REVISION,system_revision=run['system_revision'],
                cases=rows,summary=summarize(rows))


def compare(dataset, baseline, candidate, policy):
    if baseline.get('measurement_mode') != candidate.get('measurement_mode'):
        raise ValueError('Measurement modes differ; do not compare fixtures with real runs')
    base = score_run(dataset,baseline)
    changed = score_run(dataset,candidate)
    reasons = []
    for label,report in [('baseline',base),('candidate',changed)]:
        for row in report['cases']:
            for key,passed in row['checks'].items():
                if not passed:
                    reasons.append(f'{label}:{row["case_id"]}:{key}')
    deltas = {}
    for key,margin in policy['max_mean_drop'].items():
        if key not in base['summary'] or not math.isfinite(margin) or margin < 0:
            raise ValueError('Unknown metric or invalid regression margin')
        # Match the scored population as well as the aggregate denominator.
        b_ids = {r['case_id'] for r in base['cases'] if r['scores'][key] is not None}
        c_ids = {r['case_id'] for r in changed['cases'] if r['scores'][key] is not None}
        if b_ids != c_ids:
            reasons.append(f'candidate:{key}:scored-population-changed')
            deltas[key] = None
            continue
        a,b = base['summary'][key]['mean'],changed['summary'][key]['mean']
        deltas[key] = b-a if a is not None and b is not None else None
        if deltas[key] is None:
            reasons.append(f'candidate:{key}:no-scored-cases')
        elif deltas[key] < -margin-1e-12:
            reasons.append(f'candidate:{key}:drop={deltas[key]:.4f}')
    for key,floor in policy.get('min_mean',{}).items():
        if key not in changed['summary'] or not math.isfinite(floor) or not 0 <= floor <= 1:
            raise ValueError('Unknown metric or invalid absolute floor')
        value = changed['summary'][key]['mean']
        if value is None or value < floor:
            reasons.append(f'candidate:{key}:below-floor={floor}')
    return dict(passed=not reasons,reasons=reasons,dataset_revision=dataset['dataset_revision'],
                policy_revision=policy['policy_revision'],metric_revision=METRIC_REVISION,
                deltas=deltas,baseline=base,candidate=changed,
                measurement_mode=candidate.get('measurement_mode','unspecified'),
                semantic_judge='not_run',performance='not_measured')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--dataset',type=Path,default=HERE/'dataset.json')
    p.add_argument('--baseline',type=Path,default=HERE/'baseline.json')
    p.add_argument('--candidate',type=Path,default=HERE/'baseline.json')
    p.add_argument('--policy',type=Path,default=HERE/'policy.json')
    p.add_argument('--output',type=Path)
    args = p.parse_args()
    try:
        report = compare(load(args.dataset),load(args.baseline),load(args.candidate),load(args.policy))
    except (ValueError,KeyError,TypeError) as e:
        raise SystemExit(f'Invalid evaluation input: {e}')
    report['input_sha256'] = {name:hashlib.sha256(path.read_bytes()).hexdigest() for name,path in [('dataset',args.dataset),('baseline',args.baseline),('candidate',args.candidate),('policy',args.policy)]}
    text = json.dumps(report,ensure_ascii=False,indent=2,allow_nan=False)+'\n'
    if args.output:
        args.output.parent.mkdir(parents=True,exist_ok=True)
        args.output.write_text(text)
    print(json.dumps(dict(passed=report['passed'],reasons=report['reasons'],deltas=report['deltas'])))
    raise SystemExit(0 if report['passed'] else 1)


if __name__=='__main__':
    main()
