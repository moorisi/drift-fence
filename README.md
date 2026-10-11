# DriftFence

DriftFence is a GenLayer API-schema compatibility gate. It independently fetches two commit-pinned schema documents, verifies their full bytes and hashes, and asks leader and validators to normalize endpoint/method/parameter/required-field/enum changes. Exact agreement on breaking evidence yields `BREAKING`, no breaking evidence yields `COMPATIBLE`, and ambiguity yields `REVIEW`. Reports retain both commitments and source-anchored quotes. This is compatibility analysis, not a guarantee of implementation behavior.
