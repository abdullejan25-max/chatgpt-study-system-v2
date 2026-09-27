# Phase 3 Report — Read-only MCP Spike

## Phase 3 Result: PASS

只读 V2 MCP Spike 已通过。`health_report` 和 `search_study` 经由 stdio MCP
transport 同时完成了 SDK in-memory protocol 与 Codex Host 实测。

真实 QMD 只在 disposable runtime 中运行：固定 native `node.exe` 加已审计的
QMD 2.8.3 JavaScript entrypoint，真实 config 复制到临时目录，派生 SQLite index
使用 SQLite backup API 制作一致性副本。PATH 的 `.cmd` / `.ps1` launcher 仍被拒绝。
StudyVault 和原始 QMD config 的完整清单在 real smoke 前后完全一致；派生 index
的内容保持一致，SQLite WAL reader 只刷新了 `-shm` sidecar 的 mtime。

## Implemented

- A new local-only Greenfield repository on `phase-3-readonly-mcp-spike`, with
  no Git remote.
- Privacy-safe `.gitignore`, example configuration, ADR copies, fixture rules,
  and a recovery checkpoint.
- Typed Gateway contracts, stable safe errors, input validation, canonical
  Study-root containment, and `NotConfiguredHistoryBackend`.
- Strictly non-mutating `health_report` and read-only `search_study` application
  contracts.
- `QmdStudyBackend`, constrained to fixed `qmd search --format json
  --collection studyvault -n <limit> -- <query>` arguments, `shell=False`, an
  explicit timeout, controlled environment, and safe QMD URI validation.
- A fail-closed Windows launcher rule: unresolved paths and `.cmd`, `.bat`, or
  `.ps1` launchers are rejected before a process starts.
- An official MCP SDK stdio transport that exposes exactly two tools,
  `health_report` and `search_study`; it rejects extra arguments and returns
  structured, sanitized responses.
- A minimal explicit-config composition root. It creates no configuration,
  database, cache, directory, or network service.

## Project structure and dependencies

The project contains only `src/`, `tests/`, and `docs/` as working areas.
Core contracts, policy, Gateway, runtime composition, History/QMD adapters,
and the stdio transport are separated under `src/chatgpt_study_system/`.

Declared dependencies are Python 3.11+, `mcp>=1,<2`, and pytest for the `dev`
extra. The verified local environment used Python 3.12.8, `mcp==1.30.0`, and
`pytest==9.1.1`.

## Verification and security evidence

Fresh verification completed with:

```text
.venv\\Scripts\\python.exe -B -m pytest -q -p no:cacheprovider
109 passed, 1 skipped
```

The one skipped test is a physical symlink-creation check that needs a Windows
privilege unavailable on this host. A separate, non-skipped deterministic test
covers the same canonical-resolved symlink/junction escape boundary.

The suite uses only artificial fixture content. It verifies, among other
things:

- health calls do not start a subprocess or alter fixture hashes, mtimes, file
  counts, directory counts, logs, caches, or databases;
- query trimming, length, NUL, and limit constraints;
- safe error codes and absence of raw query, stderr, token, or absolute-path
  disclosure;
- traversal, absolute/rooted/UNC-looking and resolved-link path escapes;
- fixed QMD command construction, collection, option termination, timeout,
  malformed output, launcher rejection, and absence of a fallback scan;
- actual MCP protocol inventory/calls over SDK memory streams, strict tool
  inputs, safe Gateway errors, and no application socket bind after the Windows
  event loop starts.

Windows asyncio can make a transient internal socketpair while initializing its
event loop. This is not an application listener; the transport creates no HTTP,
SSE, or MCP listening endpoint.

## Real-data QMD smoke

**PASS。** 真实搜索在一次性临时 runtime 中执行并完成前后 SHA-256、size、mtime
清单比较。没有修改 StudyVault、原始 QMD config、原始 index 主文件或 WAL 内容。
`index.sqlite-shm` 的 mtime 被 SQLite WAL 读取过程刷新，hash 与 size 不变；它属于
可重建派生数据，已成为明确定义的唯一例外。

## Codex MCP E2E

**PASS。** 使用一次性的 Codex CLI MCP config override 启动真实 stdio server，
Host 顺序调用了 `health_report` 与 `search_study`；两个调用成功，后者返回一条
safe relative source。未保存项目级或用户级 MCP 配置，也未开放监听端口。

## Git and data status

- Branch: `phase-3-readonly-mcp-spike`
- Git remote: none
- Real user data modified: no
- V1/WorkBuddy/StudyVault/Basic Memory modified: no

Key implementation commits are `3ae8587` (Gateway), `651915a` (QMD adapter),
and `9cf9f24` (stdio MCP transport), followed by focused review fixes. The
complete recovery history is maintained in
`docs/phase-3-checkpoint.md`.

## Remaining work

- Phase 3 已完成。下一阶段调查当前官方 ChatGPT 接入能力并产出 capability
  report；若 entitlement、API key 或账号操作成为前提，按项目红线停下。
