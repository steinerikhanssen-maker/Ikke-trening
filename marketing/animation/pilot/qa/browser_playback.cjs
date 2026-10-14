const {chromium}=require('@playwright/test');const fs=require('node:fs');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.GNF_CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox','--autoplay-policy=no-user-gesture-required']});const results=[];
 for(const mobile of [false,true]){
  const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1100},isMobile:mobile,hasTouch:mobile});const page=await context.newPage();await page.goto('http://127.0.0.1:8090/review.html');
  const cases=[{index:0,muted:false,duration:12},{index:0,muted:true,duration:12},{index:1,muted:false,duration:2},{index:2,muted:true,duration:2},{index:3,muted:false,duration:2}];
  for(const test of cases){
   const video=page.locator('video').nth(test.index);await video.scrollIntoViewIfNeeded();
   const r=await video.evaluate(async(v,muted)=>{
    v.load();v.muted=muted;
    const end=new Promise((resolve,reject)=>{const timer=setTimeout(()=>reject(Error('Playback timeout')),25000);v.addEventListener('ended',()=>{clearTimeout(timer);resolve({width:v.videoWidth,height:v.videoHeight,duration:v.duration,currentTime:v.currentTime,frames:v.getVideoPlaybackQuality().totalVideoFrames,dropped:v.getVideoPlaybackQuality().droppedVideoFrames,muted:v.muted,audioDecodedBytes:v.webkitAudioDecodedByteCount??null,error:v.error?.message??null})},{once:true});v.addEventListener('error',()=>reject(Error(v.error?.message)),{once:true})});await v.play();return end;
   },test.muted);
   if(r.width!==1080||r.height!==1920||Math.abs(r.duration-test.duration)>.02||r.frames<test.duration*30-2||r.error)throw Error(JSON.stringify(r));
   results.push({mode:mobile?'Chromium mobile emulation':'Chromium desktop',clip:test.index,...r,status:'PASS'});
  }
  await page.locator('video').evaluateAll(vs=>Promise.all(vs.map(v=>new Promise((resolve,reject)=>{v.preload='auto';v.addEventListener('loadeddata',resolve,{once:true});v.addEventListener('error',reject,{once:true});v.load();}))));await page.screenshot({path:'marketing/animation/pilot/qa/review-'+(mobile?'mobile':'desktop')+'.png',fullPage:true});await context.close();
 }
 fs.writeFileSync('marketing/animation/pilot/qa/browser-playback.json',JSON.stringify({browser:browser.version(),physicalPhone:'NOT TESTED',humanListening:'NOT TESTED',scope:'Actual decoded playback, full film with audio enabled and muted in both viewports',results},null,2)+'\n');await browser.close();console.log('PASS: ten actual playback runs, including full film with sound enabled/muted');
})().catch(e=>{console.error(e);process.exit(1)});
