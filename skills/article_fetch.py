#!/usr/bin/env python3
"""
微信公众号 & 知乎文章正文读取器（Phase 3 - Playwright版）

功能：
  - 微信公众号文章：完整正文提取（JS渲染）
  - 知乎专栏文章：完整正文 + AI摘要
  - 其他网页：可读性正文提取

依赖：
  npm install -g playwright  (已安装)
  npx playwright install chromium  (已安装)

用法：
  python3 article_fetch.py <url>                  # 读单篇
  python3 article_fetch.py <url> --verbose        # 详细输出
  python3 article_fetch.py <url1> <url2>          # 批量读取

Node.js 引擎路径：/usr/lib/node_modules/playwright
"""
import sys, time, json, subprocess, os, re

PLAYWRIGHT_JS = """
const { chromium } = require('/usr/lib/node_modules/playwright');

async function fetchPage(url, timeout) {
  const browser = await chromium.launch({
    headless: true,
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
  });

  const context = await browser.newContext({
    userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    viewport: { width: 1280, height: 800 }
  });

  const page = await context.newPage();

  // 拦截知乎/微信的反爬
  await page.addInitScript(() => {
    Object.defineProperty(navigator, 'webdriver', { get: () => false });
  });

  const result = { url, title: '', author: '', content: '', pub_time: '', description: '', error: '' };

  try {
    await page.goto(url, { timeout: timeout * 1000, waitUntil: 'domcontentloaded' });
    await page.waitForTimeout(4000);
    // 不等 networkidle，知乎持续请求，只等固定时间

    // 提取标题
    result.title = await page.title();

    // 微信公众号正文
    try {
      result.content = await page.innerText('#js_content');
    } catch(e) {}

    // 知乎正文
    if (!result.content) {
      try {
        result.content = await page.innerText('.RichText');
      } catch(e) {}
    }

    // 知乎作者
    try {
      result.author = await page.innerText('.AuthorInfo-name');
    } catch(e) {}

    // 微信公众号作者
    if (!result.author) {
      try {
        result.author = await page.innerText('#js_name');
      } catch(e) {}
    }

    // 时间
    try {
      const timeEl = await page.$('time');
      if (timeEl) {
        result.pub_time = (await timeEl.getAttribute('datetime')) || (await timeEl.innerText());
      }
    } catch(e) {}

    if (!result.pub_time) {
      try {
        const timeEl = await page.$('#publish_time');
        if (timeEl) result.pub_time = await timeEl.innerText();
      } catch(e) {}
    }

    // OG描述
    if (!result.content && !result.description) {
      try {
        const metaDesc = await page.$('meta[name="description"]');
        if (metaDesc) result.description = await metaDesc.getAttribute('content') || '';
      } catch(e) {}
    }

    result.content = (result.content || '').replace(/\s+/g, ' ').trim();

  } catch(e) {
    result.error = e.message;
  } finally {
    await browser.close();
  }

  return result;
}

const url = process.argv[2];
const timeout = parseInt(process.argv[3] || '20');
fetchPage(url, timeout).then(r => {
  console.log(JSON.stringify(r, null, 2));
}).catch(e => {
  console.error(JSON.stringify({error: e.message}));
  process.exit(1);
});
"""

def fetch_article(url, timeout=20, verbose=False):
    """用 Node.js Playwright 抓取文章"""
    if verbose:
        print(f"  🌐 正在渲染: {url[:60]}", flush=True)

    t0 = time.time()
    try:
        result = subprocess.run(
            ['node', '-e', PLAYWRIGHT_JS, '', url, str(timeout)],
            capture_output=True, text=True, timeout=timeout + 10
        )
        if result.returncode != 0:
            return {'error': result.stderr.strip()[:200], 'url': url}

        data = json.loads(result.stdout)
        elapsed = time.time() - t0
        data['elapsed'] = round(elapsed, 1)
        data['url'] = url

        if verbose:
            if 'error' in data and data['error']:
                print(f"  ❌ {data['error'][:80]}")
            else:
                clen = len(data.get('content', ''))
                title = data.get('title', '')[:50]
                print(f"  ✅ {elapsed:.1f}秒 | {clen}字 | {title}")

        return data

    except subprocess.TimeoutExpired:
        return {'error': f'超时({timeout}秒)', 'url': url}
    except Exception as e:
        return {'error': str(e), 'url': url}

def print_article(info):
    """格式化输出"""
    if 'error' in info and info['error'] and not info.get('content'):
        print(f"  ❌ {info['error']}")
        return

    title  = info.get('title', '无标题')
    author = info.get('author', '')
    pub_time = info.get('pub_time', '')
    content = info.get('content', '')
    desc = info.get('description', '')
    url = info.get('url', '')
    elapsed = info.get('elapsed', '?')

    print(f"\n{'='*58}")
    print(f"  📰 {title}")
    if author:
        print(f"  👤 {author}")
    if pub_time:
        print(f"  🕐 {pub_time}")
    print(f"  🔗 {url}")
    print(f"  ⏱  {elapsed}秒")
    print(f"{'─'*58}")
    if content:
        print(f"  {content[:600]}...")
    elif desc:
        print(f"  摘要: {desc[:200]}")
    else:
        print("  （无正文）")

# ── 入口 ──────────────────────────────────────────

if __name__ == '__main__':
    verbose = '--verbose' in sys.argv or '-v' in sys.argv
    urls = [a for a in sys.argv[1:] if not a.startswith('-')]

    if not urls:
        print(__doc__)
        sys.exit(1)

    print(f"\n📥 Playwright 抓取 {len(urls)} 篇（渲染模式）...")
    print("=" * 58)

    for i, url in enumerate(urls, 1):
        if len(urls) > 1:
            print(f"\n[{i}/{len(urls)}]")
        result = fetch_article(url.strip(), verbose=verbose)
        print_article(result)

    print(f"\n{'='*58}")
    print(f"✅ 完成，共 {len(urls)} 篇")
