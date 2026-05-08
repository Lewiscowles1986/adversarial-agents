import argparse
import sys
from orchestrator import Orchestrator

def main():
    parser = argparse.ArgumentParser(description="Adversarial AI Orchestration System")
    parser.add_argument("prompt", help="The initial user prompt to kick off the process.")
    parser.add_argument("-c", "--config", default="config.json", help="Path to the configuration file (default: config.json)")
    parser.add_argument("--llm-cli", choices=["llm", "gemini"], help="Override the LLM CLI tool (e.g., 'llm' or 'gemini')")
    
    args = parser.parse_args()

    orchestrator = Orchestrator(config_path=args.config, cli_override=args.llm_cli)
    orchestrator.run(args.prompt)

if __name__ == "__main__":
    main()
