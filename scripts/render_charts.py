"""Render research charts as dependency-free SVG (zh/en × light/dark) from checked-in research tables."""
import csv
import json
import math
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/research'
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif"
THEMES = {
    'light': {'text': '#1f2328', 'muted': '#59636e', 'grid': '#e5e7eb', 'axis': '#d0d7de', 'CN': '#c2552d', 'NA': '#3b62b3', 'US': '#3b62b3', 'CA': '#14817c', 'band': '#f3f4f6', 's1': '#3b62b3', 's2': '#14817c', 's3': '#c2552d', 's4': '#8250df'},
    'dark': {'text': '#f0f6fc', 'muted': '#9198a1', 'grid': '#262c36', 'axis': '#3d444d', 'CN': '#f0883e', 'NA': '#4493f8', 'US': '#4493f8', 'CA': '#39c5cf', 'band': '#161b22', 's1': '#4493f8', 's2': '#39c5cf', 's3': '#f0883e', 's4': '#ab7df8'},
}


def t(x, y, s, size, fill, weight=None, anchor=None):
    a = f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"'
    if weight:
        a += f' font-weight="{weight}"'
    if anchor:
        a += f' text-anchor="{anchor}"'
    return f'<text {a}>{escape(str(s))}</text>'


def wrap_svg(w, h, title, desc, body):
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h:.0f}" width="{w}" height="{h:.0f}" role="img" '
            f'aria-labelledby="t d" font-family="{FONT}">')
    return '\n'.join([head, f'<title id="t">{escape(title)}</title>', f'<desc id="d">{escape(desc)}</desc>'] + body + ['</svg>']) + '\n'


def skill_chart(group, lang, theme, terms, rows, meta):
    th, zh = THEMES[theme], lang == 'zh'
    data = {(r['key'], r['market']): r for r in rows if r['sample'] == 'all'}
    keys = [x['key'] for x in terms if x['group'] == group]
    keys.sort(key=lambda k: -max(float(data[(k, 'CN')]['pct']), float(data[(k, 'NA')]['pct'])))
    label = {x['key']: x[lang] for x in terms}
    W, left, right, top = 1000, 300, 70, 96
    plot_w = W - left - right
    row_h = 30
    h = top + row_h * len(keys) + 70
    x = lambda pct: left + plot_w * pct / 100
    body = []
    title = meta['titles'][group][lang]
    body.append(t(24, 34, title, 20, th['text'], weight='700'))
    lx = 24
    for market in ['CN', 'NA']:
        n, e = meta['n'][market], meta['employers'][market]
        name = (f'中国 n={n}（{e} 家雇主）' if market == 'CN' else f'北美 n={n}（{e} 家雇主）') if zh else \
               (f'China n={n} ({e} employers)' if market == 'CN' else f'North America n={n} ({e} employers)')
        body.append(f'<rect x="{lx}" y="50" width="14" height="10" rx="2" fill="{th[market]}"/>')
        body.append(t(lx + 20, 59, name, 13, th['muted']))
        lx += (len(name) * 9 + 60) if zh else (len(name) * 7 + 44)
    body.append(t(W - right, 59, '细线 = 95% 置信区间' if zh else 'whiskers = 95% Wilson interval', 12, th['muted'], anchor='end'))
    for g in range(0, 101, 25):
        gx = x(g)
        body.append(f'<line x1="{gx:.1f}" y1="{top - 8}" x2="{gx:.1f}" y2="{top + row_h * len(keys)}" stroke="{th["grid"]}"/>')
        body.append(t(gx, top + row_h * len(keys) + 18, f'{g}%', 11.5, th['muted'], anchor='middle'))
    for i, k in enumerate(keys):
        y = top + i * row_h
        body.append(t(left - 12, y + 15, label[k], 13.5, th['text'], anchor='end'))
        for j, market in enumerate(['CN', 'NA']):
            r = data[(k, market)]
            pct, lo, hi = float(r['pct']), float(r['ci95_low']), float(r['ci95_high'])
            by = y + 2 + j * 11
            body.append(f'<rect x="{left}" y="{by}" width="{max(plot_w * pct / 100, 1):.1f}" height="9" rx="1.5" fill="{th[market]}"/>')
            body.append(f'<line x1="{x(lo):.1f}" y1="{by + 4.5}" x2="{x(hi):.1f}" y2="{by + 4.5}" stroke="{th["text"]}" stroke-opacity="0.55" stroke-width="1.2"/>')
            body.append(t(x(hi) + 6, by + 8.5, f'{pct:.0f}%', 11, th['muted']))
    foot = meta['foot'][lang]
    body.append(t(24, h - 22, foot, 12, th['muted']))
    desc = ('按技能统计的 JD 提及率，中国与北美对比，含 95% 置信区间。' if zh else 'Share of job descriptions mentioning each skill, China versus North America, with 95% intervals.')
    return wrap_svg(W, h, title, desc, body)


def line_chart(lang, theme, series, quarters, title, ylabel, foot, zero_line=False, partial=True):
    th, zh = THEMES[theme], lang == 'zh'
    W, H, left, right, top, bottom = 1000, 380, 80, 40, 80, 70
    vals = [v for s in series for v in s['values'] if v is not None]
    lo, hi = min(vals + ([0] if zero_line else [])), max(vals)
    step = next(s for s in [1, 2, 2.5, 5, 10, 20, 25, 50, 100, 200, 250, 500, 1000, 2000, 2500, 5000] if (hi - lo) / s <= 6)
    lo, hi = step * math.floor(lo / step - 0.3), step * math.ceil(hi / step + 0.3)
    if min(vals) >= 0 and not zero_line:
        lo = max(lo, 0)
    steps = round((hi - lo) / step)
    pw, ph = W - left - right, H - top - bottom
    x = lambda i: left + pw * (i + 0.5) / len(quarters)
    y = lambda v: top + ph * (hi - v) / (hi - lo)
    body = [t(24, 34, title, 19, th['text'], weight='700')]
    if partial:
        body.append(f'<rect x="{x(len(quarters) - 1) - pw / len(quarters) / 2:.1f}" y="{top}" width="{pw / len(quarters):.1f}" height="{ph}" fill="{th["band"]}"/>')
        body.append(t(x(len(quarters) - 1), top + 16, '部分季度' if zh else 'partial', 11, th['muted'], anchor='middle'))
    for s in range(steps + 1):
        v = lo + (hi - lo) * s / steps
        body.append(f'<line x1="{left}" y1="{y(v):.1f}" x2="{W - right}" y2="{y(v):.1f}" stroke="{th["grid"]}"/>')
        body.append(t(left - 10, y(v) + 4, f'{v:,.0f}', 11.5, th['muted'], anchor='end'))
    if zero_line and lo < 0 < hi:
        body.append(f'<line x1="{left}" y1="{y(0):.1f}" x2="{W - right}" y2="{y(0):.1f}" stroke="{th["axis"]}" stroke-width="1.5"/>')
    for i, q in enumerate(quarters):
        body.append(t(x(i), H - bottom + 22, q, 12, th['muted'], anchor='middle'))
    body.append(f'<text transform="translate(22 {top + ph / 2:.0f}) rotate(-90)" font-size="12" fill="{th["muted"]}" text-anchor="middle">{escape(ylabel)}</text>')
    lx = left
    used = []
    for s in series:
        c = th[s.get('color', s.get('country'))]
        pts = [(x(i), y(v)) for i, v in enumerate(s['values']) if v is not None]
        body.append(f'<polyline points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="none" stroke="{c}" stroke-width="2.4" stroke-linejoin="round"/>')
        body += [f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.6" fill="{c}"/>' for a, b in pts]
        last = pts[-1]
        ly = last[1] + 4
        while any(abs(ly - u) < 13 for u in used):  # keep end labels of close series apart
            ly += 13
        used.append(ly)
        body.append(t(last[0] + 8, ly, f'{s["values"][-1]:,.0f}' if s['values'][-1] >= 100 else f'{s["values"][-1]:.1f}', 11.5, c, weight='600'))
        body.append(f'<rect x="{lx}" y="50" width="14" height="10" rx="2" fill="{c}"/>')
        body.append(t(lx + 20, 59, s['label'], 13, th['muted']))
        lx += max(150, int(len(s['label']) * (13 if zh else 7.4)) + 40)
    body.append(t(24, H - 18, foot, 12, th['muted']))
    return wrap_svg(W, H, title, title, body)


def render_skill_charts():
    terms = json.loads((ROOT / 'research/skill-terms.json').read_text())['terms']
    rows = list(csv.DictReader((ROOT / 'research/skill-distribution.csv').open()))
    jds = json.loads((ROOT / 'research/jds.json').read_text())
    meta = {
        'n': {m: sum(r['market'] == m for r in jds) for m in ['CN', 'NA']},
        'employers': {m: len({r['company'] for r in jds if r['market'] == m}) for m in ['CN', 'NA']},
        'titles': {'tech_stack': {'zh': 'AIE 岗位描述中的技术栈提及率', 'en': 'Tech stack named in AI-engineering job descriptions'},
                   'role_expectations': {'zh': 'AIE 岗位描述中的能力与职责期望', 'en': 'Role expectations in AI-engineering job descriptions'}},
        'foot': {'zh': '统计单位：提到该项的 JD 占比（含必需与加分项）· 中国为人工复核样本；北美含人工复核与规则筛选样本 · 规则见 research/skill-terms.json',
                 'en': 'Share of descriptions mentioning the term (required or preferred) · China: reviewed sample; NA: reviewed + rule-screened · terms in research/skill-terms.json'},
    }
    for group in ['tech_stack', 'role_expectations']:
        for lang in ['zh', 'en']:
            for theme in THEMES:
                (OUT / f'jd-{group.replace("_", "-")}-{lang}-{theme}.svg').write_text(skill_chart(group, lang, theme, terms, rows, meta))


def render_market_charts():
    quarters = [f'{y}Q{q}' for y in [2025, 2026] for q in range(1, 5)]
    indeed = list(csv.DictReader((ROOT / 'research/market/indeed-quarterly.csv').open()))
    def series(rows, metric, field, extra=None):
        out = []
        for country in ['US', 'CA']:
            sub = {r['quarter']: float(r[field]) for r in rows if r['country'] == country and r['metric'] == metric and (extra is None or extra(r))}
            out.append({'country': country, 'values': [sub.get(q) for q in quarters]})
        return out
    names = {'zh': {'US': '美国', 'CA': '加拿大'}, 'en': {'US': 'United States', 'CA': 'Canada'}}
    specs = [
        ('market-software-postings', series(indeed, 'software_postings_index_2020_100', 'value'),
         {'zh': 'Indeed 软件开发岗位广告指数（2020-02-01 = 100）', 'en': 'Indeed Software Development postings index (1 Feb 2020 = 100)'},
         {'zh': '指数', 'en': 'Index'},
         {'zh': '来源：Indeed Hiring Lab job_postings_tracker（CC-BY-4.0）· 日值季度均值 · 2026Q4 截至 11 月 13 日',
          'en': 'Source: Indeed Hiring Lab job_postings_tracker (CC-BY-4.0) · quarterly mean of daily values · 2026Q4 to 13 Nov'}, False),
    ]
    for name, data, title, ylabel, foot, zero in specs:
        for lang in ['zh', 'en']:
            for s in data:
                s['label'] = names[lang][s['country']]
            for theme in THEMES:
                (OUT / f'{name}-{lang}-{theme}.svg').write_text(line_chart(lang, theme, [dict(s) for s in data], quarters, title[lang], ylabel[lang], foot[lang], zero))


def render_skill_tables():
    # Exact shares and intervals behind the charts, kept in sync inside each role overview.
    terms = json.loads((ROOT / 'research/skill-terms.json').read_text())
    rows = {(r['key'], r['market']): r for r in csv.DictReader((ROOT / 'research/skill-distribution.csv').open()) if r['sample'] == 'all'}
    start, end = '<!-- SKILL-TABLE:START -->', '<!-- SKILL-TABLE:END -->'
    for lang in ['zh', 'en']:
        zh = lang == 'zh'
        n_cn, n_na = rows[('python', 'CN')]['n'], rows[('python', 'NA')]['n']
        head = (f'| 类别 | 技能或期望 | 中国 n={n_cn} | 北美 n={n_na} | 北美雇主等权 |' if zh else
                f'| Group | Skill or expectation | China n={n_cn} | North America n={n_na} | NA employer-balanced |')
        lines = ['<details>', '<summary>' + ('展开全部数值与 95% 置信区间' if zh else 'Expand exact shares and 95% intervals') + '</summary>', '', head, '|---|---|---:|---:|---:|']
        for group in ['tech_stack', 'role_expectations']:
            keys = [t['key'] for t in terms['terms'] if t['group'] == group]
            keys.sort(key=lambda k: -max(float(rows[(k, 'CN')]['pct']), float(rows[(k, 'NA')]['pct'])))
            label = {t['key']: t[lang] for t in terms['terms']}
            for k in keys:
                cn, na = rows[(k, 'CN')], rows[(k, 'NA')]
                cell = lambda r: f"{float(r['pct']):.0f}% [{float(r['ci95_low']):.0f}–{float(r['ci95_high']):.0f}]"
                lines.append(f"| {terms['groups'][group][lang]} | {label[k]} | {cell(cn)} | {cell(na)} | {float(na['employer_balanced_pct']):.0f}% |")
        lines += ['', '</details>']
        path = ROOT / f'docs/{lang}/role-overview.md'
        text = path.read_text()
        if start in text:
            text = text.split(start, 1)[0] + start + '\n' + '\n'.join(lines) + '\n' + end + text.split(end, 1)[1]
            path.write_text(text)


def replace_block(path, name, lines):
    start, end = f'<!-- {name}:START -->', f'<!-- {name}:END -->'
    text = path.read_text()
    if start in text:
        path.write_text(text.split(start, 1)[0] + start + '\n' + '\n'.join(lines) + '\n' + end + text.split(end, 1)[1])


def render_enterprise_tables():
    # Capability matrix of enterprise cases and an established-vs-AI-native split of the NA sample.
    cases = json.loads((ROOT / 'research/enterprise-cases.json').read_text())
    caps = cases['capabilities']
    short = {'microsoft': 'Microsoft', 'workday': 'Workday', 'rbc': 'RBC', 'bmo': 'BMO', 'vanguard': 'Vanguard',
             'canada-life': 'Canada Life', 'stripe': 'Stripe', 'databricks': 'Databricks', 'amex': 'AmEx'}
    order = sorted(caps[1:], key=lambda c: (-sum(1 for x in cases['cases'] if x['codes'].get(c['key'])),
                                             -sum(1 for x in cases['cases'] if x['codes'].get(c['key']) == 'R')))
    terms = {t['key']: t for t in json.loads((ROOT / 'research/skill-terms.json').read_text())['terms']}
    jobs = [r for r in json.loads((ROOT / 'research/jds.json').read_text()) if r['market'] == 'NA']
    native = {'ai-native', 'developer-tools'}
    est = [r for r in jobs if r['sector'] not in native]
    nat = [r for r in jobs if r['sector'] in native]
    def share(rows, key):
        k, n = sum(r['features_v2'][key] for r in rows), len(rows)
        p = k / n; d = 1 + 1.96 ** 2 / n; c = (p + 1.96 ** 2 / (2 * n)) / d
        h = 1.96 * math.sqrt(p * (1 - p) / n + 1.96 ** 2 / (4 * n * n)) / d
        return f'{100 * p:.0f}% [{100 * max(0, c - h):.0f}–{100 * min(1, c + h):.0f}]', 100 * p
    diffs = sorted(terms, key=lambda k: share(est, k)[1] - share(nat, k)[1])
    picked = [k for k in diffs[::-1] if share(est, k)[1] - share(nat, k)[1] >= 9][:7] + \
             [k for k in ['evaluation', 'agents', 'production'] if k in terms] + \
             [k for k in diffs if share(nat, k)[1] - share(est, k)[1] >= 9][:5]
    for lang in ['zh', 'en']:
        zh = lang == 'zh'
        head = '| ' + ('能力' if zh else 'Capability') + ' | ' + ' | '.join(short[x['id']] for x in cases['cases']) + ' | ' + ('必需 / 提及' if zh else 'Required / mentioned') + ' |'
        lines = [head, '|---|' + '---|' * len(cases['cases']) + '---:|']
        lines.append(f"| {caps[0][lang]} | " + ' | '.join(x['experience'] if not zh else x['experience'].replace('yrs', '年').replace("Master's graduate (2027)", '2027 届硕士').replace('-', '–') for x in cases['cases']) + ' | — |')
        for c in order:
            marks = [{'R': '✓', 'P': '○'}.get(x['codes'].get(c['key']), '') for x in cases['cases']]
            lines.append(f"| {c[lang]} | " + ' | '.join(marks) + f" | {marks.count('✓')} / {sum(1 for m in marks if m)} |")
        lines += ['', ('✓ = 必需条件或核心职责；○ = 加分项或备选；空白 = 未提及。编码与链接见 [enterprise-cases.json](../../research/enterprise-cases.json)。' if zh else
                       '✓ = requirement or core duty; ○ = preference or alternative; blank = not mentioned. Coding and links are in [enterprise-cases.json](../../research/enterprise-cases.json).')]
        replace_block(ROOT / f'docs/{lang}/role-overview.md', 'ENTERPRISE-MATRIX', lines)
        head2 = (f'| 技能或期望 | 成熟企业 n={len(est)}（{len({r["company"] for r in est})} 家） | AI 原生公司 n={len(nat)}（{len({r["company"] for r in nat})} 家） |' if zh else
                 f'| Skill or expectation | Established employers n={len(est)} ({len({r["company"] for r in est})}) | AI-native companies n={len(nat)} ({len({r["company"] for r in nat})}) |')
        rows = [head2, '|---|---:|---:|'] + [f'| {terms[k][lang]} | {share(est, k)[0]} | {share(nat, k)[0]} |' for k in picked]
        replace_block(ROOT / f'docs/{lang}/role-overview.md', 'EMPLOYER-SPLIT', rows)


def render_canada_vacancies():
    rows = list(csv.DictReader((ROOT / 'research/market/statcan-tech-vacancies.csv').open()))
    quarters = sorted({r['quarter'] for r in rows})
    occ = [('Computer, software and Web designers and developers (2123)', 's1', '软件、计算机与 Web 开发（2123 大组）', 'Software & web devs (2123)'),
           ('Software engineers and designers (21231)', 's2', '软件工程师（21231）', 'Software engineers (21231)'),
           ('Software developers and programmers (21232)', 's3', '软件开发与程序员（21232）', 'Software developers (21232)'),
           ('Data scientists (21211)', 's4', '数据科学家（21211）', 'Data scientists (21211)')]
    for lang in ['zh', 'en']:
        zh = lang == 'zh'
        series = []
        for name, color, lzh, len_ in occ:
            # Points graded D (acceptable) or worse are left out of the chart; the CSV keeps them.
            sub = {r['quarter']: float(r['job_vacancies']) for r in rows if r['occupation'] == name and r['job_vacancies'] and r['quality'] in 'ABC'}
            series.append({'color': color, 'label': lzh if zh else len_, 'values': [sub.get(q) for q in quarters]})
        title = '加拿大科技职业职位空缺（季度，官方统计）' if zh else 'Canadian job vacancies in tech occupations (quarterly, official)'
        foot = ('来源：Statistics Canada 表 14-10-0444-01（职位空缺与工资调查），未季节调整；只画质量等级 A–C 的数据点' if zh else
                'Source: Statistics Canada Table 14-10-0444-01 (Job Vacancy and Wage Survey), unadjusted; only points graded A–C are plotted')
        for theme in THEMES:
            (OUT / f'market-canada-vacancies-{lang}-{theme}.svg').write_text(
                line_chart(lang, theme, series, [q.replace('Q', ' Q') for q in quarters], title, '职位空缺' if zh else 'Vacancies', foot, partial=False))


def render_canada_tables():
    terms = {t['key']: t for t in json.loads((ROOT / 'research/skill-terms.json').read_text())['terms']}
    rows = {(r['key'], r['market']): r for r in csv.DictReader((ROOT / 'research/skill-distribution.csv').open()) if r['sample'] == 'all'}
    cell = lambda r: f"{float(r['pct']):.0f}% [{float(r['ci95_low']):.0f}–{float(r['ci95_high']):.0f}]"
    diff = lambda k: float(rows[(k, 'CA')]['pct']) - float(rows[(k, 'US')]['pct'])
    keys = sorted(terms, key=diff, reverse=True)
    picked = [k for k in keys if diff(k) >= 8] + [k for k in ['evaluation', 'production', 'fine_tuning'] if abs(diff(k)) < 8]
    jobs = json.loads((ROOT / 'research/jds.json').read_text())
    n_emp = len({r['company'] for r in jobs if r['country'] == 'CA'})
    vac = list(csv.DictReader((ROOT / 'research/market/statcan-tech-vacancies.csv').open()))
    quarters = ['2023Q1'] + [q for q in sorted({r['quarter'] for r in vac}) if q >= '2025Q1']
    occ = [('Computer, software and Web designers and developers (2123)', '软件、计算机与 Web 开发（2123 大组）'), ('Software engineers and designers (21231)', '软件工程师（21231）'),
           ('Software developers and programmers (21232)', '软件开发与程序员（21232）'), ('Data scientists (21211)', '数据科学家（21211）'), ('Total, all occupations', '全部职业')]
    for lang in ['zh', 'en']:
        zh = lang == 'zh'
        n_ca, n_us = rows[('python', 'CA')]['n'], rows[('python', 'US')]['n']
        head = (f'| 技能或期望 | 加拿大 n={n_ca}（{n_emp} 家雇主） | 美国 n={n_us} |' if zh else f'| Skill or expectation | Canada n={n_ca} ({n_emp} employers) | United States n={n_us} |')
        lines = [head, '|---|---:|---:|'] + [f"| {terms[k][lang]} | {cell(rows[(k, 'CA')])} | {cell(rows[(k, 'US')])} |" for k in picked]
        replace_block(ROOT / f'docs/{lang}/role-overview.md', 'CANADA-SPLIT', lines)
        head = '| ' + ('职业（NOC 2021）' if zh else 'Occupation (NOC 2021)') + ' | ' + ' | '.join(quarters) + ' |'
        vlines = [head, '|---|' + '---:|' * len(quarters)]
        for name, name_zh in occ:
            sub = {r['quarter']: r for r in vac if r['occupation'] == name}
            cells = []
            for q in quarters:
                r = sub.get(q)
                cells.append(f"{int(r['job_vacancies']):,}" if r and r['job_vacancies'] and r['quality'] in 'ABC' else '—')
            vlines.append(f"| {name_zh if zh else name} | " + ' | '.join(cells) + ' |')
        vlines += ['', ('“—”表示数据质量低于 C 级，未列出。' if zh else '"—" marks values graded below C, which are not shown.')]
        replace_block(ROOT / f'docs/{lang}/role-overview.md', 'CANADA-VACANCIES', vlines)


def render_ai_share_chart():
    # Lightcast AI-skill posting shares (AI Index 2026 via Our World in Data); annual, so no partial period.
    rows = list(csv.DictReader((ROOT / 'research/market/ai-skill-postings-share.csv').open()))
    years = sorted({r['year'] for r in rows})
    spec = [('CA', 'CA', '加拿大', 'Canada'), ('US', 'US', '美国', 'United States'), ('GB', 's3', '英国', 'United Kingdom'), ('AU', 's4', '澳大利亚', 'Australia')]
    for lang in ['zh', 'en']:
        zh = lang == 'zh'
        series = []
        for code, color, lzh, len_ in spec:
            sub = {r['year']: float(r['ai_job_postings_share_pct']) for r in rows if r['country'] == code}
            series.append({'color': color, 'label': lzh if zh else len_, 'values': [sub.get(y) for y in years]})
        title = '要求 AI 技能的招聘广告占全部广告的比例（%）' if zh else 'Job postings requiring AI skills, share of all postings (%)'
        foot = ('来源：Lightcast，经 Stanford AI Index 2026 与 Our World in Data 发布 · 按岗位要求的技能统计，与 Indeed 关键词占比口径不同' if zh else
                'Source: Lightcast via Stanford AI Index 2026 and Our World in Data · counts required skills; not comparable with Indeed keyword shares')
        for theme in THEMES:
            (OUT / f'market-ai-skill-share-{lang}-{theme}.svg').write_text(
                line_chart(lang, theme, [dict(x) for x in series], years, title, '占比（%）' if zh else 'Share (%)', foot, partial=False))


def render_cops_table():
    rows = list(csv.DictReader((ROOT / 'research/market/cops-2026-2035-tech.csv').open()))
    names = {'00000': '全部职业', '20012': '计算机与信息系统经理', '21211': '数据科学家', '21220': '网络安全专家',
             '21222': '信息系统专家', '21223': '数据库分析与管理', '21230': '计算机系统开发与程序员', '21231': '软件工程师',
             '21232': '软件开发与程序员', '21234': 'Web 开发与程序员', '21311': '计算机工程师（不含软件）'}
    cond = {'Balance': ('平衡', 'Balance'), 'N/A': ('—', '—')}
    order = ['21231', '21232', '21211', '21220', '21234', '00000']
    for lang in ['zh', 'en']:
        zh = lang == 'zh'
        head = ('| 职业（NOC 2021） | 2025 年就业 | 10 年就业增长 | 2026–35 职位空缺 | 2026–35 求职者 | 近期 / 预测供需 |' if zh else
                '| Occupation (NOC 2021) | Employment 2025 | 10-year employment growth | Job openings 2026–35 | Job seekers 2026–35 | Recent / projected conditions |')
        lines = [head, '|---|---:|---:|---:|---:|---|']
        by = {r['noc2021']: r for r in rows}
        for noc in order:
            r = by[noc]
            emp, grow = int(r['employment_2025']), int(r['expansion_demand_2026_2035'])
            label = (names[noc] if zh else r['occupation']) + ('' if noc == '00000' else f'（{noc}）' if zh else f' ({noc})')
            c1, c2 = cond.get(r['recent_conditions_2023_2025'], (r['recent_conditions_2023_2025'],) * 2), cond.get(r['projected_conditions_2026_2035'], (r['projected_conditions_2026_2035'],) * 2)
            lines.append(f"| {label} | {emp:,} | {100 * grow / emp:+.1f}% | {int(r['job_openings_2026_2035']):,} | {int(r['job_seekers_2026_2035']):,} | {c1[0 if zh else 1]} / {c2[0 if zh else 1]} |")
        lines += ['', ('职位空缺 = 扩张需求 + 退休 + 其他替换需求；求职者 = 毕业生 + 新移民 + 其他流动（可为负）。[完整数据](../../research/market/cops-2026-2035-tech.csv)' if zh else
                       'Job openings = expansion + retirements + other replacement; job seekers = school leavers + new immigrants + other mobility (may be negative). [Full data](../../research/market/cops-2026-2035-tech.csv)')]
        replace_block(ROOT / f'docs/{lang}/role-overview.md', 'COPS-TABLE', lines)


def render_charts():
    OUT.mkdir(parents=True, exist_ok=True)
    render_skill_charts()
    render_market_charts()
    render_canada_vacancies()
    render_skill_tables()
    render_enterprise_tables()
    render_canada_tables()
    render_ai_share_chart()
    render_cops_table()


if __name__ == '__main__':
    render_charts()
