"""Crash-recovery example with TWO independently committed SQLite stores.

The effect service simulates an external provider that supports idempotency.
The result is specific to that provider contract, not generic exactly-once I/O.
"""
import argparse,json,os,sqlite3
from pathlib import Path

def run(directory,run_id,approve=False,fault=None):
    directory=Path(directory);directory.mkdir(parents=True,exist_ok=True)
    state=sqlite3.connect(directory/'workflow.sqlite');effect=sqlite3.connect(directory/'provider.sqlite')
    state.executescript('CREATE TABLE IF NOT EXISTS runs(id TEXT PRIMARY KEY,status TEXT); CREATE TABLE IF NOT EXISTS artifacts(run TEXT,stage TEXT,value TEXT,PRIMARY KEY(run,stage));')
    effect.execute('CREATE TABLE IF NOT EXISTS receipts(key TEXT PRIMARY KEY,value TEXT)')
    with state:state.execute("INSERT OR IGNORE INTO runs VALUES(?,'created')",(run_id,))
    status=state.execute('SELECT status FROM runs WHERE id=?',(run_id,)).fetchone()[0]
    if status=='succeeded':
        count=effect.execute('SELECT COUNT(*) FROM receipts').fetchone()[0]
        state.close();effect.close();return {'status':status,'effect_count':count}
    if not state.execute("SELECT 1 FROM artifacts WHERE run=? AND stage='review'",(run_id,)).fetchone():
        with state:
            state.execute("INSERT INTO artifacts VALUES(?,'review','review-v1')",(run_id,))
            state.execute("UPDATE runs SET status='awaiting_user' WHERE id=?",(run_id,))
    if approve:
        # CLI approval simulates a user action. A service must bind auth + expected version.
        with state:state.execute("INSERT OR IGNORE INTO artifacts VALUES(?,'approval','approved')",(run_id,))
    if not state.execute("SELECT 1 FROM artifacts WHERE run=? AND stage='approval'",(run_id,)).fetchone():
        state.close();effect.close();return {'status':'awaiting_user'}
    receipt=f'{run_id}:apply:v1'
    with effect:effect.execute("INSERT OR IGNORE INTO receipts VALUES(?, 'applied')",(receipt,))
    if fault=='after-effect':os._exit(17)  # actual abrupt process exit, before workflow checkpoint
    with state:
        state.execute("INSERT OR IGNORE INTO artifacts VALUES(?,'apply',?)",(run_id,receipt))
        state.execute("UPDATE runs SET status='succeeded' WHERE id=?",(run_id,))
    out={'status':'succeeded','effect_count':effect.execute('SELECT COUNT(*) FROM receipts').fetchone()[0]}
    state.close();effect.close();return out

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--dir',required=True);p.add_argument('--run-id',default='demo');p.add_argument('--approve',action='store_true');p.add_argument('--fault',choices=['after-effect']);a=p.parse_args()
    print(json.dumps(run(a.dir,a.run_id,a.approve,a.fault)))
