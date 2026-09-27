# Phase 6 Closeout Report

日期：2026-09-26
分支：`phase-3-readonly-mcp-spike`

## 结论

Phase 6 收口。产品完成条件是“错题原图优先、教材按需检索与核验”，不是整本教材 eager OCR。系统保留确定性 PDF/text ingestion、内容寻址、页面/片段 provenance、可续的有界 OCR，以及原始 PDF 页面视觉 resource；Gateway 不运行任何 LLM/VLM 或其他生成式 API。

## 保留的能力

- 文档 URI 稳定为 declared media type + source SHA-256，与 extraction/OCR 进度无关；重复 source 在 PDF 解析前复用已有记录。
- 初次 ingestion 只使用有界 OCR budget；剩余 suspicious/unavailable 页面由 `list_document_ocr_candidates` 暴露，`process_document_ocr_pages` 以最多 16 页一批追加确定性 derived OCR。
- `pdf_text_layer`、`pdf_ocr_derived`、`pdf_ocr_empty`、失败/不可用/限额状态分开记录；OCR 为空时不建立搜索 chunk。
- MCP 标准 resource 提供 derived text page 和原始 PDF page PNG。视觉 resource 固定 144 DPI，限制 6,000,000 pixels / 4 MiB，并返回 logical source provenance。
- Capability split、逻辑 URI、路径隐私过滤、SQLite 事务和 asset hash 校验保持不变。

## 真实副本验证（repo 外、临时派生状态）

授权副本为 269 页、23,529,416 bytes，SHA-256 为 `c31c756733a27b1412df345ca447432d90423975b4b1389bcff3859980e8dc97`。验证前后 hash、size、mtime 一致；副本未写入 Git 或 repo。

一次 fresh disposable MCP smoke 显式禁用 OCR runtime，只验证确定性 mapping 与按需链路：269 pages，`pdf_text_layer=40`、`pdf_ocr_unavailable=3`、`pdf_text_layer_suspicious=226`，database `integrity_check=ok`，45 个 lexical chunks。首次 ingestion 用时 161.834s；同一 source 第二次 ingestion 用时 0.758s，返回同一 document URI，未重复 PDF parsing/OCR。`search_documents → document page resource → original page image resource` 的 logical document/page/asset/text-origin provenance 全部通过。

真实 PDF 页面 render 额外校验为有效 PNG，1191×1684、2,154,460 bytes；原始副本仍未变化。

此前受控 OCR continuation 的四个 16-page batch 也已验证无半批状态；停止时 disposable state 为 `pdf_text_layer=40`、`pdf_ocr_derived=72`、`pdf_text_layer_suspicious=157`，共 118 chunks。整本 OCR 不再继续。

## 自动化验证

- Phase 6 targeted/MCP：`87 passed, 1 skipped`
- full regression：`280 passed, 5 skipped`
- 跳过项仍是显式 opt-in 的 Codex/QMD real smoke 与当前 Windows filesystem capability cases；没有因 Phase 6 失败而跳过测试。

## 已知限制与后续

- Tesseract/PyMuPDF 组合在受控 OCR 中仍会产生非致命 `Parameter not found` warnings；OCR 只用于 lexical location，数学公式和视觉完整性必须由 Agent 查看原始页面核验。
- PyMuPDF 的 AGPL/commercial licensing 需要在 Phase 10 release hardening 前完成审查。
- 下一主线是统一所有非原始 Source 写入的 provenance schema（Gateway-generated time、reported agent/client、run/session、source refs、version、supersedes），随后做 P1–P9 全项目自审与真实错题 E2E；不在本收口中扩大范围。
