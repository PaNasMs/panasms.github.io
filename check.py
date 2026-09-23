from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

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
            self.images += 1

pages = {p.resolve(): Page(p) for p in ROOT.rglob('*.html')}
assert len(pages) == 7
for path, page in pages.items():
    assert page.images == (0 if path.parent.name in ("privacy", "terms") else 5 if path.parent.name == "google" else 6 if path.parent.name == "rpi_radxa_penta" else 7), (path, page.images)
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
content = json.loads((ROOT.parent / 'content.json').read_text())
keys = set(content['en'])
for language, text in content.items():
    assert set(text) == keys, f'Incomplete translation: {language}'
    assert [f['id'] for f in text['features']] == ['files','storage','users','network','modules']
print('Three presentation languages, two policy pages, Google setup guide, hardware build, screenshots and local links verified.')
