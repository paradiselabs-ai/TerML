import subprocess
from typing import List, Tuple

def analyze_git_state() -> Tuple[str, List[str]]:
    """
    Analyze the current state of the git repository.
    
    Returns:
        Tuple[str, List[str]]: A tuple containing the overall state and a list of details.
    """
    try:
        # Check if we're in a git repository
        subprocess.run(["git", "rev-parse", "--is-inside-work-tree"], check=True, capture_output=True, text=True)
    except subprocess.CalledProcessError:
        return "Not a git repository", ["This directory is not a git repository."]

    status = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True).stdout.strip()
    branch = subprocess.run(["git", "rev-parse", "--abbrev-ref", "HEAD"], capture_output=True, text=True).stdout.strip()

    if not status:
        return "Clean", [f"Currently on branch '{branch}'", "Working directory clean"]

    modified = []
    staged = []
    untracked = []

    for line in status.split('\n'):
        if line.startswith(' M'):
            modified.append(line[3:])
        elif line.startswith('M '):
            staged.append(line[3:])
        elif line.startswith('??'):
            untracked.append(line[3:])

    details = [f"Currently on branch '{branch}'"]
    if modified:
        details.append(f"{len(modified)} file(s) modified")
    if staged:
        details.append(f"{len(staged)} file(s) staged for commit")
    if untracked:
        details.append(f"{len(untracked)} untracked file(s)")

    return "Changes present", details

def provide_git_guidance(state: str, details: List[str]) -> str:
    """
    Provide appropriate guidance based on the git repository state.
    
    Args:
        state (str): The overall state of the repository.
        details (List[str]): A list of detailed information about the repository state.
    
    Returns:
        str: Guidance based on the current state.
    """
    if state == "Not a git repository":
        return "To initialize a git repository, use the command: git init"

    if state == "Clean":
        return "Your working directory is clean. You can start making changes or pull updates from remote."

    guidance = "Based on your current git state:\n"
    
    if "file(s) modified" in ' '.join(details):
        guidance += "- You have modified files. Use 'git add <file>' to stage changes for commit.\n"
    
    if "file(s) staged for commit" in ' '.join(details):
        guidance += "- You have staged changes. Use 'git commit -m \"Your message\"' to commit these changes.\n"
    
    if "untracked file(s)" in ' '.join(details):
        guidance += "- You have untracked files. Use 'git add <file>' to start tracking them.\n"
    
    guidance += "\nTo see a detailed status, use 'git status'."
    return guidance

def get_quick_git_help() -> str:
    """
    Generate a quick help list for common git commands.
    
    Returns:
        str: A string containing common git commands and their descriptions.
    """
    return """
Common Git Commands:
- git init: Initialize a new git repository
- git clone <url>: Clone a repository from <url>
- git add <file>: Add file contents to the index
- git commit -m "message": Record changes to the repository
- git push: Update remote refs along with associated objects
- git pull: Fetch from and integrate with another repository or a local branch
- git branch: List, create, or delete branches
- git checkout <branch>: Switch branches or restore working tree files
- git status: Show the working tree status
- git log: Show commit logs
- git diff: Show changes between commits, commit and working tree, etc.
"""

# Additional functions for interactive lessons can be added here
