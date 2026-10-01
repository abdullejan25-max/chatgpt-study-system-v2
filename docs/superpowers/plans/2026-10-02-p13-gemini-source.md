# P13 Gemini source-only implementation plan

> 使用 executing-plans 在现有 isolated worktree 顺序执行；用户已授权 autonomous
> engineering/private migration，不增加设计审批暂停。

**Goal:** 将已取得的 Gemini 官方包 losslessly 保存为 Gateway source evidence，
完成 Gemini 范围的 exact dedup、重跑幂等与 reconciliation。

**Architecture:** offline input planner 复用 PrivateRawArchiveStore，生成固定 binary ranges、
UTF-8 HTML ranges 与 deterministic source manifest。实际 writes/readback 只用当前
native study_system tools；private ledger 保存 destination refs/receipt hashes。

**Tech stack:** Python stdlib zipfile/html.parser/hashlib、pytest、既有 Assets/Documents。

## Task 1 — Pending acquisition 与 Gateway logical URI ledger

Files: history_ledger.py、history_acquire.py、test_history_ledger.py、test_history_acquire.py。

- [x] RED：`record_catalog(..., state='acquisition_pending')` 可重开；acquire 的 unavailable
  descriptor 接受此状态；`record_outcome` 接受正式 document/asset SHA-256 URI 并拒绝 path。
- [x] GREEN：仅扩展固定 state/ref allowlist；保留现有 schema 与旧 logical IDs。
- [x] 运行两组 ledger/acquire targeted tests。

## Task 2 — Gemini source-only deterministic planner

Files: migration/gemini_takeout.py、tests/test_gemini_takeout.py。

Interfaces: `prepare_gemini_export(source_path, output_root, primary_member=audited_member)`
只访问 explicit offline input；
输出 Git 外 native-write payload files 与 private plan，不启动 MCP client 或打开 V2 store。

- [x] RED：synthetic ZIP 的完整 bytes 可由 fixed ranges 重建；raw HTML UTF-8 ranges
  可重建；renamed source 的 root manifest bytes 相同；附件 JSON 不计活动；多 primary 拒绝。
- [x] GREEN：验证 ZIP CRC/size/paths、显式 activity signature，stream member digests，
  生成 512 KiB binary ranges / 64 KiB UTF-8 ranges，manifest 在写入前验证大小与 refs。
- [x] 增加坏 ZIP、unsafe alias、duplicate members、empty/missing activity、limits 回归。
- [x] targeted tests 与 synthetic real Gateway/server integration，验证 source bytes/provenance。

## Task 3 — Private native execution 与真实 readback

- [x] 更新现有 ChatGPT catalog 为 acquisition_pending；增加此 Gemini scope，不重建旧 inventory。
- [x] 写前保存 private plan/raw checksum；按计划执行 native register_asset / ingest_documents，
  每个 receipt 都写 Git 外，不打印真实内容或 IDs。
- [x] 通过 native fetch_asset 回读所有 archive/HTML ranges；重建并核对完整原始 digest。
- [x] root manifest fetch/search/no-result；同包第二次执行 refs 不变、logical source 新增 0。
- [x] reconciliation 解释所有 archive members；活动条目不算 canonical messages。

## Task 4 — Public verification 与 checkpoint

- [x] 独立 review、targeted/full tests、wheel/sdist、working/staged/new Git objects privacy。
- [x] 更新 P13 checkpoint：Gemini-specific PASS 与全局 PARTIAL 分开；ChatGPT pending 非 blocker。
- [x] local commit；不 bump/release/push、不启动全量 normalization、不删除 V1。
