# P13 Phase A — 有界来源获取与私有证据设计

正式起点为 v0.6.0。用户已授权本地自主执行；本设计只实现 inventory 与 ledger，
不提前设计或执行 canonical normalization，不重复 P11/P12 验收。

## 方案与边界

采用显式来源描述符 + 内容指纹 + 私有 append-only ledger。沿用已有安全文件读取与
Git 外 journal 路径校验。相比按文件名登记，该方案可识别改名/移动后的相同字节；
相比扫描整个用户目录，只检查已知会话根和官方导出位置，范围可以复核。

来源记录保存类型、格式、大小、SHA-256、记录估计、时间范围、parser 状态、
role/time/boundary 质量、获取方式与私有位置。文件修改时间只用于一致性校验，
不能充当对话发生时间。结构检查不生成消息，也不保存聊天正文到 ledger。

相同类别与内容指纹可标记 exact duplicate，但所有获取位置仍分别保留。
跨格式/跨类别的相似性不自动合并。原始输入不改写、不删除。

ledger 使用独立 SQLite，事务、FULL synchronous、版本校验与 append-only 状态事件；
discovered/parsed 与 imported/reused 是不同事实。缺少真实 Gateway readback 的记录
不能登记为 imported/reused。错误信息使用固定 error class，不携带私人路径或正文。

## 质量与验收

JSON/JSONL 使用有界确定性结构 probe；不猜角色、边界或时间。Markdown/ZIP/SQLite
先记录为 source-only 或 unsupported。缺失 official export、runtime metadata、
malformed 和无法判断的记录必须保留明确状态。

测试全部手工构造：改名重复、修改版本、未知格式、缺时间、未知角色、坏 JSONL、
credential 排除、reparse/hardlink、ledger 重开与状态证据约束。公开 summary 只由
固定类别和计数组成，无位置、指纹、标题、ID 或行为时间。

## 顺序 Gate

1. Phase A：已知来源逐项归类，范围与遗漏风险可解释。
2. Phase B：正式 Gateway source-only 导入、原字节保存、去重、生产回读。
3. Phase C/D：B Gate PASS 后才设计规范化、执行并对账。
4. Phase E：完整承接与恢复 Gate PASS 后才审计/逻辑退役 V1。
5. 物理删除必须等 owner 明确确认；本阶段无删除操作。

当前 Host 未加载 production MCP 时，V2 计数与承接情况保持 UNKNOWN，不能用
离线读取私有 store 或新建直接客户端填补证据。
