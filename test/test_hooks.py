import unittest
from unittest.mock import patch, MagicMock, mock_open
import os
from hooks import HookExecutor

class TestHookExecutor(unittest.TestCase):
    @patch("hooks.os.path.exists")
    @patch("hooks.open", new_callable=mock_open, read_data='{"hooks": {"pre_router": [{"command": "echo hello"}]}}')
    def test_init_with_config(self, mock_file, mock_exists):
        """Verify that HookExecutor correctly parses hook configurations from a JSON file."""
        mock_exists.return_value = True
        executor = HookExecutor(config_path="config.json")
        self.assertEqual(executor.hooks, {"pre_router": [{"command": "echo hello"}]})

    @patch("hooks.subprocess.run")
    def test_run_hook(self, mock_run):
        """Verify that a local hook command is executed with the correct environment variables."""
        executor = HookExecutor()
        executor.hooks = {"test_hook": [{"command": "test_cmd", "env": {"VAR": "VAL"}}]}
        
        executor.run_hook("test_hook")
        
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(args[0], "test_cmd")
        self.assertEqual(kwargs["env"]["VAR"], "VAL")

    @patch("hooks.subprocess.run")
    def test_run_hook_docker(self, mock_run):
        """Verify that a Docker-based hook correctly constructs the 'docker run' command with the specified image."""
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

    @patch("hooks.os.path.exists")
    def test_init_no_config(self, mock_exists):
        """Verify that HookExecutor handles missing configuration files gracefully by initializing an empty hooks dictionary."""
        mock_exists.return_value = False
        executor = HookExecutor("non_existent.json")
        self.assertEqual(executor.hooks, {})

    @patch("hooks.subprocess.run")
    def test_run_hook_relative_cwd(self, mock_run):
        """Verify that a relative 'cwd' in a hook is resolved relative to the config directory."""
        executor = HookExecutor()
        executor.config_dir = "/fake/config/dir"
        executor.hooks = {"test_hook": [{"command": "test_cmd", "cwd": "subdir"}]}
        
        executor.run_hook("test_hook")
        
        mock_run.assert_called_once()
        args, kwargs = mock_run.call_args
        self.assertEqual(kwargs["cwd"], os.path.abspath("/fake/config/dir/subdir"))

if __name__ == "__main__":
    unittest.main()
