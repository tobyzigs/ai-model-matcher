import json,re,sys,datetime
orm=json.load(open('data/or.json')); aa=json.load(open('data/aa.json'))
CREATOR_FIX={'SpaceXAI':'xAI','Kimi':'Moonshot AI','Alibaba':'Qwen (Alibaba)','Z AI':'Z.ai'}
OR_PROV={'aion-labs':'AION Labs','amazon':'Amazon','anthracite-org':'Anthracite','anthropic':'Anthropic','apodex':'Apodex','arcee-ai':'Arcee AI','bytedance':'ByteDance','bytedance-seed':'ByteDance Seed','cognitivecomputations':'Cognitive Computations','cohere':'Cohere','deepseek':'DeepSeek','dots-studio':'Dots Studio','fireworks':'Fireworks','google':'Google','gryphe':'Gryphe','ibm-granite':'IBM','inception':'Inception','inclusionai':'InclusionAI','inference-net':'Inference.net','liquid':'Liquid AI','mancer':'Mancer','meituan':'Meituan (LongCat)','meta':'Meta','meta-llama':'Meta','microsoft':'Microsoft','minimax':'MiniMax','mistralai':'Mistral','moonshotai':'Moonshot AI','morph':'Morph','nex-agi':'Nex AGI','nousresearch':'Nous Research','nvidia':'NVIDIA','openai':'OpenAI','perceptron':'Perceptron','perplexity':'Perplexity','poolside':'Poolside','prism-ml':'Prism','qwen':'Qwen (Alibaba)','rekaai':'Reka AI','relace':'Relace','sakana':'Sakana AI','sao10k':'Sao10K','scaledown':'ScaleDown','stepfun':'StepFun','tencent':'Tencent','thedrummer':'TheDrummer','thinkingmachines':'Thinking Machines','typesafe':'Typesafe','unbiased':'Unbiased','undi95':'Undi95','upstage':'Upstage','writer':'Writer','x-ai':'xAI','xiaomi':'Xiaomi','z-ai':'Z.ai'}
def norm(s): return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')
aa_by={r['slug']:r for r in aa}
def pct(v): return None if v is None else round(v*100,1)
def coding(r):
    b=r.get('benchmarks') or {}
    tb=b.get('terminal_bench_4_0') if b.get('terminal_bench_4_0') is not None else b.get('terminalbench_hard')
    vals=[v for v in (tb,b.get('scicode')) if v is not None]
    return round(sum(vals)/len(vals)*100,1) if vals else None
def bench(r):
    if not r: return {}
    b=r.get('benchmarks') or {}
    out={'ii':None if r.get('intelligence_index') is None else round(r['intelligence_index'],1),'code':coding(r),'gpqa':pct(b.get('gpqa')),'hle':pct(b.get('hle')),
         'honest':pct(b.get('omniscience_non_hallucination')),'acc':pct(b.get('omniscience_accuracy')),'vis':pct(b.get('mmmu_pro')),'gdp':pct(b.get('gdpval_normalized')),'analyst':pct(b.get('analyst_agent')),'bank':pct(b.get('tau_banking')),'lcr':pct(b.get('lcr')),'tool':pct(b.get('tau2')),'instr':pct(b.get('ifbench')),'size':r.get('size_class'),'aa':r['slug']}
    core=[out['honest'],out['lcr'],out['code']]
    out['rel']=round(sum(core)/3,1) if None not in core else None
    return out
def params(*texts):
    t=' '.join(x for x in texts if x).lower()
    m=re.search(r'(?<![\w.])(\d+(?:\.\d+)?)\s*([bt])(?![a-z])',t)
    if not m: return None,None
    tot=float(m.group(1))*(1000 if m.group(2)=='t' else 1)
    a=re.search(r'(?<![\w.])a(\d+(?:\.\d+)?)b(?![a-z])',t)
    act=float(a.group(1)) if a else None
    if tot<0.1 or tot>3000: return None,None
    return tot,act
ALIAS={'anthropic/claude-haiku-4.5':'claude-4-5-haiku','anthropic/claude-sonnet-4.5':'claude-4-5-sonnet','anthropic/claude-opus-4.1':'claude-4-1-opus','anthropic/claude-sonnet-4':'claude-4-sonnet','anthropic/claude-opus-4':'claude-4-opus','z-ai/glm-4.5':'glm-4.5','deepseek/deepseek-chat-v3.1':'deepseek-v3-1','deepseek/deepseek-v3.2-exp':'deepseek-v3-2-0925','deepseek/deepseek-chat':'deepseek-v3','deepseek/deepseek-chat-v3-0324':'deepseek-v3-0324','google/gemini-3.1-flash-lite':'gemini-3-1-flash-lite-preview','minimax/minimax-m1':'minimax-m1-80k','x-ai/grok-build-0.1':'grok-build-0-1-06-16'}
def find_aa(mid):
    k=mid.split(':')[0]
    if k in ALIAS and ALIAS[k] in aa_by: return aa_by[ALIAS[k]]
    base=norm(mid.split('/',1)[1].split(':')[0])
    cands=[base, base.replace('-instruct',''), base.replace('-preview',''), base+'-reasoning', re.sub(r'-\d{4}$','',base), re.sub(r'-\d{8}$','',base)]
    for c in cands:
        if c in aa_by and not aa_by[c]['deprecated']: return aa_by[c]
    for c in cands:
        if c in aa_by: return aa_by[c]
    sib=[r for s,r in aa_by.items() if s.startswith(base+'-') and re.fullmatch(r'(x?high|medium|low|max|minimal|non-reasoning|reasoning|thinking)',s[len(base)+1:])]
    if sib: return max(sib,key=lambda r:r.get('intelligence_index') or 0)
    return None
# Published sizes (total, active) in billions for models whose names don't say it
KNOWN={'meta-llama/llama-4-maverick':(400,17),'meta-llama/llama-4-scout':(109,17),'deepseek/deepseek-chat':(671,37),'deepseek/deepseek-chat-v3-0324':(671,37),'deepseek/deepseek-chat-v3.1':(671,37),'deepseek/deepseek-v3.1-terminus':(671,37),'deepseek/deepseek-v3.2':(671,37),'deepseek/deepseek-v3.2-exp':(671,37),'deepseek/deepseek-r1':(671,37),'deepseek/deepseek-r1-0528':(671,37),'moonshotai/kimi-k2':(1000,32),'moonshotai/kimi-k2-0905':(1000,32),'moonshotai/kimi-k2-thinking':(1000,32),'z-ai/glm-4.5':(355,32),'z-ai/glm-4.5-air':(106,12),'z-ai/glm-4.6':(355,32),'minimax/minimax-m2':(230,10)}
rows=[];used=set()
for m in orm:
    mid=m['id']
    if mid.startswith(('~','openrouter/')) or mid.endswith(':batch'): continue
    p=m['pricing']; pi=float(p['prompt']); po=float(p['completion'])
    if pi<0 or po<0: continue
    pc=p.get('input_cache_read'); pc=None if pc is None else float(pc)*1e6
    a=find_aa(mid)
    if a: used.add(a['slug'])
    pfx=mid.split('/')[0]
    rows.append(dict(prov=OR_PROV.get(pfx,pfx),model=m['name'].split(': ',1)[-1],id=mid,ctx=m.get('context_length') or (m.get('top_provider') or {}).get('context_length'),
        pin=round(pi*1e6,4),pout=round(po*1e6,4),pcache=None if pc is None else round(pc,4),
        free=mid.endswith(':free') or (pi==0 and po==0),mod=m['architecture'].get('modality',''),
        where='OpenRouter',created=m.get('created'),**bench(a)))
    arch=m.get('architecture') or {}
    rows[-1]['inm']=arch.get('input_modalities') or []; rows[-1]['outm']=arch.get('output_modalities') or []
    io=p.get('image_output'); rows[-1]['pimg']=None if io is None else round(float(io)*1e6,4)
    rows[-1]['pb'],rows[-1]['pa']=next((v for k,v in KNOWN.items() if mid.split(':')[0]==k),None) or params(m['name'],mid,m.get('hugging_face_id'))
# direct-only AA models (current, not matched)
seen_base=set()
for r in sorted(aa,key=lambda r:-(r.get('intelligence_index') or 0)):
    if r['deprecated'] or r['slug'] in used: continue
    base=re.sub(r'-(x?high|medium|low|max|minimal|non-reasoning|reasoning)$','',r['slug'])
    if base in seen_base or any(u.startswith(base) for u in used): continue
    seen_base.add(base)
    pr=r.get('pricing_usd_per_1m_tokens') or {}
    if pr.get('input') is None or (not pr.get('input') and not pr.get('output')): continue
    cr=r['creator_name']
    rows.append(dict(prov=CREATOR_FIX.get(cr,cr),model=r['name'],id=r['slug'],ctx=r.get('context_window_tokens'),pin=pr.get('input'),pout=pr.get('output'),pcache=pr.get('cache_hit'),
        free=False,mod='',where='Direct from maker',created=None,**bench(r)))
    rows[-1]['pb'],rows[-1]['pa']=params(r['name'],r['slug'])
meta={'updated':datetime.date.today().isoformat(),'or_count':len(orm),'aa_count':len(aa),'sources':{'pricing':'https://openrouter.ai/models','benchmarks':'https://artificialanalysis.ai/leaderboards/models'}}
json.dump({'meta':meta,'rows':rows},open('models.json','w'),separators=(',',':'))
print(len(rows),sum(1 for r in rows if r.get('ii') is not None),sum(1 for r in rows if r['where']!='OpenRouter'))
print(len(set(r['prov'] for r in rows)))
for r in rows[:0]: print(r)
miss=[]# for r in rows if r['where']=='OpenRouter' and r.get('ii') is None and r['id'].startswith(('anthropic','openai/gpt-5','google/gemini-3','x-ai','deepseek','z-ai','moonshotai','qwen/qwen3.5','minimax'))]

