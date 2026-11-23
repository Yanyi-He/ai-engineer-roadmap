"""Promptfoo fixture adapter. Replace with a real SUT adapter in a learner project."""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent


def call_api(prompt,options,context):
    variant = options.get('config',{}).get('variant','baseline')
    filename = {'baseline':'baseline.json','broken':'candidate-broken.json'}[variant]
    bundle = json.loads((HERE/filename).read_text())
    case_id = context['vars']['case_id']
    row = next(r for r in bundle['cases'] if r['case_id']==case_id)
    # Return the complete fixture result so Python assertions can examine context IDs too.
    return {'output':json.dumps(row)}
