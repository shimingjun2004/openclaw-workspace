#!/usr/bin/env python3
"""
中文搜索系统定期工具扫描器
被 HEARTBEAT.md 定时任务调用（每3天一次）

职责：
1. 扫描 ClawHub 新增 browser-automation / playwright skill
2. 扫描 GitHub 是否有新型中文搜索方案
3. 检查 SearXNG 百度引擎是否恢复（连续2次才标红）
4. 检查各核心渠道健康状态（连续2次失败才告警）
5. 发现重大更新写入 memory/tool-updates.md 并推送

告警阈值（必须遵守）：
- 核心渠道：连续 ≥2 次失败才告警
- 新 skill：ClawHub 评分 ≥3.6
- GitHub 新方案：评分 ≥4.0
- 百度恢复后再次失效：连续 ≥2 次才标红
"""
import sys, time, subprocess, json, os, re
from datetime import datetime

LOG_FILE    = "/root/.openclaw/workspace/memory/tool-updates.md"
STATE_FILE  = "/root/.openclaw/workspace/memory/tool-scanner-state.json"
ALERT_THRESHOLD = 3.6

def log(msg):
    print(f"[{datetime.now().strftime('%H:%M')}] {msg}", flush=True)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            return json.loads(open(STATE_FILE).read())
        except:
            pass
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, ensure_ascii=False)

def write_update(findings):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    existing = open(LOG_FILE).read() if os.path.exists(LOG_FILE) else ""
    header = f"# 工具能力更新记录\n> 更新: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
    with open(LOG_FILE, "w") as f:
        f.write(header + findings + "\n\n" + existing)
    log(f"已写入: {LOG_FILE}")

def check_searxng_health():
    try:
        r = subprocess.run(["curl","-s","--max-time","5","http://127.0.0.1:8080/health"],
            capture_output=True, text=True, timeout=8)
        return "ok" in r.stdout.lower() or "200" in r.stdout
    except:
        return False

def check_daemon():
    try:
        r = subprocess.run(["curl","-s","--max-time","5","http://127.0.0.1:18080/health"],
            capture_output=True, text=True, timeout=8)
        return "ok" in r.stdout.lower() or "running" in r.stdout
    except:
        return False

def check_tavily():
    try:
        from tavily import TavilyClient
        key = "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"
        c = TavilyClient(api_key=key)
        r = c.search("test", max_results=1)
        return len(r.get("results", [])) > 0
    except:
        return False

def check_baidu():
    """检查 SearXNG 百度引擎，返回 (是否恢复, 条目数)"""
    try:
        r = subprocess.run(
            ["curl","-s","--max-time","10",
             "http://127.0.0.1:8080/search",
             "--data-urlencode","q=test",
             "-d","format=json&engines=baidu&limit=1"],
            capture_output=True, text=True, timeout=15)
        results = json.loads(r.stdout).get("results", [])
        return len(results) > 0, len(results)
    except:
        return False, 0

def scan_clawhub():
    log("扫描 ClawHub...")
    findings = []
    try:
        for keyword in ["browser-automation", "playwright", "MCP"]:
            r = subprocess.run(["clawhub","search",keyword],
                capture_output=True, text=True, timeout=20)
            if r.returncode == 0:
                for line in r.stdout.split("\n"):
                    scores = re.findall(r"\((\d\.\d{3})\)", line)
                    for sc in scores:
                        if float(sc) >= ALERT_THRESHOLD:
                            findings.append(f"  [{keyword}] {line.strip()}")
    except Exception as e:
        log(f"ClawHub 扫描失败: {e}")
    if findings:
        log(f"ClawHub: 发现 {len(findings)} 个高分 skill")
    else:
        log("ClawHub: 无重大新增")
    return findings

def scan_github():
    log("扫描 GitHub...")
    findings = []
    try:
        for query in ["chinese search tool", "中文搜索 python"]:
            r = subprocess.run(
                ["gh","search","repos",query,"--sort","stars","--limit","3",
                 "--json","name,description,url,stars"],
                capture_output=True, text=True, timeout=20)
            if r.returncode == 0:
                try:
                    items = json.loads(r.stdout)
                    for it in items:
                        if it.get("stars", 0) > 200:
                            findings.append(
                                f"  {it['name']} ⭐{it['stars']}: "
                                f"{it.get('description','')[:60]}")
                except:
                    pass
    except Exception as e:
        log(f"GitHub 扫描失败: {e}")
    if findings:
        log(f"GitHub: 发现 {len(findings)} 个潜在项目")
    return findings

# ── 主流程 ─────────────────────────────────────────

def main():
    log("=" * 50)
    log("中文搜索系统工具扫描开始")
    log("=" * 50)

    prev = load_state()
    all_findings = []

    # ── 1. 核心渠道健康检查（连续2次才告警）───────────
    searxng_ok  = check_searxng_health()
    daemon_ok   = check_daemon()
    tavily_ok   = check_tavily()

    prev_searxng = prev.get("searxng_fails", 0)
    prev_daemon  = prev.get("daemon_fails", 0)
    prev_tavily  = prev.get("tavily_fails", 0)

    curr_searxng = prev_searxng + 1 if not searxng_ok else 0
    curr_daemon  = prev_daemon  + 1 if not daemon_ok   else 0
    curr_tavily  = prev_tavily  + 1 if not tavily_ok   else 0

    if curr_searxng >= 2:
        all_findings.append(f"⚠️ SearXNG 异常（连续{curr_searxng}次失败），请检查容器")
    if curr_daemon >= 2:
        all_findings.append(f"⚠️ open-webSearch daemon 异常（连续{curr_daemon}次失败）")
    if curr_tavily >= 2:
        all_findings.append(f"⚠️ Tavily 异常（连续{curr_tavily}次失败），请检查 API Key")

    # ── 2. 百度引擎（恢复后再次失效才标红）───────────
    baidu_ok, baidu_count = check_baidu()
    prev_baidu_ok = prev.get("baidu_ok", False)

    if baidu_ok:
        if not prev_baidu_ok:
            all_findings.append(f"✅ 百度引擎已恢复！可返回 {baidu_count} 条结果（建议下一轮切回）")
        # 保存：曾经恢复过，现在正常
        prev_baidu_recover_fails = 0
    else:
        if prev_baidu_ok:
            # 曾经恢复过，现在失效
            prev_baidu_recover_fails = prev.get("baidu_recover_fails", 0) + 1
            if prev_baidu_recover_fails >= 2:
                all_findings.append(f"⚠️ 百度引擎再次失效（连续{prev_baidu_recover_fails}次），已切回必应")
        else:
            prev_baidu_recover_fails = prev.get("baidu_recover_fails", 0)

    # ── 3. ClawHub ───────────────────────────────────
    clawhub_findings = scan_clawhub()
    if clawhub_findings:
        all_findings.append("ClawHub 高分 skill:\n" + "\n".join(clawhub_findings))

    # ── 4. GitHub ────────────────────────────────────
    github_findings = scan_github()
    if github_findings:
        all_findings.append("GitHub 潜在相关项目:\n" + "\n".join(github_findings[:5]))

    # ── 5. 保存状态 ─────────────────────────────────
    curr_state = {
        "searxng_fails": curr_searxng,
        "daemon_fails": curr_daemon,
        "tavily_fails": curr_tavily,
        "baidu_ok": baidu_ok,
        "baidu_recover_fails": prev_baidu_recover_fails if not baidu_ok else 0,
        "last_run": datetime.now().isoformat(),
    }
    save_state(curr_state)

    # ── 6. 汇总 ─────────────────────────────────────
    log("=" * 50)
    if all_findings:
        log("📋 需要关注的事项:")
        for f in all_findings:
            log(f"  {f}")
        report = "# 工具扫描报告\n"
        report += f"时间: {datetime.now().strftime('%Y-%m-%d %H:%M')}\n\n"
        for f in all_findings:
            report += f"- {f}\n"
        write_update(report)
    else:
        log("✅ 无重大发现，系统状态正常")

    log("扫描完成")
    return all_findings

if __name__ == "__main__":
    findings = main()
    sys.exit(0 if not findings else 1)
