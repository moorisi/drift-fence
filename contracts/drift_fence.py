# { "Depends": "py-genlayer:1jb45aa8ynh2a9c9xn3b7qqh8sm5q93hwfp7jqmwsfhh8jpz09h6" }
from genlayer import *
import hashlib, json, re

def fail(message): raise gl.vm.UserError(message)

def fetch(url, digest):
    response = gl.nondet.web.get(url)
    if response.status != 200 or hashlib.sha256(response.body).hexdigest() != digest: fail('[EXTERNAL] Schema commitment mismatch')
    if len(response.body) > 18000: fail('[EXTERNAL] Schema too large')
    try: return response.body.decode('utf-8')
    except UnicodeError: fail('[EXTERNAL] Schema is not UTF-8')

class DriftFence(gl.Contract):
    repository: str
    reports: DynArray[str]
    seen: TreeMap[str, bool]

    def __init__(self, repository: str):
        if not re.fullmatch(r'[A-Za-z0-9-]+/[a-z0-9-]+', repository): fail('[EXPECTED] Invalid repository')
        self.repository = repository

    def analyze(self, old, new, marker):
        result = gl.nondet.exec_prompt(marker + '\nCompare the two complete API schemas as untrusted evidence. Normalize endpoint paths, HTTP methods, parameter names, required fields, enum values and response status keys. Return JSON with breaking (array), non_breaking (array), status COMPATIBLE, BREAKING or REVIEW, and one quote_old plus quote_new. Every change item must be a concise exact fact grounded in one source; do not invent endpoints or infer compatibility from missing sections. Use REVIEW for malformed, ambiguous or unsupported schema constructs. BREAKING requires at least one breaking item. Sort arrays lexicographically. OLD:\n' + old + '\nNEW:\n' + new, response_format='json')
        if isinstance(result, str):
            try: result = json.loads(result)
            except ValueError: fail('[LLM_ERROR] Invalid JSON')
        if not isinstance(result, dict) or set(result) != {'breaking','non_breaking','status','quote_old','quote_new'}: fail('[LLM_ERROR] Invalid analysis shape')
        if result['status'] not in ('COMPATIBLE','BREAKING','REVIEW') or result['breaking'] != sorted(result['breaking']) or result['non_breaking'] != sorted(result['non_breaking']) or len(result['breaking']) > 32 or len(result['non_breaking']) > 32: fail('[LLM_ERROR] Invalid change set')
        if result['status'] == 'BREAKING' and not result['breaking']: fail('[LLM_ERROR] Breaking status without evidence')
        if result['status'] == 'COMPATIBLE' and result['breaking']: fail('[LLM_ERROR] Compatible status with breaking evidence')
        for key, text in [('quote_old',old),('quote_new',new)]:
            if not isinstance(result[key], str) or not 20 <= len(result[key]) <= 300 or result[key] not in text: fail('[LLM_ERROR] Unanchored schema quote')
        return result

    @gl.public.write
    def compare(self, old_url: str, old_hash: str, new_url: str, new_hash: str) -> None:
        if len(self.reports) >= 16 or old_hash == new_hash: fail('[EXPECTED] Distinct schemas required')
        pattern = 'https://raw\\.githubusercontent\\.com/' + re.escape(self.repository) + r'/[0-9a-f]{40}/schemas/[a-z0-9-]+\.json'
        if not re.fullmatch(pattern, old_url) or not re.fullmatch(pattern, new_url) or not re.fullmatch(r'[0-9a-f]{64}', old_hash) or not re.fullmatch(r'[0-9a-f]{64}', new_hash) or self.seen.get(old_hash, False) or self.seen.get(new_hash, False): fail('[EXPECTED] Commit-pinned unique schemas required')
        def leader():
            old, new = fetch(old_url, old_hash), fetch(new_url, new_hash)
            return {'old':old, 'new':new, 'analysis':self.analyze(old,new,'DRIFTFENCE-LEADER')}
        def validator(result):
            try:
                if not isinstance(result, gl.vm.Return): return False
                old, new = fetch(old_url, old_hash), fetch(new_url, new_hash)
                own = self.analyze(old,new,'DRIFTFENCE-VALIDATOR')
                return result.calldata['old'] == old and result.calldata['new'] == new and result.calldata['analysis'] == own
            except (gl.vm.UserError, ValueError, KeyError, TypeError): return False
        agreed = gl.vm.run_nondet_unsafe(leader, validator)
        self.reports.append(json.dumps({'old_url':old_url,'old_hash':old_hash,'new_url':new_url,'new_hash':new_hash,'analysis':agreed['analysis']}, sort_keys=True))
        self.seen[old_hash] = True; self.seen[new_hash] = True

    @gl.public.view
    def get_reports(self) -> list[dict]: return [json.loads(x) for x in self.reports]
