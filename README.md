# PaNasMs project website

Source of [panasms.github.io](https://panasms.github.io/), the public site of
[Pavlo's NAS Management System](https://github.com/PaNasMs/panasms). The site presents
each section of the panel with a real screenshot, hosts the installation guide and the
Google, GitHub and Dropbox setup guides, and documents the Raspberry Pi 5 build the
project runs on. English is the default language. Russian and Ukrainian have their own
URLs under `/ru/` and `/uk/`.

Pages work without JavaScript. Scripts add screenshot controls, command copying and
optional Google Analytics 4. No Google tag or analytics request is loaded before the
visitor opts in. Fonts are local system fonts; advertising features are disabled.

## Build and preview

The build needs Python 3.12 or newer and no npm packages.

```sh
python3 build.py
python3 check.py
node --test analytics.test.cjs
python3 -m http.server 4173 --bind 127.0.0.1 --directory public
```

`build.py` writes the static site into `public/`, which Git ignores. `check.py` checks
the three languages, the policy pages, the setup guides, the hardware page, screenshot
files and local links. GitHub Actions runs both on pull requests and deploys `main` to
GitHub Pages, so the Pages source must be set to **GitHub Actions**. Pushing here
publishes the site only. It does not build or install NAS software.

## Analytics

`analytics.json` contains the public GA4 measurement ID (not a secret). An empty ID
disables analytics and hides its consent controls. `analytics-content.json` contains
English, Russian and Ukrainian consent text. The builder adds the same consent
component to all ten pages. The Google tag only runs on `panasms.github.io`; local
previews cannot contaminate production reports.

Use basic consent mode: load nothing from Google until **Allow analytics**. Visitors
can reject with equal prominence or change their choice in **Analytics preferences**
in every footer. The choice and first-party `panasms_ga*` cookies last at most 180
days. Revocation disables collection, removes those cookies and reloads to unload
the tag; other open tabs receive the change. Blocked storage prompts again next visit.

In the GA4 web stream, keep **Enhanced measurement off**: events are emitted by our
code so URLs can be sanitized and views are not duplicated. Keep Google signals,
user-provided data collection and advertising personalization disabled. No user ID,
form contents, private NAS data, query strings or fragments are sent. External
referrers are reduced to origins. Do not add this code to the NAS panel or relay.

| Event | Meaning |
| --- | --- |
| `page_view` | One view per page, after consent |
| `outbound_click` | Click to another HTTP(S) website; sanitized URL and domain |
| `install_guide_open` | Click to the installation guide |
| `install_command_copy` | Successful copy using the installation guide's button |
| `file_download` | Click to a linked deb/rpm/zip/gz/xz/sh file (not confirmed download or installation) |

For acceptance, test reject, accept, revisit and revoke on desktop and mobile. Before
consent/rejection there must be no requests to googletagmanager.com or
google-analytics.com. After acceptance, check GA4 Realtime for `page_view` and a
custom event. Browser blockers and refusal reduce measured traffic. Clicks on GitHub
release pages do not reveal subsequent downloads from GitHub.

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

Original website code and text use Sustainable Use License 1.0; see `LICENSE` and
`NOTICE`. Do not describe this license as open source.

Some screenshots show **Flow** by Sandra Smukaste from the
[KDE wallpaper collection](https://github.com/KDE/plasma-workspace-wallpapers/tree/master/Flow),
licensed under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/), as the
panel background. The screenshot files are shared under CC BY-SA 4.0 with that
attribution and the PaNasMs interface credit. The wiring illustrations adapt a Radxa
image licensed under CC BY 4.0. The site's credits section lists these sources.
