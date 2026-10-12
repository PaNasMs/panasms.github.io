const {test} = require('node:test');
const assert = require('node:assert/strict');
const {readFileSync} = require('node:fs');
const vm = require('node:vm');

function page({saved = null, host = 'panasms.github.io', blocked = false} = {}) {
  const nodes = new Map();
  const listeners = {};
  const scripts = [];
  const cookies = [];
  let reloads = 0;
  const storage = new Map(saved ? [['panasms-analytics-consent-v1', JSON.stringify(saved)]] : []);
  const node = name => {
    if (!nodes.has(name)) nodes.set(name, {
      hidden: true, dataset: {}, listeners: {},
      addEventListener(type, handler) { this.listeners[type] = handler; },
      focus() { document.activeElement = this; },
      querySelector: node, contains: el => [...nodes.values()].includes(el),
    });
    return nodes.get(name);
  };
  const document = {
    querySelector: node,
    querySelectorAll: () => [],
    referrer: 'https://example.org/private/path?email=private@example.org#secret',
    createElement: () => ({}),
    head: {append: el => scripts.push(el)},
    addEventListener: (type, handler) => { listeners[type] = handler; },
    get cookie() { return 'panasms_ga=sample; unrelated=preserve'; },
    set cookie(value) { cookies.push(value); },
  };
  node('script[data-measurement-id]').dataset.measurementId = 'G-TEST1234';
  const window = {addEventListener: (type, handler) => { listeners[type] = handler; }};
  const context = {
    document, window, URL, Date,
    location: {hostname: host, origin: `https://${host}`, href: `https://${host}/?secret=hidden#private`, reload: () => reloads++},
    localStorage: {
      getItem: key => { if (blocked) throw Error('Blocked'); return storage.get(key) || null; },
      setItem: (key, value) => { if (blocked) throw Error('Blocked'); storage.set(key, value); },
    },
  };
  vm.runInNewContext(readFileSync(__dirname + '/analytics.js', 'utf8'), context);
  return {node, window, scripts, cookies, storage, listeners, reloads: () => reloads,
    click: name => node(name).listeners.click(),
    commands: () => Array.from(window.dataLayer || [], args => Array.from(args)),
  };
}

test('undecided and rejected visits never load Google or queue events', () => {
  const p = page();
  assert.equal(p.node('#analytics-consent').hidden, false);
  assert.equal(p.scripts.length, 0);
  p.click('[data-consent-reject]');
  assert.equal(p.scripts.length, 0);
  assert.equal(p.commands().length, 0);
  assert.equal(p.node('#analytics-consent').hidden, true);
  assert.match(p.cookies[0], /^panasms_ga=/);
  const denied = page({saved: {value: 'denied', time: Date.now()}});
  assert.equal(denied.scripts.length, 0);
  assert.equal(denied.node('#analytics-consent').hidden, true);
});

test('consent loads one tag, denies ads, strips sensitive URL parts and sends one page view', () => {
  const p = page();
  p.click('[data-consent-accept]');
  p.click('[data-consent-accept]');
  assert.equal(p.scripts.length, 1);
  const config = p.commands().find(c => c[0] === 'config')[2];
  assert.equal(config.page_location, 'https://panasms.github.io/');
  assert.equal(config.page_referrer, 'https://example.org/');
  assert.equal(config.allow_google_signals, false);
  assert.equal(config.allow_ad_personalization_signals, false);
  assert.equal(p.commands()[0][2].ad_storage, 'denied');
  assert.equal(p.commands().filter(c => c[1] === 'page_view').length, 1);
});

test('revocation disables collection, clears only project cookies and unloads tag', () => {
  const p = page({saved: {value: 'granted', time: Date.now()}});
  p.click('[data-analytics-preferences]');
  p.click('[data-consent-reject]');
  assert.equal(p.window['ga-disable-G-TEST1234'], true);
  assert.equal(p.reloads(), 1);
  assert.equal(p.cookies.some(c => c.startsWith('unrelated=')), false);
});

test('expired, malformed and unavailable saved consent fail closed', () => {
  for (const saved of [{value: 'granted', time: 1}, {value: 'granted', time: 'invalid'}, {value:'unknown', time:Date.now()}]) {
    assert.equal(page({saved}).scripts.length, 0);
  }
  const p = page({blocked: true});
  assert.equal(p.scripts.length, 0);
  p.click('[data-consent-accept]');
  assert.equal(p.scripts.length, 1);
});

test('local previews cannot send analytics even with consent', () => {
  const p = page({host: '127.0.0.1'});
  p.click('[data-consent-accept]');
  assert.equal(p.scripts.length, 0);
});

test('revoking consent in another tab stops collection here', () => {
  const p = page({saved: {value: 'granted', time: Date.now()}});
  p.storage.clear();
  p.listeners.storage({key:null});
  assert.equal(p.window['ga-disable-G-TEST1234'], true);
  assert.equal(p.reloads(), 1);
});

test('outbound telemetry omits query and fragment and ignores email links', () => {
  const p = page({saved: {value: 'granted', time: Date.now()}});
  const click = href => p.listeners.click({target:{closest: () => ({href})}});
  click('https://github.com/PaNasMs/panasms?private=value#fragment');
  const event = p.commands().find(c => c[1] === 'outbound_click');
  assert.equal(event[2].link_url, 'https://github.com/PaNasMs/panasms');
  const before = p.commands().length;
  click('mailto:private@example.org');
  assert.equal(p.commands().length, before);
});
