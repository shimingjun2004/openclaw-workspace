# cn-search · 中文搜索入口

> 中文搜索系统 Stable v1.1 · 主入口 Skill

## 触发词

当老史说以下类型的话时，自动调用本 skill：

- "搜一下 XXX"
- "搜这个"
- "搜搜看"
- "帮我查一下"
- "帮我搜"
- "查一下 XXX"
- "搜一下 XX 相关"
- "搜一下 XX 最新动态"
- "搜一下 XX 最新消息"

**注意**：如果老史明确说"深度调研""技术深挖""对比分析"，触发 `--deep` 模式。

## 调用命令

```bash
# 自动模式（系统自动判断 hot/fast/normal/deep）
python3 /root/.openclaw/workspace/skills/cn_search.py <关键词>

# 明确快捷模式
python3 /root/.openclaw/workspace/skills/cn_search.py --hot              # 热点：微博+B站
python3 /root/.openclaw/workspace/skills/cn_search.py --fast             # 轻量：Tier-1单轮
python3 /root/.openclaw/workspace/skills/cn_search.py --normal           # 默认：智能Tier-2
python3 /root/.openclaw/workspace/skills/cn_search.py --deep             # 深度：全链路+GitHub

# 自然语言优先触发 --deep 的场景
# "深度搜 XX"
# "技术深挖 XX"
# "深度调研 XX"
# "全面搜一下 XX"
# "搜一下 XX 对比 XX"
# "搜一下 XX 评测"
# "搜一下 XX 哪个好"
# "搜一下 XX 分析"
```

## 输出格式

搜索完成后：

1. 先给**质量统计**（耗时、渠道数、去重条数）
2. 再给**Top 10 结果**（标题 + 来源 + 摘要）
3. 最后附**质量报告**（各渠道响应时间/成功率）
4. **不主动抓正文**，需要时老史说"看第X条"再单独抓

## 补充工具（按需调用）

```bash
# 知乎专项
python3 /root/.openclaw/workspace/skills/zhihu_fetch.py <关键词>

# 微信专项
python3 /root/.openclaw/workspace/skills/wechat_fetch.py --sogou <关键词>

# 视频字幕（YouTube）
yt-dlp --write-auto-sub --sub-lang zh-Hans,en "<url>"
```

## 不做的事

- 不抓微信公众号/知乎正文（平台壁垒，headless 绕不过）
- 不7路全开（分层路由，故障隔离）
- 不盲目扩源（当前7渠道已够用）
- 不在正常流程里引入 Playwright/浏览器自动化

## 适用场景

| 场景 | 推荐模式 |
|------|---------|
| 日常信息查找 | normal（自动） |
| 热点事件跟踪 | hot |
| 快速确认一件事 | fast |
| 技术工具选型 | deep |
| 方案对比评估 | deep |
| 新技术调研 | deep |
