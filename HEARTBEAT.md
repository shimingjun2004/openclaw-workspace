# HEARTBEAT.md - smj-小秘 定期任务

> 上次更新：2026-04-18
> 配置说明：下面的任务会在心跳周期被扫描执行

---

## 🏥 系统健康检查

### OpenClaw 服务状态
- **频率**：每小时
- **内容**：检查 Gateway 是否运行、进程是否正常
- **命令**：`openclaw gateway status`

---

## 🎓 2026 高考志愿跟踪 ⭐最高优先级

### 任务1：北京教育考试院公告巡查
- **频率**：每2天
- **内容**：
  1. 访问 bjeea.cn 首页，抓取最新公告
  2. 搜索"高考""招生""录取"相关最新政策
  3. 如发现新公告，整理摘要写入 memory/gaokao-updates.md
  4. 如有重大政策变化，通过 Control UI 提醒老史
- **信息源**：北京教育考试院 bjeea.cn

### 任务2：目标高校招生简章巡查
- **频率**：每3天
- **内容**：
  1. 搜索清华、北大等北京重点高校最新招生简章
  2. 关注招生专业、计划数、录取规则变化
  3. 记录到 memory/gaokao-updates.md
- **信息源**：各高校招生网、SearXNG 搜索

### 任务3：关键时间节点提醒
- **频率**：每天
- **内容**：对照以下时间线，到期前提醒老史
  - [ ] 高考报名时间（预计2025年11月）
  - [ ] 高考时间（预计2026年6月7-8日）
  - [ ] 成绩公布（预计2026年6月下旬）
  - [ ] 志愿填报（预计2026年6月底-7月初）
  - [ ] 录取结果（预计2026年7月）

---

## 🌐 技术资讯跟踪

### 任务4：AI/模型动态周报
- **频率**：每周六上午
- **内容**：
  1. 搜索本周 AI 大模型最新进展
  2. 搜索 OpenClaw/GitHub 相关更新
  3. 整理1条最值得关注的更新，写入 memory/tech-weekly.md
  4. 通过 Control UI 给老史一个一句话总结
- **关键词**：LLM, GPT, Claude, Gemini, OpenAI, Anthropic, AI Agent

---

## 🔧 工具能力扫描（中文搜索系统维护）

### 任务5：搜索工具定期扫描
- **频率**：每3天
- **任务ID**：tool_scanner
- **内容**：
  1. 扫描 ClawHub 新增 browser-automation / playwright / MCP 相关 skill
     - 命令：`clawhub search browser-automation` 和 `clawhub search playwright`
     - 关注评分 3.6+ 的新增 skill
  2. 扫描 GitHub trending 是否有新型中文搜索方案
     - 命令：`gh search repos "chinese search OR 中文搜索" --sort stars --limit 5`
  3. 扫描 SearXNG 百度引擎是否恢复
     - 命令：`curl -s "http://127.0.0.1:8080/search?q=test&format=json&engines=baidu" | grep -c results`
     - 若返回 > 0 条，通知老史可恢复百度引擎
  4. 扫描 Tavily 新模型/接口变化
     - 测试：`python3 -c "from tavily import TavilyClient; c=TavilyClient(api_key='xxx'); print(c.search('test',max_results=1))"`
  5. 若发现重大更新（评分显著提升/新能力），写入 `memory/tool-updates.md` 并通过 Control UI 推送摘要

### 任务6：中文搜索系统健康检查
- **频率**：每天
- **内容**：快速验证核心渠道是否正常
  - 微博热搜：`python3 cn_search.py --hot 2>&1 | grep -c '条'`
  - 必应搜索：`curl -s "http://127.0.0.1:8080/search?q=AI&format=json&engines=bing" | grep -c results`
  - Tavily：`python3 -c "from tavily import TavilyClient; c=TavilyClient(api_key='tvly-dev-xxx'); r=c.search('test',max_results=1); print(len(r['results']))"`
  - open-webSearch daemon：`curl -s http://127.0.0.1:18080/health`
  - SearXNG：`curl -s http://127.0.0.1:8080/health | grep -o '"status":"[^"]*"'`
  - 若任一渠道连续2次失败，写入 memory/tool-updates.md 并提醒

### 任务7：中文搜索系统深度模式使用统计（每周）
- **频率**：每周六
- **内容**：
  - 统计上一周 `--deep` 模式调用情况（若接入OpenClaw）
  - 评估 Tier-2 触发率是否合理
  - 评估 360 噪音过滤效果
  - 决定是否需要调整触发阈值
  - 将评估结论写入 `memory/search-stats-weekly.md`

---

## 📌 主动告警阈值规则（必须遵守）

所有"主动告知"必须基于明确阈值，杜绝风吹草动就报警：

### 搜索系统核心渠道
| 指标 | 告警阈值 | 说明 |
|------|---------|------|
| 核心渠道连续失败 | **≥ 2次** | 单次失败不报警，连续2次才触发 |
| 单渠道成功率 | **< 50%** | 近3次检查中该渠道失败≥2次 |
| deep模式失败率 | **≥ 50%** | 单次deep失败不报警 |
| 百度引擎失效 | **连续2次** | 恢复后再次失效才标红 |

### 高考系统
| 指标 | 告警阈值 | 说明 |
|------|---------|------|
| 政策公告 | **有变化就报警** | 报名/志愿/考试时间变更无阈值 |
| 招生简章发布 | **有就报警** | 无阈值 |
| 录取结果公布 | **有就报警** | 无阈值 |

### AI技术周报
| 指标 | 告警阈值 | 说明 |
|------|---------|------|
| 发现重大突破 | **有就推送** | 无阈值，但需经过核实 |

### 工具扫描
| 指标 | 告警阈值 | 说明 |
|------|---------|------|
| 新skill评分 | **≥ 3.6** | ClawHub评分低于此不推送 |
| 百度引擎恢复 | **立即** | 已经是已恢复备用，发现即记录 |
| 新搜索方案 | **评分≥4.0** | GitHub项目低于此不推送 |

---

## 📌 执行说明

- 所有定期任务以"发现重大更新才提醒"为原则，避免无效骚扰
- 巡查结果默认写入 memory/ 目录，不主动推送
- 发现以下情况立即提醒老史：
  1. 高考政策重大变化（报名时间、志愿填报规则）
  2. 目标院校招生简章发布
  3. 录取结果公布
  4. **搜索系统核心渠道连续 ≥2次 故障**（按上表阈值判断）
  5. **发现重大搜索能力升级机会**（评分≥3.6 ClawHub skill，≥4.0 GitHub项目）
- 每次提醒附带信息来源和简要摘要
- **禁止**：单次失败/单次超时/单次返回少就报警
- **禁止**：没有达到阈值的"疑似问题"主动推送

