"""Optional SDK integration tests; no model key, endpoint or embeddings required."""
import asyncio
import inspect
import math
import pytest
from labs.evaluation.regression import HERE,load,score_run,compare
from labs.evaluation.ragas_eval import id_metrics,numeric


def test_real_ragas_id_metrics_match_declared_id_definition():
    dataset,run=load(HERE/'dataset.json'),load(HERE/'baseline.json')
    real=asyncio.run(id_metrics(dataset,run))
    reference=score_run(dataset,run)
    for actual,expected in zip(real['cases'],reference['cases']):
        assert actual['case_id']==expected['case_id']
        assert actual['scores']==expected['scores']


@pytest.mark.parametrize('value',[math.nan,math.inf,-0.1,1.1])
def test_unavailable_or_invalid_metric_is_an_error(value):
    with pytest.raises(ValueError):numeric(value)


def test_modern_ragas_semantic_metric_signatures():
    from ragas.metrics.collections import Faithfulness,ContextPrecision,ContextRecall,FactualCorrectness
    for metric,required in [(Faithfulness,{'response','retrieved_contexts'}),
                            (ContextPrecision,{'reference','retrieved_contexts'}),
                            (ContextRecall,{'reference','retrieved_contexts'}),
                            (FactualCorrectness,{'response','reference'})]:
        assert required<=set(inspect.signature(metric.ascore).parameters)


@pytest.fixture(scope="module")
def frozen_inputs():
    return load(HERE/'dataset.json'),load(HERE/'baseline.json'),load(HERE/'policy.json')


@pytest.mark.parametrize('filename,expected', [('baseline.json',True),('candidate-broken.json',False)])
def test_release_decision_with_pytest_fixture(frozen_inputs,filename,expected):
    dataset,baseline,policy=frozen_inputs
    assert compare(dataset,baseline,load(HERE/filename),policy)['passed'] is expected


def test_judge_adapter_constructs_without_requests():
    from openai import AsyncOpenAI
    from ragas.llms import llm_factory
    from ragas.metrics.collections import Faithfulness,ContextPrecision,ContextRecall,FactualCorrectness
    async def check():
        async with AsyncOpenAI(api_key="sdk-interface-check",timeout=30,max_retries=0) as client:
            judge=llm_factory("model-placeholder",client=client,max_retries=1)
            metrics=[cls(llm=judge) for cls in [Faithfulness,ContextPrecision,ContextRecall,FactualCorrectness]]
            assert len(metrics)==4
    asyncio.run(check())
