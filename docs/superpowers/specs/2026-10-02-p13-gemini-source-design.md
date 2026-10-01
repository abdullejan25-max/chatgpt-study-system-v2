# P13 Gemini source-only acquisition design

本轮只接续 Gemini；ChatGPT 官方请求已提交，状态为 `acquisition_pending`，不阻塞
当前来源的处理。沿用现有 private ledger、worktree 与已通过的 native Gateway Gate。
不进行全量 Conversation Normalization，不退役或删除 V1。

## 选择与边界

现有 native MCP 提供 Assets/Documents 写入，但 legacy archive 接口只有读取。
新增第二套 History store 或直接调用 private SQLite 均不符合当前边界；新增 MCP
写入 contract 也不是保存本包所必需。因此复用现有 source Assets 与 derived Documents：

- 完整官方 ZIP 按固定 byte ranges 进入 `application/octet-stream` Assets。
- 一个 deterministic source-only manifest Document 关联全部 archive ranges、原始
  member names/digests、primary My Activity HTML ranges 与实际逻辑 refs。
- primary HTML 按 UTF-8 byte boundaries 分段保留原字节，通过 text Documents 索引。
  Document pages 是既有 deterministic derived text；original Asset bytes 是证据。
- 自动识别仅限 direct My Activity/Gemini 位置的已支持官方 primary 名称；本地化/改名
  member 使用 private reality audit 的 explicit descriptor，再验证 UTF-8/activity signature。
  不能把目录内所有 HTML 当成 activity candidates。
- 不执行附件 HTML，不递归解包附件，不解析附件聊天 JSON，不猜角色或会话边界。
  所有附件仍完整存在于 Gateway 保存的官方 ZIP 中。

一个 export bundle 是一个逻辑 source；asset/document ranges 不是 conversations
或 messages，也不混入既有 legacy-source 统计。activity count 只指官方 HTML 的
显式 activity blocks，不能冒充 conversation/message count。

## Identity、preservation、recovery

文件位置与导入时间不进入 manifest identity。Archive SHA-256、member bytes、range
order 与 digests 决定 evidence identity；同字节改名/移动重跑复用原逻辑 refs。
不同 archive packaging 保留独立证据；member-byte equality 只产生 duplicate-candidate
统计，不执行语义合并或删除。其它 file members 称 opaque，实际 attachment count 未知。

沿用 PrivateRawArchiveStore 的 CRC、expansion limits、稳定输入与 raw-copy 校验。
plan 在任何 production write 前完成全部 bounded validation；root manifest 最后发布。
输出根与 protected target 双向不重叠，所有写入路径再次检查；private plan/payload
原子替换，避免中断覆盖上一份有效文件。
每个 native write/readback receipt 在 Git 外持久保存，中断重跑复用 deterministic refs。
每次 native write 都比对 returned identity；不匹配时保留失败回执与未引用产物，有限重试，
不能因工具返回 ok=true 就接受不同字节。未知原因不能冒充已确认的 transport 修复。
只有所有 ranges 经正式 Gateway 回读并还原出原 ZIP/HTML SHA-256 后，ledger 才登记
imported/reused。原始时间保持 source evidence，写入时间来自 Gateway provenance。

## 验证

人工 synthetic ZIP 覆盖：正常活动、unknown timestamps、附件聊天不可误分类、坏 ZIP、
不安全 member、多个 activity candidates、UTF-8 跨分块、输入改名、重复成员字节、
manifest deterministic identity、Gateway source refs 与 ledger URI/provenance。
真实 audit、源路径、member names、digests、payloads 与 receipts 全部 Git 外。
验收使用 native register/ingest/fetch/search；不得直接读取生产 DB/store。
