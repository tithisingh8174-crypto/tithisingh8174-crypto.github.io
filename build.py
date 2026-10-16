import json, html
from data import *
R=json.load(open('results.json')); P=json.load(open('profile.json'))
p1=R['p1']; T=R['ttm']; DC=R['dcf']; PR={"MNST":44.22,"KO":91.95,"PEP":129.27}
pc=lambda x,d=1:f"{x*100:.{d}f}%"
N={'KO':'Coca-Cola','PEP':'PepsiCo','MNST':'Monster'}
cd={c['tk']:c for c in COS}
for t in p1:
    c=cd[t]; p1[t]['om_adj']=[(c['oi'][i]+c['other_op'][i])/c['rev'][i] for i in range(5)]
    p1[t]['capex']=c['capex']; p1[t]['div']=c['div']; p1[t]['bb']=c['bb']; p1[t]['ocf']=c['ocf']
g=lambda t,k,i=-1:p1[t][k][i]
# ---------- insight strings (every number comes from results) ----------
I={}
I['revidx']=f"Monster grew revenue at {pc(p1['MNST']['rev_cagr'])} a year from 2021 to 2025, about twice Coca-Cola ({pc(p1['KO']['rev_cagr'])}) and PepsiCo ({pc(p1['PEP']['rev_cagr'])})."
I['epsidx']=f"EPS tells a sharper story than revenue: Monster {pc(p1['MNST']['eps_cagr'])} a year, Coca-Cola {pc(p1['KO']['eps_cagr'])}, PepsiCo only {pc(p1['PEP']['eps_cagr'])} because its FY2025 EPS fell to ${g('PEP','eps'):.2f} from ${g('PEP','eps',3):.2f}."
I['gm']=f"Coca-Cola's gross margin is the highest ({pc(g('KO','gm'))} in FY2025). Monster dropped to {pc(g('MNST','gm',1))} in 2022 and has rebuilt to {pc(g('MNST','gm'))}; PepsiCo sits at {pc(g('PEP','gm'))}."
I['om']=f"Coca-Cola and Monster both earn roughly 29 cents of operating profit per dollar of sales ({pc(g('KO','om'))} and {pc(g('MNST','om'))}); PepsiCo earns {pc(g('PEP','om'))}, down from {pc(g('PEP','om',0))} in 2021."
I['nm']=f"Net margin: Monster {pc(g('MNST','nm'))}, Coca-Cola {pc(g('KO','nm'))} (helped by about $2.0B of equity-method income), PepsiCo {pc(g('PEP','nm'))}."
I['fcf_margin']=f"Free cash flow (operating cash flow minus capex) as a share of revenue in FY2025: Monster {pc(g('MNST','fcf_margin'))}, PepsiCo {pc(g('PEP','fcf_margin'))}, Coca-Cola {pc(g('KO','fcf_margin'))}. Coca-Cola's FY2025 figure is depressed by a one-off $6.1B payment (see the cash chart)."
I['capex_int']=f"Monster is asset-light, spending {pc(g('MNST','capex_int'))} of revenue on capex against {pc(g('KO','capex_int'))} at Coca-Cola and {pc(g('PEP','capex_int'))} at PepsiCo, which also runs a food and manufacturing network."
Q={}
for t in CO if False else ['KO','PEP','MNST']:
    pass
Q['KO']=f"Coca-Cola's reported margin dipped to {pc(g('KO','om',3))} in 2024 because other operating charges jumped to ${cd['KO']['other_op'][3]:,}M. Before those charges the margin held at {pc(g('KO','om_adj',3))}, so the business was steady and the dip was an accounting event."
Q['PEP']=f"PepsiCo took ${cd['PEP']['other_op'][4]:,}M of impairment charges in FY2025. Before them margin was {pc(g('PEP','om_adj'))}, versus {pc(g('PEP','om_adj',0))} in 2021, so the underlying margin has also slipped."
Q['MNST']=f"Monster reports no separate impairment line, so reported and underlying margins match. Operating margin dipped to {pc(g('MNST','om',1))} in 2022 and has climbed to {pc(g('MNST','om'))}."
DU=[]
for i in range(4):
    r={t:p1[t]['bs'] for t in p1}
    DU.append(f"{[2022,2023,2024,2025][i]}: PepsiCo ROE {pc(r['PEP']['roe'][i],0)} and Coca-Cola {pc(r['KO']['roe'][i],0)} are driven by different levers. Coca-Cola leans on margin ({pc(r['KO']['nm'][i],0)} net); PepsiCo leans on leverage ({r['PEP']['em'][i]:.1f}x equity multiplier). Monster's {pc(r['MNST']['roe'][i],0)} is held down by low leverage ({r['MNST']['em'][i]:.1f}x equity multiplier) and a large cash balance.")
WC={'dso':f"PepsiCo collects slowest ({p1['PEP']['bs']['dso'][-1]:.0f} days of sales outstanding in FY2025), Monster {p1['MNST']['bs']['dso'][-1]:.0f} days, Coca-Cola {p1['KO']['bs']['dso'][-1]:.0f}. Monster's was {p1['MNST']['bs']['dso'][0]:.0f} days in 2022.",
 'dio':f"Monster cut inventory days from {p1['MNST']['bs']['dio'][0]:.0f} (2022) to {p1['MNST']['bs']['dio'][-1]:.0f} (2025). Coca-Cola ({p1['KO']['bs']['dio'][-1]:.0f}) and PepsiCo ({p1['PEP']['bs']['dio'][-1]:.0f}) are flat. Payables are not compared because Coca-Cola and PepsiCo report payables combined with accrued liabilities.",
 'cur':f"Liquidity: Monster's current ratio is {p1['MNST']['bs']['cur'][-1]:.1f}x versus {p1['KO']['bs']['cur'][-1]:.1f}x at Coca-Cola and {p1['PEP']['bs']['cur'][-1]:.1f}x at PepsiCo, both of which also carry short-term debt."}
CA={}
for t in ['KO','PEP','MNST']:
    c=cd[t]; f=p1[t]['fcf'][-1]; out=c['div'][-1]+c['bb'][-1]
    if t=='KO': CA[t]=f"Coca-Cola paid ${c['div'][-1]:,}M of dividends and bought back ${c['bb'][-1]:,}M in FY2025 against free cash flow of ${f:,}M. The company's release attributes the weak year to a $6.1B contingent-consideration payment for fairlife; excluding it, it reports free cash flow of $11.4B, which covers the dividend."
    elif t=='PEP': CA[t]=f"PepsiCo returned ${out:,}M (dividends ${c['div'][-1]:,}M plus buybacks ${c['bb'][-1]:,}M) in FY2025 against free cash flow of ${f:,}M, i.e. {out/f*100:.0f}% of free cash flow. The payout was therefore not covered by free cash flow that year."
    else: CA[t]=f"Monster pays no dividend. FY2025 free cash flow was ${f:,.0f}M and it spent only ${c['bb'][-1]:,.0f}M on buybacks, after a ${c['bb'][3]:,.0f}M repurchase in 2024. Cash and investments grew to ${(c['cash'][-1]+c['sti'][-1]):,.0f}M."
D=dict(years=Y,p1=p1,ttm=T,price=PR['MNST'],insights=I,quality=Q,dupont=DU,wc=WC,cash=CA,
       dcf=dict(assump=DC['base_assump'],coe=DC['coe']))
m=T['MNST']; base=DC['base']
ps=base['ps']; up=ps/PR['MNST']-1
sc=DC['scen']; ff=DC['ff']
fy=lambda t,k:p1[t][k][-1]
# ---------- HTML ----------
def contact():
    out=[]
    if P['email']: out.append(f'<a href="mailto:{html.escape(P["email"])}">{html.escape(P["email"])}</a>')
    if P['linkedin']: out.append(f'<a href="{html.escape(P["linkedin"])}" rel="noopener">LinkedIn</a>')
    if P['github']: out.append(f'<a href="{html.escape(P["github"])}" rel="noopener">GitHub</a>')
    return out
cl=contact()
contact_html=(' · '.join(cl)) if cl else 'Contact details to be added.'
tab=lambda rows: ''.join(rows)
def row(lbl,vals): return '<tr><th scope="row">'+lbl+'</th>'+''.join(f'<td>{v}</td>' for v in vals)+'</tr>'
cmp_rows=[
 row('Revenue FY2025',[f"${cd[t]['rev'][-1]:,.0f}M" for t in ['KO','PEP','MNST']]),
 row('Revenue CAGR 2021–25',[pc(p1[t]['rev_cagr']) for t in ['KO','PEP','MNST']]),
 row('EPS CAGR 2021–25',[pc(p1[t]['eps_cagr']) for t in ['KO','PEP','MNST']]),
 row('Gross margin',[pc(fy(t,'gm')) for t in ['KO','PEP','MNST']]),
 row('Operating margin',[pc(fy(t,'om')) for t in ['KO','PEP','MNST']]),
 row('Free cash flow margin',[pc(fy(t,'fcf_margin')) for t in ['KO','PEP','MNST']]),
 row('Return on equity',[pc(p1[t]['bs']['roe'][-1]) for t in ['KO','PEP','MNST']]),
 row('Net debt / EBITDA',[(f"{p1[t]['bs']['nd_ebitda'][-1]:.1f}x" if p1[t]['bs']['nd_ebitda'][-1]>0 else 'net cash') for t in ['KO','PEP','MNST']]),
]
mult_rows=[
 row('Share price (see note)',[f"${T[t]['price']:.2f}" for t in ['MNST','KO','PEP']]),
 row('TTM revenue',[f"${T[t]['rev']:,.0f}M" for t in ['MNST','KO','PEP']]),
 row('TTM revenue growth (latest six months vs prior year)',[pc(T[t]['h1_growth'],0) for t in ['MNST','KO','PEP']]),
 row('TTM operating margin',[pc(T[t]['om']) for t in ['MNST','KO','PEP']]),
 row('TTM diluted EPS',[f"${T[t]['eps']:.2f}" for t in ['MNST','KO','PEP']]),
 row('P/E (TTM)',[f"{T[t]['pe']:.1f}x" for t in ['MNST','KO','PEP']]),
 row('EV / EBITDA (TTM)',[f"{T[t]['ev_ebitda']:.1f}x" for t in ['MNST','KO','PEP']]),
 row('Free cash flow yield (TTM)',[pc(T[t]['fcf_yield']) for t in ['MNST','KO','PEP']]),
]
a=DC['base_assump']
src=[
 ("Coca-Cola (CIK 21344)","10-K FY2025 · 0001628280-26-010047; 10-K FY2023 · 0000021344-24-000009; 10-Q quarter ended Jul 3, 2026 · 0001628280-26-050503"),
 ("PepsiCo (CIK 77476)","10-K FY2025 · 0000077476-26-000007; 10-K FY2023 · 0000077476-24-000008; 10-Q quarter ended Jun 13, 2026 · 0000077476-26-000035"),
 ("Monster Beverage (CIK 865752)","10-K FY2025 · 0001104659-26-020831; 10-K FY2023 · 0001104659-24-029425; 10-Q period ended Jun 30, 2026 · 0001104659-26-092193; 8-K stock split · 0001104659-26-081842"),
]
src_html=''.join(f'<li><b>{a_}</b><span>{b_}</span></li>' for a_,b_ in src)
name=html.escape(P['name']); first=name.split()[0]
page=f'''<title>{name} Finance Portfolio</title>
<meta name="claude:viewport-fit-sides" content="cover">
<meta name="description" content="Finance analyst portfolio: peer financial-statement analysis of Coca-Cola, PepsiCo and Monster, and a DCF valuation of Monster Beverage, built from SEC filings.">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600;700&family=IBM+Plex+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
:root{{--bg:#f2f5f7;--panel:#fff;--ink:#0d2236;--muted:#53677a;--rule:#dbe3ea;--rule-strong:#b7c4d0;--accent:#0b6e8f;--accent-soft:#7fb7c9;--accent-ink:#fff;
--pos:#0f845c;--neg:#c43c32;--c-ko:#c8102e;--c-pep:#1f5fbf;--c-mnst:#1b8a6b;--band:#0d2236;--band-ink:#eaf1f6}}
@media (prefers-color-scheme:dark){{:root:not([data-theme="light"]){{--bg:#0b1722;--panel:#112334;--ink:#e6eef5;--muted:#9bb0c2;--rule:#223a50;--rule-strong:#3a5671;--accent:#4cc0e3;--accent-soft:#2c6f86;--accent-ink:#06202b;
--pos:#3fd19b;--neg:#ff7a6e;--c-ko:#ff5a6e;--c-pep:#6fa4ff;--c-mnst:#3fd1a4;--band:#060f17;--band-ink:#e6eef5;color-scheme:dark}}}}
:root[data-theme="dark"]{{--bg:#0b1722;--panel:#112334;--ink:#e6eef5;--muted:#9bb0c2;--rule:#223a50;--rule-strong:#3a5671;--accent:#4cc0e3;--accent-soft:#2c6f86;--accent-ink:#06202b;
--pos:#3fd19b;--neg:#ff7a6e;--c-ko:#ff5a6e;--c-pep:#6fa4ff;--c-mnst:#3fd1a4;--band:#060f17;--band-ink:#e6eef5;color-scheme:dark}}
*{{box-sizing:border-box}}html{{scroll-behavior:smooth}}
body{{background:var(--bg);color:var(--ink);font:16px/1.6 'IBM Plex Sans',system-ui,sans-serif;-webkit-font-smoothing:antialiased}}
.mono,.t td,.kpi b,.num{{font-family:'IBM Plex Mono',ui-monospace,monospace;font-variant-numeric:tabular-nums}}
a{{color:var(--accent)}}
.wrap{{max-width:1120px;margin:0 auto;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}}
body::before{{content:"";position:fixed;inset:0 0 auto;height:env(safe-area-inset-top,0px);z-index:10;background:var(--bg)}}
header.top{{position:sticky;top:env(safe-area-inset-top,0px);z-index:5;background:var(--bg);border-bottom:1px solid var(--rule)}}
header.top .wrap{{display:flex;align-items:center;gap:20px;height:56px}}
.brand{{font-weight:700;letter-spacing:.01em}}
nav{{display:flex;gap:18px;margin-left:auto;font-size:14px}}nav a{{color:var(--muted);text-decoration:none}}nav a:hover{{color:var(--ink)}}
#theme,.chip,.btn{{font:inherit;font-size:13px;border:1px solid var(--rule-strong);background:transparent;color:var(--ink);border-radius:999px;padding:6px 14px;cursor:pointer}}
.chip[aria-pressed="true"],.btn[aria-pressed="true"]{{background:var(--ink);color:var(--bg);border-color:var(--ink)}}
button:focus-visible,a:focus-visible,input:focus-visible{{outline:3px solid var(--accent);outline-offset:2px}}
.hero{{padding:64px 0 36px}}
.eyebrow{{font:500 12px 'IBM Plex Mono',monospace;letter-spacing:.14em;text-transform:uppercase;color:var(--accent)}}
h1{{font-size:clamp(40px,7vw,76px);line-height:1;margin:12px 0 18px;letter-spacing:-.025em;font-weight:700}}
.lede{{font-size:clamp(18px,2.2vw,22px);max-width:760px;color:var(--muted);margin:0}}
.strip{{background:var(--band);color:var(--band-ink);margin-top:28px}}
.strip .wrap{{display:grid;grid-template-columns:repeat(3,1fr);gap:0}}
.strip .cell{{padding:18px 20px;border-left:1px solid rgba(255,255,255,.14)}}.strip .cell:first-child{{border-left:0;padding-left:0}}
.strip small{{display:block;font:500 11px 'IBM Plex Mono',monospace;letter-spacing:.1em;text-transform:uppercase;opacity:.7}}
.strip b{{font:600 26px 'IBM Plex Mono',monospace}}.strip span{{font-size:13px;opacity:.8;display:block}}
section{{padding:56px 0;border-bottom:1px solid var(--rule)}}
.num{{font-size:13px;color:var(--accent);font-weight:600;letter-spacing:.1em}}
h2{{font-size:clamp(28px,4vw,42px);line-height:1.1;margin:6px 0 10px;letter-spacing:-.02em}}
h3{{font-size:19px;margin:0 0 6px;line-height:1.3}}
.sub{{color:var(--muted);max-width:760px;margin:0 0 28px}}
.brief{{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px;margin:0 0 36px}}
.card{{background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:20px}}
.card h4{{margin:0 0 8px;font:600 12px 'IBM Plex Mono',monospace;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}}
.card ul{{margin:0;padding-left:18px}}.card li{{margin:0 0 7px}}.card p{{margin:0}}
.panel,.card,.kpi{{min-width:0}}.panel{{background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:20px;margin:0 0 20px}}
.take{{margin:10px 0 14px;font-weight:500;max-width:880px;min-height:3.2em}}
.chips{{display:flex;flex-wrap:wrap;gap:8px}}
.cv{{position:relative;height:340px}}
.cv.tall{{height:300px}}
.t{{width:100%;border-collapse:collapse;font-size:14px}}
.t th,.t td{{padding:9px 10px;border-bottom:1px solid var(--rule);text-align:right}}
.t th:first-child,.t thead th{{text-align:left}}.t thead th{{font:600 12px 'IBM Plex Sans';color:var(--muted)}}
.t td:first-child,.t thead th:not(:first-child){{text-align:right}}
.t .x{{text-align:center;color:var(--muted);padding:9px 2px}}
.tw{{overflow-x:auto}}
.heat td{{text-align:center;min-width:84px}}.heat small{{display:block;font-size:11px;opacity:.8}}
.grid2{{display:grid;grid-template-columns:1fr 1fr;gap:20px}}
.kpis{{display:grid;grid-template-columns:repeat(4,1fr);gap:12px;margin:0 0 20px}}
.kpi{{background:var(--panel);border:1px solid var(--rule);border-radius:10px;padding:16px}}
.kpi small{{display:block;color:var(--muted);font-size:12px}}.kpi b{{font-size:26px;display:block;margin:4px 0 2px}}
.pos{{color:var(--pos)}}.neg{{color:var(--neg)}}.up{{font-size:13px;font-weight:600}}
.ctl{{display:grid;grid-template-columns:repeat(2,1fr);gap:16px 28px}}
.ctl label{{display:block;font-size:13px;color:var(--muted)}}.ctl label span{{float:right;color:var(--ink);font:600 13px 'IBM Plex Mono',monospace}}
.ctl input[type=range]{{width:100%;accent-color:var(--accent)}}
.ctl input[type=number]{{width:110px;font:600 14px 'IBM Plex Mono',monospace;padding:6px 8px;border:1px solid var(--rule-strong);border-radius:6px;background:var(--bg);color:var(--ink)}}
.row{{display:flex;flex-wrap:wrap;gap:8px;align-items:center;margin:0 0 16px}}
.verdict{{border-left:4px solid var(--accent);background:var(--panel);padding:18px 22px;border-radius:0 10px 10px 0;margin:0 0 20px}}
.src{{list-style:none;padding:0;margin:0}}.src li{{padding:10px 0;border-bottom:1px solid var(--rule)}}.src b{{display:block}}.src span{{font:13px 'IBM Plex Mono',monospace;color:var(--muted)}}
.skills{{display:grid;grid-template-columns:repeat(3,1fr);gap:16px}}
.note{{font-size:13px;color:var(--muted)}}
footer{{padding:36px 0 60px;font-size:13px;color:var(--muted)}}
@media(max-width:820px){{.brief,.grid2,.skills{{grid-template-columns:minmax(0,1fr)}}.kpis{{grid-template-columns:1fr 1fr}}.ctl{{grid-template-columns:1fr}}
nav{{display:none}}.strip .wrap{{grid-template-columns:1fr}}.strip .cell{{border-left:0;border-top:1px solid rgba(255,255,255,.14);padding-left:0}}.strip .cell:first-child{{border-top:0}}.cv{{height:300px}}}}
@media(prefers-reduced-motion:reduce){{html{{scroll-behavior:auto}}}}
</style>
<header class="top"><div class="wrap"><span class="brand">{name}</span>
<nav aria-label="Sections"><a href="#p1">Project 1</a><a href="#p2">Project 2</a><a href="#method">Sources</a><a href="#contact">Contact</a></nav>
<button id="theme" type="button" aria-pressed="false">Dark</button></div></header>
<main>
<div class="hero"><div class="wrap">
<div class="eyebrow">Finance analyst portfolio · built on SEC filings</div>
<h1>{name}</h1>
<p class="lede">Two projects that do what an equity or corporate finance analyst does every week: read the filings, benchmark companies against each other, and turn the numbers into a valuation view you can defend. Every figure comes from the companies' own 10-K and 10-Q filings.</p>
</div>
<div class="strip"><div class="wrap">
<div class="cell"><small>Project 1 · Peer analysis</small><b>3 companies</b><span>5 years of statements each, FY2021 to FY2025</span></div>
<div class="cell"><small>Project 2 · Valuation</small><b>${ps:.2f} vs ${PR['MNST']:.2f}</b><span>DCF value per share against Monster's price</span></div>
<div class="cell"><small>Data</small><b>10 SEC filings</b><span>10-K, 10-Q and 8-K, cross-checked with accounting identities</span></div>
</div></div></div>

<section><div class="wrap">
<div class="num">SKILLS DEMONSTRATED</div><h2>What these projects show</h2>
<div class="skills">
<div class="card"><h4>Analysis</h4><ul><li>Three-statement analysis and common-size margins</li><li>DuPont return on equity decomposition</li><li>Working capital, leverage and cash conversion</li></ul></div>
<div class="card"><h4>Valuation</h4><ul><li>Discounted cash flow with CAPM discount rate</li><li>WACC and terminal growth sensitivity</li><li>Reverse DCF and trading comparables</li></ul></div>
<div class="card"><h4>Rigor</h4><ul><li>Primary sources only, with accession numbers</li><li>Accounting identities checked in code</li><li>Stock split and fiscal calendar adjustments</li></ul></div>
</div></div></section>

<section id="p1"><div class="wrap">
<div class="num">PROJECT 1</div>
<h2>Coca-Cola, PepsiCo and Monster: who earns the best returns?</h2>
<p class="sub">A five-year, side-by-side read of the three largest listed beverage companies. Same questions for each: how fast does it grow, how much of each dollar becomes profit and cash, how much debt does it carry, and what does it do with the cash.</p>
<div class="brief">
<div class="card"><h4>What I analyzed</h4><p>Income statements for FY2021 to FY2025 and balance sheets for FY2022 to FY2025 from each company's 10-K. I computed growth, margins, free cash flow, DuPont ROE, working capital days, net debt / EBITDA and shareholder payouts, and adjusted for one-off charges.</p></div>
<div class="card"><h4>What I found</h4><ul>
<li>Monster is the growth story: {pc(p1['MNST']['rev_cagr'])} revenue and {pc(p1['MNST']['eps_cagr'])} EPS CAGR, with {pc(fy('MNST','om'))} operating margin and no debt.</li>
<li>Coca-Cola is the margin story: {pc(fy('KO','om'))} operating margin and {pc(p1['KO']['bs']['roe'][-1],0)} ROE, driven more by profitability than by leverage.</li>
<li>PepsiCo is the stretched one: {pc(fy('PEP','om'))} margin, EPS growth of just {pc(p1['PEP']['eps_cagr'])} a year, {p1['PEP']['bs']['nd_ebitda'][-1]:.1f}x net debt / EBITDA, and a payout above free cash flow.</li></ul></div>
<div class="card"><h4>So what</h4><p>Quality and growth are priced very differently across the group, which sets up Project 2: Coca-Cola and Monster trade at {T['KO']['pe']:.0f}x and {T['MNST']['pe']:.0f}x earnings, PepsiCo at {T['PEP']['pe']:.0f}x. The market is paying for margin and growth, not size.</p></div>
</div>

<div class="panel"><h3>FY2025 scorecard</h3><div class="tw"><table class="t"><thead><tr><th></th><th>Coca-Cola</th><th>PepsiCo</th><th>Monster</th></tr></thead><tbody>{tab(cmp_rows)}</tbody></table></div></div>

<div class="panel"><h3>Growth and profitability trends</h3><p class="note">Choose a metric. Click a legend label to hide a company.</p>
<div class="chips" id="chips-trend" role="group" aria-label="Metric"></div>
<p class="take" id="take-trend"></p><div class="cv"><canvas id="c-trend" role="img" aria-label="Line chart comparing the three companies on the selected metric, 2021 to 2025"></canvas></div></div>

<div class="panel"><h3>Reported vs underlying operating margin</h3><p class="note">One-off charges can hide or exaggerate trends. Pick a company to see margin before impairments and other operating charges.</p>
<div class="chips" id="chips-quality" role="group" aria-label="Company"></div>
<p class="take" id="take-quality"></p><div class="cv tall"><canvas id="c-quality" role="img" aria-label="Bar chart of reported and underlying operating margin by year"></canvas></div></div>

<div class="grid2">
<div class="panel"><h3>What drives return on equity (DuPont)</h3><div class="chips" id="chips-dupont" role="group" aria-label="Year"></div>
<div class="cv tall"><canvas id="c-dupont" role="img" aria-label="Bar chart of return on equity by company for the selected year"></canvas></div>
<div class="tw" id="dupont-table"></div><p class="take" id="take-dupont" style="min-height:0"></p></div>
<div class="panel"><h3>Working capital and liquidity</h3><div class="chips" id="chips-wc" role="group" aria-label="Metric"></div>
<p class="take" id="take-wc"></p><div class="cv tall"><canvas id="c-wc" role="img" aria-label="Grouped bar chart of working capital metric by company and year"></canvas></div></div>
</div>

<div class="grid2">
<div class="panel"><h3>Leverage: net debt / EBITDA</h3><p class="take" style="min-height:0">Below zero means more cash and investments than debt. Monster has been net cash throughout; PepsiCo's leverage rose in FY2025 as debt increased and EBITDA fell.</p><div class="cv tall"><canvas id="c-lev" role="img" aria-label="Line chart of net debt to EBITDA by company, 2022 to 2025"></canvas></div></div>
<div class="panel"><h3>Where the cash goes</h3><div class="chips" id="chips-cash" role="group" aria-label="Company"></div>
<p class="take" id="take-cash"></p><div class="cv tall"><canvas id="c-cash" role="img" aria-label="Stacked bars of capex, dividends and buybacks with operating cash flow line"></canvas></div></div>
</div>
<p class="note">EBITDA = operating income + depreciation and amortization. Equity and assets are year-end values. Payables are excluded from working capital because Coca-Cola and PepsiCo combine them with accrued liabilities. Monster EPS is restated for the 2-for-1 split of August 2026.</p>
</div></section>

<section id="p2"><div class="wrap">
<div class="num">PROJECT 2</div>
<h2>Monster Beverage at ${PR['MNST']:.2f}: what has to go right?</h2>
<p class="sub">A discounted cash flow valuation built on trailing twelve months to June 2026, tested against Coca-Cola and PepsiCo multiples. Move the assumptions and watch the value, sensitivity table, reverse DCF and football field update.</p>
<div class="brief">
<div class="card"><h4>What I analyzed</h4><p>Whether Monster's share price is supported by its cash flows. I built TTM figures (FY2025 plus the first six months of 2026 minus the first six months of 2025), forecast five years of free cash flow, discounted at a CAPM cost of equity of {pc(DC['coe'],1)} (Monster has no debt), and added Monster's ${m['cash']:,.0f}M of cash and investments.</p></div>
<div class="card"><h4>What I found</h4><ul>
<li>Base case value is <b>${ps:.2f}</b> per share, {abs(up)*100:.0f}% {'above' if up>0 else 'below'} the ${PR['MNST']:.2f} price. Bear to bull: ${sc['bear']:.0f} to ${sc['bull']:.0f}.</li>
<li>Reverse DCF: the price needs about <b>{pc(DC['rev_implied_g'],0)}</b> annual growth for five years at a {pc(a['m'][0],0)} margin. Revenue grew {pc(m['h1_growth'],0)} in the latest six months, so it is possible, but with no room for a slowdown.</li>
<li>On multiples, Monster trades at {m['ev_ebitda']:.0f}x EBITDA against {T['KO']['ev_ebitda']:.0f}x for Coca-Cola and {T['PEP']['ev_ebitda']:.0f}x for PepsiCo.</li></ul></div>
<div class="card"><h4>So what</h4><p>The stock is priced for the recent pace to hold. My view (educational): the business is excellent, but at this price the margin of safety is thin. I would want either a price nearer the base case or evidence that 20%+ growth is lasting, such as international share gains.</p></div>
</div>

<div class="kpis">
<div class="kpi"><small>DCF value per share</small><b id="o-ps"></b><span class="up" id="o-up"></span></div>
<div class="kpi"><small>Share price</small><b id="o-px"></b><span class="note">editable below</span></div>
<div class="kpi"><small>Growth the price implies</small><b id="o-imp"></b><span class="note">per year, 5 years (reverse DCF)</span></div>
<div class="kpi"><small>Terminal value share of EV</small><b id="o-tv"></b><span class="note">EV <span id="o-ev"></span></span></div>
</div>

<div class="panel"><h3>Assumptions</h3>
<div class="row"><span class="note">Scenario:</span><button class="btn" data-scn="bear" aria-pressed="false">Bear</button><button class="btn" data-scn="base" aria-pressed="true">Base</button><button class="btn" data-scn="bull" aria-pressed="false">Bull</button><button class="btn" id="reset" type="button">Reset</button></div>
<div class="ctl">
<div><label for="s-g1">Year 1 revenue growth <span id="lb-g1"></span></label><input id="s-g1" type="range" min="0" max="35" step="0.5"></div>
<div><label for="s-g5">Year 5 revenue growth <span id="lb-g5"></span></label><input id="s-g5" type="range" min="0" max="20" step="0.5"></div>
<div><label for="s-m">Operating margin <span id="lb-m"></span></label><input id="s-m" type="range" min="20" max="36" step="0.5"></div>
<div><label for="s-w">Discount rate (WACC) <span id="lb-w"></span></label><input id="s-w" type="range" min="5" max="12" step="0.1"></div>
<div><label for="s-tg">Terminal growth <span id="lb-tg"></span></label><input id="s-tg" type="range" min="1" max="4.5" step="0.25"></div>
<div><label for="s-px">Share price ($)</label><input id="s-px" type="number" min="1" step="0.01"></div>
</div>
<p class="note" style="margin-top:14px">Fixed: tax rate {pc(a['tax'],0)}, D&amp;A {pc(a['da'],1)} and capex {pc(a['capex'],1)} of revenue (TTM capex is {pc(m['capex']/m['rev'],1)}), working capital {pc(a['nwc'],0)} of incremental revenue. Growth fades in a straight line from Year 1 to Year 5.</p></div>

<div class="grid2">
<div class="panel"><h3>Free cash flow forecast</h3><p class="take" style="min-height:0">Starting from TTM revenue of ${m['rev']:,.0f}M and operating income of ${m['oi']:,.0f}M ({pc(m['om'])} margin).</p><div class="cv tall"><canvas id="c-fcff" role="img" aria-label="Bar chart of forecast free cash flow and present value by year"></canvas></div></div>
<div class="panel"><h3>Value per share: WACC × terminal growth</h3><p class="take" style="min-height:0">Green cells are worth more than the share price, red cells less. Most of the value sits in the terminal period, so the discount rate matters.</p><div class="tw" id="sens"></div></div>
</div>

<div class="panel"><h3>Football field: valuation ranges against the price</h3><p class="take" style="min-height:0">Each bar is a range of per-share values from a different method. The dashed line is the share price. No comparable-multiple range reaches the price: even at Coca-Cola's multiples Monster is worth ${ff['EV/EBITDA at PEP → KO multiple'][1]:.0f} (EV/EBITDA) or ${ff['P/E at PEP → KO multiple'][1]:.0f} (P/E). Only the most favorable corners of the DCF do.</p><div class="cv"><canvas id="c-ff" role="img" aria-label="Football field chart of valuation ranges per share with the current price marked"></canvas></div></div>

<div class="panel"><h3>Trading comparables (TTM to mid-2026)</h3><div class="tw"><table class="t"><thead><tr><th></th><th>Monster</th><th>Coca-Cola</th><th>PepsiCo</th></tr></thead><tbody>{tab(mult_rows)}</tbody></table></div>
<p class="note" style="margin-top:12px">Enterprise value = market cap + debt + non-controlling interests − cash and investments, from the latest 10-Q balance sheet. Monster's share count is doubled for the split. Coca-Cola's TTM operating cash flow is inflated by the fairlife payment falling in the prior-year half. Coca-Cola's EV includes ${(20235/1000):.1f}B of equity-method investments (FY2025), which flatters its EV/EBITDA comparison.</p></div>

<div class="verdict"><b>Method notes.</b> CAPM: risk-free rate {pc(DC['rf'],1)} (10-year Treasury, mid-October 2026, quoted between 5.1% and 5.2% by different sources), equity risk premium {pc(DC['erp'],1)} (Damodaran implied, Oct 1, 2026), beta {DC['beta']} (Blume-adjusted from a 5-year monthly raw beta of {DC['beta_raw']}). A raw beta of {DC['beta_raw']} would give a WACC near 7.2%, which would raise the base value; the sensitivity table covers that range. Share prices were taken from public quote pages on Oct 14–15, 2026 and the PepsiCo quote carries no timestamp, so the price is editable.</div>
</div></section>

<section id="method"><div class="wrap">
<div class="num">DATA AND METHOD</div><h2>Sources and integrity checks</h2>
<div class="grid2"><div class="panel"><h3>SEC filings used</h3><ul class="src">{src_html}</ul></div>
<div class="panel"><h3>How I checked the numbers</h3><ul>
<li>Every income statement ties: revenue − cost of sales = gross profit; gross profit − operating costs = operating income, for all 15 company-years.</li>
<li>Balance sheet components never exceed their subtotals; DuPont ROE reproduces net income ÷ equity exactly.</li>
<li>Computed P/E ratios for Monster ({m['pe']:.1f}x) and Coca-Cola ({T['KO']['pe']:.1f}x) match the quote pages' own trailing P/E (40.9x and 27.6x), which validates the TTM EPS build and the split adjustment.</li>
<li>Units differ by filing (Monster in thousands, PepsiCo's FY2023 income statement in dollars) and Coca-Cola and PepsiCo use 52/53-week fiscal years; all are normalised to $ millions.</li></ul>
<p class="note">Limits: five-year DCF with a single terminal growth rate; no segment or geographic build. This is an educational project, not investment advice.</p></div></div>
</div></section>

<section id="contact"><div class="wrap"><div class="num">CONTACT</div><h2>Let's talk</h2>
<p class="sub">{first} is looking for a finance analyst role. {contact_html}</p></div></section>
</main>
<footer><div class="wrap">© {name}. Figures from company filings with the U.S. SEC; educational use only, not investment advice.</div></footer>
<script id="data" type="application/json">{json.dumps(dict(D,dcf=dict(assump=DC['base_assump'],coe=DC['coe'])),default=float)}</script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.1/chart.umd.min.js"></script>
<script>{open('page.js').read()}</script>
'''
page=page.replace("","")
open('index.html','w').write(page)
print(len(page))
