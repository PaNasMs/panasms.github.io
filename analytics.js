(() => {
  const script = document.querySelector('script[data-measurement-id]');
  const id = script.dataset.measurementId;
  const banner = document.querySelector('#analytics-consent');
  const preferences = document.querySelector('[data-analytics-preferences]');
  const close = banner.querySelector('[data-consent-close]');
  const key = 'panasms-analytics-consent-v1';
  const lifetime = 180 * 24 * 60 * 60 * 1000;
  const enabled = /^G-[A-Z0-9]+$/.test(id);
  const production = location.hostname === 'panasms.github.io';
  let loaded = false;
  let choice = readChoice();
  let returnFocus;

  function readChoice() {
    try {
      const saved = JSON.parse(localStorage.getItem(key));
      if (saved && ['granted', 'denied'].includes(saved.value) &&
          saved.time <= Date.now() && Date.now() - saved.time < lifetime) return saved.value;
    } catch {}
    return null;
  }

  function cleanURL(value, referrer = false) {
    try {
      const url = new URL(value);
      if (!['https:', 'http:'].includes(url.protocol)) return '';
      return referrer && url.origin !== location.origin ? url.origin + '/' : url.origin + url.pathname;
    } catch { return ''; }
  }

  function event(name, params = {}) {
    if (choice === 'granted' && loaded && !window['ga-disable-' + id]) {
      window.gtag('event', name, params);
    }
  }

  function start() {
    if (!enabled || !production || loaded || choice !== 'granted') return;
    loaded = true;
    window['ga-disable-' + id] = false;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('consent', 'default', {
      analytics_storage: 'denied', ad_storage: 'denied',
      ad_user_data: 'denied', ad_personalization: 'denied',
    });
    window.gtag('consent', 'update', {analytics_storage: 'granted'});
    window.gtag('js', new Date());
    window.gtag('config', id, {
      send_page_view: false,
      page_location: cleanURL(location.href),
      page_referrer: cleanURL(document.referrer, true),
      allow_google_signals: false,
      allow_ad_personalization_signals: false,
      cookie_domain: 'none', cookie_prefix: 'panasms',
      cookie_expires: lifetime / 1000, cookie_update: false,
      cookie_flags: 'SameSite=Lax;Secure',
    });
    const tag = document.createElement('script');
    tag.async = true;
    tag.referrerPolicy = 'origin';
    tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + id;
    document.head.append(tag);
    event('page_view');
  }

  function clearCookies() {
    for (const item of document.cookie.split(';')) {
      const name = item.trim().split('=')[0];
      if (name.startsWith('panasms_ga')) {
        document.cookie = name + '=; Max-Age=0; Path=/; SameSite=Lax; Secure';
      }
    }
  }

  function hide() {
    banner.hidden = true;
    if (returnFocus) returnFocus.focus({preventScroll: true});
    else if (banner.contains(document.activeElement)) preferences.focus({preventScroll: true});
  }

  function choose(value) {
    choice = value;
    try { localStorage.setItem(key, JSON.stringify({value, time: Date.now()})); } catch {}
    hide();
    if (value === 'granted') start();
    else {
      // Disable collection before unloading the already-running Google script.
      window['ga-disable-' + id] = true;
      clearCookies();
      if (loaded) location.reload();
    }
  }

  banner.querySelector('[data-consent-accept]').addEventListener('click', () => choose('granted'));
  banner.querySelector('[data-consent-reject]').addEventListener('click', () => choose('denied'));
  close.addEventListener('click', hide);
  preferences.hidden = !enabled;
  preferences.addEventListener('click', () => {
    returnFocus = preferences;
    close.hidden = !choice;
    banner.hidden = false;
    banner.querySelector('[data-consent-reject]').focus();
  });
  banner.addEventListener('keydown', e => {
    if (e.key === 'Escape' && choice) hide();
  });
  window.addEventListener('storage', e => {
    if (e.key !== key && e.key !== null) return;
    choice = readChoice();
    if (choice !== 'granted') {
      window['ga-disable-' + id] = true;
      clearCookies();
      if (loaded) location.reload();
    } else start();
    banner.hidden = !!choice || !enabled;
  });
  if (enabled) {
    banner.hidden = !!choice;
    close.hidden = !choice;
    if (choice === 'granted') start();
    else clearCookies();
  }

  document.addEventListener('click', e => {
    const link = e.target.closest('a[href]');
    if (!link) return;
    const url = new URL(link.href, location.href);
    if (!['http:', 'https:'].includes(url.protocol)) return;
    const params = {link_url: cleanURL(url.href), link_domain: url.hostname};
    if (url.origin !== location.origin) event('outbound_click', params);
    if (url.origin === location.origin && url.pathname === '/docs/setup/install/') event('install_guide_open');
    if (/\.(deb|rpm|zip|gz|xz|sh)$/i.test(url.pathname)) event('file_download', params);
  });

  for (const button of document.querySelectorAll('[data-copy-command]')) {
    button.hidden = false;
    button.addEventListener('click', async () => {
      const code = document.getElementById(button.dataset.copyCommand);
      const status = document.getElementById(button.getAttribute('aria-describedby'));
      try {
        await navigator.clipboard.writeText(code.textContent);
        status.textContent = button.dataset.success;
        event('install_command_copy');
      } catch { status.textContent = button.dataset.error; }
    });
  }
})();
