#!/usr/bin/env python3
"""中文热搜监控工具 - 微博实时热搜 + B站热门 + 微信公众号文章"""
import re, requests

def weibo_hot(limit=10):
    """微博实时热搜榜"""
    try:
        r = requests.get(
            'https://weibo.com/ajax/side/hotSearch',
            headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Referer': 'https://weibo.com/',
                'Accept': 'application/json, text/plain, */*',
                'X-Requested-With': 'XMLHttpRequest'
            }, timeout=15
        )
        d = r.json().get('data', {}).get('realtime', [])
        print(f"📊 微博实时热搜 ({len(d)}条)")
        print("-" * 50)
        for i, x in enumerate(d[:limit]):
            num = x.get('num', 0)
            print(f"  {i+1:2d}. {x['word']}")
            print(f"      🔥 {num:,}  | https://s.weibo.com/weibo?q={requests.utils.quote(x['word'])}")
        return d
    except Exception as e:
        print(f"❌ 微博失败: {e}")
        return []

def bilibili_hot(limit=10):
    """B站热门视频榜"""
    try:
        r = requests.get(
            'https://api.bilibili.com/x/web-interface/ranking/v2?rid=0&type=all',
            headers={'User-Agent': 'Mozilla/5.0', 'Accept': 'application/json'}, timeout=12
        )
        d = r.json().get('data', {}).get('list', [])
        print(f"\n📊 B站热门视频 ({len(d)}条)")
        print("-" * 50)
        for i, x in enumerate(d[:limit]):
            title = x.get('title', '').strip()
            up = x.get('owner', {}).get('name', '未知')
            likes = x.get('stat', {}).get('like', 0)
            print(f"  {i+1:2d}. {title[:45]}")
            print(f"      👤 {up}  | 👍 {likes:,}")
        return d
    except Exception as e:
        print(f"❌ B站失败: {e}")
        return []

def wechat_articles(keyword, limit=10):
    """搜狗微信搜索公众号文章
    
    数据来源: https://weixin.sogou.com/
    无需登录，直接返回微信公众号文章列表
    """
    try:
        from bs4 import BeautifulSoup
    except ImportError:
        print("❌ 需要 BeautifulSoup: pip install beautifulsoup4")
        return []

    url = f'https://weixin.sogou.com/weixin?type=2&query={requests.utils.quote(keyword)}&ie=utf8&s_from=input'
    r = requests.get(
        url,
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
        }, timeout=15
    )

    soup = BeautifulSoup(r.text, 'html.parser')
    items = soup.select('li[id^="sogou_vr_"]')
    print(f"\n📰 微信公众号文章: 「{keyword}」({len(items)}条)")
    print("-" * 50)

    results = []
    for i, item in enumerate(items[:limit]):
        # 标题
        h3 = item.find('h3')
        title = h3.get_text(strip=True) if h3 else ''
        # 公众号名
        acct = item.find('span', class_='all-time-y2')
        account = acct.get_text(strip=True) if acct else ''
        # 摘要
        summary_el = item.find('p', class_='txt-info')
        summary = summary_el.get_text(strip=True)[:80] if summary_el else ''
        # 日期
        date_el = item.find('span', class_='s2')
        date = re.sub(r'<[^>]+>', '', str(date_el)).strip() if date_el else ''
        # 文章链接（搜狗重定向）
        link = item.find('h3').find('a')['href'] if h3 and h3.find('a') else ''

        print(f"  {i+1:2d}. {title[:45]}")
        if account:
            print(f"      📣 {account}")
        if summary:
            print(f"      💬 {summary[:60]}")
        print(f"      🔗 {link[:80] if link else '无直达链接'}")

        results.append({'title': title, 'account': account, 'summary': summary})

    return results

def main():
    import sys
    limit = 10
    keyword = 'AI大模型'

    args = sys.argv[1:]
    if '--help' in args:
        print("用法: python3 chinese_hot.py [命令] [参数]")
        print("  默认: 微博+B站各10条热搜")
        print("  python3 chinese_hot.py weibo 10      # 只看微博")
        print("  python3 chinese_hot.py bilibili 10 # 只看B站")
        print("  python3 chinese_hot.py wechat AI 10 # 搜微信公众号文章")
        return

    mode = args[0] if args else 'all'

    print("=" * 50)
    print("🌡️  中文热点监控")
    print("=" * 50)

    if mode in ('all', 'weibo'):
        weibo_hot(limit)
    if mode in ('all', 'bilibili'):
        bilibili_hot(limit)
    if mode == 'wechat':
        kw = args[1] if len(args) > 1 else keyword
        lm = int(args[2]) if len(args) > 2 else limit
        wechat_articles(kw, lm)

    print("\n" + "=" * 50)

if __name__ == '__main__':
    main()