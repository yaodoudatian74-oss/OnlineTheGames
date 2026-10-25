import asyncio,time,sys,json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=await b.new_page(viewport={'width':800,'height':450})
    errs=[]
    pg.on('console',lambda m: errs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.on('pageerror',lambda e: errs.append('PAGEERR: '+str(e.stack)[:500]))
    await pg.goto('file:///home/claude/island/local.html?q=low')
    await pg.wait_for_function('window.__ris',timeout=60000)
    E=pg.evaluate
    async def frames(n=2):
      a=await E("__ris.prof.n")
      t=time.time()
      while (await E("__ris.prof.n"))<a+n and time.time()-t<60: await asyncio.sleep(0.2)
    async def step(name,code,shot=None,nf=2):
      try:
        r=await E(code)
      except Exception as ex:
        r='EXC '+str(ex)[:300]
      await frames(nf)
      print(name,'=>',r,flush=True)
      if shot: await pg.screenshot(path=shot,timeout=120000)
    await E("document.getElementById('btnNew').click()")
    await frames(3)
    await step('give',"(()=>{const R=__ris;R.invAdd('stone',10);R.invAdd('flint',4);R.invAdd('fiber',30);R.invAdd('stick',20);return 1})()")
    await step('craft',"(()=>{__ris.togglePanel('craft');const c=n=>[...document.querySelectorAll('[data-craft]')].find(b=>b.closest('.rc').querySelector('h4').textContent.startsWith(n)).click();c('ロープ');c('ロープ');c('石の斧');c('木の槍');c('ロープ');c('ロープ');c('釣り竿');__ris.dbg.closePanels();return __ris.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')})()",'g_grass.png',2)
    await step('gotoTree',"(()=>{const R=__ris,p=R.player.pos;let best=null,bd=1e9;for(const e of R.ENT)if(e.kind==='tree'&&e.alive&&e.sub==='jungle'){const d=Math.hypot(e.x-p.x,e.z-p.z);if(d<bd){bd=d;best=e}}window.__tree=best;const a=1.0;p.set(best.x+Math.cos(a)*2,R.terrainH(best.x+Math.cos(a)*2,best.z+Math.sin(a)*2),best.z+Math.sin(a)*2);R.S.sel=R.S.inv.findIndex(s=>s&&s.id==='axe');return best.sub+' hp'+best.hp+' sel'+R.S.sel})()",None,2)
    for i in range(14):
      r=await E("(()=>{const t=__tree;__ris.dbg.face(t.x,t.y+1.2,t.z);__ris.dbg.cd0();__ris.primary();return __tree.hp})()")
      await frames(1)
      if r<=0: break
    print('tree hp',r,flush=True)
    await frames(2)
    await pg.screenshot(path='g_fall.png',timeout=120000)
    await asyncio.sleep(2);await frames(4)
    await step('wood',"__ris.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')",'g_fell.png',1)
    await step('hunt',"(()=>{const R=__ris,p=R.player.pos;const a=R.AN.filter(a=>a.alive&&a.st!=='dead'&&a.type==='deer')[0];window.__an=a;a.st='idle';a.t=99;a.c=Object.assign({},a.c,{flee:0,sp:0,run:0});p.set(a.x+2,R.terrainH(a.x+2,a.z),a.z);R.S.sel=R.S.inv.findIndex(s=>s&&s.id==='spear');return a.type+' hp '+a.hp})()",None,2)
    for i in range(8):
      r=await E("(()=>{const a=__an;__ris.dbg.face(a.x,a.y+a.c.size*0.6,a.z);__ris.dbg.cd0();__ris.primary();return a.hp+' '+a.st})()")
      await frames(1)
      if 'dead' in r: break
    print('animal',r)
    await step('butcher',"(()=>{const a=__an;__ris.dbg.face(a.x,a.y+0.3,a.z);return 1})()",'g_deer.png',2)
    await step('butcher2',"(()=>{const t=__ris.target;if(t&&t.kind==='animal')__ris.interact();return (t?t.kind:'none')+' '+__ris.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')})()")
    await step('fish',"(()=>{const R=__ris;const L=R.dbg.LAKE;const x=L.x-34,z=L.z;R.player.pos.set(x,R.terrainH(x,z),z);R.player.yaw=-Math.PI/2;R.player.pitch=-0.3;R.S.sel=R.S.inv.findIndex(s=>s&&s.id==='rod');return 1})()",None,2)
    await step('cast',"(()=>{const R=__ris;R.dbg.cd0();R.primary();return JSON.stringify(R.dbg.fishing)})()",None,1)
    await step('bite',"(()=>{const f=__ris.dbg.fishing;if(f){f.bite=true;f.bt=5}__ris.primary();return __ris.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')})()",'g_lake.png',2)
    await step('builds',"(()=>{const R=__ris;R.invAdd('wood',40);R.invAdd('rope',8);R.invAdd('fiber',20);R.invAdd('stick',20);const p=R.player.pos;const out=[];let k=0;for(const t of ['shelter','collector','farm','chest','hut','tower']){const a=k++*1.05+0.4;const x=p.x-8+Math.cos(a)*9,z=p.z+Math.sin(a)*9;const ok=R.terrainH(x,z)>0.4;R.addBuild(t,x,z,0);out.push(t+':'+ok)}return out.join(',')})()",None,2)
    await step('sleep',"(()=>{const R=__ris;R.S.time=R.S.time-R.S.time%1440+21*60;const sh=R.S.builds.find(b=>b.type==='shelter');const d0=R.S.day;R.dbg.sleep(sh);return d0})()",None,1)
    await asyncio.sleep(1.5);await frames(2)
    await step('slept',"__ris.S.day+' '+Math.floor(__ris.S.time%1440/60)+'h fatigue '+__ris.S.fatigue")
    await step('rain',"(()=>{const R=__ris;Object.assign(R.S.wx,{rain:1,cloud:1});R.S.weather='rain';return 1})()",None,30)
    await step('collector',"(()=>{const c=__ris.S.builds.find(b=>b.type==='collector');return c.data.w.toFixed(3)})()")
    await step('farm',"(()=>{const R=__ris;R.invAdd('seed',1);const f=R.S.builds.find(b=>b.type==='farm');R.dbg.useBuild(f);f.data.t=1;R.dbg.useBuild(f);return R.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')})()")
    await step('chest',"(()=>{const R=__ris;const c=R.S.builds.find(b=>b.type==='chest');R.dbg.useBuild(c);document.querySelector('[data-ci]').click();const n=c.data.items.filter(Boolean).length;document.querySelector('[data-co]').click();const m=c.data.items.filter(Boolean).length;R.dbg.closePanels();return n+'->'+m})()")
    await step('view3',"(()=>{const R=__ris;Object.assign(R.S.wx,{rain:0,cloud:.2});R.S.weather='clear';R.S.time=R.S.time-R.S.time%1440+16*60;R.player.view=3;const h=R.S.builds.find(b=>b.type==='hut');R.player.pos.set(h.x+7,R.terrainH(h.x+7,h.z+3),h.z+3);R.dbg.face(h.x,h.y+1.5,h.z);return 1})()",'g_base.png',4)
    await step('remove',"(()=>{const R=__ris;R.player.view=1;const t=R.S.builds.find(b=>b.type==='tower');const n=R.S.builds.length;R.dbg.useBuild(t);return n+' y='+R.player.pos.y.toFixed(1)})()",'g_tower.png',3)
    await step('panels',"(()=>{const R=__ris;const out=[];for(const p of ['inv','craft','build','map','menu']){R.togglePanel(p);out.push(p+':'+document.querySelector('#panel').innerHTML.length);if(R.dbg.panel)R.dbg.closePanels()}return out.join(',')})()")
    await step('mapshot',"(()=>{__ris.togglePanel('map');return 1})()",'g_map.png',1)
    await step('close',"(()=>{__ris.dbg.closePanels();__ris.togglePanel('inv');return 1})()",'g_inv.png',1)
    await step('death',"(()=>{__ris.dbg.closePanels();__ris.S.water=0;__ris.S.hp=0.2;return 1})()",'g_death.png',3)
    await step('dstate',"__ris.state")
    await step('cave',"(()=>{const R=__ris;document.getElementById('btnLoad2').click();const C=R.dbg.CAVE;const P=R.dbg.CAVEPATH;R.player.pos.set(P[4].x,0,P[4].z);R.player.inCave=true;R.dbg.face(P[7].x,1.2,P[7].z);R.S.inv[0]={id:'torch',n:1,d:480};R.S.sel=0;R.S.torchOn=true;return R.state+' '+JSON.stringify(R.CAVE_E)})()",'g_cave.png',4)
    print('ERRORS:\n'+'\n'.join(errs[:20]))
    await b.close()
asyncio.run(main())
