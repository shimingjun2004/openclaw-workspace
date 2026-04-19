#!/usr/bin/env python3
"""
微信公众号文章正文读取器

功能：单篇微信公众号文章读取
  - 元数据提取（标题/作者/摘要/封面图）
  - Open Graph / Twitter Card 解析
  - 文章正文需要浏览器渲染，暂提供 Sogou 摘要补充

用法：
  python3 wechat_fetch.py <url>              # 读取单篇
  python3 wechat_fetch.py --sogou <关键词>   # 搜索 + 取第一篇元数据
  python3 wechat_fetch.py --sogou <关键词> -n 3  # 取前3篇

注意：
  微信公众号正文被微信官方 JS 渲染保护，
  直接 HTTP 请求只能获取元数据，正文需要 Playwright 浏览器方案。
"""
import sys, time, requests, re, json
from bs4 import BeautifulSoup

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Referer': 'https://weixin.sogou.com/',
}

def fetch_from_sogou(url):
    """通过 Sogou 代理获取文章元数据（部分情况可拿到摘要片段）"""
    try:
        r = requests.get(url, headers=HEADERS, timeout=15, allow_redirects=True)
        final_url = r.url
        soup = BeautifulSoup(r.text, 'html.parser')

        # 提取 OG 元数据
        og = {
            'title':       soup.find('meta', property='og:title'),
            'description': soup.find('meta', property='og:description'),
            'image':       soup.find('meta', property='og:image'),
            'site_name':   soup.find('meta', property='og:site_name'),
        }
        title = og['title']['content'] if og['title'] else ''
        desc  = og['description']['content'] if og['description'] else ''
        img   = og['image']['content'] if og['image'] else ''

        # 提取微博文章数据（如果有）
        wb_data = soup.find('meta', {'name': 'description'})
        if not desc and wb_data:
            desc = wb_data.get('content', '')

        # 提取发布时间
        time_match = re.search(r'(\d{4}年\d{1,2}月\d{1,2}日)', r.text)
        pub_time = time_match.group(1) if time_match else ''

        return {
            'title':     title or '（无标题）',
            'desc':      desc[:300] if desc else '（无摘要）',
            'image':     img,
            'url':       final_url,
            'source':    'Sogou 代理',
            'pub_time':  pub_time,
        }
    except Exception as e:
        return {'error': str(e)}

def sogou_search(query, limit=5):
    """搜索微信文章，返回文章元数据列表"""
    try:
        r = requests.get(
            f'https://weixin.sogou.com/weixin?type=2&query={requests.utils.quote(query)}&ie=utf8',
            headers=HEADERS, timeout=15)
        if r.status_code != 200:
            return []

        soup = BeautifulSoup(r.text, 'html.parser')
        items = soup.select('li[id^="sogou_vr_"]')
        results = []

        for item in items[:limit]:
            h3 = item.find('h3')
            title = h3.get_text(strip=True) if h3 else ''

            # 摘要
            summ = item.find('p', class_='txt-info')
            summary = summ.get_text(strip=True)[:120] if summ else ''

            # 来源账号
            acct = item.find('span', class_='all-time-y2')
            account = acct.get_text(strip=True) if acct else ''

            # 封面图
            img_tag = item.select_one('img[data-src]')
            cover = ''
            if img_tag:
                src = img_tag.get('data-src', '') or img_tag.get('src', '')
                # 解码 sogou 缩略图 URL 中的真实 URL
                m = re.search(r'url=(https?[^&]+)', src)
                if m:
                    import urllib.parse
                    cover = urllib.parse.unquote(m.group(1))

            # 热度/时间（无直接时间，用标签代替）
            date_tag = item.find('span', class_='s2')
            date_str = date_tag.get_text(strip=True) if date_tag else ''

            # 文章链接（Sogou 代理 URL）
            link_tag = item.select_one('h3 a')
            link = 'https://weixin.sogou.com/' + link_tag.get('href', '') if link_tag else ''

            results.append({
                'title':   title,
                'account': account,
                'summary': summary,
                'cover':   cover,
                'date':    date_str,
                'link':    link,
            })
        return results
    except Exception as e:
        return [{'error': str(e)}]

def fetch_direct(url):
    """直接抓取 mp.weixin.qq.com，尝试提取预渲染内容"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Accept': 'text/html,application/xhtml+xml',
        }
        r = requests.get(url, headers=headers, timeout=12)
        text = r.text

        # 提取预渲染数据
        title = re.search(r'<h1[^>]*class="rich_media_title"[^>]*>(.*?)</h1>', text, re.DOTALL)
        title = re.sub(r'<[^>]+>', '', title.group(1)).strip() if title else ''

        author = re.search(r'<span[^>]*class="rich_media_meta rich_media_meta_link rich_media_meta_nickname"[^>]*>(.*?)</span>', text, re.DOTALL)
        author = re.sub(r'<[^>]+>', '', author.group(1)).strip() if author else ''

        content = re.search(r'<div[^>]*id="js_content"[^>]*>(.*?)</div>', text, re.DOTALL)
        if content:
            plain = re.sub(r'<[^>]+>', '', content.group(1))
            plain = re.sub(r'\s+', ' ', plain).strip()
        else:
            plain = ''

        return {
            'title':   title or '（无标题）',
            'author':  author or '（无作者）',
            'content': plain[:1000] if plain else '（正文需浏览器渲染）',
            'url':     url,
            'source':  'mp.weixin.qq.com 直接抓取',
        }
    except Exception as e:
        return {'error': str(e)}

def print_article(info):
    if 'error' in info:
        print(f"  ⚠️ {info['error']}")
        return
    print(f"  标题: {info.get('title','无')}")
    if info.get('account'):
        print(f"  来源: {info['account']}")
    if info.get('author'):
        print(f"  作者: {info['author']}")
    if info.get('pub_time'):
        print(f"  时间: {info['pub_time']}")
    if info.get('date'):
        print(f"  日期: {info['date']}")
    if info.get('desc') and '（无' not in info['desc']:
        print(f"  摘要: {info['desc'][:200]}")
    if info.get('content') and '（无' not in info['content']:
        print(f"  正文（节选）: {info['content'][:300]}")
    if info.get('url'):
        print(f"  链接: {info['url']}")

# ── 入口 ──────────────────────────────────────────

if __name__ == '__main__':
    if '--help' in sys.argv or '-h' in sys.argv:
        print(__doc__)
        sys.exit(0)

    if '--sogou' in sys.argv or '-s' in sys.argv:
        # 搜索模式
        idx = sys.argv.index('--sogou') if '--sogou' in sys.argv else sys.argv.index('-s')
        query = ' '.join(sys.argv[idx+1:])
        # 去掉 -n 数字参数
        query = re.sub(r'-n\s+\d+', '', query).strip()
        if not query:
            print("用法: python3 wechat_fetch.py --sogou <关键词>")
            sys.exit(1)

        n_match = re.search(r'-n\s+(\d+)', ' '.join(sys.argv))
        limit = int(n_match.group(1)) if n_match else 3

        print(f"\n🔍 搜索微信文章：「{query}」（取{limit}篇）")
        print("=" * 55)
        results = sogou_search(query, limit)
        if not results or all('error' in r for r in results):
            print("  ⚠️ 搜索失败，请重试")
        else:
            for i, r in enumerate(results, 1):
                print(f"\n📄 第{i}篇:")
                print_article(r)
        sys.exit(0)

    # 单篇读取模式
    if len(sys.argv) < 2:
        print("用法: python3 wechat_fetch.py <url>")
        print("   或: python3 wechat_fetch.py --sogou <关键词>")
        sys.exit(1)

    url = sys.argv[1]

    print(f"\n📄 读取微信公众号文章...")
    print("=" * 55)

    if 'sogou.com' in url:
        info = fetch_from_sogou(url)
    elif 'mp.weixin.qq.com' in url:
        info = fetch_direct(url)
        if '（正文需浏览器渲染）' in info.get('content', ''):
            print(f"  ⚠️ 正文需浏览器渲染，尝试 Sogou 代理...")
            sogou_info = fetch_from_sogou(url)
            if sogou_info.get('desc'):
                info['desc'] = sogou_info.get('desc', '')
    else:
        print("  ⚠️ 仅支持 mp.weixin.qq.com 和 weixin.sogou.com 链接")
        sys.exit(1)

    print_article(info)
