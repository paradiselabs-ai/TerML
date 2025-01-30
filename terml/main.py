import sys
import os
import click
from .terminal_handler import TerminalHandler
from .ai_integration import AIIntegration
from .commands import CommandExecutor
from .git_helper import analyze_git_state, provide_git_guidance, get_quick_git_help
from .llm_providers import available_providers
from .config import update_config
from .lesson_system import LessonManager, LessonCategory

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """TerML - AI-powered Terminal Assistant"""
    if ctx.invoked_subcommand is None:
        click.echo("TerML: AI-powered Terminal Assistant")
        click.echo("Use 'terml [command]' to interact with TerML.")
        click.echo("Available commands: explain, suggest, debug, chat, auto, summarize, generate, analyze, test, deps, git, provider")
        click.echo("For more information, use 'terml [command] --help'")

@cli.command()
def explain():
    """Explain the last command output"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute("terml explain")

@cli.command()
def suggest():
    """Suggest a helpful next command"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute("terml suggest")

@cli.command()
def debug():
    """Debug the last command execution"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute("terml debug")

@cli.command()
@click.option('-q', '--quick', is_flag=True, help="Start a quick chat session without memory retention")
def chat(quick):
    """Start a chat session with TerML"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    if quick:
        executor.execute("terml chat -q")
    else:
        executor.execute("terml chat", retain_memory=True)

@cli.command()
@click.option('--with-user', is_flag=True, help="Run commands with user approval")
@click.option('-q', '--quick', is_flag=True, help="Quickly automate finishing the current task")
def auto(with_user, quick):
    """Automatically run commands"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    if not with_user:
        click.echo("CAUTION! This can be dangerous and may damage your project or even your operating system!")
        click.echo("ParadiseLabs and Anthropic will not be responsible for any potential damage.")
        click.echo("Please use caution and keep watch over TerML in auto mode.")
        click.echo("Use CTRL + C to exit auto mode instantly at any time.")
        click.echo("Note: 'terml auto revert' will only revert the last command ran by TerML in auto mode.")
        if not click.confirm("Do you want to proceed?"):
            return
    
    if quick:
        executor.execute("terml auto -q")
    elif with_user:
        executor.execute("terml auto --with-user")
    else:
        executor.execute("terml auto")

@cli.command()
def revert():
    """Revert the last command executed in auto mode"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute("terml auto revert")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def summarize(path):
    """Summarize the contents of a file or directory"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute(f"terml summarize {path}")

@cli.command()
@click.argument('project_type')
@click.argument('project_name')
def generate(project_type, project_name):
    """Generate a new project structure"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute(f"terml generate {project_type} {project_name}")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def analyze(path):
    """Analyze code in the specified path"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute(f"terml analyze {path}")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def test(path):
    """Generate tests for the project in the specified path"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute(f"terml test {path}")

@cli.command()
@click.argument('subcommand', type=click.Choice(['list', 'update', 'add', 'remove']))
@click.argument('args', nargs=-1)
def deps(subcommand, args):
    """Manage project dependencies"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute(f"terml deps {subcommand} {' '.join(args)}")

@cli.group()
def git():
    """Git-related commands and learning features"""
    pass

@git.command()
def status():
    """Analyze current git repository state and provide guidance"""
    state, details = analyze_git_state()
    click.echo(f"Git Repository State: {state}")
    for detail in details:
        click.echo(f"- {detail}")
    if click.confirm("Do you need help?"):
        click.echo("\nGuidance:")
        click.echo(provide_git_guidance(state, details))

@git.group()
def learn():
    """Learn git concepts and commands"""
    pass

@learn.command(name="interactive")
@click.option('--teach', '-t', is_flag=True, help="Start an interactive git learning session")
@click.option('--quick', '-q', is_flag=True, help="Show quick help for common git commands")
@click.option('--quick-teach', '-qt', is_flag=True, help="Start a quick Q&A session for git")
def interactive_learn(teach, quick, quick_teach):
    """Start an interactive git learning session"""
    lesson_manager = LessonManager()
    
    if teach:
        # Show available Git lessons
        available_lessons = lesson_manager.get_available_lessons('git')
        if not available_lessons:
            click.echo("No Git lessons available.")
            return
        
        click.echo("\nAvailable Git Lessons:")
        for lesson in available_lessons['git']:
            status = "✅" if lesson['completed'] else "⭕"
            click.echo(f"{status} {lesson['id']}: {lesson['title']}")
        
        lesson_id = click.prompt("\nEnter the lesson ID you want to start", type=str)
        lesson_manager.start_interactive_session('git', lesson_id)
    
    elif quick:
        click.echo(get_quick_git_help())
    
    elif quick_teach:
        click.echo("Starting a quick Q&A session for git...")
        # TODO: Implement quick Q&A session for git
    
    else:
        click.echo("Please specify -t for interactive lessons, -q for quick help, or -qt for a quick Q&A session.")

@learn.command(name="list")
def list_lessons():
    """List available Git lessons"""
    lesson_manager = LessonManager()
    available_lessons = lesson_manager.get_available_lessons('git')
    
    if not available_lessons:
        click.echo("No Git lessons available.")
        return
    
    click.echo("\nAvailable Git Lessons:")
    for lesson in available_lessons['git']:
        status = "✅" if lesson['completed'] else "⭕"
        click.echo(f"{status} {lesson['id']}: {lesson['title']}")

@cli.group()
def provider():
    """Manage LLM providers"""
    pass

@provider.command()
@click.argument('provider_name')
@click.option('--model', help='Specify the model for the provider')
def set(provider_name, model):
    """Set the active LLM provider"""
    providers = available_providers()
    if provider_name not in providers:
        click.echo(f"Error: Provider '{provider_name}' is not available.")
        click.echo(f"Available providers: {', '.join(providers)}")
        return
    
    try:
        # Update configuration
        update_config('llm_provider', provider_name)
        
        # If model is specified, update model configuration
        if model:
            update_config(f'{provider_name}_model', model)
        
        click.echo(f"Successfully set {provider_name} as the active LLM provider")
        if model:
            click.echo(f"Model set to {model}")
    except Exception as e:
        click.echo(f"Error setting provider: {e}")

def validate_options(ctx, param, value):
    if value and ctx.command.name not in ['chat', 'auto', 'git']:
        raise click.BadParameter(f"Option {param.name} is not valid for this command.")
    return value

cli.params.append(click.Option(('-q', '--quick'), is_flag=True, callback=validate_options, expose_value=False, help='Quick mode'))
cli.params.append(click.Option(('-t', '--teach'), is_flag=True, callback=validate_options, expose_value=False, help='Teach mode'))

if __name__ == "__main__":
    cli()
