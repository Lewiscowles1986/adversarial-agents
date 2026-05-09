# C4 Context Diagram: Adversarial AI Orchestrator

This diagram provides a high-level view of the Adversarial AI Orchestration system and how it interacts with users and external systems.

```mermaid
C4Context
    title System Context Diagram for Adversarial AI Orchestrator

    Enterprise_Boundary(user_boundary, "Private") {
        Person(user, "User/Developer", "Initiates prompts and reviews generated software artifacts.")
        
        Boundary(local_machine, "User's Local Machine") {
            System(orchestrator, "Adversarial AI Orchestrator", "Orchestrates Builder, Critic, and Judge agents to fulfill user requests.")
            System_Ext(llm_cli, "LLM CLI Tools", "Local binaries (e.g., 'llm', 'gemini') that interface with AI models.")
            System_Ext(filesystem, "Local Filesystem", "Stores configuration, intermediate GEMINI.md context, and final artifacts.")
            System_Ext(docker, "Docker Engine", "Optional: Executes isolated hook commands in containers.")
            System_Ext(llm_provider_local, "LLM Provider (local model)", "Local AI services (e.g. GGUF models, Ollama, vLLM).")
        }
    }

    Enterprise_Boundary(cloud, "Internet / Cloud") {
        System_Ext(llm_provider_cloud, "LLM Provider (remote model)", "Remote AI services (e.g., Google Gemini, OpenAI, Anthropic).")
    }

    Rel(user, orchestrator, "Provides prompt and configuration", "CLI")
    Rel(orchestrator, llm_cli, "Invokes for agent generation", "Subprocess")
    Rel(orchestrator, filesystem, "Reads/Writes config and artifacts", "File I/O")
    Rel(orchestrator, docker, "Executes isolated hooks", "CLI/Subprocess")
    
    Rel(llm_cli, llm_provider_local, "Sends prompts and receives responses", "FileSystem/API")
    Rel(llm_cli, llm_provider_cloud, "Sends prompts and receives responses", "Web/API")
    Rel(llm_cli, filesystem, "Reads context from", "GEMINI.md")
    Rel(orchestrator, user, "Delivers final judgment and artifacts", "Stdout/Files")

    UpdateLayoutConfig($c4ShapeInRow="2", $c4BoundaryInRow="1")
```

## Actors & Systems

### User/Developer
The primary actor who interacts with the system via the command line. They provide the initial prompt and consume the final implementation.

### Adversarial AI Orchestrator (The System)
The core Python application. It manages the lifecycle of a request by routing prompts through a three-stage adversarial pipeline (Builder -> Critic -> Judge). It is responsible for state management, hook execution, and artifact collection.

### LLM CLI Tools (External)
The system is designed to be agnostic of the specific LLM. It delegates the actual "thinking" to external CLI tools like Simon Willison's `llm` or the `gemini` CLI. This abstraction enables a **Hybrid LLM Strategy**:
- **Local Models**: You can use tools that interface with local engines (e.g., Ollama, vLLM, GGUF) for maximum privacy, lower latency, and zero cost.
- **Cloud Models**: You can use enterprise-grade models (e.g., Gemini 1.5 Pro, GPT-4) when high-reasoning capability is required.
- **Mixed/Isolated Usage**: Because each agent (Builder, Critic, Judge) can be configured independently, you can mix providers—for example, using a fast local model for the Builder and a powerful cloud model for the final Judge.

### LLM Providers (Local & Cloud)
- **Local Provider**: Resides within the private boundary of the user's machine. Ideal for development and sensitive code.
- **Cloud Provider**: Accessed over the internet via APIs. Provides access to the latest frontier models.

### Local Filesystem (External)
The primary persistence and communication layer.
- **Config**: Defined in `config.json`.
- **Context Swapping**: The system uses `GEMINI.md` as a "working memory" for certain CLI tools.
- **Artifacts**: Final outputs are stored in the `artifacts/` directory.

### Docker Engine (External)
An optional dependency used to provide environment isolation for hooks. This is specifically used when identity switching (`uid`/`gid`) is required or when a specific runtime (e.g., `node`, `python`) is needed for a hook without polluting the host system.
