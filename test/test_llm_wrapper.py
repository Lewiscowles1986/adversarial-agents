import unittest
from unittest.mock import patch, MagicMock
from llm_wrapper import LLMWrapper
import subprocess
import sys

class TestLLMWrapper(unittest.TestCase):
    def test_llm_cli_call_precise(self):
        """Verify that the default LLM CLI (Simon Willison's 'llm') is called with correct arguments and a timeout."""
        wrapper = LLMWrapper(cli_type="llm")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="Generated content\n", returncode=0)
            
            result = wrapper.generate("SYSTEM", "USER")
            
            self.assertEqual(result, "Generated content")
            # Verify exact command list and timeout
            mock_run.assert_called_once_with(
                ["llm", "prompt", "-s", "SYSTEM", "USER"],
                capture_output=True, text=True, check=True, env=unittest.mock.ANY, timeout=120
            )

    def test_gemini_cli_call_precise(self):
        """Verify that the 'gemini' CLI is called with the correct yolo and prompt flags and a timeout."""
        wrapper = LLMWrapper(cli_type="gemini")
        with patch("subprocess.run") as mock_run:
            mock_run.return_value = MagicMock(stdout="Gemini output\n", returncode=0)
            
            result = wrapper.generate("SYSTEM", "USER")
            
            self.assertEqual(result, "Gemini output")
            # Verify exact command list for gemini and timeout
            mock_run.assert_called_once_with(
                ["gemini", "-p", "USER", "--yolo"],
                capture_output=True, text=True, check=True, env=unittest.mock.ANY, timeout=120
            )

    def test_invalid_cli_type(self):
        """Ensure that initializing LLMWrapper with an unsupported CLI type raises a ValueError."""
        with self.assertRaises(ValueError):
            LLMWrapper(cli_type="invalid")

    @patch("sys.exit")
    def test_cli_error(self, mock_exit):
        """Verify that a non-zero exit code from the LLM CLI causes the wrapper to print an error and exit."""
        wrapper = LLMWrapper(cli_type="llm")
        with patch("subprocess.run") as mock_run:
            mock_run.side_effect = subprocess.CalledProcessError(1, ["llm"], stderr="Error message")
            
            wrapper.generate("sys", "user")
            mock_exit.assert_called_with(1)

if __name__ == "__main__":
    unittest.main()
