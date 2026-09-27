# Phase 7 checkpoint: Wrong Answer pipeline

Wrong-answer source rows reference an existing, hash-verified `asset://` or `document://` URI and are immutable. For documents, a page reference is checked against the deterministic document registry; the source retains whether text came from supplied OCR-derived text, supplied extraction, or source text. Asset-only sources do not claim OCR text. Stable source IDs include the logical source/page and submitted question/answer, so distinct problems on one page remain separate records.

Analysis rows are separate, append-only versions supplied by the Agent/client. They store `generated_by_agent`, Gateway UTC creation time, source refs, `study:` relations, and shared write provenance. Each version exposes an explicit predecessor analysis ID and provenance ID. Optional Agent/client/session values are caller-reported and unverified. The Gateway validates strict fields, existing source/asset/document refs, and existing Study files under the explicit Study root. It does not infer error type, knowledge points, solution, or advice. Idempotency keys bind to the normalized request and reported identity; exact retries replay the original saved result before checking mutable external Study/asset availability. Optimistic `expected_version` prevents lost updates.

The private SQLite database is the already configured Asset/Document database. With no document store configured, operations fail closed. The MCP contract adds source registration and analysis save/update write tools, plus bounded bundle/search read tools. Study relations use this repository's existing `study:<relative-path>` identifier form. Text returned from source and analysis fields passes through local-path redaction.

All coverage uses invented data and fake Agent analysis over the in-process MCP protocol client. No model API is called and no real private history or StudyVault is written. Phase 8 still needs to add enforceable capabilities, comprehensive audit metadata, and hardened write/path behavior before these local write operations are treated as production-hardened.

## Verification and checkpoint

- Phase 7 full regression: `217 passed, 3 skipped`.
- The skipped cases were the host's symlink restriction and the two explicitly opt-in real-QMD smoke tests.
- Coherent local implementation/fix commits: `31f86d9` and `f1e7735`.
- Phase 8 subsequently added capability enforcement, metadata audit, and local path checks; those are tracked in `phase-8-checkpoint.md`.
