/* One pure recommendation engine, shared by the browser and Node tests. */
(function (root, factory) {
  if (typeof module === 'object' && module.exports) module.exports = factory();
  else root.GNFEngine = factory();
})(typeof globalThis !== 'undefined' ? globalThis : this, () => {
  'use strict';
  const levels = {low: 0, some: 1, high: 2};
  const kinds = ['park', 'library', 'museum', 'cafe', 'viewpoint'];
  function coordinate(lat, lon) {
    return typeof lat === 'number' && Number.isFinite(lat) && Math.abs(lat) <= 90 && typeof lon === 'number' && Number.isFinite(lon) && Math.abs(lon) <= 180;
  }
  function placeValid(place) {
    return place && place.provider === 'geoapify' && typeof place.id === 'string' && place.id.length > 0 && typeof place.name === 'string' && place.name.length > 0 && kinds.includes(place.category) && coordinate(place.lat, place.lon) && !place.private && !place.unsafe && !place.closed;
  }
  function weatherMode(weather, now = Date.now()) {
    if (!weather || weather.status !== 'ok' || !Number.isFinite(Date.parse(weather.forecast_at)) || Math.abs(Date.parse(weather.forecast_at) - now) > 90 * 60000) return 'unknown';
    if (weather.wind >= 10 || weather.temperature <= 0) return 'adverse';
    if (weather.precipitation >= 0.2) return 'wet';
    return 'fair';
  }
  function environment(preferences, places) {
    if (['urban', 'suburban', 'rural', 'home', 'anywhere'].includes(preferences.environment)) return preferences.environment;
    const valid = places.filter(placeValid);
    const variety = new Set(valid.map(p => p.category)).size;
    return valid.length >= 8 && variety >= 2 ? 'urban' : valid.length >= 4 ? 'suburban' : 'rural';
  }
  function select(catalog, preferences = {}, context = {}, feedback = [], recent = [], currentId = '', sequence = 0, now = Date.now()) {
    const time = [2, 15, 30].includes(Number(preferences.time)) ? Number(preferences.time) : 2;
    const energy = Object.hasOwn(levels, preferences.energy) ? levels[preferences.energy] : 0;
    const places = Array.isArray(context.places) ? context.places.filter(placeValid) : [];
    const area = environment(preferences, places);
    const weather = weatherMode(context.weather, now);
    const negatives = {};
    const positives = {};
    for (const f of feedback.slice(-20)) {
      if (f.type === 'did_not_fit') negatives[f.family] = (negatives[f.family] || 0) + 1;
      if (f.type === 'completed_self_report') positives[f.family] = (positives[f.family] || 0) + 1;
    }
    const candidates = [];
    for (const card of catalog) {
      if (!card || ![2, 15, 30].includes(card.time) || card.time > time || !Object.hasOwn(levels, card.energy) || levels[card.energy] > energy) continue;
      if (card.instructions && (!card.reviewed || context.offline)) continue;
      if (!Array.isArray(card.contexts) || (!card.contexts.includes('anywhere') && !card.contexts.includes(area))) continue;
      if (area === 'home' && card.outdoors) continue;
      if (['wet', 'adverse'].includes(weather) && card.outdoors) continue;
      if (preferences.free !== false && card.cost !== 'free') continue;
      if ((negatives[card.family] || 0) >= 2) continue;
      const matches = card.place_category ? places.filter(p => p.category === card.place_category && (preferences.free === false || !p.possible_cost)) : [null];
      for (const place of matches) {
        const id = card.id + (place ? ':' + place.id : '');
        const score = (card.time === time ? 12 : 0) + (levels[card.energy] === energy ? 3 : 0) + (place ? 16 : 0) + (weather === 'fair' && card.outdoors ? 3 : 0) + Math.min(positives[card.family] || 0, 2) - (negatives[card.family] || 0) * 8 - (recent.includes(id) ? 30 : 0);
        const reasons = ['fits_time', 'fits_energy'];
        if (place) reasons.push('real_place');
        if (['wet', 'adverse'].includes(weather)) reasons.push('indoors_weather');
        if (preferences.environment !== 'auto') reasons.push('your_environment');
        if (feedback.length) reasons.push('your_feedback');
        candidates.push({...card, selection_id: id, place, score, reasons, area});
      }
    }
    let choices = candidates.filter(c => c.selection_id !== currentId);
    if (!choices.length) choices = candidates;
    if (!choices.length) return null;
    const unseen = choices.filter(c => !recent.includes(c.selection_id));
    if (unseen.length) choices = unseen;
    choices.sort((a, b) => b.score - a.score || a.selection_id.localeCompare(b.selection_id));
    const best = choices.filter(c => c.score === choices[0].score);
    return best[Math.abs(sequence) % best.length];
  }
  function text(card, language = 'en') {
    const source = card[language] || card.en;
    if (!source) return null;
    const replace = s => String(s || '').replaceAll('{place}', card.place ? card.place.name : '');
    return Object.fromEntries(Object.entries(source).map(([k, v]) => [k, replace(v)]));
  }
  function maps(place, directions = false) {
    if (!placeValid(place)) return null;
    const url = new URL(directions ? 'https://www.google.com/maps/dir/' : 'https://www.google.com/maps/search/');
    url.searchParams.set('api', '1');
    url.searchParams.set(directions ? 'destination' : 'query', `${place.lat},${place.lon}`);
    return url.href;
  }
  return {select, text, maps, weatherMode, environment, placeValid, coordinate};
});
