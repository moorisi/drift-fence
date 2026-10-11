Category: **Builder → Intelligent Contracts**

Title: **DriftFence: Consensus API-schema compatibility gate**

Notes / Description:

> DriftFence compares two commit-pinned API schema documents. Leader and validators independently fetch complete UTF-8 sources, verify SHA-256, and normalize endpoint paths, methods, parameters, required fields, enums and response keys. Validators independently reclassify every consequential change and compare exact breaking/non-breaking arrays, status and source-anchored quotes. Missing or ambiguous schema facts fail closed to REVIEW; invented changes and unanchored evidence are rejected. The append-only report preserves both source commitments for audit. This is a schema compatibility primitive, not legal advice or proof of runtime implementation behavior.
