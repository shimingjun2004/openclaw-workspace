#!/usr/bin/env python3
"""
知乎文章按需抓取工具

功能：
  - 搜索知乎专栏文章（通过 Tavily site:zhuanlan.zhihu.com）
  - 直接读取知乎文章（摘要级，正文需浏览器）
  - 不作为常驻搜索源，仅按需触发

用法：
  python3 zhihu_fetch.py <关键词>        # 搜索知乎（默认5篇）
  python3 zhihu_fetch.py <关键词> -n 8   # 搜索8篇
  python3 zhihu_fetch.py <url>          # 直接读单篇（摘要级）
  python3 zhihu_fetch.py --help        # 帮助

定位：
  此工具不参与 cn_search.py 主流程并发，
  作为独立按需工具，需要时单独调用。
"""
import sys, requests, re, json

TAVILY_KEY = "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"

def search_zhihu(query, limit=5):
    """
    通过 Tavily deep search 搜索知乎文章
    返回结构化摘要列表
    """
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_KEY)
        raw = client.search(
            query=f"{query} site:zhuanlan.zhihu.com",
            max_results=limit,
            include_answer=True,
        )
        results = raw.get('results', [])
        answer  = raw.get('answer', '')
        out = []
        for x in results:
            url = x.get('url', '')
            if 'zhuanlan.zhihu.com' not in url:
                continue
            match = re.search(r'/p/(\w+)', url)
            out.append({
                'title':   x.get('title', ''),
                'url':     url,
                'score':   x.get('score', 0),
                'content': x.get('content', '')[:500],
                'id':      match.group(1) if match else '',
                'source':  '知乎专栏',
            })
        return {'articles': out, 'answer': answer}
    except Exception as e:
        return {'articles': [], 'answer': '', 'error': str(e)}

def fetch_zhihu_article(url):
    """通过 Tavily 获取单篇文章摘要"""
    try:
        from tavily import TavilyClient
        client = TavilyClient(api_key=TAVILY_KEY)
        raw = client.search(query=url, max_results=1, include_answer=True)
        results = raw.get('results', [])
        if results:
            r = results[0]
            return {
                'title':   r.get('title', ''),
                'url':     r.get('url', url),
                'content': r.get('content', '')[:1000],
                'answer':  raw.get('answer', ''),
                'source':  '知乎 × Tavily',
            }
        return {'error': '未找到内容'}
    except Exception as e:
        return {'error': str(e)}

def print_results(data, limit=5):
    articles = data.get('articles', [])[:limit]
    answer   = data.get('answer', '')
    if 'error' in data:
        print(f"  ⚠️  {data['error']}")
        return
    print(f"\n🔍 知乎文章：共 {len(articles)} 篇")
    if answer:
        print(f"\n💡 AI 摘要:\n  {answer[:300]}")
    print(f"\n{'─'*55}")
    for i, a in enumerate(articles, 1):
        print(f"\n  📄 {i}. {a['title']}")
        print(f"     评分: {a.get('score', 0):.2f}")
        print(f"     链接: {a['url']}")
        c = a.get('content', '')
        if c:
            print(f"     摘要: {c[:200]}...")
    print(f"\n{'='*55}")
    print(f"✅ {len(articles)} 篇 | 💡 AI摘要: {'有' if answer else '无'}")

# ── 入口 ──────────────────────────────────────────

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    if len(sys.argv) < 2:
        print("用法:")
        print("  python3 zhihu_fetch.py <关键词>        # 搜索知乎")
        print("  python3 zhihu_fetch.py <关键词> -n 8  # 搜索8篇")
        print("  python3 zhihu_fetch.py <url>         # 读单篇")
        sys.exit(1)

    arg = sys.argv[1]
    is_url = arg.startswith('http://') or arg.startswith('https://')

    # 解析 -n 参数
    raw_args = sys.argv[1:]
    clean_args, skip_next, limit = [], False, 5
    for a in raw_args:
        if skip_next:
            skip_next = False
            continue
        if a == '-n':
            skip_next = True
            continue
        clean_args.append(a)
    n_match = re.search(r'-n\s+(\d+)', ' '.join(sys.argv))
    if n_match:
        limit = int(n_match.group(1))

    if is_url:
        print(f"\n📖 读取知乎文章...\n{'='*55}")
        info = fetch_zhihu_article(arg)
        if 'error' in info:
            print(f"  ⚠️  {info['error']}")
        else:
            print(f"  标题: {info.get('title','无')}")
            print(f"  链接: {info.get('url','无')}")
            if info.get('content'):
                print(f"\n  📝 内容摘要:\n  {info['content'][:400]}")
            if info.get('answer'):
                print(f"\n  💡 AI 回答:\n  {info['answer'][:200]}")
    else:
        query = ' '.join(clean_args)
        print(f"\n🔍 搜索知乎专栏：「{query}」")
        print("=" * 55)
        data = search_zhihu(query, limit)
        print_results(data, limit)
