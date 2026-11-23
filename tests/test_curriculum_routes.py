"""Guard the application/systems scope and real learning-path dependencies."""
import json
import unittest
from pathlib import Path
from scripts.curriculum_graph import index_units, topological_units, expand_route

ROOT = Path(__file__).resolve().parents[1]

class CurriculumRouteTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.modules = json.loads((ROOT/'data/curriculum.json').read_text())
        cls.units = index_units(cls.modules)
        cls.routes = {r['id']:r for r in json.loads((ROOT/'data/learning-routes.json').read_text())}

    def test_rejects_dependency_cycle(self):
        modules = [{'nodes':[{'id':'00.1','prerequisites':['00.2']},
                             {'id':'00.2','prerequisites':['00.1']}]}]
        with self.assertRaisesRegex(ValueError,'cycle'):
            topological_units(modules)

    def test_rejects_unknown_prerequisite(self):
        with self.assertRaisesRegex(ValueError,'Unknown'):
            topological_units([{'nodes':[{'id':'00.1','prerequisites':['99.9']}]}])

    def test_api_delivery_does_not_require_weight_training_or_gpu_serving(self):
        ids = {x for s in expand_route(self.modules,self.routes['application']) for x in s['units']}
        self.assertIn('14.6',ids)
        self.assertIn('11.8',ids)
        self.assertTrue(ids.isdisjoint({'12.2','12.3','12.6','12.7','13.3','13.6','09.2'}))

    def test_agent_loop_does_not_require_rag(self):
        route = {'stages':[{'targets':['07.3']}]}
        ids = {x for s in expand_route(self.modules,route) for x in s['units']}
        self.assertFalse(any(x.startswith('06.') for x in ids))

    def test_mcp_protocol_is_accessible_from_backend_foundations(self):
        route = {'stages':[{'targets':['10.2']}]}
        ids = {x for s in expand_route(self.modules,route) for x in s['units']}
        self.assertFalse(any(x.startswith(('06.','07.','08.','12.','13.')) for x in ids))

    def test_optional_rl_branch_is_explicit(self):
        route = self.routes['agent_platform']
        normal = {x for s in expand_route(self.modules,route) for x in s['units']}
        selected = {x for s in expand_route(self.modules,route,include_optional=True) for x in s['units']}
        self.assertNotIn('12.7',normal)
        self.assertIn('12.7',selected)
        self.assertIn('12.2',selected)

    def test_common_knowledge_does_not_require_a_specialization(self):
        for n in self.units.values():
            if n['track']=='core':
                self.assertTrue(all(self.units[p]['track']=='core' for p in n['prerequisites']),n['id'])

    def test_every_unit_has_bilingual_self_checks(self):
        for id,unit in self.units.items():
            self.assertGreaterEqual(len(unit['checks_en']),3,id)
            self.assertEqual(len(unit['checks_zh']),len(unit['checks_en']),id)
            self.assertEqual(len(set(unit['checks_en'])),len(unit['checks_en']),id)

if __name__ == '__main__':
    unittest.main()
