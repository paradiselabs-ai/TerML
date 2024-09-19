import sys
import click
from .terminal_handler import TerminalHandler
from .ai_integration import AIIntegration
from .commands import CommandExecutor

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """TerML - AI-powered Terminal Assistant"""
    if ctx.invoked_subcommand is None:
        click.echo("TerML: AI-powered Terminal Assistant")
        click.echo("Use 'terml [command]' to interact with TerML.")
        click.echo("Available commands: explain, suggest, debug, chat, auto, summarize")
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
@click.option('-q', '--quick', is_flag=True, help="Start a quick chat session")
def chat(quick):
    """Start a chat session with TerML"""
    if quick:
        executor = CommandExecutor(TerminalHandler(), AIIntegration())
        executor.execute("terml chat -q")
    else:
        click.echo("Please use 'terml chat -q' for a quick chat session.")

@cli.command()
@click.option('--with-user', is_flag=True, required=True, help="Run commands with user approval")
def auto(with_user):
    """Automatically run commands with user approval"""
    if with_user:
        executor = CommandExecutor(TerminalHandler(), AIIntegration())
        executor.execute("terml auto --with-user")
    else:
        click.echo("The --with-user flag is required for safety.")

@cli.command()
@click.argument('path', type=click.Path(exists=True))
def summarize(path):
    """Summarize the contents of a file or directory"""
    executor = CommandExecutor(TerminalHandler(), AIIntegration())
    executor.execute(f"terml summarize {path}")

if __name__ == "__main__":
    cli()