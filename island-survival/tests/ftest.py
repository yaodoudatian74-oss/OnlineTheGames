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
    R="__ris"
    await step('give',"(()=>{const R=__ris;R.invAdd('stone',10);R.invAdd('flint',4);R.invAdd('fiber',30);R.invAdd('stick',20);return JSON.stringify(R.S.inv.filter(Boolean).map(s=>s.id+':'+s.n))})()")
    await step('craftAxe',"(()=>{__ris.togglePanel('craft');const b=[...document.querySelectorAll('[data-craft]')].find(b=>b.closest('.rc').querySelector('h4').textContent.startsWith('石の斧'));b.click();const r=__ris.S.inv.some(s=>s&&s.id==='axe');__ris.dbg.closePanels();return r})()",'f_craft.png',1)
    await step('craftKnife+firekit',"(()=>{__ris.togglePanel('craft');const c=n=>[...document.querySelectorAll('[data-craft]')].find(b=>b.closest('.rc').querySelector('h4').textContent.startsWith(n)).click();c('石のナイフ');c('火起こし道具');__ris.dbg.closePanels();return __ris.S.inv.filter(Boolean).map(s=>s.id).join(',')})()")
    # chop tree
    await step('gotoTree',"(()=>{const R=__ris,p=R.player.pos;let best=null,bd=1e9;for(const e of R.ENT)if(e.kind==='tree'&&e.alive&&e.sub!=='giant'){const d=Math.hypot(e.x-p.x,e.z-p.z);if(d<bd){bd=d;best=e}}window.__tree=best;const a=1.0;p.set(best.x+Math.cos(a)*1.8,R.terrainH(best.x+Math.cos(a)*1.8,best.z+Math.sin(a)*1.8),best.z+Math.sin(a)*1.8);R.S.sel=R.S.inv.findIndex(s=>s&&s.id==='axe');return best.sub+' hp'+best.hp})()",None,2)
    await step('face',"(()=>{const t=__tree;__ris.dbg.face(t.x,t.y+1.2,t.z);return 1})()",None,2)
    await step('target',"(()=>{const t=__ris.target;return t?t.kind+(t===__tree):'none'})()",'f_tree.png',1)
    for i in range(14):
      r=await E("(()=>{const t=__tree;__ris.dbg.face(t.x,t.y+1.2,t.z);__ris.dbg.cd0();__ris.primary();return __tree.hp})()")
      await frames(1)
      if r<=0: break
    print('tree hp',r)
    await asyncio.sleep(2.5);await frames(3)
    await step('wood',"__ris.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')",'f_fell.png',1)
    # campfire
    await step('place',"(()=>{__ris.invAdd('wood',40);__ris.invAdd('rope',10);__ris.dbg.face(__ris.player.pos.x-3,__ris.player.pos.y,__ris.player.pos.z);__ris.player.pitch=-0.3;__ris.startPlace('campfire');return !!__ris.dbg.placing})()",None,3)
    await step('confirm',"(()=>{const ok=__ris.dbg.placing&&__ris.dbg.placing.ok;__ris.confirmPlace();return ok+' builds='+__ris.S.builds.length})()",None,2)
    await step('light',"(()=>{const f=__ris.S.builds.find(b=>b.type==='campfire');__ris.dbg.useBuild(f);const L=[...document.querySelectorAll('[data-f=light]')];if(L[0])L[0].click();return f.data.lit+' fuel '+f.data.fuel})()",None,1)
    await step('cook',"(()=>{__ris.invAdd('rawmeat',2);__ris.dbg.closePanels();const f=__ris.S.builds.find(b=>b.type==='campfire');__ris.dbg.useBuild(f);const c=document.querySelector('[data-cook]');if(c)c.click();__ris.dbg.closePanels();return __ris.S.inv.filter(Boolean).map(s=>s.id+':'+s.n).join(',')})()",'f_fire.png',3)
    await step('eat',"(()=>{__ris.S.food=40;const i=__ris.S.inv.findIndex(s=>s&&s.id==='meat');__ris.dbg.consume(i);return __ris.S.food})()")
    # hut, workbench
    await step('workbench',"(()=>{__ris.player.yaw+=1.6;__ris.startPlace('workbench');return 1})()",None,2)
    await step('wbconfirm',"(()=>{const ok=__ris.dbg.placing.ok;__ris.confirmPlace();return ok+' '+__ris.S.builds.map(b=>b.type).join(',')})()",None,1)
    await step('save',"(()=>{__ris.saveGame();window.__saved=JSON.stringify({b:__ris.S.builds.length,inv:__ris.S.inv.filter(Boolean).length,food:Math.round(__ris.S.food)});return __saved})()")
    await step('mutate+load',"(()=>{__ris.S.food=1;__ris.S.inv.fill(null);__ris.loadGame();return JSON.stringify({b:__ris.S.builds.length,inv:__ris.S.inv.filter(Boolean).length,food:Math.round(__ris.S.food)})+' vs '+__saved})()",None,2)
    # night + rain visuals
    await step('night',"(()=>{__ris.S.time=__ris.S.time-__ris.S.time%1440+22*60;return 1})()",'f_night.png',3)
    await step('storm',"(()=>{__ris.S.time=__ris.S.time-__ris.S.time%1440+14*60;__ris.S.weather='storm';Object.assign(__ris.S.wx,{cloud:1,rain:1,fog:.35,wind:1.8,amp:1.5,storm:1});return 1})()",'f_storm.png',3)
    await step('clear',"(()=>{__ris.S.weather='clear';Object.assign(__ris.S.wx,{cloud:.15,rain:0,fog:0,wind:.4,amp:.3,storm:0});__ris.S.time=__ris.S.time-__ris.S.time%1440+8*60;return 1})()",None,1)
    # sea swim/dive at reef
    await step('dive',"(()=>{const W=__ris.WRECK;__ris.player.pos.set(W.x+6,-2,W.z+6);__ris.dbg.face(W.x,W.h+1,W.z);return 1})()",None,4)
    await step('under',"JSON.stringify({swim:__ris.player.swim,under:__ris.player.under,breath:__ris.S.breath,y:__ris.player.pos.y})",'f_under.png',1)
    await step('surface',"(()=>{__ris.player.pos.y=-1.3;return 1})()",'f_sea.png',3)
    # lake view
    await step('lake',"(()=>{const L=__ris.dbg.LAKE;const x=L.x-L.r-10,z=L.z;__ris.player.pos.set(x,__ris.terrainH(x,z),z);__ris.dbg.face(L.x,L.y,L.z);return 1})()",'f_lake.png',4)
    # cave
    await step('cave',"(()=>{const c=__ris.CAVE_E;const a=c.ang;__ris.player.pos.set(c.x+Math.cos(a)*3,__ris.terrainH(c.x+Math.cos(a)*3,c.z+Math.sin(a)*3),c.z+Math.sin(a)*3);__ris.dbg.face(c.x,c.h+1,c.z);return 1})()",'f_caveE.png',3)
    await step('caveFace',"(()=>{const c=__ris.CAVE_E;__ris.dbg.face(c.x,c.h+1,c.z);return 1})()",'f_caveE.png',2)
    await step('caveT',"(()=>{const t=__ris.target;return t?t.kind:'none'})()")
    await step('enter',"(()=>{__ris.interact();return 1})()",None,1)
    await asyncio.sleep(1.5);await frames(3)
    await step('incave',"(()=>{__ris.S.inv[0]={id:'torch',n:1,d:480};__ris.S.sel=0;__ris.S.torchOn=true;return __ris.player.inCave})()",'f_cave.png',3)
    await step('walkCave',"(()=>{__ris.player.pos.x+=20;return JSON.stringify(__ris.player.pos)})()",'f_cave2.png',3)
    await step('exit',"(()=>{const C=__ris.dbg.CAVE;__ris.player.pos.set(C.x+0.5,0,C.z);__ris.dbg.face(C.x-1.5,0.7,C.z);return 1})()",None,2)
    await step('exitFace',"(()=>{const C=__ris.dbg.CAVE;__ris.dbg.face(C.x-1.5,0.7,C.z);return 1})()",None,2)
    await step('exitT',"(()=>{const t=__ris.target;if(t)__ris.interact();return t?t.kind:'none'})()",None,1)
    await asyncio.sleep(1.5);await frames(3)
    await step('outside',"__ris.player.inCave+' '+JSON.stringify(__ris.player.pos)")
    # escape
    await step('escape',"(()=>{const R=__ris;R.invAdd('wood',30);R.invAdd('rope',6);R.invAdd('cloth',1);R.invAdd('compass',1);const wb=R.S.builds.find(b=>b.type==='workbench');let best=null;for(let a=0;a<64;a++){for(let d=4;d<60;d+=2){const x=wb.x+Math.cos(a/10)*d,z=wb.z+Math.sin(a/10)*d;if(R.terrainH(x,z)<-1.5&&d<=6){best={x,z,a}}}}return JSON.stringify(best)})()")
    await step('escape2',"(()=>{const R=__ris;R.addBuild('escape',R.player.pos.x,R.player.pos.z,0);const e=R.S.builds.find(b=>b.type==='escape');e.x=380;e.z=0;R.dbg.useBuild(e);R.player.yaw=-Math.PI/2;return !!R.player.riding})()",None,2)
    await step('sail',"(()=>{const e=__ris.S.builds.find(b=>b.type==='escape');e.x=404;window.dispatchEvent(new KeyboardEvent('keydown',{code:'KeyW'}));return 1})()",None,8)
    await step('won',"(()=>{window.dispatchEvent(new KeyboardEvent('keyup',{code:'KeyW'}));return __ris.state+' '+__ris.S.won})()",'f_win.png',1)
    print('ERRORS:\n'+'\n'.join(errs[:20]))
    await b.close()
asyncio.run(main())
