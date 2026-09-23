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
    shots = ''
    for theme in ('light', 'dark'):
        path = f'assets/screenshots/{image}-{theme}.png'
        raw = (ROOT / path).read_bytes()
        assert raw.startswith(b'\x89PNG\r\n\x1a\n'), f'Expected PNG image: {path}'
        width, height = struct.unpack('>II', raw[16:24])
        assert 0 < width <= 10000 and 0 < height <= 10000, f'Invalid image size: {path}'
        label = caption + ' · ' + t[theme]
        shots += f'<a class="zoom" data-theme="{theme}" href="{prefix}{path}" aria-label="{e(t["enlarge"])}: {e(label)}" {"hidden" if theme == "dark" else ""}><img src="{prefix}{path}" width="{width}" height="{height}" alt="{e(label)}" loading="{"eager" if eager and theme == "light" else "lazy"}" decoding="async"><span class="zoom-hint" aria-hidden="true">↗</span></a>'
    controls = ''.join(f'<button type="button" data-show-theme="{theme}" aria-pressed="{"true" if theme == "light" else "false"}">{e(t[theme])}</button>' for theme in ('light', 'dark'))
    return f'<figure class="shot {image}"><div class="shot-themes" role="group" aria-label="{e(t["themeLabel"])}" hidden>{controls}</div><div class="shot-views">{shots}</div><figcaption>{e(caption)}</figcaption><noscript><a href="{prefix}assets/screenshots/{image}-dark.png">{e(t["dark"])} ↗</a></noscript></figure>'

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
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{e(t['title'])}</title><meta name="description" content="{e(t['description'])}"><meta name="theme-color" content="#194e43"><link rel="canonical" href="{canonical}">{alternates}<link rel="alternate" hreflang="x-default" href="{SITE}/"><meta property="og:type" content="website"><meta property="og:title" content="{e(t['title'])}"><meta property="og:description" content="{e(t['description'])}"><meta property="og:url" content="{canonical}"><meta property="og:image" content="{SITE}/assets/screenshots/desktop-light.png"><link rel="icon" href="{prefix}favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="{prefix}style.css"><script src="{prefix}app.js" defer></script></head>
<body><a class="skip" href="#main">{e(t['skip'])}</a><header class="site-header"><div class="header-inner"><a class="brand" href="{prefix}" aria-label="PaNasMs"><img src="{prefix}favicon.svg" alt="" width="32" height="32">PaNasMs</a><nav aria-label="{e(t['navFeatures'])}"><a href="#features">{e(t['navFeatures'])}</a><a href="#start">{e(t['navInstall'])}</a><a class="github-nav" href="https://github.com/PaNasMs/panasms">GitHub ↗</a></nav><div class="languages" role="group" aria-label="{e(t['language'])}">{langs}</div></div></header>
<main id="main"><section class="hero wrap" aria-labelledby="hero-title"><div class="hero-copy"><p class="eyebrow">{e(t['eyebrow'])}</p><h1 id="hero-title">{lines(t['heroTitle'])}</h1><p class="lead">{e(t['heroText'])}</p><a class="button primary" href="#features">{e(t['explore'])} <span aria-hidden="true">↓</span></a><p class="status"><span aria-hidden="true"></span>{e(t['status'])}</p></div><div class="hero-visual">{picture('desktop',t['heroCaption'],t,prefix,True)}</div></section>
<section class="platform wrap" aria-labelledby="platform-title"><div><p class="eyebrow">DIY · ARM64</p><h2 id="platform-title">{e(t['platformTitle'])}</h2><p>{e(t['platformText'])}</p></div><a class="hardware-link" href="{prefix}hardware/rpi_radxa_penta/"><img src="{prefix}assets/hardware/rpi-radxa-penta/assembled.webp" alt="" width="1086" height="1448" loading="lazy"><div><h3>{e(t['hardwareLink'])} ↗</h3><p>{e(t['hardwareText'])}</p></div></a></section><div class="feature-area" id="features"><div class="wrap"><div class="intro"><p class="eyebrow">{e(t['introLabel'])}</p><h2>{lines(t['introTitle'])}</h2><p>{e(t['introText'])}</p></div>{features}<p class="image-note">{e(t['imageNote'])}</p></div></div>
<section class="start wrap" id="start" aria-labelledby="start-title"><div class="start-intro"><p class="eyebrow">{e(t['getLabel'])}</p><h2 id="start-title">{lines(t['getTitle'])}</h2><p>{e(t['getText'])}</p></div><div class="start-grid"><div><ol class="steps">{steps}</ol><div class="cta-row"><a class="button primary" href="https://github.com/PaNasMs/backend#installation-and-operation">{e(t['installLink'])} ↗</a><a class="text-link" href="https://github.com/PaNasMs/frontend/actions/workflows/build.yml">{e(t['buildLink'])} ↗</a></div></div><aside class="requirements"><h3>{e(t['requirementsTitle'])}</h3><p>{e(t['requirements'])}</p><hr><h3>{e(t['development'])}</h3><p>{e(t['developmentText'])}</p></aside></div></section>
</main><footer><div class="wrap"><div class="footer-top"><div><a class="brand" href="{prefix}">PaNasMs</a><p>{e(t['footerDescription'])}</p></div><nav class="footer-navigation" aria-label="{e(t['resources'])}"><div><h3>{e(t['resources'])}</h3><a href="https://github.com/PaNasMs">{e(t['source'])} ↗</a><a href="#credits">{e(t['credits'])}</a></div><div><h3>{e(t['guides'])}</h3><a href="{prefix}hardware/rpi_radxa_penta/">{e(t['hardwareFooter'])}</a><a href="{prefix}docs/setup/google/">{e(t['googleLink'])}</a></div><div><h3>{e(t['legalTitle'])}</h3><a href="https://github.com/PaNasMs/panasms/blob/main/LICENSE">{e(t['license'])} ↗</a><a href="{prefix}privacy/">Privacy</a><a href="{prefix}terms/">Terms</a></div></nav></div><p class="legal">{e(t['licenseText'])}</p><details id="credits"><summary>{e(t['credits'])}</summary><p>{e(t['creditsText'])} <a href="https://github.com/KDE/plasma-workspace-wallpapers/tree/master/Flow">KDE Flow</a> · <a href="https://creativecommons.org/licenses/by-sa/4.0/">CC BY-SA 4.0</a></p></details></div></footer>
<dialog class="lightbox" aria-label="{e(t['enlarge'])}"><form method="dialog"><button autofocus aria-label="{e(t['close'])}" title="{e(t['close'])}">×</button></form><img alt=""><p></p></dialog></body></html>'''
    (page / 'index.html').write_text(html)
(OUT / '.nojekyll').touch()
(OUT / 'robots.txt').write_text(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
(OUT / 'sitemap.xml').write_text('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">' + ''.join(f'<url><loc>{SITE}{"/" if key == "en" else "/" + key + "/"}</loc></url>' for key in CONTENT) + '</urlset>')
print('Built English, Russian and Ukrainian pages in public/')

for slug, title in [('privacy', 'Privacy policy'), ('terms', 'Terms of use')]:
    page = OUT / slug
    page.mkdir(exist_ok=True)
    body = (ROOT / 'pages' / (slug + '.html')).read_text()
    (page / 'index.html').write_text(f'''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{title} · PaNasMs</title><link rel="canonical" href="{SITE}/{slug}/"><link rel="icon" href="../favicon.svg"><link rel="stylesheet" href="../style.css"></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="../">PaNasMs</a><nav aria-label="Legal information"><a href="../privacy/">Privacy</a><a href="../terms/">Terms</a></nav></div></header><main id="main" class="policy-page wrap">{body}</main><footer><div class="wrap"><a href="../">Return to PaNasMs</a></div></footer></body></html>''')

page = OUT / 'docs/setup/google'
page.mkdir(parents=True, exist_ok=True)
body = (ROOT / 'pages/google-setup.html').read_text()
(page / 'index.html').write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Set up Google integration · PaNasMs</title><meta name="description" content="Create a Google OAuth client, link your NAS account and authorize Drive. Includes screenshots and the PaNasMs relay for NAS devices without a public address."><link rel="canonical" href="{SITE}/docs/setup/google/"><link rel="icon" href="../../../favicon.svg"><link rel="stylesheet" href="../../../style.css"></head>
<body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="../../../">PaNasMs</a><nav aria-label="Documentation"><a href="../../../">Project home</a><a href="#before-you-start">Get started</a></nav></div></header><main id="main" class="guide-page wrap"><p class="eyebrow">Documentation / Setup / Google</p>{body}</main><footer><div class="wrap footer-links"><a href="../../../">Return to PaNasMs</a><a href="../../../privacy/">Privacy</a><a href="../../../terms/">Terms</a></div></footer></body></html>''')
sitemap = OUT / 'sitemap.xml'
sitemap.write_text(sitemap.read_text().replace('</urlset>', ''.join(f'<url><loc>{SITE}/{slug}/</loc></url>' for slug in ('privacy', 'terms', 'docs/setup/google')) + '</urlset>'))

page = OUT / 'hardware/rpi_radxa_penta'
page.mkdir(parents=True, exist_ok=True)
body = (ROOT / 'pages/rpi-radxa-penta.html').read_text()
(page / 'index.html').write_text(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Raspberry Pi 5 + Radxa Penta SATA HAT build · PaNasMs</title><meta name="description" content="Inside our four-drive Raspberry Pi NAS: assembly photos, hardware inventory, and two-wire MOSFET or four-wire Noctua PWM cooling connections."><link rel="canonical" href="{SITE}/hardware/rpi_radxa_penta/"><meta property="og:title" content="Our Raspberry Pi 5 NAS build"><meta property="og:image" content="{SITE}/assets/hardware/rpi-radxa-penta/assembled.webp"><link rel="icon" href="../../favicon.svg"><link rel="stylesheet" href="../../style.css"><script src="../../app.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a><header class="site-header"><div class="header-inner"><a class="brand" href="../../">PaNasMs</a><nav aria-label="Hardware navigation"><a href="../../">Project home</a><a href="#cooling">Disk cooling</a></nav></div></header><main id="main" class="hardware-page wrap">{body}</main><footer><div class="wrap footer-links"><a href="../../">Return to PaNasMs</a><a href="../../docs/setup/google/">Google setup</a><a href="../../privacy/">Privacy</a><a href="../../terms/">Terms</a></div></footer><dialog class="lightbox" aria-label="Enlarged build image"><form method="dialog"><button autofocus aria-label="Close image" title="Close image">×</button></form><img alt=""><p></p></dialog></body></html>''')
sitemap.write_text(sitemap.read_text().replace('</urlset>', f'<url><loc>{SITE}/hardware/rpi_radxa_penta/</loc></url></urlset>'))
