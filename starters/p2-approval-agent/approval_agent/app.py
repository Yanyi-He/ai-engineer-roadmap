"""FastAPI service: ticket → proposal → human approval bound to a digest → idempotent execution with an audit trail."""
import uuid

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from .agent import AmbiguousOutcome, RulePlanner, digest, find_order_id, validate
from .store import Store

DEMO_ORDERS = [('ORD-1001', 'alice', 120.0, 'delivered'), ('ORD-1002', 'bob', 45.5, 'shipped'), ('ORD-1003', 'carol', 300.0, 'delivered')]


class TicketRequest(BaseModel):
    customer: str = Field(min_length=1, max_length=64)
    text: str = Field(min_length=5, max_length=2000)


class ApprovalRequest(BaseModel):
    approver: str = Field(min_length=1, max_length=64)
    digest: str = Field(min_length=64, max_length=64)


class RefundGateway:
    """Fake external payment system. `fail_after_commit` simulates a timeout that happens after the refund was made."""

    def __init__(self, store: Store):
        self.store, self.fail_after_commit = store, 0

    def issue_refund(self, idempotency_key: str, order_id: str, amount: float) -> dict:
        refund = self.store.create_refund(idempotency_key, order_id, amount)
        if self.fail_after_commit > 0:
            self.fail_after_commit -= 1
            raise AmbiguousOutcome('Timed out waiting for the payment provider.')
        return refund


def create_app(store: Store | None = None, planner=None) -> FastAPI:
    store = store or Store()
    store.seed_orders(DEMO_ORDERS)
    planner = planner or RulePlanner()
    gateway = RefundGateway(store)
    app = FastAPI(title='P2 approval agent')
    app.state.store, app.state.gateway = store, gateway

    @app.post('/tickets')
    def create_ticket(request: TicketRequest):
        task_id = uuid.uuid4().hex[:12]
        order_id = find_order_id(request.text)
        order = store.get_order(order_id) if order_id else None
        if order and order['customer'] != request.customer:
            order = None  # a customer can only act on their own orders
        proposal = planner.propose(request.text, order)
        try:
            validate(proposal, order)
        except ValueError as error:
            proposal = {'action': 'escalate', 'reason': str(error)}
        status = {'tool': 'awaiting_approval', 'ask_customer': 'needs_info'}.get(proposal['action'], 'answered')
        task = {'id': task_id, 'ticket': request.text, 'customer': request.customer, 'status': status, 'proposal': proposal,
                'digest': digest(proposal) if proposal['action'] == 'tool' else None, 'result': None}
        store.save_task(task)
        store.log(task_id, 'proposed', {'planner': planner.name, 'action': proposal['action']})
        return task

    @app.get('/tasks/{task_id}')
    def get_task(task_id: str):
        task = store.get_task(task_id)
        if not task:
            raise HTTPException(404, 'Task not found')
        return {**task, 'events': store.events(task_id)}

    @app.post('/tasks/{task_id}/approve')
    def approve(task_id: str, request: ApprovalRequest):
        task = store.get_task(task_id)
        if not task:
            raise HTTPException(404, 'Task not found')
        if task['status'] == 'done':
            return task  # repeated approval returns the recorded result
        if task['status'] not in ('awaiting_approval', 'unknown_outcome'):
            raise HTTPException(409, f"Task is {task['status']}")
        if request.digest != task['digest']:
            store.log(task_id, 'approval_rejected', {'approver': request.approver})
            raise HTTPException(409, 'Approval does not match the proposed action')
        store.log(task_id, 'approved', {'approver': request.approver})
        args = task['proposal']['args']
        try:
            # The task ID is the idempotency key: retries after a timeout reconcile instead of paying twice.
            result = gateway.issue_refund(task_id, args['order_id'], args['amount'])
        except AmbiguousOutcome as error:
            task['status'] = 'unknown_outcome'
            store.save_task(task)
            store.log(task_id, 'outcome_unknown', {'error': str(error)})
            raise HTTPException(503, 'Outcome unknown; retry the approval to reconcile') from error
        task.update(status='done', result=result)
        store.save_task(task)
        store.log(task_id, 'executed', {'refund': result['idempotency_key']})
        return task

    return app


app = create_app()
