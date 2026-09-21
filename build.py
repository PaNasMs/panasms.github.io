from pathlib import Path
from html import escape
import json
import shutil
import struct

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'public'
CONTENT = json.loads((ROOT / 'content.json').read_text())
SITE = 'https://panasms.github.io'
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
for name in ('style.css', 'app.js', 'favicon.svg'):
    shutil.copyfile(ROOT / name, OUT / name)

def e(value):
    return escape(value, quote=True)

def lines(value):
    return '<br>'.join(e(value).split('\n'))

def picture(image, caption, t, prefix, eager=False):
    raw = (ROOT / 'assets' / (image + '.png')).read_bytes()
    width, height = struct.unpack('>II', raw[16:24])
    return f'''<figure class="shot {image}"><a class="zoom" href="{prefix}assets/{image}.png" aria-label="{e(t['enlarge'])}: {e(caption)}"><img src="{prefix}assets/{image}.png" width="{width}" height="{height}" alt="{e(caption)}" loading="{'eager' if eager else 'lazy'}" decoding="async" {'fetchpriority="high"' if eager else ''}><span class="zoom-hint" aria-hidden="true">↗</span></a><figcaption>{e(caption)}</figcaption></figure>'''

for lang, t in CONTENT.items():
    prefix = './' if lang == 'en' else '../'
    page = OUT if lang == 'en' else OUT / lang
    page.mkdir(exist_ok=True)
    canonical = SITE + ('/' if lang == 'en' else f'/{lang}/')
    langs = ''.join(f'<a href="{prefix}{"" if key == "en" else key + "/"}" lang="{key}" hreflang="{key}" {"aria-current=\"page\"" if key == lang else ""}>{label}</a>' for key, label in [('en','EN'),('ru','RU'),('uk','UK')])
    features = ''
    for i, f in enumerate(t['features'], 1):
        points = ''.join(f'<li>{e(p)}</li>' for p in f['points'])
        features += f'''<section class="feature" id="{f['id']}" aria-labelledby="title-{f['id']}"><div class="feature-copy"><p class="eyebrow"><span>{i:02d}</span> {e(f['tag'])}</p><h2 id="title-{f['id']}">{lines(f['title'])}</h2><p>{e(f['text'])}</p><ul>{points}</ul></div>{picture(f['id'],f['caption'],t,prefix)}</section>'''
    steps = ''.join(f'<li><span class="step-number">{i}</span><div><h3>{e(a)}</h3><p>{e(b)}</p></div></li>' for i,(a,b) in enumerate(t['steps'],1))
    alternates = ''.join(f'<link rel="alternate" hreflang="{key}" href="{SITE}{"/" if key == "en" else "/" + key + "/"}">' for key in CONTENT)
    html = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(t['title'])}</title><meta name="description" content="{e(t['description'])}"><meta name="theme-color" content="#194e43"><link rel="canonical" href="{canonical}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}/"><meta property="og:type" content="website"><meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['description'])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/desktop.png"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}app.js" defer></script></head>
<body><a class="skip" href="#main">{e(t['skip'])}</a><header class="site-header"><div class="header-inner"><a class="brand" href="{prefix}" aria-label="PaNasMs"><img src="{prefix}favicon.svg" alt="" width="32" height="32">PaNasMs</a><nav aria-label="{e(t['navFeatures'])}"><a href="#features">{e(t['navFeatures'])}</a><a href="#start">{e(t['navInstall'])}</a><a class="github-nav" href="https://github.com/PaNasMs/panasms">GitHub ↗</a></nav><div class="languages" role="group" aria-label="{e(t['language'])}">{langs}</div></div></header>
<main id="main"><section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">{e(t['eyebrow'])}</p><h1 id="hero-title">{lines(t['heroTitle'])}</h1><p class="lead">{e(t['heroText'])}</p><a class="button primary" href="#features">{e(t['explore'])} <span aria-hidden="true">↓</span></a><p class="status"><span aria-hidden="true"></span>{e(t['status'])}</p></div><div class="hero-visual">{picture('desktop',t['heroCaption'],t,prefix,True)}</div></section>
<div class="feature-area" id="features"><div class="wrap"><div class="intro"><p class="eyebrow">{e(t['introLabel'])}</p><h2>{lines(t['introTitle'])}</h2><p>{e(t['introText'])}</p></div>{features}<p class="image-note">{e(t['imageNote'])}</p></div></div>
<section class="start wrap" id="start" aria-labelledby="start-title"><div class="start-intro"><p class="eyebrow">{e(t['getLabel'])}</p><h2 id="start-title">{lines(t['getTitle'])}</h2><p>{e(t['getText'])}</p></div><div class="start-grid"><div><ol class="steps">{steps}</ol><div class="cta-row"><a class="button primary" href="https://github.com/PaNasMs/backend#installation-and-operation">{e(t['installLink'])} ↗</a><a class="text-link" href="https://github.com/PaNasMs/frontend/actions/workflows/build.yml">{e(t['buildLink'])} ↗</a></div></div><aside class="requirements"><h3>{e(t['requirementsTitle'])}</h3><p>{e(t['requirements'])}</p><hr><h3>{e(t['development'])}</h3><p>{e(t['developmentText'])}</p></aside></div></section>
</main><footer><div class="wrap"><div class="footer-top"><div><a class="brand" href="{prefix}">PaNasMs</a><p>{e(t['footerDescription'])}</p></div><div class="footer-links"><a href="https://github.com/PaNasMs">{e(t['source'])} ↗</a><a href="https://github.com/PaNasMs/panasms/blob/main/LICENSE">{e(t['license'])} ↗</a><a href="#credits">{e(t['credits'])}</a></div></div><p class="legal">{e(t['licenseText'])}</p><details id="credits"><summary>{e(t['credits'])}</summary><p>{e(t['creditsText'])} <a href="https://github.com/KDE/plasma-workspace-wallpapers/tree/master/Flow">KDE Flow</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a></p></details></div></footer>
<dialog class="lightbox" aria-label="{e(t['enlarge'])}"><form method="dialog"><button autofocus aria-label="{e(t['close'])}" title="{e(t['close'])}">×</button></form><img alt=""><p></p></dialog></body></html>'''
    (page / 'index.html').write_text(html)
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{"/" if key == "en" else "/" + key + "/"}</loc></url>' for key in CONTENT) + '</urlset>')
print('Built English, Russian and Ukrainian pages in public/')
