// Bot de balance: solo se carga con ?bot en la URL. Uso en consola: botRuns(15)
(function(){
const R=window.__ramal;
const per=t=>R.lapRun(t,R.S.track);
function botShop(S){
  let bt=null,bv=R.lapRun(S.train,S.track);
  S.tileOffer.forEach(k=>{for(let i=0;i<8;i++){const t=S.track.slice();t[i]={k};const v=R.lapRun(S.train,t);if(v>bv){bv=v;bt={k,i}}}});
  if(bt){S.tilePick=bt.k;R.placeTile(bt.i)}
  for(let guard=0;guard<12;guard++){
    let best=null,b=per(S.train);
    S.shop.forEach((o,i)=>{if(o.bought)return;if(Math.max(1,R.DEFS[o.k].p-S.discount)>S.money)return;
      const ow=R.owned(o.k);let t;
      if(ow)t=S.train.map(w=>w===ow?{...w,lv:(w.lv||1)+1}:w);
      else if(S.train.length-1<S.slots){const w={k:o.k,s:{}};R.DEFS[o.k].init&&R.DEFS[o.k].init(w);t=[...S.train,w]}
      else return;
      const v=per(t);if(v>b*1.02){best=i;b=v}});
    if(best===null){
      if(S.slots<7&&S.money>=S.expand+4){S.money-=S.expand;S.slots++;S.expand+=5;continue}
      if(S.money>=S.reroll+8){S.money-=S.reroll;S.reroll++;R.rollShop(false);continue}
      break}
    R.buy(best);
  }
  let imp=true,n=0;while(imp&&n++<6){imp=false;const b=per(S.train);for(let a=1;a<S.train.length;a++)for(let c=a+1;c<S.train.length;c++){const t=S.train.slice();[t[a],t[c]]=[t[c],t[a]];if(per(t)>b*1.0001){S.train.splice(0,S.train.length,...t);imp=true}}}
}
window.botRuns=function(N=15){
  const saved=JSON.stringify(R.meta);R.meta.muted=true;R.meta.open=[];R.meta.best=0;
  const results=[],ratios={};let maxTot=0,maxEv=0,info='';const t0=performance.now();
  for(let run=0;run<N&&performance.now()-t0<30000;run++){
    R.newRun();
    while(true){
      const S=R.S;
      while(S.nextSt<S.nst){S.phase='travel';S.combo=0;R.startEval();
        if(S.phase==='eval'){maxEv=Math.max(maxEv,S.ev.length);
          while(S.ev.length){const e=S.ev.shift();if(e.total!==undefined&&e.total>maxTot){maxTot=e.total;info=S.track.map(t=>t?t.k:'_').join(',')+' | '+S.train.map(w=>w.k+(w.lv>1?w.lv:'')).join(',')}R.evStep(e)}}}
      (ratios[S.lap]=ratios[S.lap]||[]).push(+(S.lapScore/S.quota).toFixed(2));
      S.phase='travel';R.endLap();
      if(S.phase==='over'){results.push(S.lap);break}
      botShop(S);
      R.beginLap(S.routes.find(r=>r.k==='principal')||S.routes[0]);
      if(S.lap>40){results.push(40);break}
    }
  }
  document.querySelector('#ovl').style.display='none';
  const med={};Object.keys(ratios).forEach(l=>{const a=ratios[l].sort((x,y)=>x-y);med[l]=a[Math.floor(a.length/2)]});
  Object.assign(R.meta,JSON.parse(saved));try{localStorage.setItem('el-ramal-meta',saved)}catch(e){}
  return {laps:results.join(' '),maxTot,maxEv,info,med,ms:Math.round(performance.now()-t0)};
};
})();
