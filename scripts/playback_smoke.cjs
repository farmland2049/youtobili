// Optional live media check; platform behavior may require interaction or login.
const { chromium } = require('playwright');
const fs = require('node:fs');
(async () => {
  const browser = await chromium.launch({ headless: true });
  const data = JSON.parse(fs.readFileSync('data.json'));
  const requested = (process.env.PLAYBACK_IDS || '').split(',').map(id => id.trim()).filter(Boolean);
  const cases = requested.length ? requested.map(id => ({ label: id, video: data.videos.find(v => v.id === id) })) : ['official_zh', 'sub_zh', 'original', 'dub_zh'].map(kind => ({
    label: kind, video: data.videos.find(v => v.versions[0].kind === kind)
  }));
  if (!requested.length) {
    cases.push({ label: 'short', video: data.videos.find(v => v.versions[0].duration < 600) });
    cases.push({ label: 'collection', video: data.videos.find(v => v.versions[0].page > 1) });
  }
  if (cases.some(sample => !sample.video) && requested.length) throw Error('Requested original is not published');
  const results = [];
  for (const sample of cases.filter(c => c.video)) {
    const v = sample.video, version = v.versions[0];
    const page = await browser.newPage();
    try {
      await page.goto((process.env.TEST_URL || 'http://127.0.0.1:8765/') + '#v/' + v.id);
      await page.locator('iframe').waitFor();
      const frame = page.locator('iframe').contentFrame();
      await frame.locator('video').waitFor({ timeout: 20000 });
      const before = await frame.locator('video').first().evaluate(e => e.currentTime);
      await frame.locator('video').first().click({ force: true });
      try {
        await frame.locator('video').first().evaluate(e => Promise.race([
          e.play(), new Promise(resolve => setTimeout(resolve, 5000))
        ]));
      } catch { /* Record the observable result rather than assume success. */ }
      await page.waitForTimeout(4000);
      const media = await frame.locator('video').first().evaluate(e => ({
        readyState: e.readyState, currentTime: e.currentTime, paused: e.paused, error: e.error?.code
      }));
      results.push({ sample: sample.label, kind: version.kind, id: v.id,
        bvid: version.bvid, page: version.page,
        playing: !media.paused && media.currentTime > before + 1, media,
        visible_text: (await frame.locator('body').innerText()).slice(0, 400) });
      await page.screenshot({ path: '.artifacts/player-' + sample.label + '.png' });
    } catch (error) {
      results.push({ sample: sample.label, error: error.message.slice(0, 250), playing: false });
    } finally { await page.close(); }
  }
  const file = process.env.PLAYBACK_REPORT || 'reports/playback-checks.json';
  fs.writeFileSync(file, JSON.stringify({ checked_at: new Date().toISOString(), checks: results }, null, 2) + '\n');
  console.log(JSON.stringify(results, null, 2));
  await browser.close();
})().catch(error => { console.error(error); process.exit(1); });
