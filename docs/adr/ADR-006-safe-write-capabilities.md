# ADR-006: Explicit Safe Write Capabilities

状态：Accepted

日期：2026-09-26

## Context

History, document, asset, and wrong-answer data are private and some MCP tools persist caller-provided bytes or Agent-authored analysis. A single implicit tool permission would make read-only use harder to guarantee and audit.

## Decision

Gateway permissions are explicit capabilities: `read`, `ingest`, `write`, and `admin`. Missing configuration fails closed to `read`. `ingest` is required for asset/document ingestion; `write` is required for wrong-answer source and analysis persistence; `admin` explicitly grants all capabilities. The MCP server advertises only operations enabled by the configured capabilities, and Gateway methods independently enforce authorization.

All configured local roots and databases are explicit paths. Storage adapters reject symlink and Windows reparse-point components before database or blob access. Persistent mutations append audit metadata (operation, resource type, logical ID, UTC timestamp, outcome) in the same SQLite transaction. Audit rows contain no source text or absolute paths.

## Consequences

- Existing configurations remain read-only unless local configuration opts in.
- An audit row cannot claim a transaction succeeded if the corresponding write rolls back.
- Path checks reduce link-based escapes; like ordinary path-based filesystem access, they do not claim protection against a hostile process racing filesystem components between checks and OS calls.
- Host-specific consent prompts are outside Core; any future transport must use the same Gateway capability boundary.
