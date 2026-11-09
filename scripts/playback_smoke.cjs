// Optional live media check; platform behavior may require interaction or login.
const { chromium } = require('playwright');
const fs = require('node:fs');

function evaluatePlaybackCheck(res) {
  const issues = [];
  if (res.error) {
    issues.push(`error: ${res.error}`);
  }
  if (!res.playing) {
    issues.push(`not playing (paused: ${res.media?.paused}, currentTime: ${res.media?.currentTime})`);
  }
  if (!res.requested_cid_observed) {
    issues.push(`expected CID ${res.cid} not observed in network requests`);
  }
  if (!res.duration_matches_segment) {
    const diff = Number.isFinite(res.media?.duration) ? Math.abs(res.media.duration - res.expected_duration).toFixed(1) : 'unknown';
    issues.push(`duration mismatch (media: ${res.media?.duration}s, expected: ${res.expected_duration}s, diff: ${diff}s > 3s)`);
  }
  return issues;
}

if (typeof module !== 'undefined' && module.exports) {
  module.exports = { evaluatePlaybackCheck };
}

if (require.main === module) {
  (async () => {
    const browser = await chromium.launch({ headless: true });
    const data = JSON.parse(fs.readFileSync('data.json'));
    const requested = (process.env.PLAYBACK_IDS || '').split(',').map(id => id.trim()).filter(Boolean);
    const requestedBvids = (process.env.PLAYBACK_BVIDS || '').split(',').map(id => id.trim());
    const requestedPages = (process.env.PLAYBACK_PAGES || '').split(',').map(id => id.trim());
    const cases = requested.length ? requested.map(id => ({ label: id, video: data.videos.find(v => v.id === id) })) : ['official_zh', 'sub_zh', 'original', 'dub_zh'].map(kind => ({
      label: kind, video: data.videos.find(v => v.versions[0].kind === kind)
    }));
    if (!requested.length) {
      cases.push({ label: 'short', video: data.videos.find(v => v.versions[0].duration < 600) });
      cases.push({ label: 'collection', video: data.videos.find(v => v.versions[0].page > 1) });
    }
    if (cases.some(sample => !sample.video) && requested.length) throw Error('Requested original is not published');
    const results = [];
    for (const [sampleIndex, sample] of cases.filter(c => c.video).entries()) {
      const v = sample.video;
      const versionIndex = requestedBvids[sampleIndex] ? v.versions.findIndex((c) => {
        const bvidMatch = c.bvid === requestedBvids[sampleIndex];
        const pageMatch = requestedPages[sampleIndex] ? String(c.page) === requestedPages[sampleIndex] : true;
        return bvidMatch && pageMatch;
      }) : 0;
      if (versionIndex < 0) throw Error('Requested Bilibili version is not published for this original');
      const version = v.versions[versionIndex];
      const page = await browser.newPage();
      const requestedCids = new Set();
      page.on('request', request => {
        try {
          const url = new URL(request.url());
          if (url.hostname === 'api.bilibili.com' && url.searchParams.has('cid')) requestedCids.add(url.searchParams.get('cid'));
        } catch { /* Only retain public segment identifiers, never signed request URLs. */ }
      });
      try {
        await page.goto((process.env.TEST_URL || 'http://127.0.0.1:8765/') + '#v/' + v.id);
        if (versionIndex) await page.locator('#version').selectOption(String(versionIndex));
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
          readyState: e.readyState, currentTime: e.currentTime, duration: e.duration, paused: e.paused, error: e.error?.code
        }));
        results.push({ sample: sample.label, kind: version.kind, id: v.id,
          bvid: version.bvid, page: version.page, cid: version.cid,
          playing: !media.paused && media.currentTime > before + 1, media,
          expected_duration: version.duration,
          duration_matches_segment: Number.isFinite(media.duration) && Math.abs(media.duration - version.duration) <= 3,
          requested_cids: [...requestedCids], requested_cid_observed: requestedCids.has(String(version.cid)),
          visible_text: (await frame.locator('body').innerText()).slice(0, 400) });
        await page.screenshot({ path: '.artifacts/player-' + sample.label + '.png' });
      } catch (error) {
        results.push({ sample: sample.label, id: v.id, bvid: version.bvid, page: version.page, cid: version.cid, error: error.message.slice(0, 250), playing: false });
      } finally { await page.close(); }
    }
    await browser.close();

    const failureMessages = [];
    for (const res of results) {
      const issues = evaluatePlaybackCheck(res);
      if (issues.length > 0) {
        failureMessages.push(`FAILED ${res.sample} (${res.bvid} P${res.page}): ${issues.join('; ')}`);
      }
    }
    const passed = failureMessages.length === 0;

    const file = process.env.PLAYBACK_REPORT || 'reports/playback-checks.json';
    fs.writeFileSync(file, JSON.stringify({ checked_at: new Date().toISOString(), passed, checks: results }, null, 2) + '\n');
    console.log(JSON.stringify(results, null, 2));

    if (!passed) {
      console.error('\n[SMOKE CHECK FAILED]\n' + failureMessages.join('\n'));
      process.exit(1);
    } else {
      console.log(`\n[SMOKE CHECK PASSED] All ${results.length} checks passed.`);
      process.exit(0);
    }
  })().catch(error => { console.error(error); process.exit(1); });
}

