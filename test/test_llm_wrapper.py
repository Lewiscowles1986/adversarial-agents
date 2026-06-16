import unittest
from unittest.mock import patch, MagicMock
from llm_wrapper import LLMWrapper
import subprocess
import sys

def make_popen_mock(stdout="", returncode=0):
    mock_proc = MagicMock()
    mock_proc.communicate.return_value = (stdout, "")
    mock_proc.returncode = returncode
    return mock_proc

class TestLLMWrapper(unittest.TestCase):
    def test_llm_cli_call_precise(self):
        """Verify that the default LLM CLI (Simon Willison's 'llm') is called with correct arguments and a timeout."""
        wrapper = LLMWrapper(cli_type="llm")
        mock_proc = make_popen_mock(stdout="Generated content\n")
        with patch("subprocess.Popen", return_value=mock_proc) as mock_popen:
            result = wrapper.generate("SYSTEM", "USER")

            self.assertEqual(result, "Generated content")
            mock_popen.assert_called_once_with(
                ["llm", "prompt", "-s", "SYSTEM", "USER"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=unittest.mock.ANY, text=True,
                env=unittest.mock.ANY, preexec_fn=unittest.mock.ANY,
            )

    def test_gemini_cli_call_precise(self):
        """Verify that the 'gemini' CLI is called with the correct yolo and prompt flags and a timeout."""
        wrapper = LLMWrapper(cli_type="gemini")
        mock_proc = make_popen_mock(stdout="Gemini output\n")
        with patch("subprocess.Popen", return_value=mock_proc) as mock_popen:
            result = wrapper.generate("SYSTEM", "USER")

            self.assertEqual(result, "Gemini output")
            mock_popen.assert_called_once_with(
                ["gemini", "-p", "USER", "--yolo"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                stdin=unittest.mock.ANY, text=True,
                env=unittest.mock.ANY, preexec_fn=unittest.mock.ANY,
            )

    def test_invalid_cli_type(self):
        """Ensure that initializing LLMWrapper with an unsupported CLI type raises a ValueError."""
        with self.assertRaises(ValueError):
            LLMWrapper(cli_type="invalid")

    @patch("sys.exit")
    def test_cli_error(self, mock_exit):
        """Verify that a non-zero exit code from the LLM CLI causes the wrapper to print an error and exit."""
        wrapper = LLMWrapper(cli_type="llm")
        mock_proc = make_popen_mock(stdout="", returncode=1)
        mock_proc.communicate.return_value = ("", "Error message")
        with patch("subprocess.Popen", return_value=mock_proc):
            wrapper.generate("sys", "user")
            mock_exit.assert_called_with(1)

if __name__ == "__main__":
    unittest.main()
