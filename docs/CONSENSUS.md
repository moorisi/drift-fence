# Consensus and state

The constructor fixes one source repository. There is no owner workflow, mutable graph, certificate, settlement or confidence threshold. A report is an append-only comparison of two immutable document commitments; successful source hashes cannot be consumed again.

1. Deterministic checks enforce the URL namespace, full commit identifiers, 64-digit hashes, distinct inputs, replay protection and storage limits.
2. The leader acquires both complete sources inside `run_nondet_unsafe`, checks HTTP status and hashes, decodes UTF-8 and rejects duplicate JSON keys or non-object documents.
3. The leader's AI proposes two bounded sorted change lists, an exact status, and existing RFC6901 pointers into both documents. Pointer existence, type bounds, list uniqueness and basic status/list consistency are deterministic checks.
4. Each validator acquires both complete sources again and compares their bytes with the candidate's sources. A separate validator prompt evaluates all and only real breaking changes, all and only real non-breaking changes, the exact status including ambiguity, and whether citations cover the material decisions. Every verdict field must be the JSON boolean `true`; missing keys, numeric/string substitutes, invented changes, omitted changes or an incorrect status reject.
5. Only an accepted nondeterministic result appends the report and consumes both hashes. Reports retain input URLs/hashes, change lists, status and pointers. Complete source texts are available through immutable URLs and in the transaction's leader equivalence output; they are not duplicated in report storage.

The validator does not share the leader's inference output as its answer. It evaluates the candidate against independently fetched full documents. Prose differences are allowed because prose equality is not the safety target. The AI judgment can affect stored compatibility even with identical structural API fields, as the ordering-guarantee proof demonstrates.

## Status rules

`COMPATIBLE`: no breaking change is found in supported schema semantics. `BREAKING`: at least one grounded breaking change is identified. `REVIEW`: unsupported constructs, unresolved references, empty response sets or ambiguous guarantees prevent an unqualified decision. Structural input failures revert instead of becoming REVIEW. These rules are model judgments independently reviewed by validators, not formal proofs of API substitutability.

## Historical failure

The original deployment required literal source quotes and exact generated-prose equality. Its first compatibility write reverted with `Unanchored schema quote` and finalized `MAJORITY_DISAGREE`. The correction replaces that fragile quote surface with pointers and independent completeness judgments. The failed receipt remains public; the four successful scenarios belong to the new deployment and source version.
