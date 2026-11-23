"""Render the README route-overview diagram (zh/en × light/dark SVG) from the curriculum."""
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets/overview'

# Stage grouping and short labels are presentation choices; every module must appear exactly once.
STAGES = [
    ('foundations', ['00', '01', '02', '03', '04']),
    ('build', ['05', '06', '07', '08', '10']),
    ('ship', ['11', '14']),
    ('hired', ['15']),
]
SPECIALIZE = ['09', '12', '13', '16']
STAGE_TEXT = {
    'en': {'foundations': 'Foundations', 'build': 'Build AI apps', 'ship': 'Evaluate & ship', 'hired': 'Get hired',
           'specialize': 'Specialize by target role'},
    'zh': {'foundations': '打基础', 'build': '构建AI应用', 'ship': '评测与上线', 'hired': '求职',
           'specialize': '按目标岗位选专项'},
}
SHORT = {
    'en': {'00': 'Role map & delivery', '01': 'Python & engineering', '02': 'Backend & data systems',
           '03': 'Math, ML & PyTorch', '04': 'Transformers & LLMs', '05': 'Model apps & prompting',
           '06': 'Retrieval & RAG', '07': 'Agents & memory', '08': 'LangGraph & frameworks',
           '09': 'Multi-agent systems', '10': 'MCP & tool safety', '11': 'Evals & observability',
           '12': 'Fine-tuning & RL', '13': 'Inference & serving', '14': 'Production delivery',
           '15': 'Portfolio & interviews', '16': 'World models & robotics'},
    'zh': {'00': '岗位地图与交付全景', '01': 'Python与软件工程', '02': '后端、数据与分布式', '03': '数学、ML与PyTorch',
           '04': 'Transformer与LLM原理', '05': '模型应用与Prompt', '06': '检索与RAG', '07': 'Agent架构与记忆',
           '08': 'LangGraph与框架', '09': '多Agent协作', '10': 'MCP与工具安全', '11': '评测与可观测性',
           '12': '微调、RL与蒸馏', '13': '推理优化与部署', '14': '端到端生产交付', '15': '作品集与面试',
           '16': '世界模型与具身智能'},
}
THEMES = {
    'light': {'text': '#1f2328', 'muted': '#59636e', 'card': '#f6f8fa', 'line': '#d0d7de',
              'foundations': '#0969da', 'build': '#8250df', 'ship': '#1a7f37', 'hired': '#bc4c00', 'specialize': '#1b7c83'},
    'dark': {'text': '#f0f6fc', 'muted': '#9198a1', 'card': '#161b22', 'line': '#3d444d',
             'foundations': '#4493f8', 'build': '#ab7df8', 'ship': '#3fb950', 'hired': '#f0883e', 'specialize': '#39c5cf'},
}
FONT = "-apple-system, BlinkMacSystemFont, 'Segoe UI', 'Noto Sans', Helvetica, Arial, 'PingFang SC', 'Hiragino Sans GB', 'Microsoft YaHei', 'Noto Sans CJK SC', sans-serif"
W, M, GAP = 1040, 20, 40
CARD_W = (W - 2*M - 3*GAP) / 4
HEAD, ROW = 70, 40


def counts(mods):
    units = [n for m in mods for n in m['nodes']]
    resources = len(json.loads((ROOT/'data/resources.json').read_text()))
    labs = len(re.findall(r'^## L\d+', (ROOT/'docs/en/labs.md').read_text(), re.M))
    capstones = len(re.findall(r'^## P\d+', (ROOT/'docs/en/capstones.md').read_text(), re.M))
    return {'modules': len(mods), 'units': len(units), 'topics': sum(len(n['topics_en']) for n in units),
            'questions': sum(len(n.get('checks_en', [])) for n in units), 'resources': resources,
            'labs': labs, 'capstones': capstones}


def check_layout(mods):
    placed = [x for _, ids in STAGES for x in ids] + SPECIALIZE
    ids = [m['id'] for m in mods]
    if sorted(placed) != sorted(ids) or len(placed) != len(set(placed)):
        raise ValueError('Overview stages must place every module exactly once')
    for lang in SHORT:
        if set(SHORT[lang]) != set(ids):
            raise ValueError(f'Overview short labels incomplete: {lang}')


def dots(x, y, nodes, color):
    out = []
    for i, n in enumerate(nodes):
        cx = x + 4 + i*10
        if n['track'] == 'core':
            out.append(f'<circle cx="{cx:.1f}" cy="{y}" r="3.6" fill="{color}"/>')
        elif n['track'] == 'advanced':
            out.append(f'<circle cx="{cx:.1f}" cy="{y}" r="3.6" fill="{color}" fill-opacity="0.35"/>')
        else:
            out.append(f'<circle cx="{cx:.1f}" cy="{y}" r="3" fill="none" stroke="{color}" stroke-width="1.3"/>')
    return out


def text(x, y, s, size, fill, weight=None, anchor=None):
    attrs = f'x="{x:.1f}" y="{y:.1f}" font-size="{size}" fill="{fill}"'
    if weight:
        attrs += f' font-weight="{weight}"'
    if anchor:
        attrs += f' text-anchor="{anchor}"'
    return f'<text {attrs}>{escape(s)}</text>'


def notes_for(key, lang, c):
    zh = lang == 'zh'
    return {
        'foundations': ['+ 入门诊断'] if zh else ['+ entry diagnostic'],
        'build': [f'+ {c["labs"]} 个动手实验'] if zh else [f'+ {c["labs"]} hands-on labs'],
        'ship': [],
        'hired': ([f'+ {c["capstones"]} 个完整项目', f'+ {c["questions"]} 道自测题'] if zh
                  else [f'+ {c["capstones"]} capstone projects', f'+ {c["questions"]} self-check questions']),
    }[key]


def svg(mods, lang, theme, c):
    t, T, S = THEMES[theme], STAGE_TEXT[lang], SHORT[lang]
    by_id = {m['id']: m for m in mods}
    zh = lang == 'zh'
    y0, note_h, v_gap = 16, 24, 20
    content = {key: HEAD + len(ids)*ROW + len(notes_for(key, lang, c))*note_h + 8 for key, ids in STAGES}
    short_h = max(content['ship'], content['hired'])
    spec_rows = (len(SPECIALIZE) + 1) // 2
    spec_h = 44 + spec_rows*38 + 6
    tall_h = max(content['foundations'], content['build'], short_h + v_gap + spec_h)
    body = []
    xs = [M + i*(CARD_W + GAP) for i in range(len(STAGES))]
    for i, (key, ids) in enumerate(STAGES):
        x, color = xs[i], t[key]
        h = tall_h if i < 2 else short_h
        n_units = sum(len(by_id[m]['nodes']) for m in ids)
        body.append(f'<rect x="{x:.1f}" y="{y0}" width="{CARD_W:.1f}" height="{h}" rx="12" fill="{t["card"]}" stroke="{t["line"]}"/>')
        label = f'阶段 {i+1} · {n_units} 个单元' if zh else f'STAGE {i+1} · {n_units} UNITS'
        body.append(text(x+16, y0+26, label, 11.5, t['muted'], weight='600'))
        body.append(text(x+16, y0+50, T[key], 18, t['text'], weight='700'))
        body.append(f'<line x1="{x+16:.1f}" y1="{y0+62}" x2="{x+52:.1f}" y2="{y0+62}" stroke="{color}" stroke-width="3" stroke-linecap="round"/>')
        y = y0 + HEAD
        for mid in ids:
            body.append(text(x+16, y+14, f'{mid}  {S[mid]}', 13.5, t['text']))
            body += dots(x+16, y+28, by_id[mid]['nodes'], color)
            y += ROW
        for note in notes_for(key, lang, c):
            body.append(text(x+16, y+14, note, 13, color, weight='600'))
            y += note_h
        if i < len(STAGES)-1:
            ax, ay = x + CARD_W + 8, y0 + 44
            body.append(f'<path d="M{ax:.1f} {ay} H{ax+GAP-16:.1f} M{ax+GAP-22:.1f} {ay-5} L{ax+GAP-16:.1f} {ay} L{ax+GAP-22:.1f} {ay+5}" fill="none" stroke="{t["muted"]}" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"/>')
    # Specializations sit under stages 3–4 and branch from stage 2.
    sx, sy = xs[2], y0 + short_h + v_gap
    sw = xs[3] + CARD_W - sx
    color = t['specialize']
    body.append(f'<rect x="{sx:.1f}" y="{sy}" width="{sw:.1f}" height="{spec_h}" rx="12" fill="{t["card"]}" stroke="{color}" stroke-opacity="0.7" stroke-dasharray="6 4"/>')
    ay = sy + spec_h/2
    ax = xs[1] + CARD_W + 8
    body.append(f'<path d="M{ax:.1f} {ay:.1f} H{sx-8:.1f} M{sx-14:.1f} {ay-5:.1f} L{sx-8:.1f} {ay:.1f} L{sx-14:.1f} {ay+5:.1f}" fill="none" stroke="{t["muted"]}" stroke-width="1.6" stroke-dasharray="4 3" stroke-linecap="round" stroke-linejoin="round"/>')
    n_spec = sum(len(by_id[m]['nodes']) for m in SPECIALIZE)
    body.append(text(sx+16, sy+28, T['specialize'], 16, t['text'], weight='700'))
    sub = f'可选纵深 · {n_spec} 个单元' if zh else f'optional depth · {n_spec} units'
    title_w = (len(T['specialize'])*16 + 12) if zh else (len(T['specialize'])*8.4 + 12)
    body.append(text(sx+16+title_w, sy+28, sub, 12.5, t['muted']))
    col_w = (sw - 32) / 2
    for j, mid in enumerate(SPECIALIZE):
        x = sx + 16 + (j % 2)*col_w
        y = sy + 44 + (j // 2)*38
        body.append(text(x, y+12, f'{mid}  {S[mid]}', 13.5, t['text']))
        body += dots(x, y+25, by_id[mid]['nodes'], color)
    y2 = y0 + tall_h + 30
    stats = (f'{c["modules"]} 个模块 · {c["units"]} 个单元 · {c["topics"]} 条主题 · {c["resources"]} 项免费资源 · {c["labs"]} 个实验 · {c["questions"]} 道自测题'
             if zh else f'{c["modules"]} modules · {c["units"]} units · {c["topics"]} topics · {c["resources"]} free resources · {c["labs"]} labs · {c["questions"]} self-check questions')
    body.append(text(M, y2, stats, 13, t['muted']))
    legend = [('core', '核心' if zh else 'core'), ('advanced', '进阶' if zh else 'advanced'), ('elective', '选修' if zh else 'elective')]
    lead = '每个圆点 = 1 个单元：' if zh else 'Each dot is one unit:'
    est = lambda s: sum(12.5 if '\u4e00' <= ch <= '\u9fff' or ch == '：' else 7.2 for ch in s)
    lx = W - M
    for k, name in reversed(legend):
        body.append(text(lx, y2, name, 12.5, t['muted'], anchor='end'))
        lx -= est(name) + 9
        body += dots(lx - 4, y2 - 4, [{'track': k}], t['text'])
        lx -= 22
    body.append(text(lx + 8, y2, lead, 12.5, t['muted'], anchor='end'))
    h = y2 + 14
    title = 'AI Engineering 学习路线总览' if zh else 'AI Engineering roadmap overview'
    desc = ('四个阶段：打基础、构建AI应用、评测与上线、求职；另有按目标岗位选择的专项。每个圆点代表一个学习单元。' if zh else
            'Four stages: foundations, building AI applications, evaluating and shipping, and getting hired, plus specializations chosen by target role. Each dot is one learning unit.')
    head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" role="img" '
            f'aria-labelledby="t d" font-family="{FONT}">')
    return '\n'.join([head, f'<title id="t">{escape(title)}</title>', f'<desc id="d">{escape(desc)}</desc>'] + body + ['</svg>']) + '\n'


def render_overview(mods):
    check_layout(mods)
    OUT.mkdir(parents=True, exist_ok=True)
    c = counts(mods)
    for lang in ['en', 'zh']:
        for theme in ['light', 'dark']:
            (OUT/f'roadmap-{lang}-{theme}.svg').write_text(svg(mods, lang, theme, c))


if __name__ == '__main__':
    render_overview(json.loads((ROOT/'data/curriculum.json').read_text()))
