# P12 Step 4 Cross-Agent Integration Design

## Scope and authority

Continue the verified v0.5.0 baseline. Reuse Step 1/2/3 evidence where Host
versions and definitions have not changed. The owner has authorized autonomous
implementation, isolated synthetic writes, ordinary configuration, testing,
privacy audits and release only after all final Gates pass.

Agent thinks; Gateway executes. Every V2 read and write, including isolated
existence checks, goes through the Gateway. Do not open store files. Cross-Agent
shared data does not mean shared conversation context. Identity remains
caller-reported / unverified, never authentication.

## Design

Three fresh real Host sessions point to one isolated Gateway configuration and
one store. Distinct persistent server names avoid production precedence issues.
Hermes creates a synthetic document, immutable Wrong Answer source and v1.
WorkBuddy receives only a marker and natural-language revision request, discovers
v1 and appends v2. A new Codex process discovers and reads the complete graph.
No source IDs, DTOs or prior session outputs enter the B/C prompts.

Use the existing canonical workflow and formal Gateway tools. Host traces stay
outside Git. Exact DTO comparisons verify preservation of documents, sources,
versions, timestamps, provenance and logical references across process exits.
The same update request/key must return v2; a new key with stale version 1 must
reach the Gateway and return CONFLICT. Only versions 1 and 2 may exist.

The existing scoped collector, renderer and manifest-owned writer generate an
isolated Vault twice. Compare every Markdown byte and manifest byte, and check
relations, reported provenance, supersession, absence of duplicates, raw bytes
and private paths. Do not reopen the Step 1 GUI appearance Gate.

## Alternatives considered

Separate stores cannot demonstrate sharing. SDK-only clients can corroborate
contract behavior but cannot replace real Host Agent routing. A new business
adapter would add an unnecessary second authority. Reuse the formal stdio
contract with independent Host lifetimes instead.

## Acceptance and release

Track all 25 owner-specified Gates separately with Real Host evidence,
Gateway/SDK corroboration and automated regression. Missing real Host evidence
is WAITING, never PASS. Keep 0.5.0 until final acceptance. After all Gates pass,
run targeted/full regression, build and audit wheel/sdist and Git object delta,
then normal main/tag push, GitHub Release and fresh-clone clean-install/stdio
verification. Never force push or publish private configs/traces/test stores.

GUI/trust/account blockers require one minimal owner action after all independent
preparation is complete. Do not use the owner to relay record data.
