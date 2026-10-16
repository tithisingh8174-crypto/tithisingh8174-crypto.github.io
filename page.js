(function(){
'use strict';
var D = JSON.parse(document.getElementById('data').textContent);
var $ = function(s,r){return (r||document).querySelector(s)};
var $$ = function(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))};
var CO = ['KO','PEP','MNST'];
var NAMES = {KO:'Coca-Cola',PEP:'PepsiCo',MNST:'Monster'};
var charts = {};

function css(v){return getComputedStyle(document.documentElement).getPropertyValue(v).trim()}
function col(t){return css('--c-'+t.toLowerCase())}
var POINT = {KO:'circle',PEP:'rect',MNST:'triangle'};
var DASH = {KO:[],PEP:[7,4],MNST:[2,3]};
function pct(x,d){return (x*100).toFixed(d==null?1:d)+'%'}
function usd(x,d){return '$'+x.toFixed(d==null?2:d)}
function bn(x){return '$'+(x/1000).toFixed(1)+'B'}

/* ---------- chart plumbing ---------- */

function base(){
  var C=window.Chart; if(!C) return;
  C.defaults.font.family="'IBM Plex Sans',system-ui,sans-serif";
  C.defaults.font.size=12; C.defaults.color=css('--muted');
  C.defaults.borderColor=css('--rule');
}
function mk(id,cfg){
  if(!window.Chart) return;
  if(charts[id]) charts[id].destroy();
  cfg.options=cfg.options||{}; cfg.options.maintainAspectRatio=false;
  charts[id]=new Chart(document.getElementById(id),cfg);
}
function ds(t,data,extra){
  return Object.assign({label:NAMES[t],data:data,borderColor:col(t),backgroundColor:col(t),pointStyle:POINT[t],
    pointRadius:5,pointHoverRadius:7,borderWidth:2.5,borderDash:DASH[t],tension:.2},extra||{});
}
function scale(fmt,extra){return Object.assign({grid:{color:css('--rule')},ticks:{callback:fmt}},extra||{})}
function chips(root,items,cb,initial){
  root.innerHTML=''; var cur=initial==null?0:initial;
  items.forEach(function(it,i){
    var b=document.createElement('button'); b.type='button'; b.className='chip'; b.textContent=it.label;
    b.setAttribute('aria-pressed',i===cur); b.onclick=function(){
      $$('button',root).forEach(function(x,j){x.setAttribute('aria-pressed',j===i)}); cb(it,i)};
    root.appendChild(b);
  });
  cb(items[cur],cur);
}

var saved=null; try{saved=localStorage.getItem('th')}catch(e){}
var dark=window.matchMedia&&matchMedia('(prefers-color-scheme: dark)').matches;
document.documentElement.setAttribute('data-theme',saved||(dark?'dark':'light'));
base();

/* ---------- Project 1 ---------- */
var P=D.p1, Y=D.years;
function idx(a){return a.map(function(v){return v/a[0]*100})}
var METRICS=[
  {label:'Revenue (2021 = 100)',k:'revidx',f:function(t){return idx(P[t].rev)},fmt:function(v){return v.toFixed(0)}},
  {label:'EPS (2021 = 100)',k:'epsidx',f:function(t){return idx(P[t].eps)},fmt:function(v){return v.toFixed(0)}},
  {label:'Gross margin',k:'gm',f:function(t){return P[t].gm},fmt:pct},
  {label:'Operating margin',k:'om',f:function(t){return P[t].om},fmt:pct},
  {label:'Net margin',k:'nm',f:function(t){return P[t].nm},fmt:pct},
  {label:'Free cash flow margin',k:'fcf_margin',f:function(t){return P[t].fcf_margin},fmt:pct},
  {label:'Capex % of revenue',k:'capex_int',f:function(t){return P[t].capex_int},fmt:pct}
];
chips($('#chips-trend'),METRICS,function(m){
  $('#take-trend').textContent=D.insights[m.k];
  mk('c-trend',{type:'line',data:{labels:Y,datasets:CO.map(function(t){return ds(t,m.f(t))})},
   options:{interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{usePointStyle:true}},
    tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+m.fmt(c.parsed.y)}}}},
    scales:{x:{grid:{display:false}},y:scale(function(v){return m.fmt(v)})}}});
});

chips($('#chips-quality'),CO.map(function(t){return {label:NAMES[t],t:t}}),function(it){
  var t=it.t,p=P[t];
  $('#take-quality').textContent=D.quality[t];
  mk('c-quality',{type:'bar',data:{labels:Y,datasets:[
    {label:'Reported operating margin',data:p.om,backgroundColor:col(t)},
    {label:'Before impairments & other operating charges',data:p.om_adj,backgroundColor:css('--rule-strong')}]},
   options:{plugins:{legend:{labels:{usePointStyle:true}},tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+pct(c.parsed.y)}}}},
    scales:{x:{grid:{display:false}},y:scale(function(v){return pct(v,0)},{min:0})}}});
});

chips($('#chips-dupont'),[2022,2023,2024,2025].map(function(y,i){return {label:String(y),i:i}}),function(it){
  var i=it.i;
  mk('c-dupont',{type:'bar',data:{labels:CO.map(function(t){return NAMES[t]}),datasets:[{label:'ROE',
    data:CO.map(function(t){return P[t].bs.roe[i]}),backgroundColor:CO.map(col)}]},
   options:{indexAxis:'y',plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return 'ROE '+pct(c.parsed.x)}}}},
    scales:{x:scale(function(v){return pct(v,0)},{min:0}),y:{grid:{display:false}}}}});
  var h='<table class="t"><thead><tr><th></th><th>Net margin</th><th class="x">×</th><th>Asset turnover</th><th class="x">×</th><th>Equity multiplier</th><th class="x">=</th><th>ROE</th></tr></thead><tbody>';
  CO.forEach(function(t){var b=P[t].bs;
    h+='<tr><th scope="row">'+NAMES[t]+'</th><td>'+pct(b.nm[i])+'</td><td class="x">×</td><td>'+b.at[i].toFixed(2)+'x</td><td class="x">×</td><td>'+b.em[i].toFixed(2)+'x</td><td class="x">=</td><td><b>'+pct(b.roe[i])+'</b></td></tr>'});
  $('#dupont-table').innerHTML=h+'</tbody></table>';
  $('#take-dupont').textContent=D.dupont[i];
});

var WCM=[{label:'Days sales outstanding',k:'dso',fmt:function(v){return v.toFixed(0)+' days'}},
  {label:'Days inventory',k:'dio',fmt:function(v){return v.toFixed(0)+' days'}},
  {label:'Current ratio',k:'cur',fmt:function(v){return v.toFixed(2)+'x'}}];
chips($('#chips-wc'),WCM,function(m){
  $('#take-wc').textContent=D.wc[m.k];
  mk('c-wc',{type:'bar',data:{labels:[2022,2023,2024,2025],datasets:CO.map(function(t){return {label:NAMES[t],data:P[t].bs[m.k],backgroundColor:col(t)}})},
   options:{plugins:{legend:{labels:{usePointStyle:true}},tooltip:{callbacks:{label:function(c){return c.dataset.label+': '+m.fmt(c.parsed.y)}}}},
    scales:{x:{grid:{display:false}},y:scale(function(v){return m.k==='cur'?v.toFixed(1):v},{beginAtZero:true})}}});
});

drawLev();

chips($('#chips-cash'),CO.map(function(t){return {label:NAMES[t],t:t}}),function(it){
  var t=it.t,p=P[t];
  $('#take-cash').textContent=D.cash[t];
  mk('c-cash',{data:{labels:Y,datasets:[
    {type:'bar',label:'Capex',data:p.capex,backgroundColor:css('--rule-strong'),stack:'u'},
    {type:'bar',label:'Dividends',data:p.div,backgroundColor:col(t),stack:'u'},
    {type:'bar',label:'Buybacks',data:p.bb,backgroundColor:css('--accent-soft'),stack:'u'},
    {type:'line',label:'Operating cash flow',data:p.ocf,borderColor:css('--ink'),backgroundColor:css('--ink'),borderWidth:2.5,pointStyle:'rectRot',pointRadius:5,tension:.15}]},
   options:{interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{usePointStyle:true}},
    tooltip:{callbacks:{label:function(c){return c.dataset.label+': $'+Math.round(c.parsed.y).toLocaleString()+'M'}}}},
    scales:{x:{stacked:true,grid:{display:false}},y:scale(function(v){return '$'+(v/1000)+'B'},{stacked:true,beginAtZero:true})}}});
});

/* ---------- Project 2: live DCF ---------- */
var A=D.dcf.assump, price=D.price;
var S={g1:A.g[0],g5:A.g[4],m:A.m[0],w:D.dcf.coe,tg:A.tg,px:price};
var SC={bear:{g1:.10,g5:.05,m:.275,tg:.025},base:{g1:A.g[0],g5:A.g[4],m:A.m[0],tg:A.tg},bull:{g1:.20,g5:.08,m:.31,tg:.035}};
function dcf(s,over){
  var o=Object.assign({},s,over||{}), rev=A.rev0, pv=0, rows=[], f=0;
  for(var i=0;i<5;i++){
    var g=o.g1+(o.g5-o.g1)*i/4, prev=rev; rev=rev*(1+g);
    var nopat=rev*o.m*(1-A.tax); f=nopat+rev*A.da-rev*A.capex-(rev-prev)*A.nwc;
    var df=1/Math.pow(1+o.w,i+1); pv+=f*df; rows.push({rev:rev,g:g,fcff:f,pv:f*df});
  }
  var tv=f*(1+o.tg)/(o.w-o.tg), pvtv=tv/Math.pow(1+o.w,5), ev=pv+pvtv, eq=ev+A.cash-A.debt;
  return {rows:rows,pv:pv,pvtv:pvtv,ev:ev,eq:eq,ps:eq/A.shares};
}
function implied(s){
  var lo=-.2,hi=1,t=s.px;
  for(var i=0;i<60;i++){var mid=(lo+hi)/2; if(dcf(s,{g1:mid,g5:mid}).ps<t) lo=mid; else hi=mid}
  return (lo+hi)/2;
}
function setOut(id,v){$('#'+id).textContent=v}
function recalc(){
  var r=dcf(S), up=r.ps/S.px-1;
  setOut('o-ps',usd(r.ps)); setOut('o-px',usd(S.px));
  var u=$('#o-up'); u.textContent=(up>=0?'+':'')+(up*100).toFixed(0)+'% '+(up>=0?'above':'below')+' price'; u.className='up '+(up>=0?'pos':'neg');
  setOut('o-ev',bn(r.ev)); setOut('o-tv',pct(r.pvtv/r.ev,0));
  var im=implied(S); setOut('o-imp',pct(im,1)); 
    var m=D.ttm.MNST;
  $('#lb-g1').textContent=pct(S.g1,1); $('#lb-g5').textContent=pct(S.g5,1); $('#lb-m').textContent=pct(S.m,1);
  $('#lb-w').textContent=pct(S.w,2); $('#lb-tg').textContent=pct(S.tg,1);
  /* fcff chart */
  mk('c-fcff',{type:'bar',data:{labels:r.rows.map(function(_,i){return 'Year '+(i+1)}),datasets:[
    {label:'Free cash flow to firm',data:r.rows.map(function(x){return x.fcff}),backgroundColor:css('--accent')},
    {label:'Present value',data:r.rows.map(function(x){return x.pv}),backgroundColor:css('--rule-strong')}]},
   options:{plugins:{legend:{labels:{usePointStyle:true}},tooltip:{callbacks:{
     afterTitle:function(it){var x=r.rows[it[0].dataIndex];return 'Revenue $'+Math.round(x.rev).toLocaleString()+'M, growth '+pct(x.g)},
     label:function(c){return c.dataset.label+': $'+Math.round(c.parsed.y).toLocaleString()+'M'}}}},
    scales:{x:{grid:{display:false}},y:scale(function(v){return '$'+(v/1000)+'B'},{beginAtZero:true})}}});
  /* sensitivity */
  var ws=[-.01,-.005,0,.005,.01].map(function(d){return S.w+d}), gs=[.02,.025,.03,.035,.04];
  var h='<table class="t heat"><thead><tr><th>WACC ↓ &nbsp; Terminal growth →</th>'+gs.map(function(g){return '<th>'+pct(g,1)+'</th>'}).join('')+'</tr></thead><tbody>';
  var lo=1e9,hi=-1e9;
  ws.forEach(function(w){h+='<tr><th scope="row">'+pct(w,2)+'</th>'+gs.map(function(g){
    var v=dcf(S,{w:w,tg:g}).ps; lo=Math.min(lo,v);hi=Math.max(hi,v);
    var d=v/S.px-1, a=Math.min(.55,Math.abs(d)*.9);
    var bg=(d>=0?'rgba(15,132,92,':'rgba(196,60,50,')+a.toFixed(2)+')';
    return '<td style="background:'+bg+'">'+usd(v)+'<small>'+(d>=0?'▲':'▼')+Math.abs(d*100).toFixed(0)+'%</small></td>'}).join('')+'</tr>'});
  $('#sens').innerHTML=h+'</tbody></table>';
  /* football field */
  var e=m.ebitda, sh=m.shares, cash=m.cash;
  function evps(x){return (x*e+cash)/sh}
  var sc={bear:dcf(S,SC.bear).ps,bull:dcf(S,SC.bull).ps};
  var rows=[
   ['DCF: WACC ±1%, terminal growth 2–4%',lo,hi],
   ['DCF: bear to bull scenario',Math.min(sc.bear,sc.bull),Math.max(sc.bear,sc.bull)],
   ['EV/EBITDA at PepsiCo to Coca-Cola multiple',evps(D.ttm.PEP.ev_ebitda),evps(D.ttm.KO.ev_ebitda)],
   ['P/E at PepsiCo to Coca-Cola multiple',D.ttm.PEP.pe*m.eps,D.ttm.KO.pe*m.eps]];
  var pl={id:'pxline',afterDatasetsDraw:function(ch){
    var x=ch.scales.x.getPixelForValue(S.px), a=ch.chartArea, c=ch.ctx;
    c.save(); c.strokeStyle=css('--neg'); c.lineWidth=2; c.setLineDash([5,4]); c.beginPath(); c.moveTo(x,a.top); c.lineTo(x,a.bottom); c.stroke();
    c.setLineDash([]); c.fillStyle=css('--neg'); c.font="600 12px 'IBM Plex Sans'"; c.textAlign='center'; c.fillText('Price '+usd(S.px),x,a.top-6); c.restore();}};
  mk('c-ff',{type:'bar',plugins:[pl],data:{labels:rows.map(function(r){return r[0]}),datasets:[{label:'Value per share',
    data:rows.map(function(r){return [r[1],r[2]]}),backgroundColor:css('--accent'),borderSkipped:false,borderRadius:3,barThickness:26}]},
   options:{indexAxis:'y',layout:{padding:{top:20}},plugins:{legend:{display:false},tooltip:{callbacks:{label:function(c){return usd(c.raw[0])+' to '+usd(c.raw[1])}}}},
    scales:{x:scale(function(v){return '$'+v},{min:0,suggestedMax:Math.max(70,S.px*1.3)}),y:{grid:{display:false},ticks:{callback:function(v){var l=this.getLabelForValue(v);return l.length>34?l.match(/.{1,34}(\s|$)/g).map(function(s){return s.trim()}):l}}}}}});
}
function bind(id,key,scalef){
  var el=$('#'+id); el.addEventListener('input',function(){S[key]=parseFloat(el.value)*(scalef||1);recalc()});
}
function sync(){
  $('#s-g1').value=S.g1*100; $('#s-g5').value=S.g5*100; $('#s-m').value=S.m*100; $('#s-w').value=S.w*100;
  $('#s-tg').value=S.tg*100; $('#s-px').value=S.px;
}
bind('s-g1','g1',.01); bind('s-g5','g5',.01); bind('s-m','m',.01); bind('s-w','w',.01); bind('s-tg','tg',.01);
$('#s-px').addEventListener('input',function(){var v=parseFloat(this.value); if(v>0){S.px=v;recalc()}});
$$('[data-scn]').forEach(function(b){b.onclick=function(){
  var k=b.getAttribute('data-scn'); Object.assign(S,SC[k]); sync(); recalc();
  $$('[data-scn]').forEach(function(x){x.setAttribute('aria-pressed',x===b)})}});
$('#reset').onclick=function(){S={g1:A.g[0],g5:A.g[4],m:A.m[0],w:D.dcf.coe,tg:A.tg,px:price};sync();recalc();
  $$('[data-scn]').forEach(function(x){x.setAttribute('aria-pressed',x.getAttribute('data-scn')==='base')})};

/* ---------- theme ---------- */
var tb=$('#theme');
function setTheme(t){document.documentElement.setAttribute('data-theme',t); try{localStorage.setItem('th',t)}catch(e){}; tb.textContent=t==='dark'?'Light':'Dark'; tb.setAttribute('aria-pressed',t==='dark');
  if(window.Chart){base(); redraw();}}
function redraw(){ $$('.chips').forEach(function(c){var p=$$('button[aria-pressed="true"]',c)[0]; if(p) p.click()}); recalc(); drawLev(); }
function drawLev(){
  mk('c-lev',{type:'line',data:{labels:[2022,2023,2024,2025],datasets:CO.map(function(t){return ds(t,P[t].bs.nd_ebitda)})},
   options:{interaction:{mode:'index',intersect:false},plugins:{legend:{labels:{usePointStyle:true}},
    tooltip:{callbacks:{label:function(c){var v=c.parsed.y;return c.dataset.label+': '+(v<0?'net cash '+Math.abs(v).toFixed(1)+'x EBITDA':v.toFixed(1)+'x EBITDA')}}}},
    scales:{x:{grid:{display:false}},y:scale(function(v){return v+'x'})}}});
}
tb.onclick=function(){setTheme(document.documentElement.getAttribute('data-theme')==='dark'?'light':'dark')};
tb.textContent=document.documentElement.getAttribute('data-theme')==='dark'?'Light':'Dark';
sync(); recalc();
window.__dcf=function(){return dcf(S)};
})();
