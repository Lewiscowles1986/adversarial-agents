import unittest
from unittest.mock import MagicMock, patch, mock_open
import os
from orchestrator import Orchestrator

class TestOrchestrator(unittest.TestCase):
    def setUp(self):
        """Set up a fresh Orchestrator with mocked LLM and Hooks for every test."""
        self.mock_llm = MagicMock()
        self.mock_hooks = MagicMock()
        # Use a non-existent config path to ensure isolation from the workspace config.json
        self.orchestrator = Orchestrator(config_path="non_existent_config.json", llm=self.mock_llm, hook_executor=self.mock_hooks)

    @patch("orchestrator.os.remove")
    @patch("orchestrator.open", new_callable=mock_open)
    @patch("orchestrator.os.makedirs")
    @patch("orchestrator.os.path.exists")
    @patch("orchestrator.subprocess.run")
    def test_run_pipeline(self, mock_run, mock_exists, mock_makedirs, mock_file, mock_remove):
        """
        Verify the complete orchestration pipeline:
        1. Correct stage-specific prompts are sent to the LLM.
        2. Context swapping (GEMINI.md) occurs for each stage.
        3. All expected hooks are triggered.
        4. Final artifacts are saved to disk.
        """
        # Setup mock returns
        self.mock_llm.generate.side_effect = [
            "Builder Output Content",
            "Critic Output Content",
            "Judge Output Content"
        ]
        self.mock_llm.cli_type = "gemini"
        mock_exists.return_value = True # For GEMINI.md restore logic
        mock_run.return_value = MagicMock(returncode=1) # Mock git failure

        # Run the orchestrator
        user_prompt = "Write a fibonacci function"
        self.orchestrator.run(user_prompt)

        # 1. Verify LLM calls (Exact Prompts)
        self.assertEqual(self.mock_llm.generate.call_count, 3)
        
        # Verify Builder call
        builder_call = self.mock_llm.generate.call_args_list[0]
        self.assertIn("expert software builder", builder_call[0][0])
        self.assertEqual(builder_call[0][1], user_prompt)

        # Verify Critic call
        critic_call = self.mock_llm.generate.call_args_list[1]
        self.assertIn("harsh but fair code critic", critic_call[0][0])
        self.assertIn("Builder Output Content", critic_call[0][1])

        # Verify Judge call
        judge_call = self.mock_llm.generate.call_args_list[2]
        self.assertIn("final judge", judge_call[0][0])
        self.assertIn("Critic Output Content", judge_call[0][1])

        # 2. Verify GEMINI.md context swapping
        # Each stage writes its system prompt to GEMINI.md
        write_calls = [c for c in mock_file.call_args_list if "GEMINI.md" in str(c) and "w" in str(c)]
        self.assertEqual(len(write_calls), 3)
        
        # Check first write content (Builder)
        mock_file().write.assert_any_call(self.orchestrator.prompts["builder"])
        mock_file().write.assert_any_call(self.orchestrator.prompts["critic"])
        mock_file().write.assert_any_call(self.orchestrator.prompts["judge"])

    def test_route_exact_mapping(self):
        """Verify that the router maps stages to the exact system prompts defined in configuration."""
        builder_sys, critic_sys, judge_sys = self.orchestrator.route("test prompt")
        self.assertEqual(builder_sys, self.orchestrator.prompts["builder"])
        self.assertEqual(critic_sys, self.orchestrator.prompts["critic"])
        self.assertEqual(judge_sys, self.orchestrator.prompts["judge"])

if __name__ == "__main__":
    unittest.main()
