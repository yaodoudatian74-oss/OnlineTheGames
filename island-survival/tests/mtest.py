import asyncio,time
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    ctx=await b.new_context(viewport={'width':844,'height':390},has_touch=True,is_mobile=True,device_scale_factor=1)
    pg=await ctx.new_page()
    errs=[]
    pg.on('pageerror',lambda e: errs.append('PAGEERR: '+str(e.stack)[:400]))
    pg.on('console',lambda m: errs.append(m.text[:200]) if m.type=='error' else None)
    await pg.goto('file:///home/claude/island/local.html?q=mid')
    await pg.wait_for_function('window.__ris',timeout=60000)
    await pg.screenshot(path='m_title.png',timeout=120000)
    await pg.tap('#btnNew')
    await asyncio.sleep(6)
    await pg.screenshot(path='m_play.png',timeout=120000)
    p0=await pg.evaluate("JSON.stringify(__ris.player.pos)")
    # drag stick up via CDP touch
    cdp=await ctx.new_cdp_session(pg)
    box=await pg.evaluate("(()=>{const r=document.getElementById('stick').getBoundingClientRect();return [r.left+r.width/2,r.top+r.height/2]})()")
    x,y=box
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':x,'y':y,'id':1}]})
    for k in range(6):
      await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':x,'y':y-10*k,'id':1}]})
    await asyncio.sleep(6)
    p1=await pg.evaluate("JSON.stringify(__ris.player.pos)")
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    print('move',p0,'->',p1)
    y0=await pg.evaluate("__ris.player.yaw")
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchStart','touchPoints':[{'x':650,'y':200,'id':2}]})
    for k in range(5):
      await cdp.send('Input.dispatchTouchEvent',{'type':'touchMove','touchPoints':[{'x':650-20*k,'y':200,'id':2}]})
    await cdp.send('Input.dispatchTouchEvent',{'type':'touchEnd','touchPoints':[]})
    print('yaw',y0,'->',await pg.evaluate("__ris.player.yaw"))
    await pg.tap('#bBag',timeout=10000);await asyncio.sleep(2)
    print('panel',await pg.evaluate("__ris.dbg.panel"))
    await pg.screenshot(path='m_bag.png',timeout=120000)
    await pg.tap('[data-close]');await asyncio.sleep(1)
    await pg.tap('#bBuild');await asyncio.sleep(2)
    await pg.screenshot(path='m_build.png',timeout=120000)
    print('panel',await pg.evaluate("__ris.dbg.panel"))
    print('\n'.join(errs[:10]))
    await b.close()
asyncio.run(main())
