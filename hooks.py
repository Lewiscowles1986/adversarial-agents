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
            docker_cmd = ["docker", "run", "--rm", "-v", f"{cwd}:/workspace", "-w", "/workspace"]
            
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
            def demote(user_uid, user_gid):
                def result():
                    os.setgid(user_gid)
                    os.setuid(user_uid)
                return result

            preexec_fn = None
            if "uid" in cmd_config or "gid" in cmd_config:
                uid = cmd_config.get("uid", os.getuid())
                gid = cmd_config.get("gid", os.getgid())
                
                if isinstance(uid, str):
                    uid = pwd.getpwnam(uid).pw_uid
                if isinstance(gid, str):
                    gid = grp.getgrnam(gid).gr_gid
                    
                if uid != os.getuid() or gid != os.getgid():
                    preexec_fn = demote(uid, gid)

            shell = isinstance(cmd, str)
            
            print(f"Executing locally: {cmd}")
            subprocess.run(cmd, env=env, cwd=cwd, shell=shell, preexec_fn=preexec_fn)
