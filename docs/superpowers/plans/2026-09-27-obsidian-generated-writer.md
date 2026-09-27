# Obsidian Generated Writer Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add an explicitly invoked, manifest-bounded writer for deterministic Obsidian projection files.

**Architecture:** Keep rendering pure and in memory. Add a separate writer that validates an explicit dedicated directory, tracks ownership with a versioned manifest, atomically replaces generated files, and removes only stale files previously listed by its manifest.

**Tech Stack:** Python standard library, pathlib, json, tempfile, pytest.

## Global Constraints

- Never connect to Gateway, databases, network services, or authoritative Study files.
- Use only synthetic content and temporary directories in tests.
- Never choose or write a real Obsidian Vault in this milestone.
- Never recursively delete directories or remove files absent from the prior ownership manifest.
- Fail closed on unsafe paths, symlinks, and malformed manifests.

---

### Task 1: Add the manifest-bounded writer

**Files:**
- Create: `src/chatgpt_study_system/obsidian_writer.py`
- Test: `tests/test_obsidian_writer.py`

**Interfaces:**
- Consumes: `dict[str, str]` rendered file map and explicit `Path` projection directory.
- Produces: `write_projection(files: Mapping[str, str], projection_dir: Path) -> None` and fixed-message `ProjectionWriteError`.

- [x] Write tests first for initial write and repeat write producing byte-identical files and manifest.
- [x] Run `uv run --extra dev pytest -q tests/test_obsidian_writer.py -p no:cacheprovider` and confirm the missing-module failure.
- [x] Implement path validation, an empty/new-directory first-use rule, a versioned ownership manifest, atomic per-file replacement, and manifest-last publication.
- [x] Add tests for stale owned-file deletion, preservation of unknown files, traversal rejection, malformed manifests, symlink rejection where supported, and replacement failure preserving the old manifest.
- [x] Rerun the focused writer tests and then `uv run --extra dev pytest -q -p no:cacheprovider`.
- [x] Run `git diff --check` and commit the tested writer separately.

### Task 2: Record the safe preparation boundary

**Files:**
- Modify: `docs/p12-obsidian-reality-audit.md`
- Modify: `docs/autonomous-run-status.md`
- Modify: `docs/current-state.md`

- [x] Document that a synthetic writer exists but no real Vault write or GUI review occurred.
- [x] Record focused and full test results only after observing them.
- [x] Confirm no private paths, generated personal Markdown, or real source data entered Git.
- [ ] Run `git diff --check` and commit the status update.
