"""Offline checks for the curriculum, public evidence and bilingual documents."""
import calendar
import collections
import csv
import datetime as dt
import json
import math
import re
from pathlib import Path
from urllib.parse import unquote
try:
    from .curriculum_graph import index_units, topological_units, expand_route
except ImportError:
    from curriculum_graph import index_units, topological_units, expand_route

ROOT = Path(__file__).resolve().parents[1]
errors = []

def check(ok, message):
    if not ok:
        errors.append(message)

def read_json(path):
    return json.loads((ROOT / path).read_text())

def read_csv(path):
    with (ROOT / path).open() as f:
        return list(csv.DictReader(f))

resources = read_json('data/resources.json')
modules = read_json('data/curriculum.json')
jobs = read_json('research/jds.json')
codebook = read_json('research/keyword-codebook.json')
repo_records = read_json('research/github-repos.json')
units = [n for m in modules for n in m['nodes']]
resource_ids = {r['id'] for r in resources}
module_ids = {m['id'] for m in modules}
unit_ids = {n['id'] for n in units}
check(len(resource_ids) == len(resources), 'Duplicate resource IDs')
check(len(module_ids) == len(modules), 'Duplicate module IDs')
check(len(unit_ids) == len(units), 'Duplicate unit IDs')
check(len(modules) >= 17 and len(units) >= 101, 'Curriculum coverage regressed')
for resource in resources:
    for field in ['id','title','url','kind','why_zh','why_en','cost','status','tier','checked_at']:
        check(bool(resource.get(field)), f'Resource missing {field}: {resource.get("id")}')
    check(resource['url'].startswith('https://'), 'Resource requires an HTTPS source')
for module in modules:
    check(set(module['related_modules']) <= module_ids, f'Unknown prerequisite: {module["id"]}')
    check(module['id'] not in module['related_modules'], f'Self prerequisite: {module["id"]}')
    for unit in module['nodes']:
        check(unit['id'].startswith(module['id']+'.'), f'Module/unit mismatch: {unit["id"]}')
        check(unit['primary_resource'] in resource_ids, f'Unknown resource: {unit["id"]}')
        check(unit['depth'] in ['explain','implement','diagnose','design'], f'Invalid depth: {unit["id"]}')
        check(unit['track'] in ['core','advanced','elective'], f'Invalid track: {unit["id"]}')
        check(set(unit['jd_keys']) <= set(codebook), f'Unknown JD key: {unit["id"]}')
        check(len(unit['topics_zh']) == len(unit['topics_en']) >= 5, f'Bilingual scope mismatch: {unit["id"]}')
        check(len(unit.get('checks_zh',[])) == len(unit.get('checks_en',[])) >= 3, f'Bilingual self-check mismatch: {unit["id"]}')
        for language in ['zh','en']:
            questions = unit.get('checks_'+language,[])
            check(all(isinstance(q,str) and q.strip() for q in questions) and len(set(questions))==len(questions), f'Empty or duplicate self-check: {unit["id"]}/{language}')
        for language in ['zh','en']:
            for field in [language, 'read_'+language, 'build_'+language, 'topics_'+language]:
                check(bool(unit.get(field)), f'Missing {field}: {unit["id"]}')
    for language in ['zh','en']:
        path = ROOT / f'docs/{language}/modules/{module["id"]}.md'
        check(path.exists(), f'Missing module page: {path.relative_to(ROOT)}')
        text = path.read_text() if path.exists() else ''
        for unit in module['nodes']:
            check(f'## {unit["id"]} ' in text, f'Unit absent from {language} page: {unit["id"]}')
            for topic in unit['topics_'+language]:
                check(topic in text, f'Generated topic absent: {unit["id"]}/{language}')
            for question in unit.get('checks_'+language,[]):
                check(question in text, f'Generated self-check absent: {unit["id"]}/{language}')
for language in ['zh','en']:
    path = ROOT / f'docs/{language}/self-check.md'
    check(path.exists(), f'Missing self-check page: {language}')
    text = path.read_text() if path.exists() else ''
    for unit in units:
        for question in unit.get('checks_'+language,[]):
            check(f'- [ ] {question}' in text, f'Self-check page missing question: {unit["id"]}/{language}')
unit_index = index_units(modules)
try:
    ordered = topological_units(modules)
    for unit in units:
        check(len(unit['prerequisites']) == len(set(unit['prerequisites'])), f'Duplicate prerequisite: {unit["id"]}')
        if unit['track']=='core':
            check(all(unit_index[x]['track']=='core' for x in unit['prerequisites']), f'Common knowledge requires specialization: {unit["id"]}')
    routes = read_json('data/learning-routes.json')
    check(len({r['id'] for r in routes})==len(routes), 'Duplicate route IDs')
    for route in routes:
        stages = expand_route(modules,route)
        done = set()
        for stage in stages:
            for id in stage['units']:
                check(id not in done, f'Duplicate route unit: {route["id"]}/{id}')
                check(set(unit_index[id]['prerequisites']) <= done, f'Route prerequisite order: {route["id"]}/{id}')
                done.add(id)
except ValueError as e:
    check(False,str(e))
audit=read_json('research/course-audit.json')
check(0 < audit['after']['units']<=len(units), 'Course-audit unit count')
check(0 < audit['after']['topics']<=sum(len(n['topics_en']) for n in units), 'Course-audit topic count')
check(0 < audit['after']['resources']<=len(resources), 'Course-audit resource count')
source_manifest=read_json('research/course-source-manifest.json')
source_files={s['file'] for s in source_manifest}
for finding in audit['findings']:
    check(set(finding['units']) <= unit_ids, f'Course-audit unit mapping: {finding["id"]}')
    check(set(finding['source_files']) <= source_files, f'Course-audit source mapping: {finding["id"]}')
for source in source_manifest:
    check(source['url'].startswith('https://') and bool(re.fullmatch('[a-f0-9]{64}',source['sha256'])), 'Course source provenance')

check(len({j['jd_id'] for j in jobs}) == len(jobs), 'Duplicate JD IDs')
check(len({j['url'] for j in jobs}) == len(jobs), 'Duplicate JD URLs')
check(len({j['body_sha256'] for j in jobs}) == len(jobs), 'Duplicate JD bodies')
for job in jobs:
    tag = job['jd_id']
    check('body' not in job, f'Employer body in public registry: {tag}')
    check(job['country'] in ['CN','US','CA'], f'Unknown country: {tag}')
    check(job['market'] == ('CN' if job['country']=='CN' else 'NA'), f'Market mismatch: {tag}')
    check(job['source_grade'] in ['A1-employer-api','A1-employer','A2-university-hosted','B1-syndicated-employer'], f'Source grade: {tag}')
    check(job['active_status'] in ['listed-at-collection','description-accessible-opening-unverified'], f'Unqualified status: {tag}')
    check(bool(re.fullmatch('[a-f0-9]{64}', job['body_sha256'])), f'Invalid hash: {tag}')
    check(set(job['features']) == set(codebook), f'Feature coverage: {tag}')
    check(all(type(v) is bool for v in job['features'].values()), f'Non-boolean feature: {tag}')
    check(bool(job.get('sections')), f'No reviewed role span: {tag}')
    intervals = []
    for span in job['sections']:
        check(0 <= span['start'] < span['end'] <= job['body_characters'], f'Invalid offset: {tag}')
        check(bool(re.fullmatch('[a-f0-9]{64}', span['sha256'])), f'Invalid span hash: {tag}')
        intervals.append((span['start'],span['end']))
    intervals.sort()
    check(all(a[1] <= b[0] for a,b in zip(intervals,intervals[1:])), f'Overlapping role spans: {tag}')
    for key, value in job['features'].items():
        check(value == any(s[key] for s in job['section_features'].values()), f'Span union mismatch: {tag}/{key}')
skill_terms = read_json('research/skill-terms.json')['terms']
skill_keys = {t['key'] for t in skill_terms}
check(len(skill_keys) == len(skill_terms) and all(t['group'] in ['tech_stack','role_expectations'] and t['zh'] and t['en'] for t in skill_terms), 'Skill term definitions')
for job in jobs:
    check(job.get('sample') in ['v3-reviewed','v4-rule-screened'], f'Unknown sample: {job["jd_id"]}')
    check(set(job.get('features_v2',{})) == skill_keys and all(type(v) is bool for v in job.get('features_v2',{}).values()), f'Skill-term coverage: {job["jd_id"]}')
    if job.get('sample') == 'v4-rule-screened':
        check(job['source_grade'] == 'A1-employer-api' and job['market'] == 'NA', f'Rule-screened provenance: {job["jd_id"]}')
for row in read_csv('research/skill-distribution.csv'):
    sample = [j for j in jobs if j['market']==row['market'] and (row['sample']=='all' or j.get('sample')==row['sample'])]
    count = sum(j['features_v2'][row['key']] for j in sample)
    check(int(row['n']) == len(sample) and int(row['count']) == count, f'Skill distribution mismatch: {row["market"]}/{row["sample"]}/{row["key"]}')
    check(float(row['ci95_low']) <= float(row['pct']) <= float(row['ci95_high']), f'Interval does not contain share: {row["key"]}')
cohorts = {label:[j for j in jobs if j['market']==label or j['country']==label] for label in ['CN','NA','CA','US']}
check(len(cohorts['CN']) >= 50 and len(cohorts['NA']) >= 50, 'Regional JD minimum not met')
rows = read_csv('research/keyword-counts.csv')
check({r['keyword'] for r in rows} == set(codebook), 'Keyword summary coverage')
for row in rows:
    key = row['keyword']
    for label,sample in cohorts.items():
        n = len(sample)
        count = sum(j['features'][key] for j in sample)
        check(int(row[label+'_n']) == n and int(row[label+'_count']) == count, f'Count mismatch: {label}/{key}')
        check(float(row[label+'_pct']) == round(100*count/n,2), f'Percentage mismatch: {label}/{key}')
        employers = collections.defaultdict(list)
        for job in sample:
            employers[job['company']].append(job)
        balanced = sum(sum(j['features'][key] for j in v)/len(v) for v in employers.values())/len(employers)*100
        check(abs(float(row[label+'_employer_balanced_pct']) - balanced) <= .00501, f'Employer weighting: {label}/{key}')
summary = read_json('research/sample-summary.json')
check(summary['overall']['n'] == len(jobs), 'Sample summary denominator')
check(summary['overall']['employers'] == len({j['company'] for j in jobs}), 'Sample summary employers')
for label in ['CN','NA']:
    check(summary['markets'][label]['n'] == len(cohorts[label]), f'Market summary: {label}')

check(len({x['full_name'].lower() for x in repo_records}) == len(repo_records), 'Duplicate repositories')
for repo in repo_records:
    check(type(repo['stargazers_count']) is int and repo['stargazers_count'] >= 0, 'Invalid star count')
    check(type(repo['archived']) is bool and bool(repo.get('captured_at')), 'Missing repository provenance')
link_checks = read_json('research/resource-link-checks.json')
check({x['id'] for x in link_checks} == resource_ids, 'Resource access-check coverage')
checks_by_id = {x['id']:x for x in link_checks}
for r in resources:
    check(checks_by_id[r['id']]['url'] == r['url'], f'Stale resource check: {r["id"]}')

# Verify aggregates independently from their public observations.
for source, aggregate, value_key in [
    ('indeed-daily-subset.csv','indeed-quarterly.csv','value'),
    ('linkedin-monthly-subset.csv','linkedin-quarterly.csv','value_pct')]:
    daily = read_csv('research/market/'+source)
    groups = collections.defaultdict(list)
    identities = set()
    for row in daily:
        check(row['country'] in ['US','CA'], f'Unexpected indicator country: {source}')
        check('2025-01-01' <= row['date'] <= '2026-11-18', f'Indicator outside cutoff: {source}')
        period = row['date'][:4]+'Q'+str((int(row['date'][5:7])-1)//3+1)
        key = (row['metric'], row['country'], row.get('group'), period)
        identity = key+(row['date'],)
        check(identity not in identities, f'Duplicate indicator: {identity}')
        identities.add(identity)
        groups[key].append(row)
        if row['metric']=='ai_keyword_share_pct':
            check(0 <= float(row[value_key]) <= 100, 'Invalid AI keyword share')
    aggregates = read_csv('research/market/'+aggregate)
    check(len(aggregates)==len(groups), f'Quarterly group coverage: {aggregate}')
    for row in aggregates:
        key = (row['metric'],row['country'],row.get('group'),row['quarter'])
        sample = groups.get(key,[])
        if not sample:
            check(False, f'Aggregate has no observations: {key}')
            continue
        expected = math.fsum(float(r[value_key]) for r in sample)/len(sample)
        check(math.isclose(float(row[value_key]),expected,rel_tol=1e-12,abs_tol=1e-12), f'Quarterly mean: {key}')
        check(int(row.get('n_months',row.get('n_observations'))) == len(sample), f'Quarterly denominator: {key}')
        check(row['last_date'] == max(r['date'] for r in sample), f'Quarterly coverage date: {key}')
        if row['quarter']=='2026Q4':
            check(row['partial_quarter']=='True', f'Unmarked partial quarter: {key}')
missing = read_csv('research/market/requested-national-active-counts.csv')
expected = {(c,r,f'{y}Q{q}') for c in ['US','CA','CN'] for r in ['AIE','SDE','MLE','SRE'] for y in [2025,2026] for q in [1,2,3,4]}
check({(r['country'],r['role'],r['quarter']) for r in missing}==expected and len(missing)==len(expected), 'Missing-observation matrix coverage')
check(all(r['active_postings_count']=='' for r in missing), 'Unsubstantiated national vacancy count')
manifest = read_json('research/market/source-manifest.json')
for source in manifest['sources']:
    check(source['url'].startswith('https://') and source['bytes'] > 0, 'Market source provenance')
    check(bool(re.fullmatch('[a-f0-9]{64}',source['sha256'])), 'Invalid market hash')

def heading_anchors(path):
    # GitHub-style heading slugs plus explicit <a id> anchors.
    text = path.read_text()
    anchors, seen = set(re.findall(r'<a id="([^"]+)"', text)), {}
    for heading in re.findall(r'^#{1,6} (.+)$', text, re.M):
        heading = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', heading).strip().lower()
        slug = re.sub(r'[^\w\- ]', '', heading).replace(' ', '-')
        n = seen.get(slug, 0); seen[slug] = n + 1
        anchors.add(slug if n == 0 else f'{slug}-{n}')
    return anchors
anchor_cache = {}
# Local links, anchors and HTML image sources are validated in all public Markdown files.
for path in ROOT.rglob('*.md'):
    text = path.read_text()
    for target in re.findall(r'!?\[[^\]]*\]\(([^)]+)\)', text):
        target = target.strip().split(' "',1)[0].strip('<>')
        if re.match(r'^[a-z][a-z0-9+.-]*:',target,re.I):
            continue
        rel, _, anchor = target.partition('#')
        dest = (path.parent / unquote(rel)) if rel else path
        check(dest.exists(), f'Broken local link: {path.relative_to(ROOT)} → {rel}')
        if anchor and dest.exists() and dest.suffix == '.md':
            if dest not in anchor_cache:
                anchor_cache[dest] = heading_anchors(dest)
            check(unquote(anchor) in anchor_cache[dest], f'Broken anchor: {path.relative_to(ROOT)} → {target}')
    for source in re.findall(r'(?:src|srcset)="([^"]+)"', text):
        if not re.match(r'^[a-z][a-z0-9+.-]*:', source, re.I):
            check((path.parent / source).exists(), f'Missing image: {path.relative_to(ROOT)} → {source}')
    check('DRAFT' not in text, f'Stale role-definition draft: {path.relative_to(ROOT)}')
for language, readme in [('zh','README.zh-CN.md'),('en','README.md')]:
    text = (ROOT / readme).read_text()
    count_pattern = str(len(units)) + (r'\s*(?:个单元|单元)' if language=='zh' else r'\s+units')
    topic_pattern = str(sum(len(n['topics_en']) for n in units)) + (r'\s*(?:条主题|主题)' if language=='zh' else r'\s+topic')
    check(bool(re.search(count_pattern,text)), f'Stale README unit count: {readme}')
    check(bool(re.search(topic_pattern,text)), f'Stale README topic count: {readme}')
    question_pattern = str(sum(len(n.get('checks_en',[])) for n in units)) + (r'\s*道' if language=='zh' else r'\s+(?:interview-style\s+)?(?:self-check\s+)?questions')
    check(bool(re.search(question_pattern,text)) and f'docs/{language}/self-check.md' in text, f'Stale README self-check entry: {readme}')
    check('role-overview.md' in text, f'Overview entry missing: {readme}')
    for m in modules:
        check(f'modules/{m["id"]}.md' in text, f'Module navigation absent: {readme}/{m["id"]}')
    labs = (ROOT / f'docs/{language}/labs.md').read_text()
    for i in range(1,18):
        check(f'## L{i:02d}\n' in labs, f'Lab missing: {language}/L{i:02d}')
    for filename in ['role-overview.md','jd-china.md','jd-north-america.md','learning-path.md','capstones.md','knowledge-tree.md','course-audit.md','evaluation-playbook.md','self-check.md']:
        check((ROOT / f'docs/{language}/{filename}').exists(), f'Bilingual page missing: {language}/{filename}')
for path in ROOT.rglob('*'):
    if path.is_file() and path.suffix in ['.md','.json','.csv','.py','.yml']:
        # Keep private project material and user-specific filesystem paths out of publication.
        text = path.read_text()
        for pattern in [r'(?<![a-z0-9])/(?:Users|home)/[a-z][a-z0-9_.-]+/',r'(?:career|resume)-research-\d{4}']:
            check(not re.search(pattern,text,re.I), f'Private material pattern in {path.relative_to(ROOT)}')

if errors:
    print('\n'.join('- '+e for e in errors))
    raise SystemExit(f'{len(errors)} validation errors')
print(f'Validated {len(modules)} modules, {len(units)} units, {sum(len(n["topics_en"]) for n in units)} topics, {sum(len(n.get("checks_en",[])) for n in units)} self-check questions, {len(resources)} resources, {len(jobs)} JDs and {len(repo_records)} repositories.')
