# Phase 5 checkpoint: deterministic History

The History backend is a private SQLite store selected only by `[history] backend = "sqlite"` and an absolute `database` path in local configuration. Existing `backend = "not_configured"` files remain valid. Loading configuration creates no database, searches no directories, and imports no records. The database parent must already exist; explicit source registration is the only operation that initializes the schema.

Each import item supplies a logical source item ID, conversation ID, role, timezone-aware timestamp, and content. Unicode content is normalized to NFC and whitespace is collapsed. Timestamps normalize to UTC while retaining microsecond precision; inputs with more than six fractional digits are rejected to prevent silent collisions. The SHA-256 of normalized UTF-8 content deduplicates payload storage, while a separate item row retains each source and conversation occurrence. Item IDs derive deterministically from the source and source item IDs. Reimporting the same record is idempotent; changing a record under the same ID is a conflict. A batch with malformed data or a conflict does not leave partial item imports.

Search uses SQLite FTS5 prefix matching and a deterministic spelling-tolerant fallback when FTS finds nothing. The adapter processes at most 2,048 matching FTS candidates, or 2,048 filtered records for the fuzzy fallback. A larger candidate set fails with `PAYLOAD_TOO_LARGE` rather than presenting incomplete pagination or materializing an unbounded result. Optional source and conversation filters, an offset bounded to 0–1000, and a limit bounded to 1–20 apply. Results order by timestamp descending and stable ID ascending. The Gateway returns bounded snippets, provenance, and safe public errors; fetch by stable ID returns normalized content. Public text redaction handles absolute Windows drive, UNC, root-relative Windows, and POSIX path tokens, including roots, spaced directory and filename segments, extensionless names, multiple extensions, and internal commas/semicolons. The bounded heuristic consumes spaces until sentence punctuation, an HTTP(S) URL, or an explicit `and`/`or`/`then`/`but` prose connector; URLs and relative references after those boundaries remain visible. Unquoted free text without such a boundary is inherently ambiguous. The MCP adapter exposes `list_history_sources`, `search_history`, and `fetch_history_item` as read-only typed tools. No History write tool, source discovery, LLM, or annotation generator is present.

All new tests use manually invented records. The in-process MCP client exercises discovery, search, fetch, validation, and fail-closed behavior. Run `uv run --extra dev pytest -q` for the full suite.

## Verification and checkpoint

- Phase 5 full regression: `183 passed, 3 skipped`.
- The skipped cases were the host's symlink restriction and the two explicitly opt-in real-QMD smoke tests.
- Coherent local implementation/fix commits: `ea531f3`, `dcfc059`, `bcbae56`, `856278c`, and `55194e7`.
- No real History export was imported or queried; all records were synthetic.
