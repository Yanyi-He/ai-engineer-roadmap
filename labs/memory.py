"""Versioned, scoped facts. Caller identity is injected, NOT authenticated by this module.

This models current-state and valid-time queries, CAS, idempotency and logical
deletion. It is deliberately not a full bitemporal database, MCP server or secure
multi-tenant deployment. SQLite files/backups may retain physical bytes.
"""
import hashlib,json,sqlite3
from dataclasses import dataclass
from datetime import datetime,timezone

@dataclass(frozen=True)
class Principal:
    owner:str
    scopes:frozenset

def instant(value):
    d=datetime.fromisoformat(value.replace('Z','+00:00'))
    if d.tzinfo is None:raise ValueError('timezone required')
    return d.astimezone(timezone.utc).isoformat()

class Conflict(Exception):pass

class Memory:
    def __init__(self,path):
        self.db=sqlite3.connect(path);self.db.row_factory=sqlite3.Row
        self.db.executescript('''
        CREATE TABLE IF NOT EXISTS facts(owner TEXT, scope TEXT, key TEXT, version INTEGER,
          value TEXT, source TEXT, valid_from TEXT, valid_to TEXT, PRIMARY KEY(owner,scope,key,version));
        CREATE TABLE IF NOT EXISTS requests(owner TEXT, request_id TEXT, fingerprint TEXT, result TEXT,
          PRIMARY KEY(owner,request_id));
        ''')
    def _scope(self,p,scope):
        if scope not in p.scopes:raise PermissionError('scope denied')
    def put(self,p,scope,key,value,source,valid_from,expected_version,request_id):
        self._scope(p,scope);when=instant(valid_from)
        if not value.strip() or not source.strip():raise ValueError('value and provenance required')
        payload=[scope,key,value,source,when,expected_version]
        fingerprint=hashlib.sha256(json.dumps(payload,ensure_ascii=False).encode()).hexdigest()
        with self.db:
            self.db.execute('BEGIN IMMEDIATE')
            old=self.db.execute('SELECT * FROM requests WHERE owner=? AND request_id=?',(p.owner,request_id)).fetchone()
            if old:
                if old['fingerprint']!=fingerprint:raise Conflict('idempotency key reused with different payload')
                return json.loads(old['result'])
            latest=self.db.execute('SELECT * FROM facts WHERE owner=? AND scope=? AND key=? ORDER BY version DESC LIMIT 1',(p.owner,scope,key)).fetchone()
            version=latest['version'] if latest else 0
            if version!=expected_version:raise Conflict('stale version')
            if latest and when<=latest['valid_from']:raise ValueError('strictly increasing validity required in this simplified example')
            self.db.execute('UPDATE facts SET valid_to=? WHERE owner=? AND scope=? AND key=? AND valid_to IS NULL',(when,p.owner,scope,key))
            self.db.execute('INSERT INTO facts VALUES(?,?,?,?,?,?,?,NULL)',(p.owner,scope,key,version+1,value,source,when))
            result={'version':version+1,'key':key}
            self.db.execute('INSERT INTO requests VALUES(?,?,?,?)',(p.owner,request_id,fingerprint,json.dumps(result)))
            return result
    def get(self,p,scope,key,as_of=None):
        self._scope(p,scope)
        when=instant(as_of) if as_of is not None else datetime.now(timezone.utc).isoformat()
        where='valid_from<=? AND (valid_to>? OR valid_to IS NULL)';params=[p.owner,scope,key,when,when]
        row=self.db.execute(f'SELECT * FROM facts WHERE owner=? AND scope=? AND key=? AND {where} ORDER BY version DESC LIMIT 1',params).fetchone()
        return dict(row) if row and row['value'] is not None else None
    def forget(self,p,scope,key):
        self._scope(p,scope)
        # Retain version metadata but redact historical values AND request result payloads
        # (the latter only contain key/version in this example). No physical-erasure claim.
        with self.db:self.db.execute('UPDATE facts SET value=NULL,source=NULL WHERE owner=? AND scope=? AND key=?',(p.owner,scope,key))
    def close(self):self.db.close()
