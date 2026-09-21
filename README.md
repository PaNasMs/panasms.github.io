# PaNasMs project website

The public presentation of **Pavlo's NAS Management System**, at
[panasms.github.io](https://panasms.github.io/).

Each feature is paired with a screenshot of the running application. English is
the default; Russian and Ukrainian have their own static URLs. Pages work without
JavaScript; JavaScript only adds an accessible screenshot viewer.

## Build and preview

Requires Python 3.12 or newer. There are no npm dependencies, external fonts,
analytics, cookies or third-party scripts.

```sh
python3 build.py
python3 check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory public
```

- `content.json`: translated descriptions, captions and navigation.
- `build.py`: static HTML, metadata and sitemap generation.
- `style.css`: responsive layout and shared visual styles.
- `app.js`: screenshot enlargement, Escape dismissal and focus restoration.
- `assets/`: original English interface screenshots, captured September 22, 2026.
- `public/`: generated website, intentionally ignored by Git.

GitHub Actions checks pull requests and deploys `main` to GitHub Pages. Pages must
use the **GitHub Actions** deployment source. Repository updates do not build or
install the NAS software.

## Screenshot policy

Capture the real English UI; do not invent working features. Choose views without
personal documents, user names, IP/MAC addresses, serial numbers, tokens or
credentials. Crop at capture time where necessary. Users and network images show
unsubmitted forms; opening them did not create users or change the network.
The Files image shows generic system folders. No NAS API or private address is
embedded in the website. Review every replacement image before committing it.

The page describes the current prototype honestly. Update its development/release
status when the first stable version is actually published. Installation links
point to the maintained backend instructions and build workflow rather than an
expiring package URL.

## Licensing and image credits

Original website code and text: PolyForm Noncommercial 1.0.0; see `LICENSE` and
`NOTICE`. Do not describe this license as unrestricted open source.

Some screenshots show **Flow** by **Sandra Smukaste**, from the
[KDE wallpaper collection](https://github.com/KDE/plasma-workspace-wallpapers/tree/master/Flow),
licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/).
The wallpaper appears as the application's background; captures are cropped and
scaled for display. The screenshot assets are shared under CC BY-SA 4.0, with
PaNasMs interface credit and the wallpaper attribution retained. Third-party
artwork retains its own license. See the visible image-credits section of the site.
