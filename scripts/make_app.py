# Wraps the artifact page (src/index.html) into the installable app page (app/index.html).
# Usage: python3 scripts/make_app.py src/index.html app/index.html
import sys
src,dst=sys.argv[1],sys.argv[2]
body=open(src).read()
head='''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<meta name="description" content="Compare AI models by price per token, context size, parameters, and coding, science, and reliability scores. Updated weekly.">
<meta name="theme-color" content="#0f6b5c">
<link rel="manifest" href="/manifest.webmanifest">
<link rel="icon" type="image/png" href="/favicon.png">
<link rel="apple-touch-icon" href="/apple-touch-icon.png">
<meta name="apple-mobile-web-app-capable" content="yes">
<meta name="mobile-web-app-capable" content="yes">
<meta name="apple-mobile-web-app-title" content="Model Matcher">
<meta name="apple-mobile-web-app-status-bar-style" content="default">
<style>:root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)}body{margin:0;font-size:14px}img{max-width:100%}[hidden]{display:none!important}</style>
'''
i=body.index('<div class="wrap">')
page=head+body[:i]+'</head>\n<body>\n'+body[i:]+'''
<script>if('serviceWorker' in navigator){addEventListener('load',()=>navigator.serviceWorker.register('/sw.js').catch(()=>{}))}</script>
</body>
</html>
'''
open(dst,'w').write(page)
