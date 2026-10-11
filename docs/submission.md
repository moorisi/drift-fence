Category: **Builder → Intelligent Contracts**

Title: **DriftFence: Consensus API-schema compatibility gate**

Notes / Description:

> DriftFence is a GenLayer API compatibility review primitive. The leader fetches two commit-pinned JSON schemas, verifies SHA-256, and proposes breaking/non-breaking changes with JSON-pointer citations. Validators independently re-fetch full sources and audit both lists for omissions and inventions, the exact COMPATIBLE/BREAKING/REVIEW decision, and citation relevance. Only accepted analysis appends a report and consumes both hashes. Four finalized MAJORITY_AGREE StudioNet proofs cover an added response, a removed operation, an empty response set, and removal of a prose ordering guarantee with unchanged API structure. Receipts match stored reports and deployed source bytes. The repository includes 28 direct tests and preserves the failed original quote-based attempt. Fixtures are synthetic; this is bounded compatibility analysis, not OpenAPI conformance or proof of runtime behavior.

Contract source: https://github.com/moorisi/drift-fence/blob/main/contracts/drift_fence.py

StudioNet contract: `0xf566F45Fcb44C6e44ba149003bA77ACee9b0f3D6`

Proofs: https://github.com/moorisi/drift-fence/blob/main/proofs/README.md
