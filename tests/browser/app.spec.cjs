const {test,expect}=require('@playwright/test');
const AxeBuilder=require('@axe-core/playwright').default;
const app=process.env.GNF_APP_PATH||'/?page_id=40';
const read=page=>page.evaluate(()=>JSON.parse(localStorage.getItem('gymnotfound.v1')));
async function open(page,language='en') {await page.goto(app);await expect(page.locator('#gnf-try')).toBeVisible();if(language==='nb')await page.locator('#gnf-language').selectOption('nb');}
test('B1/B2 first screen: real card and both actions, no account/GPS/external requests',async({page})=>{
  const external=[],errors=[];page.on('request',r=>{if(!r.url().startsWith('http://localhost:'))external.push(r.url());});page.on('pageerror',e=>errors.push(e.message));
  await page.addInitScript(()=>{window.__gnfGPS=0;navigator.geolocation.getCurrentPosition=()=>{window.__gnfGPS++;};});
  await open(page);const boxes=await Promise.all(['article','#gnf-title','#gnf-try','#gnf-new'].map(s=>page.locator(s).boundingBox()));
  for(const b of boxes)expect(b.y+b.height).toBeLessThan(760);
  expect(await page.evaluate(()=>window.__gnfGPS)).toBe(0);expect(external).toEqual([]);expect(errors).toEqual([]);
  expect(await page.locator('article p').first().textContent()).not.toContain('{place}');
  await expect(page.locator('body')).not.toContainText('Deprecated');
});
for(const language of ['en','nb'])test(`B3-B9/F5 complete local mobile journey (${language})`,async({page})=>{
  await open(page,language);await page.locator('#gnf-time').selectOption('15');await page.locator('#gnf-energy').selectOption('some');
  const titles=[];for(let i=0;i<8;i++){titles.push(await page.locator('#gnf-title').textContent());await page.locator('#gnf-new').click();}expect(new Set(titles).size).toBe(8);
  await page.locator('#gnf-try').click();await expect(page.locator('#gnf-done')).toBeVisible();expect((await read(page)).completed).toHaveLength(0);
  await page.reload();await expect(page.locator('#gnf-done')).toBeVisible();expect((await read(page)).completed).toHaveLength(0);
  await page.locator('#gnf-done').click();expect((await read(page)).completed).toHaveLength(1);expect((await read(page)).completed[0].type).toBe('completed_self_report');
  await page.locator('#gnf-try').click();await page.getByRole('button',{name:language==='nb'?'Passet ikke':'Didn’t fit',exact:true}).click();
  const rejected=(await read(page)).feedback.find(f=>f.type==='did_not_fit');expect(rejected).toBeTruthy();
  await page.reload();expect((await read(page)).feedback.some(f=>f.type==='did_not_fit')).toBe(true);
  await page.locator('#gnf-nav-history').click();await expect(page.locator('.history-list li')).toHaveCount(1);
  await page.locator('#gnf-nav-settings').click();await page.locator('#gnf-nim').uncheck();await page.locator('#gnf-nav-today').click();await expect(page.locator('.nim')).toHaveCount(0);
  await page.locator('#gnf-nav-settings').click();const downloadPromise=page.waitForEvent('download');await page.getByRole('button',{name:language==='nb'?'Eksporter mine data (JSON)':'Export my data (JSON)',exact:true}).click();const download=await downloadPromise;expect(download.suggestedFilename()).toBe('gymnotfound-data.json');
  const path=await download.path(), fs=require('node:fs');const exported=JSON.parse(fs.readFileSync(path,'utf8'));expect(exported.completed).toHaveLength(1);expect(exported.feedback.some(f=>f.type==='did_not_fit')).toBe(true);expect(JSON.stringify(exported.completed)).not.toMatch(/"(lat|lon|duration|steps)"/);
  await page.evaluate(()=>localStorage.setItem('other-site-data','preserve'));
  await page.locator('#gnf-delete').click();await expect(page.getByRole('dialog')).toBeVisible();await page.getByRole('button',{name:language==='nb'?'Avbryt':'Cancel',exact:true}).click();expect((await read(page)).completed).toHaveLength(1);
  await page.locator('#gnf-delete').click();await page.getByRole('button',{name:language==='nb'?'Ja, slett mine data':'Yes, delete my data',exact:true}).click();expect((await read(page)).completed).toHaveLength(0);expect((await read(page)).prefs.area).toBeNull();expect(await page.evaluate(()=>localStorage.getItem('other-site-data'))).toBe('preserve');
  await page.locator('#gnf-nav-today').click();await page.getByRole('button',{name:language==='nb'?'Ikke nå':'Not now',exact:true}).click();expect((await read(page)).completed).toHaveLength(0);await expect(page.locator('[role=status]')).toContainText(language==='nb'?'Helt greit':'No problem');
});
test('D9 explicit approximate position, reset and consent refusal leave no raw GPS',async({page})=>{
  const requests=[];await page.route('**/*rest_route*context*',async route=>{requests.push(route.request().postDataJSON());await route.fulfill({json:{weather:{status:'unavailable'},places:{status:'not_configured',items:[]}}});});
  await page.addInitScript(()=>{window.__gpsCalls=0;navigator.geolocation.getCurrentPosition=(success)=>{window.__gpsCalls++;success({coords:{latitude:59.9123456,longitude:10.7123456}});};});
  await open(page);expect(requests).toHaveLength(0);await page.locator('#gnf-nav-settings').click();await page.locator('#gnf-locate').click();await expect(page.locator('#gnf-clear-area')).toBeVisible();await expect.poll(()=>requests.length).toBe(1);
  expect(requests[0].lat).toBe(59.91);expect(requests[0].lon).toBe(10.71);expect((await read(page)).prefs.area.lat).toBe(59.91);
  await page.locator('#gnf-clear-area').click();expect((await read(page)).prefs.area).toBeNull();await page.reload();await page.locator('#gnf-nav-settings').click();expect(requests).toHaveLength(1);
  await page.evaluate(()=>{navigator.geolocation.getCurrentPosition=(_,error)=>error({code:1});});await page.locator('#gnf-locate').click();await expect(page.locator('[role=status]')).toContainText('Location was not available');
});
test('D4/D7 errors and offline loaded app give a usable source-free idea',async({page,context})=>{
  await page.addInitScript(()=>localStorage.setItem('gymnotfound.v1',JSON.stringify({version:1,prefs:{time:15,energy:'some',area:{lat:59.91,lon:10.71,label:'Fixture area'}}})));
  await page.route('**/*rest_route*context*',route=>route.fulfill({status:500,json:{error:'Fixture failure'}}));await open(page);await expect(page.locator('#gnf-try')).toBeVisible();
  await context.setOffline(true);await expect(page.getByText('Offline. Here is an idea that needs no source.',{exact:true})).toBeVisible();const titles=[];for(let i=0;i<8;i++){titles.push(await page.locator('#gnf-title').textContent());await page.locator('#gnf-new').click();}expect(new Set(titles).size).toBe(8);await expect(page.getByRole('link',{name:/Google Maps/})).toHaveCount(0);await context.setOffline(false);
});
test('E5 rendered external text is text, not executable markup; source and Maps attribution',async({page})=>{
  await page.addInitScript(()=>localStorage.setItem('gymnotfound.v1',JSON.stringify({version:1,prefs:{time:15,energy:'some',area:{lat:59.91,lon:10.71,label:'Fixture area'}}})));
  await page.route('**/*rest_route*context*',route=>route.fulfill({json:{weather:{status:'ok',forecast_at:new Date().toISOString(),temperature:14,wind:2,precipitation:0},places:{status:'ok',items:[{id:'TEST_FIXTURE_LIB',name:'<img src=x onerror="window.__xss=1"> Fixture library',category:'library',lat:59.91,lon:10.71,provider:'geoapify',possible_cost:false,retrieved_at:new Date().toISOString()}]}}}));
  await page.goto(app);await expect(page.locator('#gnf-title')).toContainText('Fixture library');expect(await page.evaluate(()=>window.__xss||0)).toBe(0);await expect(page.locator('article img')).toHaveCount(0);
  for(const name of ['Based on data from MET Norway','Powered by Geoapify','© OpenStreetMap contributors'])await expect(page.getByRole('link',{name,exact:true})).toBeVisible();
  const url=new URL(await page.getByRole('link',{name:'Directions in Google Maps ↗',exact:true}).getAttribute('href'));expect(url.hostname).toBe('www.google.com');expect(url.searchParams.get('destination')).toBe('59.91,10.71');expect(url.searchParams.has('origin')).toBe(false);
});
test('B2/E7/F1 keyboard, axe checks in both languages, focus and reduced motion',async({page})=>{
  await page.emulateMedia({reducedMotion:'reduce'});await open(page);await page.keyboard.press('Tab');const focus=await page.evaluate(()=>getComputedStyle(document.activeElement).outlineStyle);expect(focus).not.toBe('none');
  for(const language of ['en','nb']){await page.locator('#gnf-language').selectOption(language);for(const view of ['today','history','settings']){await page.locator('#gnf-nav-'+view).click();expect(await page.locator('#gnf-title').evaluate(n=>document.activeElement===n)).toBe(true);const result=await new AxeBuilder({page}).include('#gymnotfound').withTags(['wcag2a','wcag2aa','wcag21aa','wcag22aa']).analyze();expect(result.violations).toEqual([]);}}
});
for(const width of [320,360,390,768,1024,1440])test(`F1 layout ${width}px, no overflow or hidden buttons`,async({page},info)=>{
  await page.setViewportSize({width,height:844});await open(page,'nb');for(const view of ['today','history','settings']){await page.locator('#gnf-nav-'+view).click();expect(await page.evaluate(()=>document.documentElement.scrollWidth<=innerWidth)).toBe(true);}
  await page.locator('#gnf-nav-today').click();await page.screenshot({path:`screenshots/${info.project.name}-${width}-nb.png`,fullPage:true});
});
test('Storage unavailable is explained without losing the activity flow',async({page})=>{
  await page.addInitScript(()=>Object.defineProperty(window,'localStorage',{get(){throw new Error('Fixture storage denied');}}));await open(page);await expect(page.getByText(/This browser cannot save app data/)).toBeVisible();await page.locator('#gnf-new').click();await page.locator('#gnf-try').click();await expect(page.locator('#gnf-done')).toBeVisible();await page.locator('#gnf-done').click();await expect(page.locator('#gnf-try')).toBeVisible();
});
test('D9 delete cancels a delayed location result; removed data stays removed',async({page})=>{
  const requests=[];page.on('request',r=>{if(r.url().includes('context'))requests.push(r);});
  await page.addInitScript(()=>{navigator.geolocation.getCurrentPosition=success=>{window.__lateLocation=success;};});
  await open(page);await page.locator('#gnf-nav-settings').click();await page.locator('#gnf-locate').click();
  await page.locator('#gnf-delete').click();await page.getByRole('button',{name:'Yes, delete my data',exact:true}).click();
  await page.evaluate(()=>window.__lateLocation({coords:{latitude:59.912345,longitude:10.712345}}));
  expect((await read(page)).prefs.area).toBeNull();expect(requests).toHaveLength(0);
});
test('D1/D10 stale forecast is removed when the opened app becomes visible again',async({page})=>{
  const now=Date.now();await page.clock.install({time:new Date(now)});
  await page.addInitScript(()=>localStorage.setItem('gymnotfound.v1',JSON.stringify({version:1,prefs:{area:{lat:59.91,lon:10.71,label:'Fixture area'}}})));
  await page.route('**/*rest_route*context*',route=>route.fulfill({json:{weather:{status:'ok',forecast_at:new Date(now).toISOString(),temperature:14,wind:2,precipitation:0},places:{items:[]}}}));
  await open(page);await expect(page.getByRole('link',{name:'Based on data from MET Norway',exact:true})).toBeVisible();
  await page.clock.setSystemTime(new Date(now+6*3600000));await page.evaluate(()=>document.dispatchEvent(new Event('visibilitychange')));
  await expect(page.getByRole('link',{name:'Based on data from MET Norway',exact:true})).toHaveCount(0);await expect(page.locator('#gnf-try')).toBeVisible();
});
test('E3 old pending instruction text is never reissued after the reviewed card is removed',async({page,context})=>{
  await page.addInitScript(()=>localStorage.setItem('gymnotfound.v1',JSON.stringify({version:1,pending:{uid:'TEST_REMOVED',id:'TEST_REMOVED',selection_id:'TEST_REMOVED',family:'routine',title:'TEST instruction: do ten squats',at:new Date().toISOString(),instructions:true}})));
  await page.goto(app);await expect(page.locator('#gnf-done')).toBeVisible();await expect(page.locator('main')).not.toContainText('do ten squats');
  await context.setOffline(true);await expect(page.locator('main')).not.toContainText('do ten squats');await context.setOffline(false);
});
