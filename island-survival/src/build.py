import os
sh=open('shell.html').read(); g=open('game.js').read()
cdn='<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>'
man='<link rel="manifest" href="manifest.webmanifest"><link rel="apple-touch-icon" href="icon-192.png">'
sw="<script>if('serviceWorker' in navigator&&location.protocol==='https:'){addEventListener('load',()=>{navigator.serviceWorker.register('sw.js').catch(()=>{})})}</script>"
art=sh.replace('<!--MANIFEST-->',man).replace('<!--THREE-->',cdn).replace('<!--GAME-->','<script>\n'+g+'\n</script>'+sw)
open('index.html','w').write(art)
three=open('three.min.js').read()
wrap=lambda body:'<!doctype html><html lang="ja"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover"></head><body>'+body+'</body></html>'
local=sh.replace('<!--MANIFEST-->','').replace('<!--THREE-->','<script>'+three+'</script>').replace('<!--GAME-->','<script>\n'+g+'\n</script>')
open('local.html','w').write(wrap(local))
os.makedirs('dist',exist_ok=True)
