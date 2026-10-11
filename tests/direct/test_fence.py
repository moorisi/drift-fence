import copy
import hashlib
import json
import re
from pathlib import Path
import pytest

ROOT = Path(__file__).resolve().parents[2]
REPO = 'moorisi/drift-fence'
OLD = (ROOT / 'schemas/old.json').read_bytes()

@pytest.fixture
def fence(direct_deploy):
    return direct_deploy(str(ROOT / 'contracts/drift_fence.py'), REPO)

def setup(vm, name='compatible', override=None, own=None, corrupt=False):
    vm.clear_mocks()
    new = (ROOT / 'schemas' / (name+'.json')).read_bytes()
    urls = [f'https://raw.githubusercontent.com/{REPO}/' + 'a'*40 + '/schemas/' + n+'.json' for n in ['old',name]]
    for url, body in zip(urls, [OLD,new]): vm.mock_web(re.escape(url), {'status':200, 'body': body + (b' ' if corrupt else b'')})
    analysis = {'status': {'compatible':'COMPATIBLE','breaking':'BREAKING','malformed':'REVIEW'}[name], 'breaking': ['GET /items removed'] if name == 'breaking' else [], 'non_breaking': ['404 response added'] if name == 'compatible' else [], 'evidence_old': ['/paths/~1items/get'], 'evidence_new':['/paths/~1items']}
    if override: analysis.update(override)
    vm.mock_llm(r'.*DRIFTFENCE-LEADER.*', json.dumps(analysis))
    vm.mock_llm(r'.*DRIFTFENCE-VALIDATOR.*', json.dumps(own or {key:True for key in ['breaking_complete','non_breaking_complete','status_correct','evidence_supports']}))
    return [urls[0], hashlib.sha256(OLD).hexdigest(), urls[1], hashlib.sha256(new).hexdigest()], analysis

@pytest.mark.parametrize('name,status',[('compatible','COMPATIBLE'),('breaking','BREAKING'),('malformed','REVIEW')])
def test_outcomes_and_validator(fence, direct_vm, name, status):
    args, _ = setup(direct_vm, name)
    fence.compare(*args)
    assert fence.get_reports()[0]['analysis']['status'] == status
    assert direct_vm.run_validator() is True

def test_replay_cannot_append(fence, direct_vm):
    args, _ = setup(direct_vm)
    fence.compare(*args)
    with direct_vm.expect_revert('unique schemas'): fence.compare(*args)
    assert len(fence.get_reports()) == 1

@pytest.mark.parametrize('field', ['breaking_complete','non_breaking_complete','status_correct','evidence_supports'])
def test_validator_checks_every_consequential_criterion(fence, direct_vm, field):
    args, analysis = setup(direct_vm)
    fence.compare(*args)
    own = {key:True for key in ['breaking_complete','non_breaking_complete','status_correct','evidence_supports']}; own[field] = False
    setup(direct_vm, own=own)
    assert direct_vm.run_validator() is False

def test_validator_refetches(fence, direct_vm):
    args, _ = setup(direct_vm); fence.compare(*args)
    setup(direct_vm, corrupt=True)
    assert direct_vm.run_validator() is False

@pytest.mark.parametrize('override', [{'evidence_new':['/invented']}, {'evidence_new':['/paths/~2items']}, {'evidence_new':[]}, {'status':'BREAKING','breaking':[]}, {'status':'COMPATIBLE','breaking':['removed']}, {'status':'YES'}, {'breaking':['z','a']}, {'non_breaking':['x']*33}, {'breaking':[1]}, {'breaking':'removed'}, {'breaking':['x','x']}, {'breaking':['x'],'non_breaking':['x']}])
def test_bad_analysis_cannot_append(fence, direct_vm, override):
    args, _ = setup(direct_vm, override=override)
    with direct_vm.expect_revert(): fence.compare(*args)
    assert fence.get_reports() == []

@pytest.mark.parametrize('verdict', [{'breaking_complete':True}, {key:'true' for key in ['breaking_complete','non_breaking_complete','status_correct','evidence_supports']}, {key:1 for key in ['breaking_complete','non_breaking_complete','status_correct','evidence_supports']}])
def test_validator_rejects_malformed_or_non_boolean_verdict(fence,direct_vm,verdict):
    args, _ = setup(direct_vm); fence.compare(*args)
    setup(direct_vm, own=verdict)
    assert direct_vm.run_validator() is False

def test_bad_commitment_cannot_append(fence, direct_vm):
    args, _ = setup(direct_vm, corrupt=True)
    with direct_vm.expect_revert('commitment mismatch'): fence.compare(*args)
    assert fence.get_reports() == []

@pytest.mark.parametrize('kind',['main','foreign','same-hash'])
def test_input_scope(fence, direct_vm, kind):
    args, _ = setup(direct_vm)
    if kind == 'main': args[0] = args[0].replace('a'*40,'main')
    if kind == 'foreign': args[0] = args[0].replace(REPO,'other/drift-fence')
    if kind == 'same-hash': args[3] = args[1]
    with direct_vm.expect_revert(): fence.compare(*args)
    assert fence.get_reports() == []
