# P13 remaining source reconciliation

Owner authorizes autonomous execution from the existing Gemini checkpoint. No prior
inventory, Gemini, MCP or P12 gate is repeated. ChatGPT remains acquisition_pending.
Normalization design/execution waits until all acquired inputs have an explained disposition.

## Evidence storage

Add an immutable source-file index and exact-byte payload table to the existing configured
History SQLite database. This is the V2 source evidence layer, not another Memory or DB
engine. Source identity is SHA-256(source system + NUL + original byte digest); paths,
filenames and import clocks do not participate. Identical bytes share payload storage.

Already preserved legacy records are referenced without copying their payload. A verified
existing Gemini manifest is indexed as the same evidence bundle, without reimporting or
rerunning Gemini migration. Original refs and provenance remain intact. Registration is
distinct from creating another logical source. Exact-byte aliases keep acquisition locators
in the private ledger. Different packaging/metadata only yields explicit duplicate candidates.

Each source record declares source system, format, record kind, digest, byte count, evidence
refs and importer provenance. Occurrence time is nullable. Runtime metadata is explicitly
distinct from conversation evidence. Source bytes are immutable; raw malformed/unsupported
inputs are preserved. Source registration never manufactures messages or message roles.

## Gateway-only execution

Expose ingestion, bounded raw readback, metadata search/counts and reconciliation as formal
MCP/Gateway operations. Ingestion requires the existing ingest capability and an explicitly
configured private migration inbox. Requests name a relative immutable manifest plus its
digest, cursor and bounded batch size; arbitrary absolute file inputs are rejected. Every
input path, byte digest and file stability check is validated before persistence. Never use
a direct production SQLite client or inline MCP configuration override.

New tool discovery uses a fresh actual Codex Host in this trusted worktree with its existing
study_system configuration. A CLI/SDK success code alone is insufficient: persist actual
MCP tool traces and returned Gateway receipts. Existing initiating-Host tools remain valid.

## Private source recovery and V1 discovery

Continue the existing ledger. Freeze the recorded file versions into a Git-external inbox;
for append-only files recover a recorded prefix only when byte length and digest prove it.
If a mutable runtime record was replaced, retain the failure and distinguish known metadata
supersession from missing unique conversation evidence. No silent loss or guessed replacement.

Locate V1 through P11 journals, original config references, cold DB archive descriptors,
known legacy project/config roots and explicit provenance mappings. Do not scan unrelated
directories or credential stores. The P11 cold native-memory DB has been located; source
schema/object audit is offline input work, never an authoritative V2 read.

## Gate

Account separately for input versions, source files, packages, persisted evidence refs,
duplicates/candidates, malformed/unsupported, runtime-only records and pending/deferred.
Compare every acquired input with an actual Gateway identity/receipt or an explicit retained
disposition. Repeat ingestion and verify stable identity/provenance and zero new logical sources.
After source-only completion, proceed automatically to deterministic normalization design.
V1 retirement remains behind normalization reconciliation and full V2 recovery gates.
