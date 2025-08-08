import subprocess

def is_git_repo():
    result = subprocess.run("git rev-parse --is-inside-work-tree", shell=True, capture_output=True, text=True)
    return result.returncode == 0

def execute_git_commands(commands):
    if not is_git_repo():
        print("❌ Error: Not inside a Git repository. Run 'git init' first.")
        return

    for cmd in commands:
        print(f"⚡ Running: {cmd}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        print(result.stdout if result.returncode == 0 else f"❌ {result.stderr}")
