const { chromium } = require('playwright');
const fs = require('node:fs');
const { evaluatePlaybackResults } = require('./playback_smoke.cjs');

async function main() {
  const inputFile = process.argv[2];
  const outputFile = process.argv[3];
  if (!inputFile || !outputFile) {
    console.error('Usage: node scripts/test_playback_batch.cjs <input_json> <output_json>');
    process.exit(1);
  }

  const items = JSON.parse(fs.readFileSync(inputFile, 'utf-8'));
  const data = JSON.parse(fs.readFileSync('data.json', 'utf-8'));
  const browser = await chromium.launch({ headless: true });
  const results = [];
  const videoTimeout = 15000;

  for (const item of items) {
    const vid = item.vid;
    const bvid = item.bvid;
    const pageNum = item.page || 1;
    const video = data.videos.find(v => v.id === vid);
    if (!video) {
      results.push({ sample: vid, id: vid, bvid, page: pageNum, error: 'Video not in data.json', playing: false });
      continue;
    }
    const version = video.versions.find(c => c.bvid === bvid && c.page === pageNum) || video.versions[0];
    const page = await browser.newPage();
    const requestedCids = new Set();
    page.on('request', req => {
      try {
        const u = new URL(req.url());
        if (u.hostname === 'api.bilibili.com' && u.searchParams.has('cid')) {
          requestedCids.add(u.searchParams.get('cid'));
        }
      } catch {}
    });

    try {
      await page.goto('http://127.0.0.1:8765/#v/' + vid);
      await page.locator('iframe').waitFor();
      const frame = page.locator('iframe').contentFrame();
      await frame.locator('video').waitFor({ timeout: videoTimeout });
      
      try {
        await frame.waitForFunction(() => {
          const v = document.querySelector('video');
          return v && (v.readyState >= 1 || Boolean(v.src) || Boolean(v.currentSrc));
        }, { timeout: 10000 });
      } catch {}

      const before = await frame.locator('video').first().evaluate(e => e.currentTime);
      await frame.locator('video').first().click({ force: true });
      try {
        await frame.locator('video').first().evaluate(e => Promise.race([
          e.play(), new Promise(resolve => setTimeout(resolve, 4000))
        ]));
      } catch {}

      await page.waitForTimeout(1000);
      try {
        const isPaused = await frame.locator('video').first().evaluate(e => e.paused);
        if (isPaused) {
          await frame.locator('video').first().evaluate(e => e.play()).catch(() => {});
        }
      } catch {}

      await page.waitForTimeout(2500);
      const media = await frame.locator('video').first().evaluate(e => ({
        readyState: e.readyState,
        currentTime: e.currentTime,
        duration: e.duration,
        paused: e.paused,
        error: e.error ? e.error.code : null
      }));

      const isPlaying = !media.paused && media.currentTime > before + 0.5;
      const durationMatches = Number.isFinite(media.duration) ? Math.abs(media.duration - version.duration) <= 3 : false;
      const cidObserved = requestedCids.has(String(version.cid));

      results.push({
        sample: vid,
        id: vid,
        bvid: version.bvid,
        page: version.page,
        cid: version.cid,
        playing: isPlaying,
        media,
        expected_duration: version.duration,
        duration_matches_segment: durationMatches,
        requested_cid_observed: cidObserved
      });
      console.log(`[PASS] ${vid} ${bvid} P${pageNum}: playing=${isPlaying}, dur=${media.duration}s`);
    } catch (err) {
      console.log(`[FAIL] ${vid} ${bvid} P${pageNum}: ${err.message}`);
      results.push({
        sample: vid,
        id: vid,
        bvid: version.bvid,
        page: version.page,
        cid: version.cid,
        error: err.message.slice(0, 250),
        playing: false
      });
    } finally {
      await page.close();
    }
  }

  await browser.close();
  const evaluation = evaluatePlaybackResults(results);
  fs.writeFileSync(outputFile, JSON.stringify({
    checked_at: new Date().toISOString(),
    passed: evaluation.passed,
    checks: evaluation.checks
  }, null, 2) + '\n');

  console.log(`Batch playback finished: passed=${evaluation.passed}, total=${results.length}`);
  if (!evaluation.passed) {
    console.error(evaluation.failureMessages.join('\n'));
    process.exit(1);
  }
}

main().catch(err => {
  console.error(err);
  process.exit(1);
});
