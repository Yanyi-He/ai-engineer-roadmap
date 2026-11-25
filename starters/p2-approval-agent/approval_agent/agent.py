"""Planner and executor.

The planner only proposes. Reads run immediately; writes need a human approval bound to a digest of the exact action.
RulePlanner is the offline baseline; replace it with an LLM planner that returns the same JSON shape, and keep the
validation, approval and idempotency below unchanged.
"""
import hashlib
import json
import re

ORDER_ID = re.compile(r'\bORD-\d{4,}\b')
REFUND_INTENT = re.compile(r'\b(refund|money back|charged twice|return)\b', re.I)
WRITE_TOOLS = {'issue_refund'}


class AmbiguousOutcome(Exception):
    """The external call may have committed before the timeout; the next attempt must reconcile, not repeat."""


class RulePlanner:
    name = 'rule-baseline'

    def propose(self, ticket: str, order: dict | None) -> dict:
        if order is None:
            return {'action': 'ask_customer', 'reason': 'No valid order ID found in the ticket.'}
        if not REFUND_INTENT.search(ticket):
            return {'action': 'reply', 'reason': 'No refund request detected.'}
        if order['status'] != 'delivered':
            return {'action': 'reply', 'reason': f"Order is {order['status']}; refunds apply to delivered orders."}
        # Amounts come from the order system, never from ticket text, so injected numbers cannot raise a refund.
        return {'action': 'tool', 'tool': 'issue_refund', 'args': {'order_id': order['id'], 'amount': order['amount']},
                'reason': 'Customer requests a refund for a delivered order.'}


def digest(proposal: dict) -> str:
    canonical = json.dumps({'tool': proposal.get('tool'), 'args': proposal.get('args')}, sort_keys=True, separators=(',', ':'))
    return hashlib.sha256(canonical.encode()).hexdigest()


def validate(proposal: dict, order: dict | None) -> None:
    if proposal.get('action') != 'tool':
        return
    if proposal.get('tool') not in WRITE_TOOLS:
        raise ValueError(f"Unknown tool: {proposal.get('tool')}")
    args = proposal.get('args') or {}
    if order is None or args.get('order_id') != order['id'] or not 0 < float(args.get('amount', 0)) <= order['amount']:
        raise ValueError('Proposal does not match the order record.')


def find_order_id(ticket: str) -> str | None:
    match = ORDER_ID.search(ticket)
    return match.group(0) if match else None
