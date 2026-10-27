from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json
import re
import struct

ROOT = Path(__file__).resolve().parent / 'public'

class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.path = path
        self.ids = set()
        self.links = []
        self.images = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            assert attrs['id'] not in self.ids, f'Duplicate id: {self.path}: {attrs["id"]}'
            self.ids.add(attrs['id'])
        for key in ('href', 'src'):
            if key in attrs:
                self.links.append(attrs[key])
        if tag == 'img' and attrs.get('src'):
            assert 'alt' in attrs, f'Missing image alt: {self.path}'
            assert 'width' in attrs and 'height' in attrs, f'Missing dimensions: {attrs}'
            if 'assets/screenshots/' in attrs['src']:
                image = (self.path.parent / attrs['src']).resolve()
                raw = image.read_bytes()
                assert raw.startswith(b'\x89PNG\r\n\x1a\n'), f'Not PNG: {image}'
                size = struct.unpack('>II', raw[16:24])
                assert size == (int(attrs['width']), int(attrs['height'])), f'Wrong dimensions: {image}'
                assert all(0 < value <= 10000 for value in size), f'Unreasonable dimensions: {image}'
            self.images += 1

pages = {p.resolve(): Page(p) for p in ROOT.rglob('index.html')}
assert len(pages) == 10
assert (ROOT / 'googleb68279be115e9c18.html').read_bytes() == (ROOT.parent / 'googleb68279be115e9c18.html').read_bytes()
canonicals = set()
titles = set()
descriptions = set()
for path, page in pages.items():
    html = path.read_text()
    title = re.search(r'<title>([^<]+)</title>', html)
    description = re.search(r'<meta name="description" content="([^"]+)"', html)
    canonical = re.search(r'<link rel="canonical" href="([^"]+)"', html)
    assert title and description and canonical, f'Missing search metadata: {path}'
    expected = 'https://panasms.github.io/' + ('/'.join(path.relative_to(ROOT).parts[:-1]) + '/' if path.parent != ROOT else '')
    assert canonical.group(1) == expected, f'Wrong canonical URL: {path}'
    titles.add(title.group(1))
    descriptions.add(description.group(1))
    canonicals.add(canonical.group(1))
    assert 'id="analytics-consent"' in html and 'data-analytics-preferences' in html, f'Missing consent UI: {path}'
    assert 'googletagmanager.com' not in html and 'google-analytics.com' not in html, f'Google loaded before consent: {path}'
    assert page.images == (0 if path.parent.name in ("privacy", "terms", "install") else 1 if path.parent.name in ("github", "dropbox") else 5 if path.parent.name == "google" else 7 if path.parent.name == "rpi_radxa_penta" else 2 + len(list((ROOT / 'assets/screenshots').glob('home-*.png')))), (path, page.images)
    for link in page.links:
        url = urlsplit(link)
        if url.scheme or url.netloc:
            assert url.scheme in ('https', 'mailto'), f'Non-HTTPS external link: {link}'
            continue
        target = (path.parent / unquote(url.path)).resolve() if url.path else path
        if target.is_dir():
            target /= 'index.html'
        assert target.is_file(), f'Broken local link: {path}: {link}'
        if url.fragment:
            assert target in pages and url.fragment in pages[target].ids, f'Broken anchor: {link}'
assert len(titles) == len(descriptions) == len(canonicals) == len(pages), 'Duplicate search metadata'
sitemap_urls = set(re.findall(r'<loc>([^<]+)</loc>', (ROOT / 'sitemap.xml').read_text()))
assert sitemap_urls == canonicals, 'Sitemap and canonical URLs differ'
assert 'Sitemap: https://panasms.github.io/sitemap.xml' in (ROOT / 'robots.txt').read_text()
content = json.loads((ROOT.parent / 'content.json').read_text())
consent = json.loads((ROOT.parent / 'analytics-content.json').read_text())
assert set(consent) == set(content)
for language, text in consent.items():
    assert set(text) == set(consent['en']), f'Incomplete analytics translation: {language}'
keys = set(content['en'])
for language, text in content.items():
    assert set(text) == keys, f'Incomplete translation: {language}'
    assert [f['id'] for f in text['features']] == ['files','storage','users','network','modules','containers','cloud','history']
print('Three presentation languages, two policy pages, Google, GitHub and Dropbox setup guides, hardware build, screenshots and local links verified.')
