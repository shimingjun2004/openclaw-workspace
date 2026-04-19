#!/usr/bin/env python3
"""
中文深度搜索工具 - 两层架构
├─ 发现层（List）：快速发现入口，不抓正文
└─ 正文层（Fetch）：按需抓取，独立调用

分级路由：
  Tier-1（一级）：百度、360搜索、微博热搜、B站热门
                 → 轻量、快速，永不阻断
  Tier-2（二级）：Tavily、B站视频搜索、搜狗微信列表
                 → Tier-1 结果不足时补入
  Tier-3（三级）：GitHub CLI、browser、open-webSearch fetch
                 → 需显式指定 --deep 时启用

缓存策略：
  微博热搜：90 秒（变动频繁）
  B站热门：90 秒
  普通搜索：15 分钟
  技术/GitHub：60 分钟

用法：
  python3 cn_search.py AI大模型              # 默认5条/源，分级搜索
  python3 cn_search.py AI大模型 --deep      # 开启 Tier-3
  python3 cn_search.py AI大模型 3           # 每源3条（轻量发现）
  python3 cn_search.py AI大模型 3 --deep    # 每源3条 + Tier-3
  python3 cn_search.py --weibo 10           # 只看微博热搜
  python3 cn_search.py --hot                # 全网热点（微博+B站）

新增模块：
  wechat_fetch.py <url>          # 单篇微信正文读取
  zhihu_fetch.py <url>            # 单篇知乎正文读取（按需）
"""
import sys, time, hashlib, threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from concurrent.futures.thread import ThreadPoolExecutor as TPE
import requests, re, json

# ═══════════════════════════════════════════════════════
# 基础配置
# ═══════════════════════════════════════════════════════
SEARXNG_BASE  = "http://127.0.0.1:8080"
TAVILY_KEY    = "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"
TIMEOUT       = 12           # 单请求超时（秒）
DEFAULT_LIMIT = 5            # 统一默认条数

# ═══════════════════════════════════════════════════════
# 缓存层
# ═══════════════════════════════════════════════════════
class SearchStats:
    """可观测性统计（Priority 4）"""
    def __init__(self):
        self._lock = threading.Lock()
        self.reset()

    def reset(self):
        self.channel_times   = {}   # channel → (count, total_ms)
        self.channel_success = {}   # channel → success_count
        self.cache_hits     = 0
        self.cache_misses   = 0
        self.tier2_triggered = 0
        self.tier2_skipped  = 0
        self.noise_filtered = 0
        self.total_results  = 0

    def record_channel(self, channel, elapsed_ms, success):
        with self._lock:
            cnt, tot = self.channel_times.get(channel, (0, 0.0))
            self.channel_times[channel] = (cnt+1, tot+elapsed_ms)
            if success:
                self.channel_success[channel] = self.channel_success.get(channel, 0) + 1

    def record_cache(self, hit):
        with self._lock:
            if hit: self.cache_hits += 1
            else:   self.cache_misses += 1

    def record_tier2(self, triggered):
        with self._lock:
            if triggered: self.tier2_triggered += 1
            else:         self.tier2_skipped += 1

    def record_noise(self, count):
        with self._lock:
            self.noise_filtered += count

    def record_results(self, count):
        with self._lock:
            self.total_results = count

    def report(self):
        lines = []
        with self._lock:
            lines.append("  📊 质量报告")
            if self.channel_times:
                lines.append("  ── 渠道响应 ──")
                for ch, (cnt, tot) in sorted(self.channel_times.items()):
                    avg = tot/cnt if cnt else 0
                    ok  = self.channel_success.get(ch, 0)
                    pct = int(ok/cnt*100) if cnt else 0
                    lines.append(f"    {ch:<8} {cnt}次 | 均{avg:.1f}ms | 成功率{pct}%")
            cache_total = self.cache_hits + self.cache_misses
            if cache_total:
                hit_pct = int(self.cache_hits/cache_total*100)
                lines.append(f"  ── 缓存 ──  {self.cache_hits}命中 / {cache_total}次 = {hit_pct}%")
            lines.append(f"  ── Tier-2 ── 触发{self.tier2_triggered}次 / 跳过{self.tier2_skipped}次")
            if self.noise_filtered:
                lines.append(f"  ── 噪音过滤 ── 共挡{self.noise_filtered}条")
        return "\n".join(lines)


_STATS = SearchStats()


class SearchCache:
    """简单内存缓存，TTL 支持"""
    def __init__(self):
        self._lock  = threading.Lock()
        self._store = {}        # key → (expire_ts, value)

    def _key(self, fn_name, *args):
        """生成缓存键"""
        raw = f"{fn_name}:{':'.join(str(a) for a in args)}"
        return hashlib.md5(raw.encode()).hexdigest()

    def get(self, fn_name, *args):
        key = self._key(fn_name, *args)
        with self._lock:
            if key not in self._store:
                return None
            expire_ts, value = self._store[key]
            if time.time() > expire_ts:
                del self._store[key]
                return None
            return value

    def set(self, fn_name, *args, ttl=900, value=None):
        key = self._key(fn_name, *args)
        with self._lock:
            self._store[key] = (time.time() + ttl, value)

    def cached(self, fn_name, *args, ttl=900):
        """装饰器用法"""
        def decorator(func):
            def wrapper(*a, **kw):
                v = self.get(fn_name, *a)
                if v is not None:
                    return v
                result = func(*a, **kw)
                self.set(fn_name, *a, ttl=ttl, value=result)
                return result
            return wrapper
        return decorator

_cache = SearchCache()

# ═══════════════════════════════════════════════════════
# 工具函数
# ═══════════════════════════════════════════════════════
def _ua():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

def safe_get(url, headers=None, params=None, timeout=TIMEOUT):
    try:
        r = requests.get(url, headers=headers or {}, params=params, timeout=timeout)
        return r
    except Exception:
        return None

def clean_title(raw):
    if not raw:
        return ''
    t = re.sub(r'<[^>]+>', '', raw)
    t = re.sub(r'[\s]+', ' ', t).strip()
    return t[:120]

def _fmt_desc(content, maxlen=80):
    if not content:
        return ''
    return clean_title(content)[:maxlen]

# ═══════════════════════════════════════════════════════
# 渠道函数（发现层）
# ═══════════════════════════════════════════════════════

# ── Tier-1 ─────────────────────────────────────────


def search_sogou(query, limit=5, _cache_hit=False):
    """
    搜狗搜索，直接调，不走 SearXNG。
    SearXNG 的 Bing 引擎对中文查询漂移严重，搜狗返回高度相关结果（~500ms）。
    用 BeautifulSoup 解析，确保结果干净。
    """
    if _cache_hit:
        return _cache.get('sogou', query, limit) or []
    try:
        url = f"https://www.sogou.com/web?query={requests.utils.quote(query)}&num={limit}"
        r = safe_get(url, headers={**_ua(), 'Accept': 'text/html'}, timeout=12)
        if not r:
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        items = []
        for h3 in soup.find_all('h3'):
            a_tag = h3.find('a', href=True)
            if not a_tag:
                continue
            title = a_tag.get_text(strip=True)
            href = a_tag['href']
            if not title or len(title) < 5:
                continue
            if not href or len(title) < 5:
                continue
            # 搜狗相对链接 /link?url=... 也是有效链接，保留
            if not href.startswith('http') and not href.startswith('/link'):
                continue
            items.append({
                "channel": "搜狗",
                "title": clean_title(title),
                "url": href,
                "desc": ""
            })
        _cache.set('sogou', query, ttl=900, value=items[:limit])
        return items[:limit]
    except Exception:
        return []

def search_baidu(query, limit=5, _cache_hit=False):
    """必应（替换已损坏的百度引擎），中文内容良好，TTL=15分钟"""
    if _cache_hit:
        return _cache.get('baidu', query, limit) or []
    try:
        r = safe_get(f"{SEARXNG_BASE}/search",
            params={"q": query, "format": "json", "engines": "bing", "limit": limit,
                    "language": "zh-CN"})
        if not r or r.status_code != 200:
            return []
        out = [{"channel": "必应",
                "title": clean_title(x.get('title', '')),
                "url":   x.get('url', ''),
                "desc":  _fmt_desc(x.get('content', ''))}
               for x in r.json().get('results', [])[:limit]]
        _cache.set('baidu', query, limit, ttl=900, value=out)
        return out
    except Exception:
        return []

def search_360(query, limit=5, _cache_hit=False):
    """360搜索（SearXNG），TTL=15分钟"""
    if _cache_hit:
        return _cache.get('360', query, limit) or []
    try:
        r = safe_get(f"{SEARXNG_BASE}/search",
            params={"q": query, "format": "json", "engines": "360search", "limit": limit})
        if not r or r.status_code != 200:
            return []
        out = [{"channel": "360搜索",
                "title": clean_title(x.get('title', '')),
                "url":   x.get('url', ''),
                "desc":  _fmt_desc(x.get('content', ''))}
               for x in r.json().get('results', [])[:limit]]
        _cache.set('360', query, limit, ttl=900, value=out)
        return out
    except Exception:
        return []

def search_weibo_hot(limit=10, _cache_hit=False, query=""):
    """
    微博实时热搜，TTL=90秒（变动频繁）。
    query 非空时按关键词过滤（jieba分词），避免普通搜索时全量噪音。
    """
    if _cache_hit:
        return _cache.get('weibo_hot', limit) or []
    try:
        r = safe_get(
            'https://weibo.com/ajax/side/hotSearch',
            headers={**_ua(),
                     'Referer': 'https://weibo.com/',
                     'Accept': 'application/json, text/plain, */*',
                     'X-Requested-With': 'XMLHttpRequest'},
            timeout=15)
        if not r:
            return []
        items = r.json().get('data', {}).get('realtime', [])[:limit]
        # query 过滤：简单字符包含匹配（不用 jieba，避免导入失败）
        if query:
            # 取 query 前4个字作为关键词（简单有效）
            q_keywords = [c for c in query if '一' <= c <= '鿿'][:4]
            if q_keywords:
                filtered = [x for x in items
                            if any(kw in x.get('word','') for kw in q_keywords)]
                if filtered:
                    items = filtered
        out = [{"channel": "微博热搜",
                "title": x.get('word', ''),
                "url":   f"https://s.weibo.com/weibo?q={requests.utils.quote(x['word'])}",
                "desc":  f"🔥 {x.get('num', 0):,}"}
               for x in items[:limit]]
        _cache.set('weibo_hot', limit, ttl=90, value=out)
        return out
    except Exception:
        return []

def search_bilibili_hot(limit=10, _cache_hit=False, query=""):
    """
    B站热门，TTL=90秒。
    若传了 query 参数，按关键词过滤（jieba 分词）。
    """
    if _cache_hit:
        return _cache.get('bilibili_hot', limit) or []
    try:
        r = safe_get(
            'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all',
            headers={**_ua(), 'Accept': 'application/json'}, timeout=12)
        if not r:
            return []
        items = r.json().get('data', {}).get('list', [])[:limit]
        out = [{"channel": "B站热门",
                "title": x.get('title', '').strip(),
                "url":   f"https://www.bilibili.com/video/{x.get('bvid','')}",
                "desc":  f"👤 {x.get('owner',{}).get('name','?')} | 👍 {x.get('stat',{}).get('like',0):,}"}
               for x in items]
        _cache.set('bilibili_hot', limit, ttl=90, value=out)
        return out
    except Exception:
        return []

# ── Tier-2 ─────────────────────────────────────────

def search_tavily(query, limit=5, _cache_hit=False):
    """Tavily 结构化搜索，TTL=15分钟"""
    if _cache_hit:
        return _cache.get('tavily', query, limit) or []
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_KEY)
        raw = client.search(query=query, max_results=limit)
        out = [{"channel": "Tavily",
                "title": x.get('title', ''),
                "url":   x.get('url', ''),
                "desc":  _fmt_desc(x.get('content', ''), 100)}
               for x in raw.get('results', [])[:limit]]
        _cache.set('tavily', query, limit, ttl=900, value=out)
        return out
    except Exception:
        return []

def search_bilibili_video(query, limit=5, _cache_hit=False):
    """B站视频搜索，TTL=15分钟"""
    if _cache_hit:
        return _cache.get('bilibili_video', query, limit) or []
    try:
        r = safe_get(
            "https://api.bilibili.com/x/web-interface/search/type",
            params={"search_type": "video", "keyword": query, "page": 1, "page_size": limit},
            headers={**_ua(), 'Accept': 'application/json'})
        if not r:
            return []
        items = r.json().get('data', {}).get('result', [])
        out = [{"channel": "B站视频",
                "title": re.sub(r'<[^>]+>', '', x.get('title', '')),
                "url":   f"https://www.bilibili.com/video/{x.get('bvid','')}",
                "desc":  f"UP: {x.get('author','')} | 👀{x.get('play',0)} 👍{x.get('like',0)}"}
               for x in items[:limit]]
        _cache.set('bilibili_video', query, limit, ttl=900, value=out)
        return out
    except Exception:
        return []

def search_wechat(query, limit=5, _cache_hit=False):
    """搜狗微信列表，TTL=15分钟（只返回列表，不抓正文）"""
    if _cache_hit:
        return _cache.get('wechat', query, limit) or []
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        return []
    try:
        r = safe_get(
            f"https://weixin.sogou.com/weixin?type=2&query={requests.utils.quote(query)}&ie=utf8",
            headers=_ua(), timeout=15)
        if not r or r.status_code != 200:
            return []
        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.select('li[id^="sogou_vr_"]')
        out = []
        for item in items[:limit]:
            h3 = item.find('h3')
            title = h3.get_text(strip=True) if h3 else ''
            acct  = item.find('span', class_='all-time-y2')
            summ  = item.find('p', class_='txt-info')
            if not title:
                continue
            out.append({
                "channel": "微信公众号",
                "title":  title,
                "url":    "https://weixin.sogou.com/",     # 列表页，正文需 wechat_fetch.py
                "desc":   f"📣{acct.get_text(strip=True) if acct else ''} | {summ.get_text(strip=True)[:50] if summ else ''}",
            })
        _cache.set('wechat', query, limit, ttl=900, value=out)
        return out
    except Exception:
        return []

# ── Tier-3 ─────────────────────────────────────────

def search_github(query, limit=5):
    """GitHub 仓库搜索，TTL=60分钟（单独命令，不走 HTTP）"""
    try:
        import subprocess, json as _json
        raw = subprocess.check_output(
            ['gh', 'search', 'repos', query,
             '--sort', 'stars', '--limit', str(limit),
             '--json', 'name,description,url'],
            stderr=subprocess.DEVNULL, timeout=15
        )
        items = _json.loads(raw)
        return [{"channel": "GitHub",
                 "title": it.get('name', ''),
                 "url":   it.get('url', ''),
                 "desc":  _fmt_desc(it.get('description', ''))}
                for it in items]
    except Exception:
        return []

# ═══════════════════════════════════════════════════════
# 两段式搜索
# ═══════════════════════════════════════════════════════


def _auto_scale(query, ranked, mode, all_results):
    """
    按需扩容：去重后发现覆盖不足，智能增加返回条数。

    触发条件（任意一个）：
      1. 去重后总条数 < 8
      2. 有效来源渠道数 < 3
      3. broad 意图（比较/对比/方案/调研/趋势/推荐）
      4. 前5条标题相似度 > 50%

    扩容策略：
      normal:  追加 Tavily 3条（不再受 limit 限制）
      deep:     追加 Tavily 4条 + 触发 GitHub
    """
    intents = _detect_query_intent(query)
    broad_intents = {'compare', 'explain', 'news'}
    is_broad = bool(intents and any(i in broad_intents for i in intents))

    # 简单相似度检测：前5条中，含相同关键词对数超过50%即视为重复
    titles = [item['title'].lower() for item in ranked[:5]]
    similar_pairs = 0
    for i, t1 in enumerate(titles):
        kw1 = set(c for c in t1 if '\u4e00' <= c <= '\u9fff')
        for t2 in titles[i+1:]:
            kw2 = set(c for c in t2 if '\u4e00' <= c <= '\u9fff')
            if kw1 and kw2:
                overlap = len(kw1 & kw2) / min(len(kw1), len(kw2))
                if overlap > 0.5:
                    similar_pairs += 1

    active_sources = sum(1 for ch, items in all_results.items() if items)
    trigger_reasons = []
    if len(ranked) < 8:
        trigger_reasons.append(f"结果少({len(ranked)}条)")
    if active_sources < 3:
        trigger_reasons.append(f"来源少({active_sources}个)")
    if is_broad:
        trigger_reasons.append("broad意图")
    if similar_pairs > len(titles) * 0.4:
        trigger_reasons.append("标题相似")

    if not trigger_reasons:
        return ranked

    print(f"  [扩容] 触发原因: {'; '.join(trigger_reasons)}")

    scaled = list(ranked)
    added = 0

    # normal: 追加 Tavily 结果（不走 limit 限制）
    if mode in ("normal", "fast"):
        tavily_items = all_results.get("Tavily", [])
        existing_urls = {item["url"] for item in ranked}
        for item in tavily_items:
            if item["url"] not in existing_urls and added < 3:
                scaled.append(item)
                added += 1

    # deep: 追加更多 Tavily + 保留 GitHub（已在 r3 里，这里做补充）
    elif mode == "deep":
        tavily_items = all_results.get("Tavily", [])
        existing_urls = {item["url"] for item in ranked}
        for item in tavily_items:
            if item["url"] not in existing_urls and added < 4:
                scaled.append(item)
                added += 1

    if added:
        print(f"  [扩容] 已追加 {added} 条，结果从 {len(ranked)} → {len(scaled)} 条")

    return scaled


def deduplicate_and_rank(all_results):
    """
    第二段：去重 + 重排
    - 同标题去重（标题相似度简单判断）
    - 按 channel 权重打分
    - 返回 Top-N（默认10条）
    """
    seen_titles = set()
    scored = []

    # 渠道权重（质量可信度）
    WEIGHT = {
        'Tavily':      1.2,   # 结构化摘要，质量高
        'GitHub':      1.1,   # 技术精准
        'B站视频':      1.0,   # 技术教程价值高
        'B站热门':      0.85,  # 娱乐为主
        '知乎':         1.15,  # 内容深度高
        '微信公众号':    1.0,   # 质量差异大
        '微博热搜':      0.6,  # 娱乐/时效，轻量参考
        '必应':         0.9,   # 综合，中文可用
        '360搜索':      0.8,   # 综合
    }

    for channel, items in all_results.items():
        w = WEIGHT.get(channel, 0.8)
        for item in items:
            title = item['title'].lower()
            # 简单去重：标题前30字符相同就视为重复
            short = re.sub(r'[^\w\u4e00-\u9fff]', '', title)[:30]
            if short in seen_titles:
                continue
            seen_titles.add(short)
            scored.append((w, item))

    # 权重排序，同权重按标题字顺序
    scored.sort(key=lambda x: (-x[0], x[1]['title']))
    ranked = [item for _, item in scored]

    # ── 按需扩容：去重后结果过少时，智能增加渠道条数 ──────────────
    # 触发条件（任意一个）：
    #   1. 去重后总条数 < 8
    #   2. 来源渠道数 < 3
    #   3. 查询意图偏 broad（比较/对比/方案/调研/趋势/推荐）
    #   4. 前5条标题相似度超过50%（被过滤掉的有价值条目）
    ranked = _auto_scale(query, ranked, mode, all_results)

    return ranked

def fetch_content(results, limit=6):
    """
    正文读取层（第二段）
    对 Top-N 结果调用 open-webSearch fetch-web
    当前仅做信息输出，不阻塞主流程
    """
    targets = results[:limit]
    fetched = []

    def _fetch_one(item):
        url = item.get('url', '')
        title = item.get('title', '')
        if not url or url.startswith('https://weixin.sogou.com/'):
            return None   # 搜狗微信列表页不抓，留给 wechat_fetch.py
        try:
            import subprocess
            raw = subprocess.check_output(
                ['curl', '-s', '--max-time', '15',
                 '-X', 'POST', 'http://127.0.0.1:18080/fetch-web',
                 '-H', 'Content-Type: application/json',
                 '-d', json.dumps({"url": url, "maxChars": 2000, "readability": True})],
                stderr=subprocess.DEVNULL, timeout=20
            )
            d = json.loads(raw)
            content = d.get('data', {}).get('content', '')
            return {"title": title, "url": url, "content": content[:500], "channel": item.get('channel', '')}
        except Exception:
            return None

    with ThreadPoolExecutor(max_workers=3) as ex:
        futures = [ex.submit(_fetch_one, r) for r in targets]
        for f in as_completed(futures, timeout=25):
            try:
                r = f.result()
                if r:
                    fetched.append(r)
            except Exception:
                pass

    return fetched

# ═══════════════════════════════════════════════════════
# 主搜索编排
# ═══════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════
# Priority 3：4 种模式定义
# ═══════════════════════════════════════════════════════════════════════════

MODES = {
    "hot": {
        "limit":      10,
        "tier2":      False,
        "tier3":      False,
        "desc":       "🌡 热点追踪（微博+B站，不走主流程）",
    },
    "fast": {
        "limit":      3,
        "tier2":      False,
        "tier3":      False,
        "desc":       "⚡ 快速发现（Tier-1 单轮，轻量）",
    },
    "normal": {
        "limit":      5,
        "tier2":      None,   # None = 智能判断
        "tier3":      False,
        "desc":       "🌐 默认搜索（Tier-1 + 智能Tier-2）",
    },
    "deep": {
        "limit":      8,
        "tier2":      True,   # 强制触发
        "tier3":      True,
        "desc":       "🔎 深度调研（全链路 + GitHub）",
    },
}

def detect_mode(query, explicit_mode):
    """
    检测模式：优先用用户显式指定，否则从查询词推断
    """
    if explicit_mode:
        return explicit_mode, MODES.get(explicit_mode, MODES["normal"])

    q = query.lower()
    # 热点词 → hot
    # 深度词 → deep（优先，防止被热点词覆盖）
    deep_kw = ['分析', '对比', '横评', '评测', '哪个好', '为什么', '原理', '入门',
               '最新动态', '最新消息', '最新发布']
    if any(k in q for k in deep_kw):
        return "deep", MODES["deep"]

    # 热点词 → hot（次优先）
    hot_kw = ['热搜', '热点', '今日', '突发']
    if any(k in q for k in hot_kw):
        return "hot", MODES["hot"]

    # 简单词 → fast
    short_kw = ['是什么', '啥', '有没有', '好不好']
    if any(k in q for k in short_kw) or len(q) <= 4:
        return "fast", MODES["fast"]

    return "normal", MODES["normal"]


def tier1_search(query, limit):
    """Tier-1：轻量快速，永远先跑"""
    funcs = [
        # 微博/B站热搜已移出 Tier-1（只代表"平台热点"，和 topical 查询几乎不相关）
        # topical 搜索专注 Tavily（中文+英文高质量），Tier-2 补微信公众号+B站视频
        ("Tavily", lambda: _timed_search("Tavily", search_tavily, query, limit)),
    ]
    return _run_parallel(funcs, timeout=25)

def _timed_search(channel, fn, *args, **kwargs):
    """包装搜索函数，记录耗时和成功率"""
    t0 = time.time()
    try:
        result = fn(*args, **kwargs)
        elapsed = (time.time() - t0) * 1000
        _STATS.record_channel(channel, elapsed, len(result) > 0)
        return result
    except Exception:
        elapsed = (time.time() - t0) * 1000
        _STATS.record_channel(channel, elapsed, False)
        return []



def tier2_search(query, limit):
    """Tier-2：补充层，按需补入"""
    funcs = [
        # Tavily 已在Tier-1，这里不再重复
        ("B站视频",      lambda: _timed_search("B站视频",      search_bilibili_video, query, limit)),
        ("微信公众号",   lambda: _timed_search("微信公众号",   search_wechat,       query, limit)),
    ]
    return _run_parallel(funcs, timeout=30)

def tier3_search(query, limit):
    """Tier-3：仅 --deep 时启用"""
    t0 = time.time()
    try:
        result = {"GitHub": search_github(query, limit)}
        elapsed = (time.time() - t0) * 1000
        _STATS.record_channel("GitHub", elapsed, True)
        return result
    except Exception:
        _STATS.record_channel("GitHub", 0, False)
        return {"GitHub": []}



# ═══════════════════════════════════════════════════════════════════════════
# 360 搜索噪音过滤器（Priority 2）
# ═══════════════════════════════════════════════════════════════════════════

# 常见误伤词黑名单（出现则视为噪音）
NOISE_BLACKLIST = [
    'aida', '艾达', '营销模型', '注意力模型',   # AIDA 营销模型
    '销售模型', '消费者行为', '购买决策',
    '广告模型', '品牌模型', '营销漏斗',
]

# 高权重关键词（命中这些说明查询偏技术/深度，360 结果质量通常差）
TECH_KEYWORDS = [
    'ai', 'llm', 'gpt', '大模型', '模型', '算法', '训练',
    '开源', 'benchmark', '评测', '推理', '微调', 'rag',
    'agent', 'copilot', 'code', '编程', '开发',
]

def is_noisy_title(title, query):
    """判断 360 结果标题是否为噪音"""
    t = title.lower()
    q = query.lower()

    # 1. 黑名单命中
    for word in NOISE_BLACKLIST:
        if word.lower() in t:
            return True

    # 2. 标题含查询词太少（覆盖率 < 30%）
    q_chars = [c for c in q if c.isalnum()]
    if q_chars:
        hit = sum(1 for c in q_chars if c in t)
        if hit / len(q_chars) < 0.3:
            return True

    return False

def filter_360_noise(results, query):
    """对 360 结果做轻量噪音过滤，返回干净结果"""
    original = len(results)
    clean = [r for r in results if not is_noisy_title(r['title'], query)]
    removed = original - len(clean)
    return clean, removed


# ═══════════════════════════════════════════════════════════════════════════
# Tier-2 智能触发判断（Priority 1）
# ═══════════════════════════════════════════════════════════════════════════

def _title_similarity(t1, t2):
    """简单字符级相似度（共同字符比例）"""
    s1 = set(re.sub(r'[^\w\u4e00-\u9fff]', '', t1.lower()))
    s2 = set(re.sub(r'[^\w\u4e00-\u9fff]', '', t2.lower()))
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)

def _detect_query_intent(query):
    """识别查询意图类型"""
    q = query.lower()
    intents = []
    # learn 优先（防止被 tech 覆盖）
    if any(k in q for k in ['教程','入门','学习','上手','指南','什么是','哪几种','有哪些','是什么']):
        intents.append('learn')
    # compare / explain / news
    if any(k in q for k in ['分析','对比','横评','评测','测评','哪个好','哪个强']):
        intents.append('compare')
    if any(k in q for k in ['原理','怎么做到','如何实现','为什么']):
        intents.append('explain')
    if any(k in q for k in ['最新','新发布','新模型','最新动态','最新消息','动态','新闻']):
        intents.append('news')
    return intents

def should_trigger_tier2(r1_results, query, limit):
    """
    判断是否触发 Tier-2
    条件：数量 + 质量 联合判断
    """
    all_items = []
    for items in r1_results.values():
        all_items.extend(items)

    if not all_items:
        return True, "Tier-1 结果为空"

    tier1_count = len(all_items)
    tier1_sources = sum(1 for v in r1_results.values() if v)

    # ── 条件1：数量不足 ─────────────────────────
    if tier1_count < limit * 1.5:
        return True, f"数量不足({tier1_count}<{limit*1.5})"

    if tier1_sources < 3:
        return True, f"来源不足({tier1_sources}<3)"

    # ── 条件2：来源过于集中 ───────────────────
    source_dist = {}
    for items in r1_results.values():
        for item in items:
            ch = item.get('channel', 'unknown')
            source_dist[ch] = source_dist.get(ch, 0) + 1

    max_source_pct = max(source_dist.values()) / tier1_count if tier1_count else 1
    if max_source_pct > 0.65:
        dominant = max(source_dist, key=source_dist.get)
        return True, f"来源过于集中({dominant}占{int(max_source_pct*100)}%)"

    # ── 条件3：标题重复率过高 ─────────────────
    titles = [r['title'] for r in all_items[:6]]
    if len(titles) >= 3:
        pairs = [(titles[i], titles[j])
                 for i in range(len(titles))
                 for j in range(i+1, len(titles))]
        high_sim = sum(1 for a, b in pairs if _title_similarity(a, b) > 0.55)
        if high_sim / len(pairs) > 0.4:
            return True, f"标题重复率高({int(high_sim/len(pairs)*100)}%相似对)"

    # ── 条件4：弱相关检测（360噪音标题） ──────
    noisy_360 = sum(1 for r in all_items
                   if r.get('channel') == '360搜索'
                   and is_noisy_title(r['title'], query))
    if noisy_360 / max(tier1_count, 1) > 0.3:
        return True, f"360噪音过多({noisy_360}条弱相关)"

    # ── 条件5：缺少高可信来源 ─────────────────
    high_quality_channels = {'必应', 'Tavily', 'GitHub'}
    has_hq = any(r.get('channel') in high_quality_channels for r in all_items)
    if not has_hq and tier1_count < limit * 2:
        return True, "缺少高可信来源且数量偏少"

    # ── 条件6：查询意图要求深度 ────────────────
    intents = _detect_query_intent(query)
    deep_intents = {'compare', 'explain', 'learn', 'news'}
    if intents and any(i in deep_intents for i in intents):
        matched = set(intents) & deep_intents
        return True, f"查询意图偏深度({','.join(matched)})"

    return False, "Tier-1 结果质量合格"




def _run_parallel(funcs, timeout=30):
    """独立线程执行，超时不影响其他渠道"""
    results = {}
    with ThreadPoolExecutor(max_workers=len(funcs)) as ex:
        futs = {ex.submit(f): name for name, f in funcs}
        for f in as_completed(futs, timeout=timeout):
            name = futs[f]
            try:
                results[name] = f.result()
            except Exception:
                results[name] = []
    return results

def deep_search(query, mode="normal", do_fetch=False):
    """
    统一入口
      query       : 搜索词
      mode        : hot | fast | normal | deep
      do_fetch    : 是否对 Top 结果抓正文（第二段）
    """
    mode_cfg = MODES.get(mode, MODES["normal"])
    limit    = mode_cfg["limit"]
    tier2Cfg = mode_cfg["tier2"]   # None=智能判断, True=强制, False=禁用
    tier3Cfg = mode_cfg["tier3"]
    tier2_force = tier2Cfg if tier2Cfg is not None else None

    _STATS.reset()
    _STATS.record_tier2(tier2_force is True)  # 记录为"未触发（待智能判断）"

    desc = mode_cfg["desc"]
    print(f"\n{desc}")
    print(f"  模式: {mode} | 每源: {limit}条 | 查询:「{query}」")
    print("=" * 58)
    print(f"\n🌐 搜索：「{query}」 × {limit}条/源 [{mode}]")
    print("=" * 58)

    # ── 第一段：发现层 ────────────────────────────
    t0 = time.time()
    all_results = {}

    # Tier-1 必须跑
    t1 = time.time()
    r1 = tier1_search(query, limit)
    all_results.update(r1)

    # 对 360 结果做噪音过滤（Priority 2）
    removed_noise = 0
    if '360搜索' in r1 and r1['360搜索']:
        clean, removed = filter_360_noise(r1['360搜索'], query)
        r1['360搜索'] = clean
        all_results['360搜索'] = clean
        removed_noise = removed

    print(f"  [Tier-1] {len(r1)}个渠道，用时{time.time()-t1:.1f}秒" +
          (f"（过滤360噪音{removed_noise}条）" if removed_noise else ""))

    # Tier-2 判断：mode强制 > 智能判断
    if tier2_force is True:
        t2 = time.time()
        r2 = tier2_search(query, limit)
        all_results.update(r2)
        print(f"  [Tier-2] {len(r2)}个渠道，用时{time.time()-t2:.1f}秒（mode=deep 强制开启）")
    elif tier2_force is False:
        print(f"  [Tier-2] 跳过（mode=fast，禁用Tier-2）")
    else:
        # None = 智能判断
        trigger, reason = should_trigger_tier2(r1, query, limit)
        if trigger:
            t2 = time.time()
            r2 = tier2_search(query, limit)
            all_results.update(r2)
            print(f"  [Tier-2] {len(r2)}个渠道，用时{time.time()-t2:.1f}秒（{reason}）")
            _STATS.record_tier2(True)
        else:
            print(f"  [Tier-2] 跳过（{reason}）")
            _STATS.record_tier2(False)

    if tier3Cfg:
        t3 = time.time()
        r3 = tier3_search(query, limit)
        all_results.update(r3)
        print(f"  [Tier-3] {len(r3)}个渠道，用时{time.time()-t3:.1f}秒")

    print(f"\n⏱  发现层总耗时: {time.time()-t0:.1f}秒")

    # ── 去重 + 重排 ──────────────────────────────
    ranked = deduplicate_and_rank(all_results)
    total_discovered = len(ranked)
    print(f"📋 去重后共 {total_discovered} 条（已按质量权重排序）")

    # ── 分渠道输出 ──────────────────────────────
    print(f"\n{'─'*58}")
    for name, items in all_results.items():
        if not items:
            continue
        print(f"📌 【{name}】({len(items)}条)")
        for i, r in enumerate(items, 1):
            print(f"  {i:2d}. {r['title'][:50]}")
            if r.get('desc'):
                print(f"      └ {r['desc'][:65]}")

    # ── 第二段：正文读取（可选）──────────────────
    fetch_results = []
    if do_fetch and ranked:
        print(f"\n{'─'*58}")
        print(f"📥 正文读取层（Top {min(6, len(ranked))} 条）...")
        t_f = time.time()
        fetch_results = fetch_content(ranked, limit=6)
        print(f"⏱  正文层耗时: {time.time()-t_f:.1f}秒")
        for fr in fetch_results:
            print(f"\n  ▶ {fr['title'][:50]}")
            if fr.get('content'):
                print(f"    {fr['content'][:200]}...")

    print(f"\n{'='*58}")
    print(f"✅ 完成！发现 {total_discovered} 条 / 正文 {len(fetch_results)} 篇")
    print(_STATS.report())
    return {"discovered": ranked, "fetched": fetch_results}

# ═══════════════════════════════════════════════════════
# 快捷模式
# ═══════════════════════════════════════════════════════

def hot_search(limit=10):
    """全网热点：微博热搜 + B站热门"""
    print(f"\n🌡 全网热点监控（微博 + B站）")
    print("=" * 50)
    funcs = [
        ("微博热搜", lambda: search_weibo_hot(limit)),
        ("B站热门",  lambda: search_bilibili_hot(limit)),
    ]
    results = _run_parallel(funcs, timeout=20)
    for name, items in results.items():
        if not items:
            continue
        print(f"\n📌 【{name}】({len(items)}条)")
        for i, r in enumerate(items, 1):
            print(f"  {i:2d}. {r['title'][:50]}")
            if r.get('desc'):
                print(f"      └ {r['desc'][:65]}")
    return results

# ═══════════════════════════════════════════════════════
# 入口
# ═══════════════════════════════════════════════════════

if __name__ == '__main__':
    if '--help' in sys.argv:
        print(__doc__)
        sys.exit(0)

    # 快捷模式
    if '--hot' in sys.argv:
        hot_search(limit=10)
        sys.exit(0)

    # 解析显式模式
    explicit_mode = None
    for m in ('--fast', '--deep', '--normal'):
        if m in sys.argv:
            explicit_mode = m.replace('--', '')
            break

    query = sys.argv[1] if len(sys.argv) > 1 else 'AI大模型'
    fetch = '--fetch' in sys.argv

    # 推断模式
    mode, cfg = detect_mode(query, explicit_mode)

    deep_search(query, mode=mode, do_fetch=fetch)