import sys
import click
from .terminal_handler import TerminalHandler
from .ai_integration import AIIntegration
from .commands import CommandExecutor
from .git_helper import analyze_git_state, provide_git_guidance, get_quick_git_help

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """TerML - AI-powered Terminal Assistant"""
    if ctx.invoked_subcommand is None:
        click.echo("TerML: AI-powered Terminal Assistant")
        click.echo("Use 'terml [command]' to interact with TerML.")
        click.echo("Available commands: explain, suggest, debug, chat, auto, summarize, generate, analyze, test, deps, git")
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

@learn.command()
@click.option('-t', '--teach', is_flag=True, help="Start an interactive git learning session")
@click.option('-q', '--quick', is_flag=True, help="Show quick help for common git commands")
@click.option('-qt', '--quick-teach', is_flag=True, help="Start a quick Q&A session for git")
def interactive(teach, quick, quick_teach):
    """Start an interactive git learning session"""
    if teach:
        click.echo("Starting an interactive git learning session...")
        # TODO: Implement interactive git learning session
    elif quick:
        click.echo(get_quick_git_help())
    elif quick_teach:
        click.echo("Starting a quick Q&A session for git...")
        # TODO: Implement quick Q&A session for git
    else:
        click.echo("Please specify -t for interactive lessons, -q for quick help, or -qt for a quick Q&A session.")

def validate_options(ctx, param, value):
    if value and ctx.command.name not in ['chat', 'auto', 'git']:
        raise click.BadParameter(f"Option {param.name} is not valid for this command.")
    return value

cli.params.append(click.Option(('-q', '--quick'), is_flag=True, callback=validate_options, expose_value=False, help='Quick mode'))
cli.params.append(click.Option(('-t', '--teach'), is_flag=True, callback=validate_options, expose_value=False, help='Teach mode'))

if __name__ == "__main__":
    cli()
