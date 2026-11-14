/* Versioned guest data. Coordinates never enter completed events or feedback. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GNFStorage = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, () => {
  'use strict';
  const KEY = 'gymnotfound.v1';
  const clean = (value, length = 200) => typeof value === 'string' ? value.replace(/[\u0000-\u001f]/g, '').slice(0, length) : '';
  function defaults(language = 'en') {
    return {version: 1, prefs: {language: language === 'nb' ? 'nb' : 'en', time: 2, energy: 'low', environment: 'auto', free: true, nim: true, area: null}, completed: [], feedback: [], recent: [], pending: null, sequence: 0};
  }
  function normalize(data, language = 'en') {
    const result = defaults(language);
    if (!data || typeof data !== 'object' || ![0, 1].includes(data.version)) return result;
    const p = data.prefs || data.preferences || {};
    if (['en', 'nb'].includes(p.language)) result.prefs.language = p.language;
    if ([2, 15, 30].includes(Number(p.time))) result.prefs.time = Number(p.time);
    if (['low', 'some', 'high'].includes(p.energy)) result.prefs.energy = p.energy;
    if (['auto', 'urban', 'suburban', 'rural', 'home', 'anywhere'].includes(p.environment)) result.prefs.environment = p.environment;
    if (typeof p.free === 'boolean') result.prefs.free = p.free;
    if (typeof p.nim === 'boolean') result.prefs.nim = p.nim;
    if (p.area && typeof p.area.lat === 'number' && Number.isFinite(p.area.lat) && Math.abs(p.area.lat) <= 90 && typeof p.area.lon === 'number' && Number.isFinite(p.area.lon) && Math.abs(p.area.lon) <= 180) {
      result.prefs.area = {lat: Math.round(p.area.lat * 100) / 100, lon: Math.round(p.area.lon * 100) / 100, label: clean(p.area.label, 100)};
    }
    result.completed = (Array.isArray(data.completed) ? data.completed : []).slice(-500).filter(e => e && e.type === 'completed_self_report' && typeof e.uid === 'string' && Number.isFinite(Date.parse(e.at))).map(e => ({uid: clean(e.uid, 80), id: clean(e.id, 120), title: clean(e.title), family: clean(e.family, 40), type: 'completed_self_report', at: e.at}));
    result.feedback = (Array.isArray(data.feedback) ? data.feedback : []).slice(-100).filter(f => f && ['accepted', 'planned', 'completed_self_report', 'did_not_fit', 'later', 'not_now', 'rested'].includes(f.type)).map(f => ({id: clean(f.id, 120), family: clean(f.family, 40), type: f.type, at: clean(f.at, 40)}));
    result.recent = (Array.isArray(data.recent) ? data.recent : []).filter(x => typeof x === 'string').map(x => clean(x, 120)).slice(-12);
    if (data.pending && typeof data.pending.uid === 'string') {
      const v = data.pending;
      result.pending = {uid: clean(v.uid, 80), id: clean(v.id, 120), selection_id: clean(v.selection_id, 240), family: clean(v.family, 40), title: clean(v.title), at: clean(v.at, 40), instructions: v.instructions === true};
    }
    result.sequence = Number.isSafeInteger(data.sequence) && data.sequence >= 0 ? data.sequence : 0;
    return result;
  }
  function load(storage, language = 'en') {
    try { return {state: normalize(JSON.parse(storage.getItem(KEY)), language), available: true}; }
    catch { return {state: defaults(language), available: false}; }
  }
  function save(storage, state) {
    try { storage.setItem(KEY, JSON.stringify(normalize(state, state.prefs.language))); return true; }
    catch { return false; }
  }
  function feedback(state, card, type, at = new Date().toISOString()) {
    state.feedback.push({id: card.id, family: card.family, type, at});
    state.feedback = state.feedback.slice(-100);
  }
  function accept(state, card, title, uid, at = new Date().toISOString(), planned = false) {
    state.pending = {uid, id: card.id, selection_id: card.selection_id, title, family: card.family, at, instructions: card.instructions === true};
    feedback(state, card, planned ? 'planned' : 'accepted', at);
  }
  function complete(state, at = new Date().toISOString()) {
    const p = state.pending;
    if (!p) return false;
    if (!state.completed.some(e => e.uid === p.uid)) {
      state.completed.push({uid: p.uid, id: p.id, title: p.title, family: p.family, type: 'completed_self_report', at});
      state.completed = state.completed.slice(-500);
      feedback(state, p, 'completed_self_report', at);
    }
    state.pending = null;
    return true;
  }
  function clear(storage, language) {
    try { storage.removeItem(KEY); } catch { /* In-memory reset still works. */ }
    return defaults(language);
  }
  return {KEY, defaults, normalize, load, save, feedback, accept, complete, clear};
});
