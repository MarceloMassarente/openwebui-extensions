# Playwright OpenWebUI Plugin Test — Learnings

> 这是一个持续积累的知识库，由 `plugin-tester.agent.md` 在每次会话后自动维护。
> 每次测试开始前必须先读取本文件；测试结束后必须将新发现追加到对应章节。

---

## ✅ 已验证的可靠 Selectors

### 登录页面

- Email 输入框: `input[name="email"], input[autocomplete="username"], input[type="email"]`
- 密码输入框: `input[type="password"]`
- 登录按钮: `button[type="submit"]`
- 登录完成检测: `[id="chat-textarea"], div[contenteditable]`

### 管理员面板

- 导航到函数页: `/admin/functions`
- 函数列表项: `.function-item, [data-function-id]`（待验证，随版本变化）

### 聊天界面

- 消息输入框: `[id="chat-textarea"], textarea, div[contenteditable]`
- 发送按钮: `button[data-element-id="send-message-button"], button[aria-label*="send" i]`
- AI 回复消息: `.message-content, [data-role="assistant"]`

### Action 插件

- 消息工具栏（需 hover 触发）: `.message-toolbar, [class*="action"]`
- Action 按钮（按文本过滤）: `button[title], button.action-button`

---

## ❌ 已知失效或不稳定的 Selectors

> （新发现时追加到此处，注明日期和原因）

---

## ⚡ 已知时序敏感点

- **登录后延迟**: 页面跳转完成后需 `waitForTimeout(1500)` 才能可靠交互
- **Action 按钮显示**: 需先 hover 消息区域，再等 300ms，按钮才会出现
- **模型下拉**: 点击后等 500ms 再选择选项，否则列表未渲染完
- **插件 HTML 输出**: Action 执行后需等 2000ms+ 才能检查 iframe 内容

---

## 🧪 已验证的测试用例

> （每次通过测试后追加，格式：日期 | 插件名 | 测试内容 | 结果）

---

## 🐛 已发现的 UI Bug

> （格式：日期 | 插件名 | 描述 | 截图路径 | 状态）

---

## 📝 部署注意事项

- `scripts/.env` 格式: `api_key=sk-...` + `url=http://...`（不带引号）
- `scripts/install_all_plugins.py` 会跳过 `_cn.py` 和中文文件名
- `scripts/verify_deployment_tools.py` 可在部署前验证环境是否就绪
- Action 插件部署后需在 Admin 面板**手动启用**，脚本不会自动 enable

---

## 🗺️ OWUI 版本兼容性观察

> （格式：OWUI 版本 | 变化点 | 影响的 selector 或行为）
