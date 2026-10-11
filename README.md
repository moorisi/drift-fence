# DriftFence

DriftFence records consensus compatibility reviews of two API schemas. The leader fetches complete commit-pinned JSON documents, verifies SHA-256, and proposes breaking/non-breaking changes, a status, and JSON-pointer citations. Validators independently re-fetch both documents and evaluate the completeness of both change lists, the exact status, and the relevance of every citation. They judge meaning; they do not compare generated prose byte for byte.

Descriptions matter: removing a documented ordering guarantee can break clients even when paths, methods and response shapes remain identical. The [live description-only scenario](proofs/v2-description.json) demonstrates this consequential AI decision.

StudioNet contract: `0xf566F45Fcb44C6e44ba149003bA77ACee9b0f3D6` (chain 61999, gasless simulation network).

- [Contract source](contracts/drift_fence.py)
- [Four finalized onchain scenarios and the failed original attempt](proofs/README.md)
- [Consensus and state design](docs/CONSENSUS.md)
- [Ready-to-submit description](docs/submission.md)

## Validate

Use Python 3.13 and Node.js 20 or later:

```sh
python -m pip install -r requirements-dev.txt
python -m pytest tests/direct -q
genvm-lint check contracts/drift_fence.py --json
node scripts/verify-proofs.cjs
```

For the live verifier, install `genlayer` CLI, select `genlayer network set studionet`, and set `GENLAYER_CLI_PATH` to its installed `genlayer/dist/index.js` file. Verification sends read-only RPC/CLI requests and does not sign transactions. Direct tests require no network once dependencies and the pinned SDK are cached.

The 28 direct tests use mocked web/LLM responses and explicitly invoke the validator callback. They test application behavior and rejection paths, not real distributed consensus. The four published write receipts supply live StudioNet evidence. The verifier checks deployed source bytes, successful finalized execution, strict majority votes, exact input commitments, evidence locations, and append counts.

## Interface and limits

Deploy with repository `moorisi/drift-fence`. Anyone can call `compare(old_url, old_hash, new_url, new_hash)` and read `get_reports()`. URLs must be raw GitHub URLs pinned to a full 40-character commit in that fixed repository's `schemas/` directory. A successful comparison consumes both content hashes globally in this instance; another comparison cannot reuse either hash. There are at most 16 reports, 18,000 bytes per document, 32 changes per category and 16 citations per side.

`REVIEW` is a successful analysis result for unsupported or ambiguous schema semantics. Transport failures, hash mismatches, invalid JSON, duplicate keys and malformed model output revert. Consensus disagreement also prevents appending a report.

This is a bounded AI review primitive, not a complete OpenAPI conformance checker or proof of runtime behavior. The fixtures are synthetic schema fragments. Model omissions, malicious prose and common model errors remain possible; consensus does not turn schema claims into implementation guarantees. It holds no funds and does not execute upgrades.
