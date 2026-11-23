"""Render publication artifacts from the checked-in research tables.

Optional dependency: pip install -r requirements-viz.txt
"""
import collections,csv,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'assets/research';OUT.mkdir(parents=True,exist_ok=True)
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,'axes.spines.right':False,'axes.titleweight':'bold','axes.labelcolor':'#334155','text.color':'#172337','axes.edgecolor':'#cbd5e1','grid.color':'#e2e8f0','svg.fonttype':'none','svg.hashsalt':'aie-roadmap-2026','savefig.facecolor':'white'})
COL={'CN':'#c76a35','CA':'#117d7a','US':'#3d62b3','NA':'#3d62b3'}
def save(fig,name):
 fig.savefig(OUT/(name+'.png'),dpi=165,bbox_inches='tight',metadata={'Software':'AI Engineering Roadmap'});fig.savefig(OUT/(name+'.svg'),bbox_inches='tight',metadata={'Date':None,'Creator':'AI Engineering Roadmap'});plt.close(fig)
def csvrows(path):return list(csv.DictReader(path.open()))
def main():
 rows=csvrows(ROOT/'research/keyword-counts.csv');by={r['keyword']:r for r in rows}
 labels={'production_ownership':'Delivery / production','evaluation_experiments':'Evaluation / experiments','latency_cost_performance':'Latency / cost / performance','observability':'Observability','python':'Python','security_governance':'Security / governance','rag':'RAG','java_spring':'Java / Spring','mcp':'MCP','multi_agent':'Multi-agent','typescript_javascript':'JavaScript / TypeScript','fine_tuning_sft_lora':'Fine-tuning / SFT / LoRA','reinforcement_learning':'Reinforcement learning','langgraph':'LangGraph'}
 keys=list(labels);cn=[float(by[k]['CN_pct']) for k in keys];na=[float(by[k]['NA_pct']) for k in keys];y=np.arange(len(keys))
 fig,ax=plt.subplots(figsize=(11,7));ax.barh(y-.18,cn,height=.34,color=COL['CN'],label='China (51 descriptions)');ax.barh(y+.18,na,height=.34,color=COL['NA'],label='North America (53 descriptions)');ax.set_yticks(y,list(labels.values()));ax.invert_yaxis();ax.set_xlim(0,111);ax.set_xlabel('Share of descriptions mentioning the term (%)');ax.grid(axis='x',alpha=.5);ax.set_axisbelow(True)
 for i,(a,b) in enumerate(zip(cn,na)):
  ax.text(a+1,i-.18,f'{a:.1f}',va='center',fontsize=8);ax.text(b+1,i+.18,f'{b:.1f}',va='center',fontsize=8)
 ax.legend(loc='lower right',frameon=False);fig.suptitle('What sampled AI-engineering roles mention',x=.02,ha='left',fontsize=16,fontweight='bold');fig.text(.02,.01,'Purposive sample · reviewed role text · mentions include alternatives and preferences · collected 18–19 Nov 2026',fontsize=9,color='#64748b');fig.tight_layout(rect=(0,.04,1,.96));save(fig,'jd-skills-cn-na')

 jobs=json.loads((ROOT/'research/jds.json').read_text());levels=['intern','entry','mid','senior','staff_plus','lead_architect_expert','unspecified'];names=['Intern','Entry / graduate','Mid (explicit)','Senior','Staff / Principal+','Lead / Architect / Expert','Unspecified'];colors=['#8cb8cf','#62a990','#83a7db','#4c72b0','#7656a0','#c89452','#d8dee7']
 fig,axes=plt.subplots(1,3,figsize=(13,5))
 for ax,country,title in zip(axes,['CN','US','CA'],['China','United States','Canada']):
  sample=[j for j in jobs if j['country']==country];counts=collections.Counter(j['seniority'] for j in sample);values=[counts[x] for x in levels];ax.pie(values,colors=colors,startangle=90,autopct=lambda p:f'{p:.0f}%' if p>=6 else '',pctdistance=.79,wedgeprops={'width':.43,'edgecolor':'white'});ax.text(0,0,f'n={len(sample)}',ha='center',va='center',fontweight='bold',fontsize=15);ax.set_title(title)
 fig.legend([plt.Rectangle((0,0),1,1,color=c) for c in colors],names,loc='lower center',ncol=4,frameon=False,bbox_to_anchor=(.5,.03));fig.suptitle('Seniority labels in the JD sample',fontsize=16,fontweight='bold');fig.text(.5,0,'Title-based labels only · unmarked levels retained · no population or vacancy-market inference',ha='center',fontsize=9,color='#64748b');fig.tight_layout(rect=(0,.19,1,.93));save(fig,'jd-levels-by-country')

 indeed=csvrows(ROOT/'research/market/indeed-quarterly.csv');linkedin=csvrows(ROOT/'research/market/linkedin-quarterly.csv');quarters=[f'{y}Q{q}' for y in [2025,2026] for q in range(1,5)]
 fig,axes=plt.subplots(3,1,figsize=(11,10),sharex=True)
 configs=[('ai_keyword_share_pct','AI-related keywords in all postings','Posting share (%)',indeed,'value'),('software_postings_index_2020_100','Software Development postings index','1 Feb 2020 = 100',indeed,'value'),('ai_builders_relative_hiring_growth_yoy','AI builders: relative hiring growth','Monthly YoY, quarterly mean (%)',linkedin,'value_pct')]
 for ax,(metric,title,ylabel,data,field) in zip(axes,configs):
  for country in ['CA','US']:
   sub={r['quarter']:float(r[field]) for r in data if r['country']==country and r['metric']==metric};ax.plot(quarters,[sub.get(q,float('nan')) for q in quarters],marker='o',lw=2.2,color=COL[country],label='Canada' if country=='CA' else 'United States')
  ax.axvspan(6.5,7.5,color='#f1f5f9');ax.set_title(title,loc='left',pad=12);ax.set_ylabel(ylabel);ax.grid(axis='y',alpha=.65);ax.legend(frameon=False,loc='upper left');ax.text(.99,.9,'Q4 partial',transform=ax.transAxes,ha='right',color='#64748b',fontsize=9)
 fig.suptitle('Published market indicators, 2025–2026',x=.06,ha='left',fontsize=17,fontweight='bold');fig.text(.06,.012,'Sources: Indeed Hiring Lab; LinkedIn Economic Graph. China series unavailable in these releases.\nQ4 coverage: AI share to 31 Oct; software index to 13 Nov; LinkedIn to Oct. These are not active AIE/SDE/MLE/SRE totals.',fontsize=9,color='#64748b');fig.tight_layout(rect=(0,.055,1,.96));save(fig,'market-quarterly-indicators')

 fig,axes=plt.subplots(1,2,figsize=(12,4.6),sharey=True)
 for ax,country,title in zip(axes,['US','CA'],['United States','Canada']):
  for group,label,color in [('SIZE_10001+','10,001+ employees','#3d62b3'),('SIZE_1001_5000','1,001–5,000 employees','#117d7a')]:
   sub={r['quarter']:float(r['value_pct']) for r in linkedin if r['country']==country and r['metric']=='linkedin_hiring_rate' and r['group']==group};ax.plot(quarters,[sub.get(q,float('nan')) for q in quarters],marker='o',lw=2,color=color,label=label)
  ax.axhline(0,color='#94a3b8',lw=.8);ax.axvspan(6.5,7.5,color='#f1f5f9');ax.set_title(title,loc='left');ax.tick_params(axis='x',rotation=40);ax.grid(axis='y',alpha=.6);ax.legend(frameon=False,fontsize=9)
 axes[0].set_ylabel('Monthly hiring YoY, quarterly mean (%)');fig.suptitle('Company-size hiring context — all roles',x=.05,ha='left',fontsize=16,fontweight='bold');fig.text(.05,.01,'LinkedIn Economic Graph · not AIE-specific demand · no China series · 2026Q4 covers October only',fontsize=9,color='#64748b');fig.tight_layout(rect=(0,.065,1,.91));save(fig,'company-size-hiring-context')
 print('Rendered 4 PNG/SVG research figures.')
if __name__=='__main__':main()
