import asyncio,sys,json
from playwright.async_api import async_playwright
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(args=['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist'])
    pg=await b.new_page(viewport={'width':800,'height':450})
    errs=[]
    pg.on('console',lambda m: errs.append(m.type+': '+m.text) if m.type in('error','warning') else None)
    pg.on('pageerror',lambda e: errs.append('PAGEERR: '+str(e.stack)))
    import time;t=time.time()
    await pg.goto('file:///home/claude/island/local.html'+('?q='+(__import__('os').environ.get('Q','low'))))
    try:
      await pg.wait_for_function('window.__ris',timeout=60000)
    except Exception as e:
      print('TIMEOUT');print('\n'.join(errs[:30]));await b.close();return
    print('load',round(time.time()-t,1))
    await pg.wait_for_timeout(2500)
    await pg.screenshot(path='s_title.png',timeout=120000)
    await pg.evaluate('document.getElementById("btnNew").click()')
    await pg.wait_for_timeout(3000)
    await pg.screenshot(path='s_play.png',timeout=120000)
    for code in sys.argv[1:]:
      r=await pg.evaluate(code); print('>>',r)
      await pg.wait_for_timeout(1500)
      await pg.screenshot(path='s_%d.png'%sys.argv.index(code),timeout=120000)
    print('\n'.join(errs[:30]))
    await b.close()
asyncio.run(main())
