"""FastAPI service: permission-aware retrieval, cited answers and one structured log line per request."""
import json
import logging
import re
import time
import uuid
from pathlib import Path

from fastapi import FastAPI
from pydantic import BaseModel, Field

from .documents import load_chunks
from .model import model_from_env
from .retrieval import BM25Index

DOCS = Path(__file__).resolve().parent.parent / 'data' / 'docs'
log = logging.getLogger('knowledge_service')
if not log.handlers:  # print the JSON line as-is; replace with your tracing exporter (OpenTelemetry, Langfuse) at L2
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter('%(message)s'))
    log.addHandler(_handler)
    log.setLevel(logging.INFO)


class AskRequest(BaseModel):
    question: str = Field(min_length=3, max_length=500)
    role: str = Field(default='employee', pattern=r'^[a-z_]{1,32}$')


class Citation(BaseModel):
    n: int
    doc_id: str
    chunk_id: str
    title: str
    version: str


class AskResponse(BaseModel):
    request_id: str
    answer: str
    citations: list[Citation]
    model: str
    latency_ms: float


def create_app(docs_dir: Path = DOCS, model=None) -> FastAPI:
    index = BM25Index(load_chunks(docs_dir))
    llm = model or model_from_env()
    app = FastAPI(title='P1 knowledge service')

    @app.get('/healthz')
    def healthz():
        return {'status': 'ok', 'chunks': len(index.chunks), 'model': llm.name}

    @app.post('/ask', response_model=AskResponse)
    def ask(request: AskRequest) -> AskResponse:
        start, request_id = time.perf_counter(), uuid.uuid4().hex[:12]
        hits = index.search(request.question, request.role, k=3)
        answer = llm.answer(request.question, hits)
        cited = sorted({int(n) for n in re.findall(r'\[(\d+)\]', answer) if 0 < int(n) <= len(hits)})
        citations = [Citation(n=n, doc_id=hits[n - 1][1].doc_id, chunk_id=hits[n - 1][1].chunk_id,
                              title=hits[n - 1][1].title, version=hits[n - 1][1].version) for n in cited]
        latency = round(1000 * (time.perf_counter() - start), 2)
        # A trace-like log line: what was retrieved, what was cited, how long it took. Never log the full answer text.
        log.info(json.dumps({'request_id': request_id, 'role': request.role, 'retrieved': [c.chunk_id for _, c in hits],
                             'cited': [c.chunk_id for c in citations], 'model': llm.name, 'latency_ms': latency}))
        return AskResponse(request_id=request_id, answer=answer, citations=citations, model=llm.name, latency_ms=latency)

    return app


app = create_app()
