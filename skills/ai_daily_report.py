#!/usr/bin/env python3
"""
AI 日报生成器
每天 9:00 自动执行，搜索当天AI动态，按趋势简报模板保存
"""
import sys
import os
from datetime import datetime

# 添加 skills 路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tavily import TavilyClient

CLIENT = TavilyClient(api_key='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')
TODAY = datetime.now().strftime('%Y-%m-%d')
REPORT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'research', 'ai-trends')
REPORT_PATH = os.path.join(REPORT_DIR, f'{TODAY}-AI日报.md')

# 搜索词组合，确保覆盖新内容
QUERIES = [
    'AI大模型 最新进展 2026',
    'OpenAI Anthropic Google AI 新动态',
    'AI Agent RAG 搜索 最新消息',
    '人工智能 中国 AI 新突破',
]

def search(query, max_results=5):
    try:
        r = CLIENT.search(query, max_results=max_results)
        return r.get('results', [])
    except Exception as e:
        print(f'搜索失败 [{query[:20]}]: {e}', file=sys.stderr)
        return []

def main():
    print(f'🔍 AI日报生成 | {TODAY}')

    # 1. 搜索
    all_items = []
    for q in QUERIES:
        results = search(q, max_results=5)
        for r in results:
            r['_query'] = q
        all_items.extend(results)
        print(f'  [{q[:25]}] → {len(results)}条')

    # 2. 去重（按URL）
    seen_urls = set()
    unique = []
    for item in all_items:
        url = item.get('url', '')
        if url and url not in seen_urls:
            seen_urls.add(url)
            unique.append(item)

    # 3. 生成报告
    # 按来源分组
    news_items = [x for x in unique if 'news' in x.get('url','').lower() or '新闻' in x.get('title','') or '最新' in x.get('title','')]
    tech_items = [x for x in unique if x not in news_items]

    lines = [
        f'# AI日报 | {TODAY}',
        '',
        f'> 自动生成 | smj-小秘 | 来源：{len(unique)}条有效结果',
        '',
        '---',
        '',
        '## 本期重点',
        '',
        '（请根据以下内容填写本期最重要的一件事）',
        '',
        '---',
        '',
        '## AI 大模型动态',
        '',
    ]
    for i, item in enumerate(news_items[:5], 1):
        title = item.get('title','')
        url = item.get('url','')
        content = item.get('content','')[:150]
        lines.append(f'{i}. **{title}**')
        if content:
            lines.append(f'   > {content}...')
        lines.append(f'   > 来源：{url}')
        lines.append('')

    lines.extend([
        '## 技术/产品动态',
        '',
    ])
    for i, item in enumerate(tech_items[:5], 1):
        title = item.get('title','')
        url = item.get('url','')
        content = item.get('content','')[:120]
        lines.append(f'{i}. **{title}**')
        if content:
            lines.append(f'   > {content}...')
        lines.append(f'   > 来源：{url}')
        lines.append('')

    lines.extend([
        '## 值得关注',
        '',
        '（记录值得深入了解的方向）',
        '',
        '## 对我的影响',
        '',
        '（结合老史的工作方向：企业AI研发、建筑AI）',
        '',
        '## 是否需要跟进',
        '',
        '- [ ] 需要深入调研',
        '- [ ] 下周关注',
        '- [ ] 暂不需要行动',
        '',
        '---',
        f'*本报告由 smj-小秘 自动生成 | {TODAY} 09:00*',
    ])

    content = '\n'.join(lines)

    # 4. 保存
    os.makedirs(REPORT_DIR, exist_ok=True)
    with open(REPORT_PATH, 'w', encoding='utf-8') as f:
        f.write(content)

    print(f'\n✅ 已保存：{REPORT_PATH}')
    print(f'   共 {len(unique)} 条来源')
    return REPORT_PATH

if __name__ == '__main__':
    main()
