# 长期开发规则

- ChatGPT 是最终产品的主大脑，Local Gateway 不是第二个 Agent。
- 一个 Codex 任务只做一个明确目标。
- 新 Codex 对话优先读取 `roadmap.md` 和当前 checkpoint，不重新扫描全部历史。
- 长任务必须更新 checkpoint。
- 小任务完成后测试、Git commit、停止；未经授权不自动做下一节点。
- 保护真实教材、错题、聊天历史等权威数据。
- QMD index、cache、WAL 等可重建派生数据，可以在明确边界内正常写入；它们不与权威数据采用相同保护等级。
- 不提供任意 Shell，不让提示词充当权限边界。
- 面向用户的自然语言、checkpoint、报告、ADR 正文尽量使用简体中文。
- 代码标识符、API、错误码、CLI、库名、Git commit message 保留英文。
- 已有英文历史文档不批量翻译，修改到时再逐步中文化。
- 默认优先简单可靠的方案，避免过度工程化。
- Phase 10 负责 GitHub 发布准备。本次任务已授权在 Release Gate 全部通过后创建 public repository 并首次 push；在 clean-checkout Desktop GUI 验证通过之前不执行这些操作。不重写旧开发 history，改以独立 clean root 发布。
