import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from hooks import HookExecutor

class TestHookExecutor(unittest.TestCase):
    @patch("hooks.os.path.exists")
    @patch("hooks.open", new_callable=mock_open, read_data='{"hooks": {"pre_router": [{"command": "echo hello"}]}}')
    def test_init_with_config(self, mock_file, mock_exists):
        mock_exists.return_value = True
        executor = HookExecutor(config_path="config.json")
        self.assertEqual(executor.hooks, {"pre_router": [{"command": "echo hello"}]})

    @patch("hooks.subprocess.run")
    def test_run_hook(self, mock_run):
        executor = HookExecutor()
        executor.hooks = {"test_hook": [{"command": "test_cmd", "env": {"VAR": "VAL"}}]}
        
        executor.run_hook("test_hook")
        
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], "test_cmd")
        self.assertEqual(kwargs["env"]["VAR"], "VAL")

    @patch("hooks.subprocess.run")
    def test_run_hook_docker(self, mock_run):
        executor = HookExecutor()
        executor.hooks = {"test_hook": [{"command": "test_cmd", "use_docker": True, "docker_image": "test_image"}]}
        
        executor.run_hook("test_hook")
        
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        cmd = args[0]
        self.assertIn("docker", cmd)
        self.assertIn("run", cmd)
        self.assertIn("test_image", cmd)
        self.assertIn("test_cmd", cmd)

    @patch("hooks.os.setuid")
    @patch("hooks.os.setgid")
    @patch("hooks.subprocess.run")
    def test_run_hook_demote(self, mock_run, mock_setgid, mock_setuid):
        executor = HookExecutor()
        # Mocking os.getuid to be different from the demote uid
        with patch("hooks.os.getuid", return_value=0):
            executor.hooks = {"test_hook": [{"command": "test_cmd", "uid": 1000, "gid": 1000}]}
            executor.run_hook("test_hook")
        
        mock_run.assert_called_once()
        # The preexec_fn should have been set
        preexec = mock_run.call_args[1]["preexec_fn"]
        self.assertIsNotNone(preexec)
        
        # Execute the preexec function and verify it calls setuid/setgid
        preexec()
        mock_setuid.assert_called_with(1000)
        mock_setgid.assert_called_with(1000)

    @patch("hooks.os.path.exists")
    def test_init_no_config(self, mock_exists):
        mock_exists.return_value = False
        executor = HookExecutor("non_existent.json")
        self.assertEqual(executor.hooks, {})

if __name__ == "__main__":
    unittest.main()
