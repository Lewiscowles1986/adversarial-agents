import argparse
import sys
from orchestrator import Orchestrator

def main():
    parser = argparse.ArgumentParser(description="Adversarial AI Orchestration System")
    parser.add_argument("prompt", help="The initial user prompt to kick off the process.")
    parser.add_argument("-c", "--config", default="config.json", help="Path to the configuration file (default: config.json)")
    parser.add_argument("--llm-cli", choices=["llm", "gemini", "claude"], help="Override the LLM CLI tool (e.g., 'llm', 'claude' or 'gemini')")
    parser.add_argument("--model", default=None, help="Override the model (e.g., 'claude-sonnet-4-6', 'claude-opus-4-8', 'claude-haiku-4-5-20251001', or shorthand 'sonnet', 'opus', 'haiku')")

    args = parser.parse_args()

    orchestrator = Orchestrator(config_path=args.config, cli_override=args.llm_cli, model_override=args.model)
    orchestrator.run(args.prompt)

if __name__ == "__main__":
    main()
