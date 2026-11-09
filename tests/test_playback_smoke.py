import json
import os
import subprocess
import tempfile
import threading
import unittest
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = ROOT / "scripts" / "playback_smoke.cjs"

class TestPlaybackSmoke(unittest.TestCase):
    def evaluate_results(self, results):
        code = """
        const fs = require('node:fs');
        const { evaluatePlaybackResults } = require('./scripts/playback_smoke.cjs');
        const results = JSON.parse(fs.readFileSync(0, 'utf8'));
        const before = JSON.stringify(results);
        const summary = evaluatePlaybackResults(results);
        if (JSON.stringify(results) !== before) throw Error('Input mutated');
        console.log(JSON.stringify(summary));
        """
        result = subprocess.run(
            ['node', '-e', code], cwd=ROOT, input=json.dumps(results),
            capture_output=True, text=True, check=True, timeout=10,
        )
        return json.loads(result.stdout)

    def passing_check(self):
        return {
            'sample': 'test', 'bvid': 'BV1234567890', 'page': 1, 'cid': 12345,
            'playing': True, 'requested_cid_observed': True,
            'duration_matches_segment': True,
        }

    def test_evaluate_results_all_pass(self):
        summary = self.evaluate_results([self.passing_check(), self.passing_check()])
        self.assertTrue(summary['passed'])
        self.assertEqual(summary['failureMessages'], [])
        for check in summary['checks']:
            self.assertTrue(check['passed'])
            self.assertEqual(check['issues'], [])

    def test_evaluate_results_any_failure(self):
        for field, value, issue in [
            ('playing', False, 'not playing'),
            ('requested_cid_observed', False, 'expected CID'),
            ('duration_matches_segment', False, 'duration mismatch'),
            ('error', 'Timeout exceeded', 'error: Timeout exceeded'),
        ]:
            with self.subTest(field=field):
                failed = {**self.passing_check(), field: value}
                summary = self.evaluate_results([self.passing_check(), failed])
                self.assertFalse(summary['passed'])
                self.assertTrue(summary['checks'][0]['passed'])
                self.assertFalse(summary['checks'][1]['passed'])
                self.assertTrue(any(issue in msg for msg in summary['checks'][1]['issues']))
                self.assertTrue(summary['failureMessages'])

    def test_evaluate_results_empty_fails(self):
        summary = self.evaluate_results([])
        self.assertFalse(summary['passed'])
        self.assertEqual(summary['checks'], [])
        self.assertTrue(summary['failureMessages'])

    def test_evaluate_playback_check_all_pass(self):
        code = """
        const { evaluatePlaybackCheck } = require('./scripts/playback_smoke.cjs');
        const res = {
            sample: 'test1', bvid: 'BV1234567890', page: 1, cid: 12345,
            playing: true,
            media: { readyState: 4, currentTime: 4.0, duration: 100, paused: false },
            expected_duration: 100,
            duration_matches_segment: true,
            requested_cid_observed: true
        };
        const issues = evaluatePlaybackCheck(res);
        console.log(JSON.stringify(issues));
        """
        out = subprocess.check_output(["node", "-e", code], cwd=ROOT).decode("utf-8").strip()
        issues = json.loads(out)
        self.assertEqual(issues, [])

    def test_evaluate_playback_check_not_playing(self):
        code = """
        const { evaluatePlaybackCheck } = require('./scripts/playback_smoke.cjs');
        const res = {
            sample: 'test2', bvid: 'BV1234567890', page: 1, cid: 12345,
            playing: false,
            media: { readyState: 2, currentTime: 0.1, duration: 100, paused: true },
            expected_duration: 100,
            duration_matches_segment: true,
            requested_cid_observed: true
        };
        const issues = evaluatePlaybackCheck(res);
        console.log(JSON.stringify(issues));
        """
        out = subprocess.check_output(["node", "-e", code], cwd=ROOT).decode("utf-8").strip()
        issues = json.loads(out)
        self.assertTrue(any("not playing" in issue for issue in issues))

    def test_evaluate_playback_check_duration_mismatch(self):
        code = """
        const { evaluatePlaybackCheck } = require('./scripts/playback_smoke.cjs');
        const res = {
            sample: 'test3', bvid: 'BV1234567890', page: 1, cid: 12345,
            playing: true,
            media: { readyState: 4, currentTime: 4.0, duration: 327.8, paused: false },
            expected_duration: 336,
            duration_matches_segment: false,
            requested_cid_observed: true
        };
        const issues = evaluatePlaybackCheck(res);
        console.log(JSON.stringify(issues));
        """
        out = subprocess.check_output(["node", "-e", code], cwd=ROOT).decode("utf-8").strip()
        issues = json.loads(out)
        self.assertTrue(any("duration mismatch" in issue for issue in issues))

    def test_evaluate_playback_check_cid_not_observed(self):
        code = """
        const { evaluatePlaybackCheck } = require('./scripts/playback_smoke.cjs');
        const res = {
            sample: 'test4', bvid: 'BV1234567890', page: 1, cid: 99999,
            playing: true,
            media: { readyState: 4, currentTime: 4.0, duration: 100, paused: false },
            expected_duration: 100,
            duration_matches_segment: true,
            requested_cid_observed: false
        };
        const issues = evaluatePlaybackCheck(res);
        console.log(JSON.stringify(issues));
        """
        out = subprocess.check_output(["node", "-e", code], cwd=ROOT).decode("utf-8").strip()
        issues = json.loads(out)
        self.assertTrue(any("expected CID" in issue for issue in issues))

    def test_evaluate_playback_check_error(self):
        code = """
        const { evaluatePlaybackCheck } = require('./scripts/playback_smoke.cjs');
        const res = {
            sample: 'test5', bvid: 'BV1234567890', page: 1, cid: 12345,
            error: 'Timeout 20000ms exceeded',
            playing: false
        };
        const issues = evaluatePlaybackCheck(res);
        console.log(JSON.stringify(issues));
        """
        out = subprocess.check_output(["node", "-e", code], cwd=ROOT).decode("utf-8").strip()
        issues = json.loads(out)
        self.assertTrue(any("error:" in issue for issue in issues))

    def test_cli_unpublished_original_fails(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "playback-report.json"
            data_path = Path(tmpdir) / 'data.json'
            data_path.write_text(json.dumps({'videos': []}), encoding='utf-8')
            env = os.environ.copy()
            env["PLAYBACK_IDS"] = "nonexistent_vid_for_test"
            env["PLAYBACK_REPORT"] = str(report_path)
            env['PLAYBACK_DATA'] = str(data_path)
            res = subprocess.run(
                ["node", str(SMOKE_SCRIPT)],
                cwd=tmpdir,
                env=env,
                capture_output=True,
                text=True,
                timeout=20,
            )
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("Requested original is not published", res.stderr + res.stdout)

    def test_cli_caught_video_timeout_fails_and_reports_missing_samples(self):
        class QuietHandler(SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass

        with tempfile.TemporaryDirectory() as tmpdir:
            fixture = Path(tmpdir)
            (fixture / 'index.html').write_text(
                '<!doctype html><select id="version"><option value="0">Fixture</option>'
                '</select><iframe src="/empty.html"></iframe>', encoding='utf-8',
            )
            (fixture / 'empty.html').write_text('<!doctype html><body>Empty player</body>', encoding='utf-8')
            data_path = fixture / 'fixture-data.json'
            data_path.write_text(json.dumps({'videos': [{
                'id': 'fixture_vid', 'versions': [{
                    'kind': 'original', 'bvid': 'BV1234567890',
                    'page': 1, 'cid': 12345, 'duration': 100,
                }],
            }]}), encoding='utf-8')
            server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=tmpdir))
            thread = threading.Thread(target=server.serve_forever, daemon=True)
            thread.start()
            try:
                for requested in ('fixture_vid', ''):
                    with self.subTest(requested=requested):
                        report_path = fixture / 'playback-report.json'
                        report_path.unlink(missing_ok=True)
                        env = os.environ.copy()
                        env.update({
                            'TEST_URL': f'http://127.0.0.1:{server.server_port}/',
                            'PLAYBACK_IDS': requested,
                            'PLAYBACK_BVIDS': '', 'PLAYBACK_PAGES': '',
                            'PLAYBACK_DATA': str(data_path),
                            'PLAYBACK_REPORT': str(report_path),
                            'PLAYBACK_VIDEO_TIMEOUT_MS': '200',
                        })
                        res = subprocess.run(
                            ['node', str(SMOKE_SCRIPT)], cwd=tmpdir, env=env,
                            capture_output=True, text=True, timeout=20,
                        )
                        self.assertEqual(res.returncode, 1, res.stdout + res.stderr)
                        self.assertIn('[SMOKE CHECK FAILED]', res.stderr)
                        report = json.loads(report_path.read_text(encoding='utf-8'))
                        self.assertFalse(report['passed'])
                        checks = report['checks']
                        timeouts = [check for check in checks if check.get('id') == 'fixture_vid']
                        self.assertTrue(timeouts)
                        for check in timeouts:
                            self.assertFalse(check['passed'])
                            self.assertIn('200ms', check['error'])
                            self.assertTrue(any('error:' in issue for issue in check['issues']))
                        if not requested:
                            self.assertEqual(len(checks), 6)
                            missing = [check for check in checks if 'id' not in check]
                            self.assertEqual(len(missing), 4)
                            for check in missing:
                                self.assertFalse(check['passed'])
                                self.assertIn('No published video', check['error'])
                                self.assertTrue(check['issues'])
            finally:
                server.shutdown()
                thread.join(timeout=5)
                server.server_close()

if __name__ == "__main__":
    unittest.main()
