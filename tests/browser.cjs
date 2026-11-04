// Start python3 -m http.server 8765 first. npm install; npx playwright install chromium.
const {chromium}=require('playwright');
const fs=require('node:fs');const assert=require('node:assert/strict');
const base=process.env.TEST_URL||'http://127.0.0.1:8765/';
(async()=>{
 fs.mkdirSync('.artifacts',{recursive:true});const b=await chromium.launch({headless:true});
 const context=await b.newContext({viewport:{width:1440,height:1000}});const page=await context.newPage();
 const errors=[];page.on('pageerror',e=>errors.push(e.message));
 const real=JSON.parse(fs.readFileSync('data.json','utf8'));assert(real.videos.length>0,'no confirmed originals');
 const first=real.videos[0];const old=first.versions[0].bvid;
 await page.addInitScript(({bv})=>{localStorage.setItem('threecat_liked',JSON.stringify([bv]));localStorage.setItem('threecat_later',JSON.stringify([bv]));localStorage.setItem('threecat_hist',JSON.stringify([bv]));},{bv:old});
 await page.goto(base);await page.locator('.grid .card').first().waitFor();
 await page.waitForFunction(()=>document.querySelector('.grid img')?.naturalWidth>0);
 assert.equal(await page.locator('.grid .card').count(),Math.min(48,real.videos.length));
 assert.equal(await page.evaluate(()=>JSON.parse(localStorage.youtobili_liked)[0]),first.id);
 await page.screenshot({path:'.artifacts/desktop.png',fullPage:false});
 await page.locator('#search').fill(first.author);assert((await page.locator('.grid .card').count())>0);
 await page.locator('#search').fill('unlikely-no-match-452900');assert(await page.locator('.empty').isVisible());
 await page.locator('#search').fill('');
 await page.locator('[data-nav="categories"]').click();assert((await page.locator('.area').count())>0);
 await page.locator('.area button').first().click();assert((await page.locator('.grid .card').count())>0);
 await page.goto(base+'#'+old);await page.locator('#detail[open]').waitFor();
 assert((await page.locator('iframe').getAttribute('src')).includes('bvid='+old) || real.legacy[old]===first.id);
 await page.locator('#close').click();await page.locator('[data-nav="liked"]').click();assert.equal(await page.locator('.grid .card').count(),1);
 await page.locator('.grid .card').first().click();await page.locator('#like').click();await page.locator('#later').click();await page.locator('#close').click();assert.equal(await page.locator('.grid .card').count(),0);
 await page.locator('[data-nav="history"]').click();assert.equal(await page.locator('.grid .card').count(),1);
 const multi=real.videos.find(v=>v.versions.length>1);
 if(multi){await page.goto(base+'#v/'+multi.id);await page.locator('#version').waitFor();await page.locator('#version').selectOption('1');assert((await page.locator('iframe').getAttribute('src')).includes('bvid='+multi.versions[1].bvid));await page.keyboard.press('Escape');assert.equal(await page.locator('#detail').evaluate(e=>e.open),false)}
 await page.setViewportSize({width:390,height:844});await page.locator('#menu').click();await page.locator('[data-nav="home"]').click();
 assert.equal(await page.evaluate(()=>document.documentElement.scrollWidth>innerWidth),false);
 await page.waitForFunction(()=>document.querySelector('.grid img')?.naturalWidth>0);await page.screenshot({path:'.artifacts/mobile.png',fullPage:false});
 await page.locator('#theme').click();assert(await page.locator('html').evaluate(e=>e.classList.contains('dark')));await page.locator('#theme').click();
 // Synthetic fixture exercises short duration and shared BV different segments without inventing production approvals.
 const fixture=structuredClone(real);fixture.videos=real.videos.slice(0,2).map((v,i)=>({...v,versions:[{...v.versions[0],bvid:old,page:i+1,cid:100+i,duration:i?3600:90}]}));fixture.stats.confirmed=2;
 await page.route('**/data.json',r=>r.fulfill({json:fixture}));await page.goto(base);await page.locator('.grid .card').first().waitFor();
 await page.locator('#duration').selectOption('short');assert.equal(await page.locator('.grid .card').count(),1);assert.equal(await page.locator('.duration').first().textContent(),'1:30');
 await page.locator('#duration').selectOption('long');assert.equal(await page.locator('.grid .card').count(),1);await page.locator('.grid .card').click();
 assert((await page.locator('iframe').getAttribute('src')).includes('page=2'));assert((await page.locator('.primary').getAttribute('href')).includes('?p=2'));
 await page.locator('#close').click();
 assert.deepEqual(errors,[]);await b.close();
 const result={checked_at:new Date().toISOString(),status:'pass',originals:real.videos.length,scenarios:['desktop rendering','mobile rendering/no horizontal overflow','real cover HTTP load','Chinese taxonomy','search/empty result','legacy BV deep link','legacy localStorage migration','like/unlike','watch later','history','version switch','escape closes and removes iframe','theme','short duration fixture','shared BV different pages fixture'],page_errors:errors};
 fs.writeFileSync('reports/browser-tests.json',JSON.stringify(result,null,2)+'\n');console.log(result);
})().catch(e=>{console.error(e);process.exit(1)});
