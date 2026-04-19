# 系统状态查询

> 老史随时可以问："系统状态怎么样？" "搜索系统健康吗？"

## 查询方式

读取以下文件获取最新状态：

```
memory/search-health-weekly.md   → 每周渠道健康日志
memory/tool-updates.md            → 工具能力更新记录（最近一次扫描）
```

## 快速检查命令

```bash
# 核心渠道快速检查（30秒）
python3 /root/.openclaw/workspace/skills/search_health_weekly.py

# 工具扫描（完整，包含 ClawHub/GitHub 新工具）
python3 /root/.openclaw/workspace/skills/tool_scanner.py
```

## 预期返回值

如果老史问"系统状态"，读取后告诉他：
1. 各核心渠道是否正常（ SearXNG / open-webSearch daemon / Tavily / GitHub CLI）
2. 距离下次工具扫描还有几天
3. 是否有最近的升级机会记录

## 不主动推送

系统状态**不主动推送**，老史有需要时直接问。
