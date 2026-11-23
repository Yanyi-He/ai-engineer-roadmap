"""Deterministic Promptfoo assertion using the same deterministic contracts as the Python runner."""
import json
from pathlib import Path
import importlib.util

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('evaluation_reference_regression',HERE/'regression.py')
regression = importlib.util.module_from_spec(spec)
spec.loader.exec_module(regression)


def get_assert(output,context):
    dataset = json.loads((HERE/'dataset.json').read_text())
    case = next(c for c in dataset['cases'] if c['case_id']==context['vars']['case_id'])
    row = json.loads(output) if isinstance(output,str) else output
    result = regression.score_case(case,row)
    failed = [k for k,v in result['checks'].items() if not v]
    return {'pass':not failed,'score':0.0 if failed else 1.0,'reason':', '.join(failed) or 'fixture contracts/retrieval passed; semantic judge not run'}
