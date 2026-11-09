// Audit all 59 untested versions against live player
const { chromium } = require('playwright');
const fs = require('node:fs');
const { evaluatePlaybackCheck } = require('./playback_smoke.cjs');

(async () => {
  const items = JSON.parse(fs.readFileSync('data/work/untested-59.json', 'utf8'));
  const data = JSON.parse(fs.readFileSync('data.json', 'utf8'));
  const testUrl = process.env.TEST_URL || 'http://127.0.0.1:8765/';
  const reportPath = process.env.PLAYBACK_REPORT || 'reports/playback-audit-59.json';

  console.log(`Starting playback audit for ${items.length} versions...`);
  fs.mkdirSync('.artifacts/audit59', { recursive: true });

  const browser = await chromium.launch({ headless: true });
  const results = [];
  let passedCount = 0;
  let failedCount = 0;

  for (let i = 0; i < items.length; i++) {
    const item = items[i];
    const prefix = `[${i + 1}/${items.length}] ${item.id} (${item.bvid} P${item.page})`;
    const video = data.videos.find(v => v.id === item.id);
    if (!video) {
      console.error(`${prefix} -> FAILED: video id not found in data.json`);
      results.push({ sample: item.id, bvid: item.bvid, page: item.page, cid: item.cid, error: 'Video not in data.json', playing: false });
      failedCount++;
      continue;
    }
    const versionIndex = video.versions.findIndex(c => c.bvid === item.bvid && String(c.page) === String(item.page));
    if (versionIndex < 0) {
      console.error(`${prefix} -> FAILED: version not found in data.json`);
      results.push({ sample: item.id, bvid: item.bvid, page: item.page, cid: item.cid, error: 'Version not in data.json', playing: false });
      failedCount++;
      continue;
    }
    const version = video.versions[versionIndex];
    const page = await browser.newPage();
    const requestedCids = new Set();
    page.on('request', request => {
      try {
        const url = new URL(request.url());
        if (url.hostname === 'api.bilibili.com' && url.searchParams.has('cid')) requestedCids.add(url.searchParams.get('cid'));
      } catch {}
    });

    try {
      await page.goto(`${testUrl}#v/${item.id}`);
      if (versionIndex > 0) {
        await page.locator('#version').waitFor({ timeout: 5000 });
        await page.locator('#version').selectOption(String(versionIndex));
      }
      await page.locator('iframe').waitFor({ timeout: 10000 });
      const frame = page.locator('iframe').contentFrame();
      await frame.locator('video').waitFor({ timeout: 20000 });
      const before = await frame.locator('video').first().evaluate(e => e.currentTime);
      await frame.locator('video').first().click({ force: true });
      try {
        await frame.locator('video').first().evaluate(e => Promise.race([
          e.play(), new Promise(resolve => setTimeout(resolve, 5000))
        ]));
      } catch {}
      await page.waitForTimeout(4000);
      const media = await frame.locator('video').first().evaluate(e => ({
        readyState: e.readyState, currentTime: e.currentTime, duration: e.duration, paused: e.paused, error: e.error?.code
      }));
      const res = {
        sample: item.id,
        kind: version.kind,
        id: item.id,
        bvid: version.bvid,
        page: version.page,
        cid: version.cid,
        playing: !media.paused && media.currentTime > before + 1,
        media,
        expected_duration: version.duration,
        duration_matches_segment: Number.isFinite(media.duration) && Math.abs(media.duration - version.duration) <= 3,
        requested_cids: [...requestedCids],
        requested_cid_observed: requestedCids.has(String(version.cid)),
        visible_text: (await frame.locator('body').innerText()).slice(0, 300)
      };
      await page.screenshot({ path: `.artifacts/audit59/${item.id}_${item.bvid}_p${item.page}.png` });

      const issues = evaluatePlaybackCheck(res);
      if (issues.length === 0) {
        console.log(`${prefix} -> OK (dur: ${media.duration.toFixed(1)}s, CID observed: true, playing: true)`);
        passedCount++;
      } else {
        console.error(`${prefix} -> FAILED: ${issues.join('; ')}`);
        failedCount++;
      }
      results.push(res);
    } catch (err) {
      console.error(`${prefix} -> ERROR: ${err.message}`);
      results.push({
        sample: item.id,
        id: item.id,
        bvid: item.bvid,
        page: item.page,
        cid: item.cid,
        error: err.message.slice(0, 250),
        playing: false
      });
      failedCount++;
    } finally {
      await page.close();
    }
  }

  await browser.close();

  const report = {
    audited_at: new Date().toISOString(),
    total: items.length,
    passed_count: passedCount,
    failed_count: failedCount,
    all_passed: failedCount === 0,
    checks: results
  };

  fs.writeFileSync(reportPath, JSON.stringify(report, null, 2) + '\n');
  console.log(`\nAudit complete: ${passedCount} passed, ${failedCount} failed. Report written to ${reportPath}`);

  if (failedCount > 0) {
    process.exit(1);
  } else {
    process.exit(0);
  }
})().catch(err => {
  console.error('Fatal audit error:', err);
  process.exit(1);
});
