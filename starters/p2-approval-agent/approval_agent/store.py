"""SQLite storage for tasks, an audit trail and a fake order system with idempotent refunds."""
import json
import sqlite3
import threading
import time

SCHEMA = """
CREATE TABLE IF NOT EXISTS orders (id TEXT PRIMARY KEY, customer TEXT, amount REAL, status TEXT);
CREATE TABLE IF NOT EXISTS refunds (idempotency_key TEXT PRIMARY KEY, order_id TEXT, amount REAL, created_at REAL);
CREATE TABLE IF NOT EXISTS tasks (id TEXT PRIMARY KEY, ticket TEXT, customer TEXT, status TEXT, proposal TEXT, digest TEXT, result TEXT);
CREATE TABLE IF NOT EXISTS events (task_id TEXT, at REAL, event TEXT, detail TEXT);
"""


class Store:
    def __init__(self, path: str = ':memory:'):
        self.db = sqlite3.connect(path, check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.lock = threading.Lock()
        with self.lock:
            self.db.executescript(SCHEMA)

    def seed_orders(self, orders):
        with self.lock, self.db:
            self.db.executemany('INSERT OR REPLACE INTO orders VALUES (?, ?, ?, ?)', orders)

    def get_order(self, order_id):
        row = self.db.execute('SELECT * FROM orders WHERE id = ?', (order_id,)).fetchone()
        return dict(row) if row else None

    def refunds_for(self, order_id):
        return [dict(r) for r in self.db.execute('SELECT * FROM refunds WHERE order_id = ?', (order_id,))]

    def create_refund(self, idempotency_key, order_id, amount):
        """Insert once per key; a repeated key returns the existing refund instead of paying twice."""
        with self.lock, self.db:
            self.db.execute('INSERT OR IGNORE INTO refunds VALUES (?, ?, ?, ?)', (idempotency_key, order_id, amount, time.time()))
        return dict(self.db.execute('SELECT * FROM refunds WHERE idempotency_key = ?', (idempotency_key,)).fetchone())

    def save_task(self, task):
        with self.lock, self.db:
            self.db.execute('INSERT OR REPLACE INTO tasks VALUES (?, ?, ?, ?, ?, ?, ?)',
                            (task['id'], task['ticket'], task['customer'], task['status'], json.dumps(task.get('proposal')),
                             task.get('digest'), json.dumps(task.get('result'))))

    def get_task(self, task_id):
        row = self.db.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        if not row:
            return None
        task = dict(row)
        task['proposal'], task['result'] = json.loads(task['proposal']), json.loads(task['result'])
        return task

    def log(self, task_id, event, detail=None):
        with self.lock, self.db:
            self.db.execute('INSERT INTO events VALUES (?, ?, ?, ?)', (task_id, time.time(), event, json.dumps(detail)))

    def events(self, task_id):
        return [r['event'] for r in self.db.execute('SELECT event FROM events WHERE task_id = ? ORDER BY rowid', (task_id,))]
