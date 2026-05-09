# Adversarial AI Orchestrator

This is a simple system for exploring adversarial AI by orchestrating different LLM "personas" (Builder, Critic, Judge) using local LLM CLI tools.

## Architecture

The system takes a single user prompt and orchestrates a pipeline:
1.  **Pre-Router Hook**: Run commands before routing.
2.  **Router**: Selects the appropriate system prompts for Builder, Critic, and Judge (currently static generic prompts).
3.  **Post-Router Hook**: Run commands after routing.
4.  **Builder**: An LLM session that attempts to solve the user's prompt.
5.  **Critic**: An LLM session that reviews the user's prompt and the Builder's output.
6.  **Judge**: An final LLM session that reviews the user's prompt, Builder output, and Critic review to determine the final solution.
7.  **Finished Hook**: Run commands after the entire pipeline finishes.

Between each phase, you can define commands to run. These commands can be executed:
- Locally (with optional `uid`, `gid`, `cwd`, and `env` controls).
- Inside an isolated Docker container (`use_docker: true`).

## Prerequisites

- Python 3.10+
- An LLM CLI installed. By default, it uses Simon Willison's `llm` CLI (`pip install llm`). You can switch to `gemini` CLI in `config.json`.
- Optional: Docker (if you want to run hooks in isolated containers).

## Setup & Dependencies

This project supports multiple Python environment managers. Choose the one you prefer:

### Using `uv` (Recommended)
`uv` is extremely fast and manages the environment for you.
```bash
# Install dependencies and sync environment
uv sync --extra dev
# Run tests
uv run pytest
# Run the application
uv run python main.py "Your prompt"
```

### Using `poetry`
```bash
# Install dependencies
poetry install --with dev
# Run tests
poetry run pytest
# Run the application
poetry run python main.py "Your prompt"
### Using `pip`
```bash
# Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt
# Run tests
pytest
# Run the application
python main.py "Your prompt"
```

## Testing & Quality

### Unit Tests
We use `pytest` for unit testing.
```bash
uv run pytest
```

### Mutation Testing (Test Fitness)
To evaluate the quality of our tests, we use `mutmut`. This introduces intentional bugs into the code to see if the tests catch (kill) them.
```bash
# Run mutation testing
uv run mutmut run
# View results summary
uv run mutmut results
```

> **Note**: `requirements.txt` is kept in sync with `pyproject.toml` for `pip` users. If you update `pyproject.toml`, regenerate it using:
> ```bash
> uv pip compile pyproject.toml --extra dev --no-deps -o requirements.txt
> ```

## Configuration (`config.json`)

The `config.json` allows you to configure which LLM CLI to use and define hook commands:

```json
{
  "llm_cli": "llm",
  "hooks": {
    "pre_router": [
      {
        "command": "echo 'Preparing...'",
        "cwd": "."
      }
    ],
    "post_builder": [
      {
        "command": "npm install",
        "use_docker": true,
        "docker_image": "node:latest"
      }
    ]
  }
}
```

### Hook Command Options
- `command` (string or array): The command to execute.
- `cwd` (string): Working directory for the command.
- `env` (object): Environment variables to pass.
- `uid` / `gid` (int or string): User/Group to run as.
- `use_docker` (boolean): Run inside a docker container.
- `docker_image` (string): Docker image to use if `use_docker` is true.

## Usage

```bash
python3 main.py "Write a python script that reverses a string."
```

Switch the LLM CLI via command line:
```bash
python3 main.py --llm-cli gemini "Write a python script that reverses a string."
```

If you want to use a custom configuration file:
```bash
python3 main.py -c custom_config.json "Write a python script that reverses a string."
```

The system will generate artifacts in the `artifacts/` folder containing the outputs from the Builder, Critic, and Judge.
