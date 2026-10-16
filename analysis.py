import json
from data import *
PRICES = {"MNST":44.22,"KO":91.95,"PEP":129.27}
RF, ERP, BETA_RAW = 0.051, 0.042, 0.49
BETA = round(0.67*BETA_RAW+0.33,2)           # Blume-adjusted
COE = RF + BETA*ERP                           # no debt -> WACC = cost of equity
def cagr(a,b,n): return (b/a)**(1/n)-1
R = {"years":Y}
P1 = {}
for c in COS:
    t=c['tk']; d={}
    d['rev']=c['rev']; d['rev_cagr']=cagr(c['rev'][0],c['rev'][-1],4)
    d['gm']=[c['gp'][i]/c['rev'][i] for i in range(5)]
    d['om']=[c['oi'][i]/c['rev'][i] for i in range(5)]
    d['nm']=[c['ni'][i]/c['rev'][i] for i in range(5)]
    d['fcf']=[c['ocf'][i]-c['capex'][i] for i in range(5)]
    d['fcf_margin']=[d['fcf'][i]/c['rev'][i] for i in range(5)]
    d['capex_int']=[c['capex'][i]/c['rev'][i] for i in range(5)]
    d['cash_conv']=[d['fcf'][i]/c['ni'][i] for i in range(5)]
    d['eps']=c['eps'] if t!="MNST" else [round(e/2,3) for e in c['eps']]
    d['eps_cagr']=cagr(d['eps'][0],d['eps'][-1],4)
    d['oi']=c['oi']; d['ni']=c['ni']; d['ebitda']=[c['oi'][i]+c['da'][i] for i in range(5)]
    d['payout_div']=[c['div'][i]/c['ni'][i] for i in range(5)]
    d['shareholder_ret']=[c['div'][i]+c['bb'][i] for i in range(5)]
    # balance sheet metrics 2022-2025 (index j -> year idx j+1)
    b={}
    b['dso']=[c['ar'][j]/c['rev'][j+1]*365 for j in range(4)]
    b['dio']=[c['inv'][j]/c['cogs'][j+1]*365 for j in range(4)]
    b['cur']=[c['tca'][j]/c['tcl'][j] for j in range(4)]
    b['cash_tot']=[c['cash'][j]+c['sti'][j] for j in range(4)]
    b['net_debt']=[c['debt'][j]-b['cash_tot'][j] for j in range(4)]
    b['nd_ebitda']=[b['net_debt'][j]/d['ebitda'][j+1] for j in range(4)]
    b['at']=[c['rev'][j+1]/c['ta'][j] for j in range(4)]          # asset turnover (year-end assets)
    b['em']=[c['ta'][j]/c['eq'][j] for j in range(4)]
    b['nm']=d['nm'][1:]
    b['roe']=[b['nm'][j]*b['at'][j]*b['em'][j] for j in range(4)]
    assert all(abs(b['roe'][j]-c['ni'][j+1]/c['eq'][j])<1e-9 for j in range(4))
    d['bs']=b; P1[t]=d
R['p1']=P1
# ---- TTM
TTM={}
for c in COS:
    t=c['tk']; h=H[t]; f=lambda key,fy: fy+h[key][0]-h[key][1]
    ttm=dict(rev=f('rev',c['rev'][-1]), oi=f('oi',c['oi'][-1]), da=f('da',c['da'][-1]), ni=f('ni',c['ni'][-1]),
             eps=f('eps',c['eps'][-1] if t!="MNST" else c['eps'][-1]/2), ocf=f('ocf',c['ocf'][-1]), capex=f('capex',c['capex'][-1]))
    ttm['ebitda']=ttm['oi']+ttm['da']; ttm['fcf']=ttm['ocf']-ttm['capex']
    ttm['h1_growth']=h['rev'][0]/h['rev'][1]-1
    b=h['bs']; px=PRICES[t]
    ttm['price']=px; ttm['mcap']=px*b['sh']; ttm['ev']=ttm['mcap']+b['debt']+b['mi']-b['cash']-b['inv_sec']
    ttm['pe']=px/ttm['eps']; ttm['ev_ebitda']=ttm['ev']/ttm['ebitda']; ttm['ev_sales']=ttm['ev']/ttm['rev']
    ttm['om']=ttm['oi']/ttm['rev']; ttm['fcf_yield']=ttm['fcf']/ttm['mcap']; ttm['shares']=b['sh']
    ttm['cash']=b['cash']+b['inv_sec']; ttm['debt']=b['debt']; ttm['mi']=b['mi']
    TTM[t]=ttm
R['ttm']=TTM
# ---- DCF
def dcf(a):
    rev=a['rev0']; pv=0; rows=[]; fcff=0
    for i in range(5):
        rev*=1+a['g'][i]; m=a['m'][i]
        ebit=rev*m; nopat=ebit*(1-a['tax']); prev=rev/(1+a['g'][i])
        reinv_nwc=(rev-prev)*a['nwc']
        fcff=nopat+rev*a['da']-rev*a['capex']-reinv_nwc
        df=1/(1+a['wacc'])**(i+1); pv+=fcff*df
        rows.append(dict(rev=rev,ebit=ebit,nopat=nopat,fcff=fcff,pv=fcff*df))
    tv=fcff*(1+a['tg'])/(a['wacc']-a['tg']); pvtv=tv/(1+a['wacc'])**5
    ev=pv+pvtv; eq=ev+a['cash']-a['debt']
    return dict(rows=rows,pv=pv,tv=tv,pvtv=pvtv,ev=ev,eq=eq,ps=eq/a['shares'])
m=TTM['MNST']
fade=lambda a,b:[a+(b-a)*i/4 for i in range(5)]
BASE=dict(rev0=m['rev'], g=fade(0.15,0.06), m=[0.29]*5, tax=0.24, da=0.013, capex=0.016, nwc=0.15,
          wacc=COE, tg=0.03, cash=m['cash'], debt=0, shares=m['shares'])
base=dcf(BASE)
print('beta',BETA,'coe',COE, 'base ps',base['ps'], 'ev',base['ev'], 'tv share',base['pvtv']/base['ev'])
# sensitivity
waccs=[COE-0.01+0.005*i for i in range(5)]; tgs=[0.02,0.025,0.03,0.035,0.04]
sens=[[dcf({**BASE,'wacc':w,'tg':g})['ps'] for g in tgs] for w in waccs]
# reverse DCF: uniform growth multiplier on years 1-5 that matches price
lo,hi=-0.5,3.0
for _ in range(80):
    mid=(lo+hi)/2; g=[0.15*mid/0.15]*0  # placeholder
    gg=[x*(1+mid) if False else x for x in BASE['g']]
    # solve a flat 5y growth rate g that gives price
    break
def flat(gr): return dcf({**BASE,'g':[gr]*5})['ps']
lo,hi=-0.1,0.6
for _ in range(80):
    mid=(lo+hi)/2
    if flat(mid)<PRICES['MNST']: lo=mid
    else: hi=mid
rev_g=(lo+hi)/2
print('implied flat 5y growth',rev_g)
# scenarios
bear={**BASE,'g':fade(0.10,0.05),'m':[0.275]*5,'tg':0.025}
bull={**BASE,'g':fade(0.20,0.08),'m':[0.31]*5,'tg':0.035}
scen={k:dcf(v)['ps'] for k,v in dict(bear=bear,base=BASE,bull=bull).items()}
print(scen, sens[2][2])
# football field
e=m['ebitda']; sh=m['shares']; cash=m['cash']
def ev_ps(mult): return (mult*e+cash)/sh
ff={'DCF sensitivity (WACC ±1%, g 2–4%)':[min(map(min,sens)),max(map(max,sens))],
    'DCF scenarios (bear → bull)':[scen['bear'],scen['bull']],
    'EV/EBITDA at PEP → KO multiple':[ev_ps(TTM['PEP']['ev_ebitda']),ev_ps(TTM['KO']['ev_ebitda'])],
    'P/E at PEP → KO multiple':[TTM['PEP']['pe']*m['eps'],TTM['KO']['pe']*m['eps']]}
print(ff)
R['dcf']=dict(base_assump=BASE,base=base,sens=sens,waccs=waccs,tgs=tgs,rev_implied_g=rev_g,scen=scen,ff=ff,
              rf=RF,erp=ERP,beta_raw=BETA_RAW,beta=BETA,coe=COE)
json.dump(R,open('results.json','w'),indent=1,default=float)
for t in TTM: print(t,{k:round(v,2) for k,v in TTM[t].items()})
for t in P1: print(t,'cagr',round(P1[t]['rev_cagr'],3),'eps',round(P1[t]['eps_cagr'],3),'nd/ebitda',[round(x,2) for x in P1[t]['bs']['nd_ebitda']],'roe',[round(x,3) for x in P1[t]['bs']['roe']])
