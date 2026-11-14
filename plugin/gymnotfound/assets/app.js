(function () {
  'use strict';
  const root = document.getElementById('gymnotfound');
  if (!root) return;
  const cfg = window.GNF_CONFIG || {};
  const E = window.GNFEngine, S = window.GNFStorage;
  let local;
  try { local = window.localStorage; } catch { local = null; }
  const loaded = S.load(local, cfg.language);
  let state = loaded.state, storageOK = loaded.available;
  let catalog = Array.isArray(cfg.catalog) ? cfg.catalog : window.GNF_CATALOG;
  let context = {places: [], weather: null, offline: !navigator.onLine};
  let view = 'today', mode = state.pending ? 'pending' : 'card';
  let card = null, notice = '', results = [], locating = false, searching = false;
  let requestVersion = 0, locationVersion = 0, controller = null;
  const t = key => (window.GNF_LOCALES[state.prefs.language] || window.GNF_LOCALES.en)[key] || key;
  function el(tag, attrs = {}, ...children) {
    const node = document.createElement(tag);
    for (const [key, value] of Object.entries(attrs)) {
      if (key.startsWith('on') && typeof value === 'function') node.addEventListener(key.slice(2), value);
      else if (key === 'checked' || key === 'disabled') node[key] = Boolean(value);
      else if (value !== null && value !== undefined) node.setAttribute(key, String(value));
    }
    for (const child of children.flat()) if (child !== null && child !== undefined) node.append(child instanceof Node ? child : document.createTextNode(String(child)));
    return node;
  }
  const button = (key, action, attrs = {}) => el('button', {type: 'button', onclick: action, ...attrs}, t(key));
  const link = (label, url, attrs = {}) => el('a', {href: url, target: '_blank', rel: 'noopener noreferrer', ...attrs}, label);
  function persist() { storageOK = S.save(local, state); }
  function choose() {
    state.sequence++;
    card = E.select(catalog, state.prefs, context, state.feedback, state.recent, card ? card.selection_id : '', state.sequence);
    if (card) state.recent = [...state.recent, card.selection_id].slice(-12);
    persist();
  }
  function selectField(id, label, value, options, handler) {
    const select = el('select', {id, onchange: e => handler(e.target.value)}, options.map(([val, key]) => el('option', {value: val}, t(key))));
    select.value = String(value);
    return el('label', {for: id}, t(label), select);
  }
  function changePreference(key, value) {
    state.prefs[key] = key === 'time' ? Number(value) : value;
    if (key === 'language') {
      persist(); render(); return;
    }
    choose(); render();
    if (['time','environment'].includes(key) && state.prefs.area) refreshContext();
  }
  const timeOptions = [[2,'two'],[15,'fifteen'],[30,'thirty']];
  const energyOptions = [['low','low'],['some','some'],['high','high']];
  function quick() {
    return el('div', {class: 'quick'},
      selectField('gnf-time','time',state.prefs.time,timeOptions,v=>changePreference('time',v)),
      selectField('gnf-energy','energy',state.prefs.energy,energyOptions,v=>changePreference('energy',v)));
  }
  function answer(type, message) {
    const target = mode === 'pending' ? state.pending : card;
    if (target) S.feedback(state, target, type);
    if (mode === 'pending') state.pending = null;
    notice = message; mode = 'card'; choose(); render(true);
  }
  function accept() {
    if (!card) return;
    S.accept(state, card, E.text(card, state.prefs.language).title, crypto.randomUUID ? crypto.randomUUID() : Date.now().toString(36) + Math.random().toString(36).slice(2));
    mode = 'pending'; notice = ''; persist(); render(true);
  }
  function complete() {
    if (!S.complete(state)) return;
    notice = 'savedDone'; mode = 'card'; choose(); render(true);
  }
  function date(value) {
    const stamp = new Date(value);
    return Number.isFinite(stamp.getTime()) ? stamp.toLocaleDateString(state.prefs.language === 'nb' ? 'nb-NO' : 'en-GB', {year:'numeric',month:'short',day:'numeric'}) : '';
  }
  function weather() {
    if (!state.prefs.area) return null;
    const condition = E.weatherMode(context.weather);
    if (condition === 'unknown') return cfg.weatherEnabled ? el('p',{class:'muted'},t('weatherUnknown')) : null;
    const label = condition === 'fair' ? 'weatherFair' : condition === 'wet' ? 'weatherWet' : 'weatherAdverse';
    return el('div',{class:'weather'},t(label), el('div',{class:'source'},link(t('metCredit'),'https://api.met.no/doc/locationforecast/HowTO')));
  }
  function activity() {
    if (!card) return el('section',{class:'card'},el('h1',{id:'gnf-title',tabindex:'-1'},t('noMatch')),el('p',{},t('noMatchText')),button('rest',()=>answer('rested','savedRest')));
    const words = E.text(card, state.prefs.language);
    const minutes = t(card.time === 2 ? 'two' : card.time === 15 ? 'fifteen' : 'thirty');
    const node = el('article',{class:'card','data-card-id':card.id,'data-family':card.family,'aria-labelledby':'gnf-title'},
      el('span',{class:'kicker'},t(card.family === 'home' ? 'home_family' : card.family)),
      el('h1',{id:'gnf-title',tabindex:'-1'},words.title),
      el('p',{},words.description),
      el('div',{class:'meta'},el('span',{class:'tag'},t('allocated')+': '+minutes),el('span',{class:'tag'},t(card.cost === 'free' ? 'purchaseFree' : 'costMaybe'))),
      el('div',{class:'step'},el('strong',{},t('step')),el('p',{},words.step)),
      el('div',{class:'actions'},button('try',accept,{class:'primary',id:'gnf-try'}),button('newIdea',()=>{notice='';choose();render(true);},{id:'gnf-new'})),
      button('notNow',()=>answer('not_now','savedNotNow'),{class:'quiet'}),
      el('details',{},el('summary',{},t('why')),el('ul',{},card.reasons.map(r=>el('li',{},t(r))))));
    if (card.instructions) node.append(el('p',{},t('safety')+': '+card.safety),el('p',{},t('alternative')+': '+card.alternative));
    if (card.place) {
      node.append(el('div',{class:'place-info'},el('p',{class:'muted'},t('placeCaution')),
        el('div',{class:'actions'},link(t('maps'),E.maps(card.place),{class:'button'}),link(t('directions'),E.maps(card.place,true),{class:'button'})),
        el('p',{class:'muted'},t('mapsInfo')),
        el('p',{class:'source'},link(t('geoCredit'),'https://www.geoapify.com/'),' · ',link(t('osmCredit'),'https://www.openstreetmap.org/copyright'),el('br'),t('foundAt')+': '+date(card.place.retrieved_at))));
    }
    return node;
  }
  function today() {
    const nodes = [quick()];
    if (mode === 'pending' && state.pending) {
      const p = state.pending;
      const current = catalog.find(c=>c.id===p.id);
      // A pending title is not a fresh professional approval. Never redisplay an old dose.
      const title = p.instructions ? t('pending') : current && !current.place_category ? E.text(current,state.prefs.language).title : p.title;
      nodes.push(el('section',{class:'card'},el('span',{class:'kicker'},t('pending')),
        el('h1',{id:'gnf-title',tabindex:'-1'},t('phoneAway')),el('h2',{},title),el('p',{},t('phoneAwayText')),el('p',{class:'muted'},t('pendingText')),
        el('div',{class:'actions'},button('done',complete,{class:'primary',id:'gnf-done'}),button('didntFit',()=>answer('did_not_fit','savedReject'))),
        el('div',{class:'actions'},button('later',()=>answer('later','savedLater')),button('notNow',()=>answer('not_now','savedNotNow'))),
        button('back',()=>{mode='card';render(true);},{class:'quiet'})));
    } else {
      if (state.pending) nodes.push(button('pending',()=>{mode='pending';render(true);},{class:'quiet'}));
      nodes.push(weather(),activity());
      if (state.prefs.nim && card) nodes.push(el('aside',{class:'nim','aria-label':'NIM'},el('img',{src:cfg.nim,alt:'',width:48,height:48}),el('span',{},E.text(card,state.prefs.language).nim)));
    }
    nodes.push(el('p',{class:'source'},t('noAdvice')));
    return nodes;
  }
  function history() {
    return [el('h1',{id:'gnf-title',tabindex:'-1'},t('recorded')),el('p',{class:'muted'},t('historyNote')),
      state.completed.length ? el('ol',{class:'history-list'},[...state.completed].reverse().map(e=>el('li',{},el('strong',{},e.title),el('span',{class:'muted'},t('selfReport')),el('time',{datetime:e.at},date(e.at))))) : el('p',{class:'empty'},t('historyEmpty'))];
  }
  function exportData() {
    const file = new Blob([JSON.stringify(S.normalize(state,state.prefs.language),null,2)],{type:'application/json'});
    const url = URL.createObjectURL(file);
    const a = el('a',{href:url,download:'gymnotfound-data.json'});a.click();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  function deleteDialog() {
    const dialog = el('dialog',{'aria-labelledby':'gnf-delete-title','aria-describedby':'gnf-delete-description'},
      el('h2',{id:'gnf-delete-title'},t('deleteTitle')),el('p',{id:'gnf-delete-description'},t('deleteText')));
    const close = () => {dialog.close();dialog.remove();document.getElementById('gnf-delete')?.focus();};
    dialog.append(el('div',{class:'actions'},button('cancel',close,{autofocus:true}),button('confirmDelete',()=>{
      requestVersion++;locationVersion++;locating=false;controller?.abort();
      state = S.clear(local,state.prefs.language);context = {places:[],weather:null,offline:!navigator.onLine};
      results=[];card=null;mode='card';notice='deleted';dialog.close();dialog.remove();
      storageOK = true;choose();render(true);
    },{class:'primary'})));
    dialog.addEventListener('cancel',e=>{e.preventDefault();close();});
    root.append(dialog);dialog.showModal();
  }
  function settings() {
    const prefs = el('section',{class:'settings-group'},el('h2',{},t('preferences')),quick(),
      selectField('gnf-environment','environment',state.prefs.environment,[['auto','auto'],['urban','urban'],['suburban','suburban'],['rural','rural'],['home','home'],['anywhere','anywhere']],v=>changePreference('environment',v)),
      el('label',{class:'field'},el('input',{id:'gnf-free',type:'checkbox',checked:state.prefs.free,onchange:e=>changePreference('free',e.target.checked)}),t('free')),
      el('label',{class:'field'},el('input',{id:'gnf-nim',type:'checkbox',checked:state.prefs.nim,onchange:e=>changePreference('nim',e.target.checked)}),t('nim')));
    const area = el('section',{class:'settings-group'},el('h2',{},t('location')),el('p',{class:'muted'},t('locationInfo')),
      el('p',{},state.prefs.area ? state.prefs.area.label || t('approximateArea') : t('noArea')),
      button(locating?'locating':'useLocation',locate,{id:'gnf-locate',disabled:locating}),
      state.prefs.area ? button('clearArea',forgetArea,{id:'gnf-clear-area'}) : null);
    if (cfg.placesEnabled) {
      const input = el('input',{id:'gnf-query',type:'search',minlength:2,maxlength:80,required:true,autocomplete:'off'});
      const form = el('form',{onsubmit:e=>{e.preventDefault();search(input.value);}},el('label',{for:'gnf-query',class:'field'},t('searchTown'),input),button(searching?'searching':'search',()=>{}, {type:'submit',disabled:searching}),el('p',{class:'muted'},t('searchInfo')));
      area.append(form,el('div',{class:'search-results'},results.map((item,i)=>el('button',{type:'button',id:'gnf-result-'+i,onclick:()=>{setArea(item);results=[];}},item.label))));
    } else area.append(el('p',{class:'muted'},t('placesOff')));
    if (!cfg.weatherEnabled) area.append(el('p',{class:'muted'},t('weatherOff')));
    const data = el('section',{class:'settings-group'},el('h2',{},t('privacy')),el('p',{class:'privacy-text'},t('privacyText')),
      el('div',{class:'actions'},button('export',exportData),button('delete',deleteDialog,{id:'gnf-delete'})));
    return [el('h1',{id:'gnf-title',tabindex:'-1'},t('settings')),prefs,area,data,el('p',{class:'source'},t('contentCredit'))];
  }
  function render(focus = false) {
    const previous = document.activeElement?.id;
    root.lang = state.prefs.language;
    if (document.body.classList.contains('gnf-shell')) document.documentElement.lang = state.prefs.language;
    const main = el('main',{id:'gnf-main'},
      el('div',{class:'notice',role:'status','aria-live':'polite'},notice ? t(notice) : ''),
      !storageOK ? el('p',{class:'notice'},t('storageError')) : null,
      context.offline ? el('p',{class:'notice'},t('offline')) : null,
      view === 'settings' ? settings() : view === 'history' ? history() : today());
    root.replaceChildren(
      el('a',{class:'gnf-skip',href:'#gnf-title'},t('idea')),
      el('header',{class:'gnf-header'},el('div',{class:'header-inner'},el('div',{class:'brand'},el('span',{class:'brand-mark','aria-hidden':'true'},el('img',{src:cfg.mark,width:24,height:24,alt:''})),el('div',{},el('strong',{},'GymNotFound.'),el('small',{},t('tagline')))),
        el('div',{class:'language'},selectField('gnf-language','language',state.prefs.language,[['en','English'],['nb','Norsk']],v=>changePreference('language',v))))),main,
      el('nav',{'aria-label':'GymNotFound'},['today','history','settings'].map(name=>button(name,()=>{view=name;notice='';render(true);},{'aria-current':view===name?'page':null,id:'gnf-nav-'+name}))));
    // Language names are names, not translatable UI keys.
    document.querySelector('#gnf-language option[value=en]').textContent = 'English';
    document.querySelector('#gnf-language option[value=nb]').textContent = 'Norsk';
    if (focus) document.getElementById('gnf-title')?.focus({preventScroll:true});
    else if (previous) document.getElementById(previous)?.focus({preventScroll:true});
  }
  function endpoint(route) {
    const url = new URL(cfg.endpoint,location.href);
    if (url.origin !== location.origin || !['context','search'].includes(route)) throw new Error('Invalid API');
    if (url.searchParams.has('rest_route')) url.searchParams.set('rest_route',url.searchParams.get('rest_route').replace(/\/$/,'')+'/'+route);
    else url.pathname=url.pathname.replace(/\/$/,'')+'/'+route;
    return url;
  }
  async function request(route,data,signal) {
    const response = await fetch(endpoint(route),{method:'POST',credentials:'omit',headers:{'Content-Type':'application/json'},body:JSON.stringify(data),signal});
    if (!response.ok) throw new Error('Source unavailable');
    const body = await response.text();
    if (body.length>196608) throw new Error('Response too large');
    return JSON.parse(body);
  }
  async function refreshContext() {
    const area = state.prefs.area;
    const version = ++requestVersion;
    controller?.abort();controller=new AbortController();
    const currentController=controller;
    context = {places:[],weather:null,offline:!navigator.onLine};
    if (!area || !navigator.onLine || (!cfg.weatherEnabled && !cfg.placesEnabled)) {choose();render();return;}
    // Show an honest generic card while waiting; never keep an expired forecast visible.
    if (mode==='card') choose();render();
    const timeout = setTimeout(()=>currentController.abort(),12000);
    try {
      const data = await request('context',{lat:area.lat,lon:area.lon,time:state.prefs.time,environment:state.prefs.environment},currentController.signal);
      if (version!==requestVersion) return;
      context={places:Array.isArray(data.places?.items)?data.places.items.filter(E.placeValid):[],weather:data.weather,offline:!navigator.onLine};
      if (view==='today' && mode==='card') choose();
    } catch {if(version===requestVersion) {context={places:[],weather:null,offline:!navigator.onLine};if(mode==='card')choose();}}
    finally {clearTimeout(timeout);if(version===requestVersion)render();}
  }
  function setArea(area) {
    if (!E.coordinate(area.lat,area.lon)) return;
    state.prefs.area={lat:Math.round(area.lat*100)/100,lon:Math.round(area.lon*100)/100,label:String(area.label||t('approximateArea')).slice(0,100)};
    results=[];notice='';persist();render();refreshContext();
  }
  function forgetArea() {
    requestVersion++;locationVersion++;locating=false;controller?.abort();state.prefs.area=null;context={places:[],weather:null,offline:!navigator.onLine};
    results=[];notice='areaForgotten';choose();render();
  }
  function locate() {
    if (!navigator.geolocation) {notice='locationDenied';render();return;}
    const version=++locationVersion;locating=true;render();
    navigator.geolocation.getCurrentPosition(position=>{
      if(version!==locationVersion)return;
      locating=false;setArea({lat:position.coords.latitude,lon:position.coords.longitude,label:t('approximateArea')});
    },()=>{if(version!==locationVersion)return;locating=false;notice='locationDenied';render();},{enableHighAccuracy:false,timeout:8000,maximumAge:300000});
  }
  async function search(query) {
    if (!cfg.placesEnabled || searching) return;
    searching=true;results=[];notice='';render();
    const abort = new AbortController();const timeout=setTimeout(()=>abort.abort(),7000);
    try {
      const data = await request('search',{query:query.trim()},abort.signal);
      results=Array.isArray(data.items)?data.items.filter(x=>E.coordinate(x.lat,x.lon)&&typeof x.label==='string'):[];
      if (!results.length) notice=data.status==='ok'?'noResults':'sourceError';
    } catch {notice='sourceError';}
    finally {clearTimeout(timeout);searching=false;render();}
  }
  window.addEventListener('offline',()=>{requestVersion++;controller?.abort();context={places:[],weather:null,offline:true};if(mode==='card')choose();render();});
  window.addEventListener('online',()=>refreshContext());
  document.addEventListener('visibilitychange',()=>{
    if (document.visibilityState==='visible' && state.prefs.area && context.weather?.status==='ok' && E.weatherMode(context.weather)==='unknown') refreshContext();
  });
  choose();render();
  if (state.prefs.area) refreshContext();
})();
