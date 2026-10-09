# PaNasMs project website

Source of [panasms.github.io](https://panasms.github.io/), the public site of
[Pavlo's NAS Management System](https://github.com/PaNasMs/panasms). The site presents
each section of the panel with a real screenshot, hosts the installation guide and the
Google, GitHub and Dropbox setup guides, and documents the Raspberry Pi 5 build the
project runs on. English is the default language. Russian and Ukrainian have their own
URLs under `/ru/` and `/uk/`.

Pages work without JavaScript. The script only adds the theme switch for screenshots
and an accessible screenshot viewer. The site loads no external fonts, analytics,
cookies or third-party scripts.

## Build and preview

The build needs Python 3.12 or newer and no npm packages.

```sh
python3 build.py
python3 check.py
python3 -m http.server 4173 --bind 127.0.0.1 --directory public
```

`build.py` writes the static site into `public/`, which Git ignores. `check.py` checks
the three languages, the policy pages, the setup guides, the hardware page, screenshot
files and local links. GitHub Actions runs both on pull requests and deploys `main` to
GitHub Pages, so the Pages source must be set to **GitHub Actions**. Pushing here
publishes the site only. It does not build or install NAS software.

## Layout

| Path | Contents |
| --- | --- |
| `content.json` | Landing-page text, captions and navigation in en, ru and uk |
| `pages/` | English pages: installation guide, Google, GitHub and Dropbox setup, privacy policy, terms of use, hardware build |
| `assets/screenshots/home-*.png` | Screenshots used by the landing page; older files without the `home-` prefix are kept for history and are not used |
| `assets/google-setup/`, `assets/github-setup/`, `assets/dropbox-setup/` | Screenshots for the setup guides |
| `assets/hardware/rpi-radxa-penta/` | Edited build photos (WebP) and wiring illustrations (PNG) |
| `style.css`, `app.js` | Layout, theme switch and screenshot viewer with Escape and focus handling |

The supported operating systems on the site follow `scripts/install.py` in
[PaNasMs/updates](https://github.com/PaNasMs/updates). Update both together.

## Screenshots

Capture the real English interface and do not show features that do not work. Pick
views without personal files, user names, IP or MAC addresses, serial numbers, tokens
or credentials, and crop or redact at capture time. Opaque redaction is allowed for
account email addresses and drive serial numbers. Do not remove controls or sections
from a capture. Forms in the users and network images were opened and not submitted.

Browser captures can contain JPEG data under a `.png` name. Re-encode them as PNG:
the build reads the PNG signature to get image dimensions, and wrong dimensions break
the page layout.

A figure shows the theme switch only when both a light and a dark capture exist.
Files and Network have light captures only and Cloud Sync has a dark capture only.
The landing page dates its captures: most are from October 4, 2026, and Files and
Disks and arrays were recaptured on October 9 with stable 0.2.15.

## Hardware build page

`pages/rpi-radxa-penta.html` describes the owner's NAS: Raspberry Pi 5, Radxa Penta
SATA HAT and four 2.5-inch drives. The photos illustrate assembly stages. The pin tables
are what governs electrical connections. Never publish original desktop photos, serial
numbers, monitor content or private hardware notes. CAD files are not included yet.

## Licensing and image credits

Original website code and text use PolyForm Noncommercial 1.0.0; see `LICENSE` and
`NOTICE`. Do not describe this license as open source.

Some screenshots show **Flow** by Sandra Smukaste from the
[KDE wallpaper collection](https://github.com/KDE/plasma-workspace-wallpapers/tree/master/Flow),
licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), as the
panel background. The screenshot files are shared under CC BY-SA 4.0 with that
attribution and the PaNasMs interface credit. The wiring illustrations adapt a Radxa
image licensed under CC BY 4.0. The site's credits section lists these sources.
