import spacy, re
nlp = spacy.load("en_core_web_sm")

def parse_git_command(command_text):
    command_text = command_text.lower()

    # ✅ Undo last commit (moved to top for priority)
    if "undo" in command_text or "revert" in command_text:
        return ["git reset --soft HEAD~1"]

    # ✅ Commit changes
    if "commit" in command_text:
        msg = re.search(r"message ['\"](.*?)['\"]", command_text)
        commit_msg = msg.group(1) if msg else "voice commit"
        return [f"git add .", f'git commit -m "{commit_msg}"']

    # ✅ Push changes
    elif "push" in command_text:
        return ["git push origin main"]

    # ✅ Pull changes
    elif "pull" in command_text:
        return ["git pull origin main"]

    # ✅ Create new branch
    elif "branch" in command_text and "create" in command_text:
        match = re.search(r"branch ([\w\-]+)", command_text)
        if match:
            branch_name = match.group(1)
            return [f"git branch {branch_name}", f"git checkout {branch_name}"]
        else:
            return ["Unknown command"]

    # ✅ Switch branch
    elif "switch" in command_text or "checkout" in command_text:
        match = re.search(r"branch ([\w\-]+)", command_text)
        if match:
            branch_name = match.group(1)
            return [f"git checkout {branch_name}"]

    # ✅ Show status
    elif "status" in command_text:
        return ["git status"]

    else:
        return ["Unknown command"]
