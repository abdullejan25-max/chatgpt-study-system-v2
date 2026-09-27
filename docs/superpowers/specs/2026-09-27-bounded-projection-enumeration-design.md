# Bounded Projection Enumeration Design

## Goal

Provide an opt-in, read-only Gateway path that lets the P12 collector enumerate all bounded History and Wrong Answer DTOs without query guessing or direct database access from the renderer.

## Authorization boundary

Bulk export is exposed only under a new `projection` capability. It is separate from `read`, `write`, `ingest`, and `admin`; a normal read-only Host will not see or call the export tool unless its trusted local configuration explicitly enables `projection`. The operation never writes to either database or to the filesystem.

## Per-store protocol

The protocol has three operations: `begin`, `sources`, and `records`. `begin` captures a domain-specific SQLite high-water token and returns source/record counts and stored-payload byte totals. `sources` pages over registered sources at that token. `records` pages over the records belonging to one known source using the same token. Page size is capped at 20. History uses its History database; Wrong Answer uses the Documents/Assets database. A page cursor is an opaque nonnegative row/version position and is validated against the captured watermark.

History items and Wrong Answer sources/analyses are append-only through their supported Gateway operations. Watermarks exclude later inserts. Each domain is capped at 10,000 sources, 10,000 records, and 32 MiB of stored payload; History also caps sources plus items at 10,000 to fit the renderer's snapshot bound. The collector must reconcile every source's reported record count and the domain-wide count before rendering. If the snapshot exceeds limits, the Gateway returns a fixed `PAYLOAD_TOO_LARGE` error; no partial result may be called complete. This protocol does not create a global atomic point across the two SQLite databases; outputs retain independent per-store watermarks and counts.

## DTO and privacy boundary

The Gateway reuses safe DTO handling, redacts local paths, checks source references, and reduces provenance to the categorical fields the renderer displays. It returns only bounded pages and logical IDs required for continuation. No absolute database path, SQL diagnostics, or private storage metadata is returned. The renderer remains a pure function over explicitly supplied DTOs, and the writer remains a separately invoked filesystem operation. A collector still needs to consume all pages and reconcile the per-source and domain totals before calling the renderer.

## Verification

Synthetic SQLite tests cover capability isolation, empty and populated stores, stable continuation under later inserts, deterministic order, per-source and total count/byte reporting, bounds, malformed cursors/tokens, and read-only behavior. MCP schema tests verify the new tool is absent for plain `read` and present only for `projection` or `admin`. No personal database or Vault is used.
