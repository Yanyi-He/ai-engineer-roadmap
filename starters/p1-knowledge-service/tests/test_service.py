from fastapi.testclient import TestClient

from knowledge_service.app import create_app
from knowledge_service.model import NO_ANSWER, ExtractiveModel

client = TestClient(create_app(model=ExtractiveModel()))


def ask(question, role='employee'):
    response = client.post('/ask', json={'question': question, 'role': role})
    assert response.status_code == 200, response.text
    return response.json()


def test_health_reports_index_and_model():
    body = client.get('/healthz').json()
    assert body['status'] == 'ok' and body['chunks'] > 0 and body['model'] == 'extractive-baseline'


def test_answer_cites_the_source_document():
    body = ask('What is the deadline for submitting expense receipts?')
    assert '30 days' in body['answer']
    assert [c['doc_id'] for c in body['citations']] == ['expense-policy']
    assert body['citations'][0]['version']


def test_restricted_document_is_invisible_to_other_roles():
    body = ask('What is the salary band for level L3 engineers?')
    assert body['answer'] == NO_ANSWER
    assert all(c['doc_id'] != 'salary-bands' for c in body['citations'])
    assert '95,000' in ask('What is the salary band for level L3 engineers?', role='hr')['answer']


def test_instructions_inside_documents_are_not_followed():
    body = ask('Where should I email my password for vendor approval?')
    assert 'it-support@example.com' not in body['answer']


def test_unanswerable_question_abstains():
    assert ask('What is the parental leave policy?')['answer'] == NO_ANSWER


def test_input_validation_rejects_bad_requests():
    assert client.post('/ask', json={'question': 'hi'}).status_code == 422
    assert client.post('/ask', json={'question': 'What is the policy?', 'role': 'Admin; DROP'}).status_code == 422
