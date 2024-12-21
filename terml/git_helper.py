import subprocess
from typing import List, Tuple
import click
from .lesson_system import LessonManager

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

class GitLearningSession:
    """Manages interactive Git learning sessions and Q&A"""
    
    def __init__(self):
        self.lesson_manager = LessonManager()
        self.common_questions = {
            "init": ("git init initializes a new Git repository in the current directory. "
                    "It creates a .git folder to store all the version control information."),
            "clone": ("git clone <url> creates a copy of a remote repository on your local machine. "
                     "It automatically sets up the remote tracking."),
            "add": ("git add stages changes for commit. Use git add <file> for specific files "
                   "or git add . for all changes."),
            "commit": ("git commit -m \"message\" saves your staged changes with a descriptive message. "
                      "Make sure your message clearly describes the changes."),
            "push": ("git push uploads your committed changes to the remote repository. "
                    "Use git push origin <branch> to specify the remote and branch."),
            "pull": ("git pull fetches changes from the remote repository and merges them into "
                    "your current branch."),
            "branch": ("git branch shows all branches. Use git branch <name> to create a new branch "
                      "and git checkout <name> to switch to it."),
            "merge": ("git merge <branch> incorporates changes from the specified branch into "
                     "your current branch.")
        }

    def start_lesson(self, lesson_id: str = "01_basics"):
        """Start an interactive Git lesson"""
        click.echo("\nStarting Git lesson...")
        self.lesson_manager.start_interactive_session('git', lesson_id)

    def show_available_lessons(self):
        """Show available Git lessons"""
        click.echo("\nAvailable Git Lessons:")
        self.lesson_manager.show_category_progress('git')

    def start_quick_qa(self):
        """Start a quick Q&A session about Git"""
        click.echo("\nStarting Git Q&A session. Type 'exit' to end.")
        click.echo("Ask any question about Git commands or concepts.")
        
        while True:
            question = click.prompt("\nYour question").lower()
            if question == 'exit':
                click.echo("Ending Q&A session.")
                break

            # Check current git state for context-aware answers
            state, details = analyze_git_state()
            
            # Look for keywords in the question
            answer = None
            for keyword, response in self.common_questions.items():
                if keyword in question:
                    answer = response
                    break

            if not answer:
                if "status" in question or "state" in question:
                    answer = provide_git_guidance(state, details)
                elif "help" in question:
                    answer = get_quick_git_help()
                else:
                    answer = ("I'm not sure about that specific question. Try asking about "
                            "specific Git commands like init, add, commit, push, etc.")

            click.echo(f"\n{answer}")
            
            # Provide additional context based on current repository state
            if state != "Not a git repository":
                click.echo("\nBased on your current repository state:")
                click.echo("\n".join(f"- {detail}" for detail in details))

    def verify_task(self, task_type: str, task_input: str) -> bool:
        """Verify practical task completion"""
        if task_type == "init":
            try:
                subprocess.run(["git", "rev-parse", "--git-dir"], 
                             check=True, capture_output=True, text=True)
                return True
            except subprocess.CalledProcessError:
                return False
        elif task_type == "add":
            status = subprocess.run(["git", "status", "--porcelain"], 
                                  capture_output=True, text=True).stdout
            return bool(status and not status.startswith("??"))
        elif task_type == "commit":
            try:
                last_commit = subprocess.run(["git", "log", "-1", "--pretty=%B"], 
                                          capture_output=True, text=True).stdout.strip()
                return bool(last_commit)
            except subprocess.CalledProcessError:
                return False
        return False
