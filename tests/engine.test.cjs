const {test}=require('node:test');
const assert=require('node:assert/strict');
const catalog=require('../plugin/gymnotfound/content/activities.json');
const E=require('../plugin/gymnotfound/assets/engine.js');
const now=Date.parse('2026-10-14T12:00:00Z');
const fair={status:'ok',forecast_at:new Date(now).toISOString(),temperature:14,wind:2,precipitation:0};
const prefs={time:15,energy:'some',free:true,environment:'auto'};
const poi=(i,category='park',extra={})=>({id:'TEST_ONLY_'+i,name:'Fixture '+category+' '+i,provider:'geoapify',category,lat:59.9+i/10000,lon:10.7,possible_cost:['cafe','museum'].includes(category),...extra});
const city=Array.from({length:12},(_,i)=>poi(i,['park','library','cafe','museum'][i%4]));
function series(p,ctx={},feedback=[],n=8){const out=[],recent=[];for(let i=0;i<n;i++){const card=E.select(catalog,p,ctx,feedback,recent,out.at(-1)?.selection_id||'',i,now);assert.ok(card);out.push(card);recent.push(card.selection_id);}return out;}
test('36 genuinely distinct bilingual templates; >=12 source-free fallbacks',()=>{
  assert.equal(catalog.length,36);assert.equal(new Set(catalog.map(c=>c.id)).size,36);
  for(const language of ['en','nb']){assert.equal(new Set(catalog.map(c=>c[language].title)).size,36);for(const c of catalog)for(const field of ['title','description','step','nim'])assert.ok(c[language][field]?.length>5);}
  assert.ok(catalog.filter(c=>!c.place_category&&!c.instructions).length>=12);
  for(const time of [2,15,30]) assert.ok(catalog.some(c=>c.time===time));
  assert.ok(catalog.some(c=>c.family==='routine'));
});
test('C1 urban chooses an actual named source place; no invented destination',()=>{
  assert.equal(E.environment(prefs,city),'urban');const c=E.select(catalog,prefs,{places:city,weather:fair},[],[], '',0,now);
  assert.ok(c.place);assert.ok(city.some(p=>p.id===c.place.id));assert.ok(E.text(c,'nb').title.includes(c.place.name));assert.equal(c.place.category,'library');
});
test('C2 sparse countryside never fabricates a cafe or museum',()=>{const rural=[poi(1),poi(2)];assert.equal(E.environment(prefs,rural),'rural');for(const c of series(prefs,{places:rural,weather:fair}))assert.ok(!c.place||c.place.category==='park');});
test('C3 zero places yields >=3 different generic tasks, with >=8 consecutive choices',()=>{const cards=series({time:2,energy:'low',free:true,environment:'rural'},{places:[]},[],8);assert.equal(new Set(cards.map(c=>c.id)).size,8);assert.ok(cards.every(c=>!c.place_category&&c.cost==='free'));});
test('C4 two rejections change the family and remember feedback',()=>{const first=E.select(catalog,prefs,{},[],[], '',0,now);const feedback=[{family:first.family,type:'did_not_fit'},{family:first.family,type:'did_not_fit'}];for(const c of series(prefs,{},feedback))assert.notEqual(c.family,first.family);});
test('C5 private/unsafe/closed/paid places cannot enter a free recommendation',()=>{
  const places=[poi(1,'park',{private:true}),poi(2,'park',{unsafe:true}),poi(3,'park',{closed:true}),poi(4,'museum'),poi(5,'cafe'),poi(6,'park',{possible_cost:true})];
  for(const c of series(prefs,{places,weather:fair}))assert.equal(c.place,null);
  const optional=E.select(catalog.filter(c=>c.place_category==='cafe'),{...prefs,free:false},{places},[],[], '',0,now);assert.equal(optional.cost,'maybe');
});
test('C6 Google Maps URLs are fixed, encoded, with only a public destination',()=>{const p=poi(9,'park',{name:'<img src=x onerror=alert(1)> Å & /'});for(const directions of [false,true]){const u=new URL(E.maps(p,directions));assert.equal(u.hostname,'www.google.com');assert.equal(u.searchParams.get(directions?'destination':'query'),`${p.lat},${p.lon}`);assert.equal(u.searchParams.has('origin'),false);assert.equal(u.searchParams.has('key'),false);}assert.equal(E.maps({...p,provider:'https://evil.invalid'}),null);});
test('C7 explicit environment overrides source density',()=>{assert.equal(E.environment({...prefs,environment:'rural'},city),'rural');for(const c of series({...prefs,environment:'rural'},{places:[]}))assert.ok(c.contexts.includes('anywhere')||c.contexts.includes('rural'));});
test('Weather fair / rain / wind / cold / unknown / stale controls outdoor eligibility',()=>{
  const cases=[['fair',fair],['wet',{...fair,precipitation:2}],['adverse',{...fair,wind:15}],['adverse',{...fair,temperature:-3}],['unknown',null],['unknown',{...fair,forecast_at:'2025-01-01T00:00:00Z'}]];
  for(const [mode,w]of cases){assert.equal(E.weatherMode(w,now),mode);const cards=series({time:2,energy:'low',free:true,environment:'auto'},{weather:w});assert.equal(new Set(cards.map(c=>c.id)).size,8);if(['wet','adverse'].includes(mode))assert.ok(cards.every(c=>!c.outdoors));}
});
test('Time and energy are hard constraints, all combinations remain usable',()=>{for(const time of [2,15,30])for(const energy of ['low','some','high']){const cards=series({...prefs,time,energy});assert.ok(cards.every(c=>c.time<=time));const levels=['low','some','high'];assert.ok(cards.every(c=>levels.indexOf(c.energy)<=levels.indexOf(energy)));assert.equal(cards[0].time,time);}});
test('Unreviewed instructional cards stay hidden, including reviewed cards offline',()=>{const exercise={...catalog[0],id:'TEST_REVIEW',instructions:true,reviewed:false};assert.equal(E.select([exercise],prefs),null);assert.equal(E.select([{...exercise,reviewed:true}],prefs,{offline:true}),null);assert.ok(E.select([{...exercise,reviewed:true}],prefs));});
test('Empty/exhausted catalog yields an honest no-match, never bypasses safety',()=>{assert.equal(E.select([],prefs),null);const feedback=catalog.flatMap(c=>[{family:c.family,type:'did_not_fit'},{family:c.family,type:'did_not_fit'}]);assert.equal(E.select(catalog.slice(-1),prefs,{},feedback),null);});
