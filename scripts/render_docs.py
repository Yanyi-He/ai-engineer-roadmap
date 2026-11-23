"""Render bilingual module pages, the knowledge tree and unit-based study routes."""
import json
import re
from pathlib import Path
try:
    from .curriculum_graph import index_units, topological_units, expand_route
    from .render_overview import render_overview
    from .render_charts import render_charts
except ImportError:
    from curriculum_graph import index_units, topological_units, expand_route
    from render_overview import render_overview
    from render_charts import render_charts
ROOT=Path(__file__).resolve().parents[1]
mods=json.loads((ROOT/'data/curriculum.json').read_text())
resources={r['id']:r for r in json.loads((ROOT/'data/resources.json').read_text())}
routes=json.loads((ROOT/'data/learning-routes.json').read_text())
units=index_units(mods)
depth={'explain':('解释：讲清机制、边界与选择依据','Explain mechanisms, limits and choices'),'implement':('实现：独立完成小型实现并验证行为','Implement a small system and verify behavior'),'diagnose':('诊断：定位失败、设计对照并修正','Diagnose failures, compare and repair'),'design':('设计：在约束下选择架构并论证取舍','Design under constraints and defend tradeoffs')}
refs={
'00':['swyx-aie','cs329z','fsdl','ml-course','roadmap-sh'], '01':['python','asyncio-tasks','pythonds','missing','fastapi','claude-code-best-practices','agents-md'], '02':['fastapi','sql','idempotency','system-design-primer','owasp-cheatsheets','docker','actions','ts','vercel-ai-sdk','ag-ui','spring-ai','langchain4j','spring-ai-alibaba'],
'03':['d2l','openintro-stats','pytorch-tutorials','cs336-resource-accounting'],'04':['hf-llm','d2l','cs336','cs336-2026','nanogpt-course','hf-vlms','clip','chinchilla','deepseek-v2','happy-llm'],'05':['litellm','anthropic-prompt-tutorial','function','structured','context','routellm','openai-prompt-caching','openai-batch','aws-bedrock','bailian','cs336-evaluation','hf-vision','hf-audio'],
'06':['llm-zoomcamp','docling','mineru','rag-from-scratch','contextual-retrieval','llamaindex','sentence','mteb','ir','pgvector','qdrant','milvus','alce','graphrag','colpali','jxnl-rag','ragas','azure-doc-intel','ragflow'],'07':['effective','hf-agents','ms-begin','deep-course','12factor','agent-skills-post','agent-skills','mem0','graphiti','cs329z-hw1','hello'],
'08':['lg-course','lg-code','langgraph','adk','pydantic-ai','maf','openai-agents-sdk','claude-agent-sdk','temporal','dspy','dify','coze','n8n','langchain-v1','dify-source','copilot-studio','agentscope','spring-ai-alibaba','hello'],'09':['cs329z','adk','deepagents','a2a','inspect'],
'10':['anthropic-tools','function','mcp-server','mcp-sdk','mcp-auth','mcp-security','docker-security','gvisor','injection-patterns','lethal-trifecta','owasp-agentic','purple-llama','qwen3guard','presidio'],'11':['hamel-evals','hamel-judge','inspect','ragas','error-bars','scipy-bootstrap','otel','langfuse','promptfoo','cs329z-hw2','cs336-evaluation','terminal-bench','tau2-bench','pytest','deepeval','ragas-precision','ragas-faithfulness','promptfoo-ci','langfuse-eval','inspect-evalsets'],
'12':['cs336-data','cs336-a4','hf-llm','trl','peft','llamafactory','unsloth','ms-swift','rlhf-book','cs336-a5','verl','trl-gkd','obp','dr-paper','self-llm'],'13':['mlx','llamacpp','vllm','sglang','mooncake','profiler','cs336-resource-accounting','cs336-inference','self-llm'],
'14':['fsdl','applied-llms','pair-guidebook','sre','actions','owasp','cac-genai','cac-labeling','eu-ai-act','nist-ai-rmf','gum-paper'],'15':['tech-interview-handbook','ml-interviews-book','llms-from-scratch','genai-platform','system-design-primer','design-docs-google','llm-zoomcamp','sre'],'16':['hf-deep-rl','dreamerv3','mujoco','lerobot','ros2']}
def resource_link(rid,lang):
    r=resources[rid]
    return f"[{r['title']}]({r['url']}) — {r['why_'+lang]}"
def unit_link(id,lang,prefix=''):
    return f"[{id} {units[id][lang]}]({prefix}modules/{id.split('.')[0]}.md#unit-{id.replace('.','-')})"
def write_self_check(out,lang):
    zh=lang=='zh'
    all_units=[n for m in mods for n in m['nodes']]
    total=sum(len(n['checks_'+lang]) for n in all_units)
    core=sum(len(n['checks_'+lang]) for n in all_units if n['track']=='core')
    if zh:
        lines=['# 自测题清单','','[知识树](knowledge-tree.md) · [学习顺序](dependency-order.md) · [入门诊断](entry-diagnostic.md) · [能力评审](assessment.md)','',
               f'每个单元3道面试式自测题，共{total}道。三道题大致对应：讲清机制、诊断问题、设计或实现。题目不附标准答案，答好所需的要点在对应单元的知识框架和主读资源里。','',
               '用法：','','- 不看资料，口头或在纸上作答，每题2–3分钟。','- 答不出来：回到该单元的主读资源和知识框架。',
               '- 能讲清原理，却举不出自己的代码、实验或线上案例：完成该单元的实践产物。',
               f'- 先覆盖core单元（{core}道）；advanced和elective按目标岗位选做。','- Fork本仓库后，把`[ ]`改成`[x]`记录进度。','']
    else:
        lines=['# Self-check question bank','','[Map](knowledge-tree.md) · [Study order](dependency-order.md) · [Entry diagnostic](entry-diagnostic.md) · [Assessment](assessment.md)','',
               f'Three interview-style questions per unit, {total} in total. They roughly follow the order: explain a mechanism, diagnose a problem, then design or implement. There is no answer key; the unit’s outline and primary reading cover what a good answer needs.','',
               'How to use it:','','- Answer aloud or on paper without notes, 2–3 minutes per question.','- If you can’t answer, return to the unit’s primary reading and outline.',
               '- If you can explain the idea but can’t point to your own code, experiment or production case, do the unit’s build task.',
               f'- Cover core units first ({core} questions); choose advanced and elective units by target role.','- After forking the repository, change `[ ]` to `[x]` to track progress.','']
    for m in mods:
        lines+=[f"## [{m['id']} · {m[lang]}](modules/{m['id']}.md)",'']
        for n in m['nodes']:
            lines+=[f"### {unit_link(n['id'],lang)} · `{n['track']}`",'']+[f'- [ ] {q}' for q in n['checks_'+lang]]+['']
    (out/'self-check.md').write_text('\n'.join(lines)+'\n')
def main():
    ordered=topological_units(mods)
    for lang in ['zh','en']:
        zh=lang=='zh';out=ROOT/f'docs/{lang}';(out/'modules').mkdir(exist_ok=True)
        for m in mods:
            lines=[f"# {m['id']} · {m[lang]}",'',('[总览](../knowledge-tree.md) · [学习顺序](../dependency-order.md) · [自测题](../self-check.md) · [课程对照审阅](../course-audit.md)' if zh else '[Map](../knowledge-tree.md) · [Study order](../dependency-order.md) · [Self-check](../self-check.md) · [Course audit](../course-audit.md)'),'',m['outcome_'+lang],'',('相关模块：' if zh else 'Related modules: ')+(', '.join(f"[{k}](./{k}.md)" for k in m['related_modules']) or '—'),'',('单元先修按知识点计算。core是共同知识；advanced按岗位深入；elective是方向拓展。实作按所选项目路线推进；路线只展开该作品所需先修，共同知识按图谱持续补齐。' if zh else 'Prerequisites operate at unit level. Core is common knowledge; advanced follows role needs; electives explore adjacent fields. Routes expand prerequisites for the selected product; continue filling common knowledge from the map.'),'']
            if m['id'] in ['06','11']:
                lines += [('[评测操作：Ragas、pytest、promptfoo与CI](../evaluation-playbook.md)' if zh else '[Evaluation operations: Ragas, pytest, promptfoo and CI](../evaluation-playbook.md)'), '']
            for n in m['nodes']:
                lines += [f'<a id="unit-{n["id"].replace(".","-")}"></a>','',f"## {n['id']} {n[lang]}",'',f"`{n['track']}` · {depth[n['depth']][0 if zh else 1]}",'',('先修：' if zh else 'Prerequisites: ')+(', '.join(unit_link(x,lang,'../') for x in n['prerequisites']) or '—'),'',('### 知识框架' if zh else '### Knowledge outline'),'']
                lines += ['- '+t for t in n['topics_'+lang]]
                lines += ['',('### 资源与阅读范围' if zh else '### Reading and scope'),'',resource_link(n['primary_resource'],lang),'',n['read_'+lang],'',('### 实践产物' if zh else '### Practical evidence'),'',n['build_'+lang],'',('### 自测题' if zh else '### Self-check'),'']
                lines += [f'{i}. {q}' for i,q in enumerate(n['checks_'+lang],1)]+['']
            lines += [('## 按需参考' if zh else '## References'),'']+['- '+resource_link(r,lang) for r in refs[m['id']]]
            (out/'modules'/f"{m['id']}.md").write_text('\n'.join(lines)+'\n')
        lines=['# '+('AIE知识树' if zh else 'AI Engineering knowledge tree'),'',('从模块进入单元，再看机制、失败、资源和实践产物。分类图用于总览；[学习顺序](dependency-order.md)按单元先修与项目路线展开；[课程审阅](course-audit.md)说明CS329Z/CS336对照与取舍。' if zh else 'Browse modules and units, then mechanisms, failures, readings and evidence. The taxonomy gives an overview; [study order](dependency-order.md) expands unit prerequisites and project routes. The [course audit](course-audit.md) explains CS329Z/CS336 comparisons.'),'','```mermaid','mindmap','  root((AI Engineering))']
        for m in mods:
            lines.append('    '+m['id']+' '+m[lang])
            for n in m['nodes']:lines.append('      '+n['id']+' '+n[lang].replace('(','（').replace(')','）'))
        lines+=['```','']
        for m in mods:
            lines += [f"## [{m['id']} {m[lang]}](modules/{m['id']}.md)",'',m['outcome_'+lang],'']
            for n in m['nodes']:
                r=resources[n['primary_resource']]
                lines.append(f"- **{unit_link(n['id'],lang)}** · `{n['track']}` · [{r['title']}]({r['url']})")
                lines += ['  - '+t for t in n['topics_'+lang]]
            lines.append('')
        (out/'knowledge-tree.md').write_text('\n'.join(lines)+'\n')
        write_self_check(out,lang)
        readme_path=ROOT/('README.zh-CN.md' if zh else 'README.md')
        readme=readme_path.read_text()
        start='<!-- FULL-KNOWLEDGE-TREE:START -->'
        end='<!-- FULL-KNOWLEDGE-TREE:END -->'
        tree='\n'.join(lines).split('```mermaid',1)[1].split('```',1)[0]
        summary=(f'展开完整知识树：{len(mods)}模块、{len(units)}单元' if zh else f'Expand the full tree: {len(mods)} modules, {len(units)} units')
        block=start+'\n<details>\n<summary>'+summary+'</summary>\n\n```mermaid'+tree+'```\n\n</details>\n'+end
        if start in readme:
            readme=readme.split(start,1)[0]+block+readme.split(end,1)[1]
        else:
            marker='| 模块 |' if zh else '| Module |'
            position=readme.index(marker)
            readme=readme[:position]+block+'\n\n'+readme[position:]
        # Module titles are kept consistent with the authoritative taxonomy.
        for module in mods:
            path=f'docs/{lang}/modules/{module["id"]}.md'
            old_label_pattern=r'\['+module['id']+r' · [^\]]+\]\('+re.escape(path)+r'\)'
            readme=re.sub(old_label_pattern,f"[{module['id']} · {module[lang]}]({path})",readme)
        readme_path.write_text(readme)
        lines=['# '+('单元先修、并行学习与项目路线' if zh else 'Unit prerequisites, parallel study and project routes'),'',('先修精确到单元，模块编号只作分类。可以先做模型API和无框架Agent，再按任务加入RAG或LangGraph；应用交付可使用托管模型。SFT、GPU服务与多Agent工程在相应专项路线展开。' if zh else 'Prerequisites name individual units; module numbers classify topics. Build an API and framework-neutral agent early, then add RAG or LangGraph as needed. Hosted models support application delivery; SFT, GPU serving and multi-agent engineering belong to selected branches.'),'','```mermaid','flowchart LR','  A[Software and API] --> B[Evaluation baseline]','  B --> C[Framework-neutral harness]','  C --> D[Authorized tools and recovery]','  D --> E[Product delivery]','  B --> F[Knowledge and RAG]','  C --> G[Agent platforms]','  B --> H[Local models and adaptation]','  I[Math and model foundations] -. parallel .-> E','```','']
        for route in routes:
            lines += [f"## {route['zh' if zh else 'en']}",'',route['purpose_zh' if zh else 'purpose_en'],'','| '+('阶段 | 该阶段展开的先修与目标 | 实验 |' if zh else 'Stage | Expanded prerequisites and targets | Labs |'),'|---|---|---|']
            for stage in expand_route(mods,route):
                opt=stage.get('skipped_optional',False)
                ids=stage['targets'] if opt else stage['units']
                label=stage['zh' if zh else 'en']+('（可选，按单元先修进入）' if zh and opt else ' (optional; inspect unit prerequisites)' if opt else '')
                links=', '.join(f"[{x}](modules/{x.split('.')[0]}.md#unit-{x.replace('.','-')})" for x in ids) or '—'
                labs=', '.join(f'[{x}](labs.md#{x.lower()})' for x in stage['labs']) or '—'
                lines.append(f'| {label} | {links} | {labs} |')
            lines.append('')
        lines += [('## 全部单元的先修' if zh else '## All unit prerequisites'),'',('下表为一种可行拓扑顺序；同批无依赖主题可以并行。已有能力通过[诊断](entry-diagnostic.md)抵免。可选分支的先修仅在选择该分支时展开。' if zh else 'The table is one valid topological order. Independent units can run in parallel. Demonstrate prior learning through the [diagnostic](entry-diagnostic.md). Expand optional prerequisites when selecting that branch.'),'','| Unit | Track | Prerequisites |','|---|---|---|']
        for id in ordered:
            n=units[id];lines.append(f"| {unit_link(id,lang)} | {n['track']} | {', '.join(unit_link(x,lang) for x in n['prerequisites']) or '—'} |")
        (out/'dependency-order.md').write_text('\n'.join(lines)+'\n')
    render_overview(mods)
    render_charts()
    print(f'Rendered {len(mods)} modules, {len(units)} units and {len(routes)} routes in both languages.')
if __name__=='__main__':main()
