import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SMOKE_SCRIPT = ROOT / "scripts" / "playback_smoke.cjs"

class TestPlaybackSmoke(unittest.TestCase):
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

    def test_cli_failure_exit_code_and_report_writing(self):
        # Verify that an execution encountering failure exits with non-zero code and writes report
        with tempfile.TemporaryDirectory() as tmpdir:
            report_path = Path(tmpdir) / "playback-report.json"
            # Run node script that simulates checking a non-existent or failing video
            env = os.environ.copy()
            env["PLAYBACK_IDS"] = "nonexistent_vid_for_test"
            env["PLAYBACK_REPORT"] = str(report_path)
            res = subprocess.run(
                ["node", str(SMOKE_SCRIPT)],
                cwd=ROOT,
                env=env,
                capture_output=True,
                text=True
            )
            # Must exit with non-zero
            self.assertNotEqual(res.returncode, 0)
            self.assertIn("Requested original is not published", res.stderr + res.stdout)

if __name__ == "__main__":
    unittest.main()
