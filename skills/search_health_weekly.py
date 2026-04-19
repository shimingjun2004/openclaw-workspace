#!/usr/bin/env python3
"""
中文搜索系统每周健康检查（静默写入日志）
被 cron 每周六调用，不主动推送，只写文件
"""
import subprocess, json, os, time
from datetime import datetime

LOG = "/root/.openclaw/workspace/memory/search-health-weekly.md"

def timed(func, label):
    t0 = time.time()
    try:
        r = func()
        return r, (time.time()-t0)*1000, None
    except Exception as e:
        return None, 0, str(e)

def check_searxng():
    r = subprocess.run(["curl","-s","--max-time","8","http://127.0.0.1:8080/search",
        "--data-urlencode","q=AI大模型","-d","format=json&engines=bing&limit=3"],
        capture_output=True, text=True, timeout=12)
    d = json.loads(r.stdout)
    return len(d.get("results",[]))

def check_daemon():
    r = subprocess.run(["curl","-s","--max-time","5","http://127.0.0.1:18080/health"],
        capture_output=True, text=True, timeout=8)
    return "ok" in r.stdout.lower()

def check_tavily():
    from tavily import TavilyClient
    c = TavilyClient(api_key="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")
    r = c.search("AI大模型2026", max_results=1)
    return len(r.get("results",[]))

def check_gh():
    r = subprocess.run(["gh","search","repos","AI大模型","--sort","stars","--limit","3"],
        capture_output=True, text=True, timeout=10)
    return r.returncode == 0

channels = [
    ("SearXNG(必应)", check_searxng),
    ("open-webSearch daemon", check_daemon),
    ("Tavily", check_tavily),
    ("GitHub CLI", check_gh),
]

results = []
for name, fn in channels:
    ok, ms, err = timed(fn, name)
    status = "✅" if ok else "❌"
    info = f"{ms:.0f}ms" if ms else (err or "失败")
    results.append(f"| {name} | {status} | {info} |")
    print(f"  {status} {name}: {info}")

# 写入周志
date = datetime.now().strftime("%Y-%m-%d %H:%M")
week = int(datetime.now().strftime("%W"))
existing = open(LOG).read() if os.path.exists(LOG) else "# 中文搜索系统每周健康日志\n\n"

row = f"| {date} (第{week}周) | " + " | ".join([r.split("|")[2].strip() for r in results]) + " |\n"

with open(LOG, "w") as f:
    f.write(existing + row)

print(f"\n已写入: {LOG}")
