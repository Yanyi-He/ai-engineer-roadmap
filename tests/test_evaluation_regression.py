"""Verify the release gate detects failures that aggregate quality can hide."""
import copy
import unittest
from labs.evaluation.regression import HERE,load,compare,score_run,score_case,parse_output

class EvaluationRegressionTests(unittest.TestCase):
    def setUp(self):
        self.dataset=load(HERE/'dataset.json')
        self.base=load(HERE/'baseline.json')
        self.policy=load(HERE/'policy.json')

    def test_unchanged_system_passes(self):
        self.assertTrue(compare(self.dataset,self.base,self.base,self.policy)['passed'])

    def test_security_failure_survives_permissive_quality_margins(self):
        broken=load(HERE/'candidate-broken.json')
        self.policy['max_mean_drop']={'id_recall':1,'id_precision':1}
        self.policy['min_mean']={}
        out=compare(self.dataset,self.base,broken,self.policy)
        self.assertFalse(out['passed'])
        self.assertIn('candidate:tenant:authorized_context',out['reasons'])

    def test_missing_or_duplicate_cases_are_invalid(self):
        for rows in [self.base['cases'][:-1],self.base['cases']+[self.base['cases'][0]]]:
            bad={**self.base,'cases':rows}
            with self.assertRaisesRegex(ValueError,'case IDs'):
                score_run(self.dataset,bad)

    def test_no_positive_labels_is_not_perfect_recall(self):
        report=score_run(self.dataset,self.base)
        row=next(r for r in report['cases'] if r['case_id']=='unanswerable')
        self.assertIsNone(row['scores']['id_recall'])
        self.assertEqual(report['summary']['id_recall']['n_scored'],4)
        self.assertEqual(report['summary']['id_recall']['n_total'],6)

    def test_retrieval_regression_with_valid_contracts_is_detected(self):
        bad=copy.deepcopy(self.base)
        row=next(r for r in bad['cases'] if r['case_id']=='refund')
        row['retrieved_context_ids']=['refunds']
        row['retrieved_contexts']=[self.dataset['corpus']['refunds']]
        row['output']='{"answer":"Finance approval.","citations":["refunds"],"abstained":false}'
        result=compare(self.dataset,self.base,bad,self.policy)
        self.assertTrue(all(next(r for r in result['candidate']['cases'] if r['case_id']=='refund')['checks'].values()))
        self.assertFalse(result['passed'])
        self.assertTrue(any('id_recall:drop' in r for r in result['reasons']))

    def test_dataset_revision_change_requires_reexecution(self):
        bad={**self.base,'dataset_revision':'different'}
        with self.assertRaisesRegex(ValueError,'revisions differ'):
            compare(self.dataset,self.base,bad,self.policy)

    def test_unsupported_citation_fails(self):
        case=self.dataset['cases'][0]
        row={**self.base['cases'][0],'output':'{"answer":"30 days","citations":["shipping"],"abstained":false}'}
        self.assertFalse(score_case(case,row)['checks']['citation_membership'])

    def test_unchanged_poor_baseline_still_fails_absolute_floor(self):
        poor=copy.deepcopy(self.base)
        row=next(r for r in poor['cases'] if r['case_id']=='refund')
        row['retrieved_context_ids']=['refunds']
        row['retrieved_contexts']=[self.dataset['corpus']['refunds']]
        row['output']='{"answer":"Finance approval.","citations":["refunds"],"abstained":false}'
        out=compare(self.dataset,poor,poor,self.policy)
        self.assertEqual(out['deltas']['id_recall'],0)
        self.assertFalse(out['passed'])
        self.assertTrue(any('below-floor' in r for r in out['reasons']))

    def test_schema_rejects_wrong_field_types(self):
        self.assertIsNone(parse_output('{"answer":"x","citations":[],"abstained":1}'))

if __name__=='__main__':unittest.main()
