# Privacy Boundary

## Protected external data

The V1 StudyVault, Basic Memory database, textbooks, exercise images, transcripts, archive, and other personal learning records remain in their existing locations. Repository setup does not copy, move, migrate, or import those sources. Runtime access is limited to locations explicitly named in ignored local configuration and is governed by Gateway capabilities. Study search uses disposable QMD copies; History is exposed as a read layer; writes to Assets, Documents, and Wrong Answers must use the formal Gateway operations and an enabled local capability.

## Never commit

- `.env`, local configuration, tokens, credentials, certificates, or private keys.
- `var/`, databases and SQLite `-wal`, `-shm`, and `-journal` sidecars, logs, caches, transcripts, archives, and local backups.
- Personal study PDFs, scans, photographs, or other learning material.
- Private `StudyVault`, History, Wrong Answer, Asset store, inbox, staging, OCR-cache, and QMD index directories.
- Any real StudyVault, Basic Memory, or chat/archive content.

`.gitignore` enforces common file and directory classes. It is a guardrail, not a security boundary: inspect `git status` before every commit and do not force-add protected data.

## Fixtures

Tests may use only short, manually authored synthetic examples. They must use invented people, paths, titles, and study content. Never derive a fixture by copying, paraphrasing, cropping, or sanitizing a real personal record. See [fixture rules](../tests/fixtures/README.md).

## Runtime handling

Local paths and credentials belong only in ignored local configuration or an appropriate secret store. `config.local.toml` configures the Gateway's private data sources; `.codex/config.toml` is generated per checkout for the Desktop Host and contains that checkout's absolute path. Both are ignored and must remain untracked. Tool results and logs must not expose absolute personal paths, credentials, raw backend stderr, or full private queries. The initial `health_report` must be a side-effect-free probe.

Write provenance stores logical IDs, source references, runtime UTC timestamps, origin/version metadata, and optional caller-reported Agent/client/session strings. Reported identities are unverified and are not authorization credentials. Provenance and audit rows must not contain source text, image bytes, absolute paths, or credentials. Legacy records are marked `pre_provenance`; unknown identity/import facts remain unknown.

Phase 11's local-only `study-migrate dry-run` may create a bounded temporary copy of an explicitly selected SQLite database and its WAL in the current user's temporary directory. This avoids SQLite read-only WAL access changing the source `-shm` file. The scratch location is checked to stay outside the repository and every configured source/target path; source hashes are checked before and after copying, and normal command completion deletes the scratch copy. A forced process termination can leave a `study-migration-snapshot-*` directory in the local temporary directory; inspect that exact prefix before removing stale scratch. The private manifest path and its SQLite sidecars are checked against configured source/target roots and databases before opening. The command never copies database contents into its manifest or Git.
