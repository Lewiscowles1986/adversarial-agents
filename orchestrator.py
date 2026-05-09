import os
import json
import subprocess
from typing import Optional
from hooks import HookExecutor
from llm_wrapper import LLMWrapper
from llm_interface import LLMInterface

DEFAULT_PROMPTS = {
    "builder": "You are an expert software builder. Provide a complete, functional implementation to the user's request. Focus on clean code, best practices, and accuracy. Provide ONLY the code/solution, without conversational filler.",
    "critic": "You are a harsh but fair code critic. Review the user's original request and the builder's implementation. Identify bugs, security flaws, architectural issues, and missing requirements. Provide a structured review detailing flaws and suggested fixes. Be concise and precise.",
    "judge": "You are the final judge. Review the user's request, the builder's implementation, and the critic's review. Determine if the solution is acceptable. If it is, output the final polished solution. If the critic found fatal flaws, explain why the solution fails and provide the corrected version if possible. Your output must be the final authoritative response."
}

class Orchestrator:
    def __init__(self, config_path: str = "config.json", cli_override: Optional[str] = None, llm: Optional[LLMInterface] = None, hook_executor: Optional[HookExecutor] = None):
        self.hook_executor = hook_executor if hook_executor else HookExecutor(config_path)
        self.config = {}
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.config = json.load(f)
        
        if llm:
            self.llm = llm
        else:
            cli_type = cli_override if cli_override else self.config.get("llm_cli", "llm")
            self.llm = LLMWrapper(cli_type=cli_type)
        
        # In the future, this could be dynamic
        self.prompts = self.config.get("prompts", DEFAULT_PROMPTS)

    def route(self, user_prompt):
        """
        Future routing logic. For now, we return the generic builder, critic, and judge system prompts.
        """
        print("Routing user prompt to Generic Builder, Critic, Judge...")
        return self.prompts["builder"], self.prompts["critic"], self.prompts["judge"]

    def _swap_context(self, content):
        """Swaps GEMINI.md with the stage-specific content."""
        if getattr(self.llm, "cli_type", None) != "gemini":
            return
        
        # Backup strategy: if it exists, we just overwrite. 
        # We rely on git to restore it later.
        with open("GEMINI.md", "w") as f:
            f.write(content)

    def _restore_context(self):
        """Restores GEMINI.md to its original state using git."""
        if getattr(self.llm, "cli_type", None) != "gemini":
            return
            
        if os.path.exists("GEMINI.md"):
            # Check if it was tracked/modified
            try:
                res = subprocess.run(["git", "ls-files", "--error-unmatch", "GEMINI.md"], capture_output=True, timeout=10)
                if res.returncode == 0:
                    # File is tracked, restore it
                    subprocess.run(["git", "checkout", "HEAD", "--", "GEMINI.md"], timeout=10)
                else:
                    # File is not tracked, just remove it to avoid pollution
                    os.remove("GEMINI.md")
            except subprocess.TimeoutExpired:
                print("Warning: git command timed out during GEMINI.md restoration.")

    def run(self, user_prompt):
        print("Starting Adversarial AI Orchestration Pipeline...")
        
        # 1. Pre-Router
        self.hook_executor.run_hook("pre_router")
        
        # 2. Routing
        builder_sys, critic_sys, judge_sys = self.route(user_prompt)
        
        # 3. Post-Router
        self.hook_executor.run_hook("post_router")
        
        # 4. Builder
        self.hook_executor.run_hook("pre_builder")
        print("\n--- [Builder Stage] ---")
        self._swap_context(builder_sys)
        try:
            builder_output = self.llm.generate(builder_sys, user_prompt)
        finally:
            self._restore_context()
        print("Builder Output generated.")
        self.hook_executor.run_hook("post_builder")
        
        # 5. Critic
        self.hook_executor.run_hook("pre_critic")
        print("\n--- [Critic Stage] ---")
        self._swap_context(critic_sys)
        try:
            critic_input = f"User Request:\n{user_prompt}\n\nBuilder Implementation:\n{builder_output}"
            critic_output = self.llm.generate(critic_sys, critic_input)
        finally:
            self._restore_context()
        print("Critic Output generated.")
        self.hook_executor.run_hook("post_critic")
        
        # 6. Judge
        self.hook_executor.run_hook("pre_judge")
        print("\n--- [Judge Stage] ---")
        self._swap_context(judge_sys)
        try:
            judge_input = f"User Request:\n{user_prompt}\n\nBuilder Implementation:\n{builder_output}\n\nCritic Review:\n{critic_output}"
            judge_output = self.llm.generate(judge_sys, judge_input)
        finally:
            self._restore_context()
        print("Judge Output generated.")
        self.hook_executor.run_hook("post_judge")
        
        # 7. Finished
        self.hook_executor.run_hook("finished")
        
        print("\n=== FINAL JUDGMENT ===")
        print(judge_output)
        
        # Optionally save artifacts
        self.save_artifacts(user_prompt, builder_output, critic_output, judge_output)

    def save_artifacts(self, prompt, builder, critic, judge):
        os.makedirs("artifacts", exist_ok=True)
        with open("artifacts/builder_output.md", "w") as f:
            f.write(builder)
        with open("artifacts/critic_output.md", "w") as f:
            f.write(critic)
        with open("artifacts/judge_output.md", "w") as f:
            f.write(judge)
        print("\nArtifacts saved to the 'artifacts/' directory.")
