#!/usr/bin/env python3
"""
中文搜索系统定期工具扫描器
被 HEARTBEAT.md 定时任务调用（每3天一次）

职责：
1. 扫描 ClawHub 新增 browser-automation / playwright skill
2. 扫描 GitHub trending 是否有新型中文搜索方案
3. 检查 SearXNG 百度引擎是否恢复
4. 检查各核心渠道健康状态
5. 发现重大更新写入 memory/tool-updates.md
"""
import sys, time, subprocess, json, os
from datetime import datetime

LOG_FILE = "/root/.openclaw/workspace/memory/tool-updates.md"
ALERT_THRESHOLD = 3.6  # ClawHub skill 评分门槛

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M')}] {msg}", flush=True)

def write_update(findings):
    """写入重大更新到 memory"""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    existing = ""
    if os.path.exists(LOG_FILE):
        existing = open(LOG_FILE).read()

    header = f"# 工具能力更新记录\n> 更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    with open(LOG_FILE, "w") as f:
        f.write(header + findings + "\n\n" + existing)
    log(f"已写入更新记录: {LOG_FILE}")

def check_searxng_baidu():
    """检查 SearXNG 百度引擎是否恢复"""
    log("检查 SearXNG 百度引擎...")
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "10",
             "http://127.0.0.1:8080/search",
             "--data-urlencode", "q=test",
             "-d", "format=json&engines=baidu&limit=1"],
            capture_output=True, text=True, timeout=15
        )
        results = json.loads(r.stdout).get("results", [])
        count = len(results)
        if count > 0:
            msg = f"✅ 百度引擎恢复！可返回 {count} 条结果（建议改回百度引擎）"
            log(msg)
            return {"ok": True, "count": count, "msg": msg}
        else:
            log(f"百度引擎仍返回0条（维持必应替代）")
            return {"ok": False, "count": 0}
    except Exception as e:
        log(f"百度引擎检查失败: {e}")
        return {"ok": False, "error": str(e)}

def check_searxng_health():
    """检查 SearXNG 整体健康状态"""
    log("检查 SearXNG 健康状态...")
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "5", "http://127.0.0.1:8080/health"],
            capture_output=True, text=True, timeout=8
        )
        if "ok" in r.stdout.lower() or "200" in r.stdout:
            log("SearXNG: ✅ 健康")
            return True
        else:
            log(f"SearXNG: ⚠️ 异常 {r.stdout[:50]}")
            return False
    except Exception as e:
        log(f"SearXNG: ❌ 检查失败 {e}")
        return False

def check_owdaemon():
    """检查 open-webSearch daemon"""
    log("检查 open-webSearch daemon...")
    try:
        r = subprocess.run(
            ["curl", "-s", "--max-time", "5", "http://127.0.0.1:18080/health"],
            capture_output=True, text=True, timeout=8
        )
        if "\"ok\"" in r.stdout or "\"running\"" in r.stdout:
            log("open-webSearch: ✅ 运行中")
            return True
        else:
            log(f"open-webSearch: ⚠️ 异常 {r.stdout[:50]}")
            return False
    except Exception as e:
        log(f"open-webSearch: ❌ 检查失败 {e}")
        return False

def check_tavily():
    """检查 Tavily 是否正常"""
    log("检查 Tavily...")
    try:
        from tavily import TavilyClient
        key = "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"
        client = TavilyClient(api_key=key)
        r = client.search(query="AI大模型2026", max_results=1)
        count = len(r.get("results", []))
        if count > 0:
            log(f"Tavily: ✅ 正常 ({count}条)")
            return True
        else:
            log("Tavily: ⚠️ 返回为空")
            return False
    except Exception as e:
        log(f"Tavily: ❌ 失败 {e}")
        return False

def scan_clawhub():
    """扫描 ClawHub 新增 skill"""
    log("扫描 ClawHub 新增 skill...")
    findings = []
    try:
        for keyword in ["browser-automation", "playwright", "MCP"]:
            r = subprocess.run(
                ["clawhub", "search", keyword],
                capture_output=True, text=True, timeout=15
            )
            if r.returncode == 0:
                for line in r.stdout.split("\n"):
                    parts = line.strip().split()
                    if parts and parts[-1].replace(".","").replace("(","").replace(")","").replace(",","").replace(" ","").replace("\t","").replace("[","").replace("]","").replace("(","").replace(")","").replace(".","0").replace(" ","").replace("\t","").strip().endswith(")") or parts[-1].endswith(")"):
                        pass
                # 简单解析：取评分>阈值的行
                for line in r.stdout.split("\n"):
                    if any(word in line.lower() for word in ["browser", "playwright", "mcp"]):
                        # 提取评分（格式：name 评分(x.XX)）
                        import re
                        scores = re.findall(r"\((\d\.\d{3})\)", line)
                        for sc in scores:
                            if float(sc) >= ALERT_THRESHOLD:
                                findings.append(f"  [{keyword}] {line.strip()} (评分 {sc})")
    except Exception as e:
        log(f"ClawHub 扫描失败: {e}")

    if findings:
        msg = "发现高评分 skill:\n" + "\n".join(findings)
        log(msg)
    else:
        log("ClawHub: 无重大新增")
    return findings

def scan_github():
    """扫描 GitHub 是否有新型中文搜索方案"""
    log("扫描 GitHub trending...")
    findings = []
    try:
        # 搜索中文搜索相关热门仓库
        for query in ["chinese search tool", "中文搜索 python", "search engine china github"]:
            r = subprocess.run(
                ["gh", "search", "repos", query, "--sort", "stars", "--limit", "3",
                 "--json", "name,description,url,stars"],
                capture_output=True, text=True, timeout=15
            )
            if r.returncode == 0:
                try:
                    items = json.loads(r.stdout)
                    for it in items:
                        stars = it.get("stars", 0)
                        if stars > 100:
                            findings.append(f"  {it['name']} ⭐{stars}: {it.get('description','')[:60]}")
                except:
                    pass
    except Exception as e:
        log(f"GitHub 扫描失败: {e}")
    if findings:
        log(f"GitHub: 发现 {len(findings)} 个潜在相关项目")
    return findings

# ── 主流程 ─────────────────────────────────────────

def main():
    log("=" * 50)
    log("中文搜索系统工具扫描开始")
    log("=" * 50)

    all_findings = []

    # 1. 核心渠道健康检查
    health_ok = True
    if not check_searxng_health():
        all_findings.append("⚠️ SearXNG 异常，请检查容器")
        health_ok = False

    if not check_owdaemon():
        all_findings.append("⚠️ open-webSearch daemon 异常")
        health_ok = False

    if not check_tavily():
        all_findings.append("⚠️ Tavily 异常，请检查 API Key")
        health_ok = False

    # 2. 百度引擎检查
    baidu_check = check_searxng_baidu()
    if baidu_check.get("ok"):
        all_findings.append(f"✅ 百度引擎已恢复（可替换必应）: {baidu_check['msg']}")

    # 3. ClawHub skill 扫描
    clawhub_findings = scan_clawhub()
    if clawhub_findings:
        all_findings.append("ClawHub 高分 skill:\n" + "\n".join(clawhub_findings))

    # 4. GitHub 扫描
    github_findings = scan_github()
    if github_findings:
        all_findings.append("GitHub 潜在相关项目:\n" + "\n".join(github_findings[:5]))

    # 5. 汇总报告
    log("=" * 50)
    if all_findings:
        log("📋 发现以下需要关注的事项:")
        for f in all_findings:
            log(f"  {f}")
        report = "# 工具扫描报告\n"
        report += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        for f in all_findings:
            report += f"- {f}\n"
        write_update(report)
        log("已写入 memory/tool-updates.md")
    else:
        log("✅ 无重大发现，系统状态正常")

    log("扫描完成")
    return all_findings

if __name__ == "__main__":
    findings = main()
    sys.exit(0 if not findings else 1)
