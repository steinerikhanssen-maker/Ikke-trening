// Actual Chromium playback in desktop and mobile emulation; no physical-phone claim.
const {chromium}=require('@playwright/test');
const fs=require('node:fs'); const path=require('node:path');
(async()=>{
 const browser=await chromium.launch({executablePath:process.env.GNF_CHROMIUM_PATH||'/usr/bin/chromium',headless:true,args:['--no-sandbox']});
 const results=[];
 for(const mobile of [false,true]){
  const context=await browser.newContext({viewport:mobile?{width:390,height:844}:{width:1440,height:1000},isMobile:mobile,hasTouch:mobile});
  const page=await context.newPage();
  await page.goto('http://127.0.0.1:8090/review.html');
  for(const index of [0,1,2]){
   await page.locator('video').nth(index).scrollIntoViewIfNeeded();
   const r=await page.locator('video').nth(index).evaluate(async video=>{
    video.muted=true; // Can verify decoded playback, not human audibility.
    const completion=new Promise((resolve,reject)=>{ video.addEventListener('ended',()=>resolve({width:video.videoWidth,height:video.videoHeight,duration:video.duration,currentTime:video.currentTime,error:video.error?.message||null,frames:video.getVideoPlaybackQuality().totalVideoFrames}),{once:true});video.addEventListener('error',()=>reject(Error(video.error?.message)),{once:true});setTimeout(()=>reject(Error('Playback timeout')),15000);});
    await video.play();return completion;
   });
   if(r.width!==540||r.height!==960||Math.abs(r.duration-2)>.02||r.frames<59)throw Error(JSON.stringify(r));
   results.push({mode:mobile?'Chromium mobile emulation':'Chromium desktop',clip:index,...r,status:'PASS'});
  }
  // Restore posters so full-page screenshots include offscreen video cards.
  await page.locator('video').evaluateAll(videos=>videos.forEach(video=>video.load()));
  await page.evaluate(async()=>Promise.all([...document.images].map(img=>img.decode().catch(()=>{}))));
  await page.screenshot({path:path.join('marketing/animation/pilot/qa',mobile?'review-mobile.png':'review-desktop.png'),fullPage:true});
  await context.close();
 }
 fs.writeFileSync('marketing/animation/pilot/qa/browser-playback.json',JSON.stringify({browser:browser.version(),audioListening:'NOT TESTED',physicalPhone:'NOT TESTED',results},null,2)+'\n');
 await browser.close(); console.log('PASS: six actual Chromium playback runs');
})().catch(e=>{console.error(e);process.exit(1)});
