import subprocess
import json
import sys
import os
from llm_interface import LLMInterface

class LLMWrapper(LLMInterface):
    def __init__(self, cli_type="llm"):
        if cli_type not in ["llm", "gemini"]:
             raise ValueError(f"Unknown CLI type: {cli_type}")
        self.cli_type = cli_type # "llm", "gemini", or custom

    def generate(self, system_prompt, user_prompt):
        env = os.environ.copy()

        if self.cli_type == "llm":
            # Using Simon Willison's llm CLI: `llm prompt -s "system prompt" "user prompt"`
            cmd = ["llm", "prompt", "-s", system_prompt, user_prompt]
        elif self.cli_type == "gemini":
            # We assume GEMINI.md is already set by the orchestrator for this stage.
            # Using -p for non-interactive and --yolo for agentic behavior.
            # If we need to pass the system_prompt as a fallback or for non-file context:
            # combined_prompt = f"INSTRUCTIONS:\n{system_prompt}\n\nPROMPT:\n{user_prompt}"
            # But here we rely on the GEMINI.md swap strategy.
            cmd = ["gemini", "-p", user_prompt, "--yolo"]

        try:
            print(f"Calling LLM CLI: {self.cli_type}...")
            result = subprocess.run(cmd, capture_output=True, text=True, check=True, env=env)
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error calling LLM CLI:\nSTDOUT: {e.stdout}\nSTDERR: {e.stderr}", file=sys.stderr)
            sys.exit(1)
        except FileNotFoundError:
            print(f"Error: The CLI tool '{cmd[0]}' is not installed or not in PATH.", file=sys.stderr)
            sys.exit(1)
