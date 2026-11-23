import json,math,sqlite3,subprocess,sys,tempfile,unittest
import concurrent.futures,threading
from pathlib import Path
from labs.retrieval import BM25,metrics,evaluate
from labs.memory import Memory,Principal,Conflict
from labs.durable import run

class RetrievalTests(unittest.TestCase):
    def test_known_graded_ndcg(self):
        r=metrics(['b','a'],{'a':2,'b':1},2)
        self.assertEqual(r['recall'],1)
        self.assertAlmostEqual(r['ndcg'],(1+3/math.log2(3))/(3+1/math.log2(3)))
    def test_unanswerable_is_not_perfect_recall(self):
        self.assertIsNone(metrics([],{},3)['recall'])
        self.assertFalse(metrics(['a'],{},3)['empty_result'])
    def test_duplicate_results_fail(self):
        with self.assertRaises(ValueError):metrics(['a','a'],{'a':1},2)
    def test_empty_and_authorized_scope(self):
        self.assertEqual(BM25([]).search('anything'),[])
        docs=[{'id':'a','scope':'alpha','text':'secret budget'},{'id':'b','scope':'beta','text':'secret budget'}]
        self.assertEqual(BM25(docs).search('budget',scope='beta'),['b'])
    def test_fixture_splits_and_qrels(self):
        p=Path(__file__).parents[1]/'labs/retrieval-fixture.json';d=json.loads(p.read_text())
        self.assertEqual({q['split'] for q in d['queries']},{'dev','holdout'})
        self.assertTrue(set(q['group'] for q in d['queries'] if q['split']=='dev').isdisjoint(q['group'] for q in d['queries'] if q['split']=='holdout'))
        self.assertGreater(evaluate(d,'holdout',3)['n_queries'],0)

class MemoryTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'memory.sqlite';self.m=Memory(self.path)
        self.a=Principal('alice',frozenset({'work','personal'}));self.b=Principal('bob',frozenset({'work'}))
    def tearDown(self):self.m.close();self.tmp.cleanup()
    def put(self,**kw):
        args=dict(p=self.a,scope='work',key='city',value='A',source='user:1',valid_from='2026-01-01T00:00:00Z',expected_version=0,request_id='r1');args.update(kw);return self.m.put(**args)
    def test_idempotent_and_payload_conflict(self):
        self.assertEqual(self.put(),self.put())
        with self.assertRaises(Conflict):self.put(value='B')
    def test_update_and_valid_time(self):
        self.put();self.put(value='B',valid_from='2026-02-01T00:00:00Z',expected_version=1,request_id='r2')
        self.assertEqual(self.m.get(self.a,'work','city')['value'],'B')
        self.assertEqual(self.m.get(self.a,'work','city','2026-01-15T00:00:00Z')['value'],'A')
    def test_owner_scope_and_missing(self):
        self.put();self.assertIsNone(self.m.get(self.b,'work','city'));self.assertIsNone(self.m.get(self.a,'personal','city'))
        with self.assertRaises(PermissionError):self.m.get(self.b,'personal','city')
    def test_stale_write_rolls_back(self):
        self.put()
        with self.assertRaises(Conflict):self.put(value='bad',valid_from='2026-02-01T00:00:00Z',request_id='r2')
        self.assertEqual(self.m.get(self.a,'work','city')['value'],'A')
        self.put(value='B',valid_from='2026-02-01T00:00:00Z',expected_version=1,request_id='r2')
    def test_delete_covers_historical_reads(self):
        self.put();self.m.forget(self.a,'work','city')
        self.assertIsNone(self.m.get(self.a,'work','city'));self.assertIsNone(self.m.get(self.a,'work','city','2026-01-15T00:00:00Z'))
        self.assertEqual(self.m.db.execute('SELECT count(*) FROM facts WHERE value IS NOT NULL').fetchone()[0],0)
    def test_state_survives_reopen(self):
        self.put();self.m.close();self.m=Memory(self.path);self.assertEqual(self.m.get(self.a,'work','city')['value'],'A')
    def test_scheduled_update_does_not_replace_current_fact(self):
        self.put();self.put(value='future',valid_from='9998-01-01T00:00:00Z',expected_version=1,request_id='future')
        self.assertEqual(self.m.get(self.a,'work','city')['value'],'A')
    def test_concurrent_compare_and_swap(self):
        barrier=threading.Barrier(2)
        def write(request):
            m=Memory(self.path);barrier.wait()
            try:
                m.put(self.a,'work','city','A','user:1','2026-01-01T00:00:00Z',0,request)
                return 'accepted'
            except Conflict:return 'conflict'
            finally:m.close()
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            self.assertCountEqual(list(pool.map(write,['x','y'])),['accepted','conflict'])

class DurableTests(unittest.TestCase):
    def test_waits_for_approval(self):
        with tempfile.TemporaryDirectory() as d:
            self.assertEqual(run(d,'r')['status'],'awaiting_user')
            db=sqlite3.connect(Path(d)/'provider.sqlite');self.assertEqual(db.execute('SELECT count(*) FROM receipts').fetchone()[0],0);db.close()
    def test_effect_commit_then_hard_exit_then_resume(self):
        with tempfile.TemporaryDirectory() as d:
            p=subprocess.run([sys.executable,'-B','-m','labs.durable','--dir',d,'--run-id','r','--approve','--fault','after-effect'],capture_output=True,text=True)
            self.assertEqual(p.returncode,17)
            db=sqlite3.connect(Path(d)/'workflow.sqlite');self.assertEqual(db.execute("SELECT count(*) FROM artifacts WHERE stage='apply'").fetchone()[0],0);db.close()
            self.assertEqual(run(d,'r'),{'status':'succeeded','effect_count':1})
            self.assertEqual(run(d,'r'),{'status':'succeeded','effect_count':1})

if __name__=='__main__':unittest.main()
