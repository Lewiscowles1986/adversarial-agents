import os
import subprocess
import pwd
import grp
import json

class HookExecutor:
    def __init__(self, config_path=None):
        self.hooks = {}
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                self.hooks = json.load(f).get('hooks', {})

    def run_hook(self, hook_name):
        commands = self.hooks.get(hook_name, [])
        if not commands:
            return

        print(f"--- Running hook: {hook_name} ---")
        for cmd_config in commands:
            self._execute_command(cmd_config)

    def _execute_command(self, cmd_config):
        cmd = cmd_config.get("command")
        if not cmd:
            return

        env = os.environ.copy()
        if "env" in cmd_config:
            env.update(cmd_config["env"])

        cwd = cmd_config.get("cwd", os.getcwd())
        use_docker = cmd_config.get("use_docker", False)

        if use_docker:
            image = cmd_config.get("docker_image", "ubuntu:latest")
            docker_cmd = ["docker", "run", "--rm", "-v", f"{cwd}:/workspace", "-w", "/workspace", image]
            
            for k, v in cmd_config.get("env", {}).items():
                docker_cmd.extend(["-e", f"{k}={v}"])
                
            if "uid" in cmd_config or "gid" in cmd_config:
                uid = cmd_config.get("uid", os.getuid())
                gid = cmd_config.get("gid", os.getgid())
                docker_cmd.extend(["-u", f"{uid}:{gid}"])

            if isinstance(cmd, str):
                docker_cmd.extend(["sh", "-c", cmd])
            else:
                docker_cmd.extend(cmd)
            
            print(f"Executing in Docker: {' '.join(docker_cmd)}")
            subprocess.run(docker_cmd, env=env)
        else:
            # Local execution
            shell = isinstance(cmd, str)
            
            if "uid" in cmd_config or "gid" in cmd_config:
                print(f"Warning: 'uid' and 'gid' are ignored for local execution for stability. Use 'use_docker: true' for identity switching.")

            print(f"Executing locally: {cmd}")
            # Note: We've removed preexec_fn (demote) because it is not fork-safe on macOS
            # and was causing segmentation faults during high-concurrency mutation testing.
            # If UID/GID switching is required, it should be handled via 'sudo' or similar
            # wrappers within the command string itself.
            subprocess.run(cmd, env=env, cwd=cwd, shell=shell, timeout=300)
