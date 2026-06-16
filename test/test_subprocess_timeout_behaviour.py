"""
Empirical tests for subprocess.run timeout behaviour under conditions
that match how llm_wrapper.py launches Claude.

These tests use real subprocesses (no mocks) to observe actual behaviour.
Run with: python -m pytest test/test_subprocess_timeout_behaviour.py -v -s
"""
import subprocess
import sys
import time
import unittest


TOLERANCE_SECONDS = 3  # how much longer than the timeout we allow before flagging a problem


class TestSubprocessTimeoutWithOutput(unittest.TestCase):

    def test_timeout_fires_with_small_output(self):
        """Baseline: timeout fires promptly when child produces little output."""
        script = "import time; print('hi'); time.sleep(999)"
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                timeout=1,
            )
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 1 + TOLERANCE_SECONDS,
                        f"Took {elapsed:.2f}s — much longer than timeout suggests a hang")

    def test_timeout_fires_with_large_output(self):
        """Does timeout still fire promptly when child writes more than the pipe buffer (64KB)?

        If Python's background reader thread stalls, this will take much longer
        than the timeout or hang indefinitely.
        """
        # Write 1MB to stdout then sleep — more than any pipe buffer
        script = "import sys, time; sys.stdout.write('x' * 1_000_000); sys.stdout.flush(); time.sleep(999)"
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                timeout=1,
            )
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 1 + TOLERANCE_SECONDS,
                        f"Took {elapsed:.2f}s — large output may be causing a slow drain after kill")

    def test_timeout_fires_when_grandchild_holds_pipe(self):
        """Does the timeout hang when a grandchild process inherits the stdout pipe FD?

        This is the deadlock scenario: Python kills the child, but grandchild still
        holds the write end of the stdout pipe. communicate() waits for EOF that
        never arrives.
        """
        # Child spawns a grandchild (inheriting all FDs) and both sleep
        script = (
            "import subprocess, sys, time; "
            "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(999)']); "
            "time.sleep(999)"
        )
        start = time.monotonic()
        try:
            subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                timeout=1,
            )
            self.fail("Expected TimeoutExpired")
        except subprocess.TimeoutExpired:
            pass
        elapsed = time.monotonic() - start
        self.assertLess(elapsed, 1 + TOLERANCE_SECONDS,
                        f"Took {elapsed:.2f}s — grandchild holding pipe FD caused a {elapsed:.1f}s hang")

    def test_stdin_from_tty_vs_devnull(self):
        """Does connecting stdin to a real TTY vs DEVNULL affect timeout behaviour?

        Claude inherits stdin from the terminal by default (subprocess.run does not
        redirect it). This test checks whether that matters when the timeout fires.
        """
        script = "import time; time.sleep(999)"

        # With inherited stdin (matches current llm_wrapper.py behaviour)
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                timeout=1,
            )
        elapsed_inherited = time.monotonic() - start

        # With stdin from /dev/null
        start = time.monotonic()
        with self.assertRaises(subprocess.TimeoutExpired):
            subprocess.run(
                [sys.executable, "-c", script],
                capture_output=True,
                stdin=subprocess.DEVNULL,
                timeout=1,
            )
        elapsed_devnull = time.monotonic() - start

        print(f"\n  stdin=inherited: {elapsed_inherited:.2f}s")
        print(f"  stdin=DEVNULL:   {elapsed_devnull:.2f}s")
        # Neither should hang; just recording the difference for visibility
        self.assertLess(elapsed_inherited, 1 + TOLERANCE_SECONDS)
        self.assertLess(elapsed_devnull, 1 + TOLERANCE_SECONDS)


if __name__ == "__main__":
    unittest.main(verbosity=2)
